# 示例接口 输出-输入链路细化分析（字段级，脱敏）

## 1) 入口与范围

- 入口：`ExampleController#generateAuthCode`（`POST /api/example/auth-code`）
- 本次目标：对该入口触发的**所有输出**逐项反向追踪其输入来源、内部逻辑、默认/异常路径。
- 下钻范围：
  - 同步主链路：`AuthServiceImpl#createAuthRecord`
  - 异步链路：`CompletableFuture.runAsync -> QualityManager#calcOrgRunStatus`
  - 异步链路下游：`cleanAuthRecord -> initAuthChecks -> processDeviceCheck -> authCheckCorrection -> calcOrgRunStatusAll -> calcOrgRunStatus -> calcQuarterOrYearStatus`
- 不在本次范围：
  - MyBatis XML 的具体 SQL 文本（但保留调用点与数据来源）
  - 全局异常处理器对 HTTP 错误报文的统一包装细节

---

## 2) 输出发现表（5 类）

| 类别 | 候选输出落点 | 状态 | 证据 | 备注 |
|---|---|---|---|---|
| 返回输出 | `AuthCodeResponse(authCode, validInfo)` | Found | `AuthServiceImpl#createAuthRecord` | 同步返回 |
| 持久化输出 | `auth_record` 插入 | Found | `authRecordMapper.insert(entity)` | 同步事务内 |
| 外部输出 | HTTP 响应体（Controller 返回） | Found | `ExampleController#generateAuthCode` | 对调用方可见 |
| 异步输出 | `auth_check_record`、`device_check_record`、`org_run_detail` 写入/更新 | Found | `asyncCalcOrgRunStatus -> QualityManager#calcOrgRunStatus` | `runAsync` 触发 |
| 衍生输出 | 日志 `info/error/warn` | Found | Controller/Service/Manager 多处 `log.*` | 非业务主输出 |

---

## 3) 输出链路详解（字段级）

### 3.1 返回输出：`AuthCodeResponse.authCode`

- 落点：`AuthCodeResponse#setAuthCode`
- 字段：`authCode`
- 输入来源：
  - 请求：`param.app`、`param.deviceCode`
  - 枚举配置：`AppTypeEnum`（`appCode -> prefixValue`）
  - 当天日期：`LocalDate.now()`
- 逻辑：
  1. `appType = AppTypeEnum.getByCode(param.app)`；
  2. `digestValue = KeyGenUtil.getDigestValue(appType.prefixValue, deviceCode)`，其原串为 `prefixValue + "salt" + deviceCode + yyyy-MM-dd`，再做 MD5；
  3. `authCode = appType.prefixValue + digestValue` 最后 6 位（大写）。
- 兜底/异常：
  - `appType == null` -> 抛 `BusinessException("[createAuthRecord]Invalid app: ...")`；
  - 任意异常统一捕获后抛 `BusinessException("获取授权码失败")`。
- 时序：同步计算并返回。
- 风险：中（依赖当天日期，授权码天然与日期绑定）。

### 3.2 返回输出：`AuthCodeResponse.validInfo`

- 落点：`AuthCodeResponse#setValidInfo`
- 字段：`validInfo`
- 输入来源：
  - 系统日期：`authDate = LocalDate.now()`
- 逻辑：
  - `invalidDate = authDate.plusDays(365)`；
  - `validInfo = "有效期截至" + invalidDate.toString()`。
- 兜底/异常：无单独兜底，跟随主流程异常处理。
- 时序：同步计算并返回。
- 风险：低（纯时间计算）。

### 3.3 持久化输出：`auth_record`（同步插入）

- 落点：`authRecordMapper.insert(entity)`
- 字段级来源（按“直接输入 / 上下文 / 计算”分类）：

| 字段 | 来源类型 | 来源明细 | 逻辑说明 |
|---|---|---|---|
| `app` | 直接输入 | `param.app` | 原样写入 |
| `source` | 常量 | `"external"` | 固定值 |
| `user_id` | 登录上下文 | `loginUser.userId` | 原样写入 |
| `org_code` | 直接输入 | `param.orgCode` | 原样写入 |
| `tenant_id` | 登录上下文 | `loginUser.tenantId` | 原样写入 |
| `record_id` | 直接输入 | `param.recordId` | 原样写入 |
| `operator_name` | 登录上下文 | `loginUser.name` | 原样写入 |
| `auth_date` | 计算 | `LocalDate.now()` 转当天 00:00:00 | 按系统时区转换 `Date` |
| `invalid_date` | 计算 | `authDate + 365 天` 转 00:00:00 | 按系统时区转换 `Date` |
| `device_code` | 直接输入 | `param.deviceCode` | 原样写入 |
| `auth_code` | 计算 | 见 3.1 | 同返回字段 |
| `org_name` | 直接输入 | `param.orgName` | 原样写入 |
| `client_source` | 直接输入 | `param.clientSource` | 原样写入（允许为空） |
| `hostname` | 直接输入 | `param.hostname` | 原样写入 |
| `sn` | 直接输入 | `param.sn` | 原样写入 |
| `region` | 直接输入 | `param.region` | 原样写入 |
| `version` | 直接输入 | `param.version` | 原样写入 |

- 事务：处于 `createAuthRecord` 同步事务上下文（方法本身未显式 `@Transactional`，但 DB 写入在同一调用中完成）。
- 风险：中（大量字段直接信任请求输入）。

### 3.4 异步三表总览（先总后分）

- 总体顺序：`auth_record` -> 生成/修正 `auth_check_record` -> 归并生成 `device_check_record` -> 回写修正 `auth_check_record` -> 计算并落库 `org_run_detail`。
- 对阅读最关键的一点：这三张表不是“独立生成”，而是**前表结果驱动后表，后表又反向覆盖前表**（尤其 `device_check_record` 会二次覆盖 `auth_check_record`）。
- 因此同一个业务字段（例如机构编码）可能存在：
  - 首次值：来自请求原始授权；
  - 中间值：来自主数据映射；
  - 最终值：来自设备归并规则与时间线策略。

### 3.5 异步输出 A：`auth_check_record`（初始化 + 二次修正）

- 落点：
  - 首次落库：`authCheckService.saveOrUpdateBatch(allAuthChecks)`（`initAuthChecks`）
  - 二次修正：`authCheckService.updateBatchById(needUpdate)`（`authCheckCorrection`）

#### 3.5.1 字段级生成说明

| 字段 | 第一次赋值来源 | 第一次赋值逻辑 | 第二次是否可能覆盖 | 最终值主导因素 |
|---|---|---|---|---|
| `auth_record_id` | `auth_record.id` | 每条 `AuthCheck` 绑定对应授权主键 | 否 | 授权记录主键 |
| `real_client_source` | 优先 `auth_record.client_source` | 初始化直接透传；若 `orgCode` 为空且按名称匹配到机构编码且原值为空，则兜底 `"外部终端"` | 是 | `device_check_record.client_source`（修正阶段覆盖） |
| `real_org_code` | 优先 `auth_record.org_code` | 若为空则尝试 `orgName -> orgCode` 映射；映射失败设空串 | 是 | `device_check_record.real_org_code`（修正阶段覆盖） |
| `real_org_name` | 优先 `auth_record.org_name` | 若空则尝试 `orgCode -> orgName` 反查补齐 | 是 | `device_check_record.real_org_name`（修正阶段覆盖） |
| `check_status` | 非当前链路直接写入 | 在当前触发链路可见代码中未直接赋值该字段 | Unknown | 需补 Mapper/其他任务写入点 |

#### 3.5.2 覆盖时序（决定“最终值看哪里”）

1. **初始化阶段**：先把 `auth_record` 原始机构/来源字段灌入 `auth_check_record`。  
2. **主数据补全阶段**：处理“机构编码缺失/机构名称缺失”问题。  
3. **设备归并反写阶段**：`authCheckCorrection` 根据 `device_check_record` 把 `realOrgCode/realOrgName/realClientSource` 再覆盖一遍。  

- 结论：`auth_check_record` 的最终机构与来源字段，通常应以**设备归并后结果**为准，而不是请求原值。

### 3.6 异步输出 B：`device_check_record`（设备维度归并）

- 落点：
  - `deviceCheckService.saveBatch(needInsert)`（不存在则新增）
  - `deviceCheckService.updateBatchById(needUpdate)`（已存在且 `source=1` 才更新）
  - `deviceCheckService.updateAuthCheck(deviceCodeSet)`（联动同步）

#### 3.6.1 字段级生成说明

| 字段 | 输入来源 | 计算/选择规则 | 兜底/跳过 |
|---|---|---|---|
| `device_code` | `authCheckBO` 分组键 | 按设备码分组逐个处理 | 无 |
| `source` | 记录创建策略 | 新增记录固定 `1`（计算来源）；已存在记录保留原值 | 已存在且 `source!=1` 时整条跳过更新 |
| `real_org_name` | “最后有效授权”中的 `realOrgName` | 由 `getLastValidAuthCheckBO` 选出的记录决定 | 若找不到有效授权则空串 |
| `real_org_code` | “最后有效授权”中的 `realOrgCode` | 同上 | 若找不到有效授权则空串 |
| `client_source` | 设备下所有授权聚合统计 | `internalOrgCodeCnt==0 && orgCodeCnt>=1` -> `"外部终端"`；否则 `"内部终端"` | 无 |
| `device_status` | 同上 | 外部终端判定 -> `1`，否则 `0` | 无 |

#### 3.6.2 “最后有效授权”选择规则（复杂核心）

- 输入：同一 `deviceCode` 下所有授权记录（`AuthCheckBO`）。
- 规则：
  1. 使用 `calcTimeLine` 划分“时间线前”与“时间线后”；
  2. 若“时间线前”非空：取其中 `createTime` 最大（最新）；
  3. 若“时间线前”为空：对“时间线后”按时间升序，`size>=2` 取第 2 条，否则取第 1 条。
- 影响：`real_org_code/real_org_name` 的最终归属可能并非最新授权，属于业务策略性选择。

### 3.7 异步输出 C：`org_run_detail`（运行状态快照）

- 落点：`orgRunDetailService.calcOrgRunStatus(detailList, req)`（该服务内执行删旧插新）
- 主链路输入：
  1. `auth_record + auth_check_record` 取有效授权；
  2. 提取 `deviceCode/appType/version`；
  3. 以设备码与季度查询 `submit_record`；
  4. `checkRunStatus` 计算 full/rapid/scanStatus；
  5. 聚合生成 `OrgRunDetail` 各字段。

#### 3.7.1 字段级说明

| 字段 | 直接来源 | 计算逻辑 | 关键分支/注意点 |
|---|---|---|---|
| `quarter` | 请求季度上下文 | `req.quarter` 写入 | 历史季度会循环重算到当前 |
| `year` | 请求季度上下文 | `req.year` 写入 | 同上 |
| `time_type` | `QuarterDTO.timeType` | 季度/年度维度标识 | 季度与年度都会生成 |
| `org_code` | 机构清单记录 | 当前机构编码 | 受上游筛选范围影响 |
| `scan_type_a` | `scanSet` | `scanSet.contains(1)?1:0` | appType=1 |
| `scan_type_b` | `scanSet` | `scanSet.contains(2)?1:0` | appType=2 |
| `scan_type_a_ext` | `scanSet` | `scanSet.contains(3)?1:0` | appType=3（扩展口径） |
| `scan_type_b_ext` | `scanSet` | `scanSet.contains(4)?1:0` | appType=4（扩展口径） |
| `scan_time_type_a` | `scanTimeMap[1]` | 该 appType 最近 `createTime` | 取 max，不是首条 |
| `scan_time_type_b` | `scanTimeMap[2]` | 同上 | 取 max |
| `scan_time_type_a_ext` | `scanTimeMap[3]` | 同上 | 取 max |
| `scan_time_type_b_ext` | `scanTimeMap[4]` | 同上 | 取 max |
| `scan_info` | `submitRecordList` | 非空：`已扫码\n+首条时间`；空：`未扫码` | **首条时间 != 最近时间** |
| `version_info` | 授权版本集合 | `versionSet` 用换行拼接 | 来源于授权表版本 |
| `version_info_a` | A口径版本集合 | `versionASet` 拼接 | appType 1/3 入集合 |
| `version_info_b` | B口径版本集合 | `versionBSet` 拼接 | appType 2/4 入集合 |
| `run_status_a` | 当前状态 + 历史状态 | 历史>0且当前>0 ->2；历史=0且当前>0 ->1；否则0 | A口径优先级：`rapid` 优先于 `full` |
| `run_status_b` | 当前状态 + 历史状态 | 历史>0且当前>0 ->2；历史=0且当前>0 ->1；否则0 | B口径当前态内：`full` 优先于 `rapid` |
| `rapid_a` | `rapidRunSet` | `contains(1)?1:0` | 来自 `checkRunStatus` |
| `rapid_b` | `rapidRunSet` | `contains(2)?1:0` | 来自 `checkRunStatus` |
| `rapid_a_ext` | `rapidRunSet` | `contains(3)?1:0` | 来自 `checkRunStatus` |
| `rapid_b_ext` | `rapidRunSet` | `contains(4)?1:0` | 来自 `checkRunStatus` |
| `full_a` | `fullSet` | `contains(1)?1:0` | 来自 `checkRunStatus` |
| `full_b` | `fullSet` | `contains(2)?1:0` | 来自 `checkRunStatus` |
| `full_a_ext` | `fullSet` | `contains(3)?1:0` | 来自 `checkRunStatus` |
| `full_b_ext` | `fullSet` | `contains(4)?1:0` | 来自 `checkRunStatus` |

#### 3.7.2 `checkRunStatus` 如何驱动上述字段

- `rapidRun=true`：同时命中 `purchaseActId` 与至少一个 `commonActIds`。
- `fullRun=true`：未命中 rapid，且过滤后仍有“有效 act”（已去除基础 act、排除 act、空值/0 次）。
- `scanStatus=false`：既不 rapid 也不 full。
- 对 `scanSet` 的特殊影响：
  - appType `1/2`：只要产生判定结果就计入；
  - appType `3/4`：仅 `scanStatus=true` 时才计入。

- 风险：高（动作 ID 口径复杂且 appType=1/2 与 3/4 的计入规则不对称）。

---

## 4) 关键细节（防漏点）

- `app=0` 时的口径分裂：
  - `getAppType` 会根据 `authCode` 前缀把同一授权拆成 appType `3/4`（或同时 3、4），不是简单等于请求 `app`。
- `scanInfo` 不是“最近扫码时间”：
  - 文案使用 `submitRecordList.get(0).createTime`，并非最大时间；而 `scan_time_*` 才是 max 逻辑。
- `runStatus` 聚合优先级不对称：
  - A口径 `runStatusA`：`rapid` 优先于 `full`；
  - B口径 `runStatusB`：`full` 优先于 `rapid`。
- 异步不阻塞主返回：
  - 主接口返回成功后，异步计算仍可能失败，仅体现在日志，不影响本次 HTTP 成功响应。
- 时间线策略会改变“最终归属机构”：
  - `device_check_record` 取“最后有效授权”并非总是最新记录。

---

## 5) 复杂字段审计与关注优先级（本次补充）

> 说明：这一节只标记“逻辑复杂但当前文档仍有概括成分”的字段，便于优先审阅。  
> 复杂度评级：`L1-低` / `L2-中` / `L3-高` / `L4-极高`。  
> 展开充分性：`充分` / `部分充分` / `不足`。

| 字段 | 所在表 | 当前复杂度 | 当前展开充分性 | 为什么复杂 | 还缺的细节（建议重点补扫） |
|---|---|---|---|---|---|
| `check_status` | `auth_check_record` | L3 | 不足 | 字段在主链路可见代码中未直接赋值，可能由 SQL/批处理/其他任务更新 | 需要全局检索 `check_status` 更新点、对应任务触发条件、状态码字典含义 |
| `real_org_code` | `auth_check_record` | L3 | 部分充分 | 先取授权，再按名称映射，再被 `device_check_record` 回写；多阶段覆盖 | 各阶段“覆盖优先级冲突”在并发场景的最终一致性（异步重算时序） |
| `real_org_name` | `auth_check_record` | L3 | 部分充分 | 同上，且存在 code->name 反查路径 | 反查失败时的空值传播、后续报表是否按空值过滤 |
| `real_client_source` | `auth_check_record` | L3 | 部分充分 | 可能被兜底 `"外部终端"`，后续又被设备归并覆盖 | 哪些入口会写入非标准值（非“内部/外部终端”） |
| `real_org_code` | `device_check_record` | L4 | 部分充分 | 由“最后有效授权”选择策略决定，而该策略依赖时间线且并非取最新 | `calcTimeLine` 的配置值来源、变更后历史重算影响范围 |
| `real_org_name` | `device_check_record` | L4 | 部分充分 | 与上同源，受“第二条记录”规则影响明显 | 时间线前为空时取第2条的业务依据与边界验证（仅1条/2条/多条） |
| `client_source` | `device_check_record` | L3 | 部分充分 | 由聚合计数推导，不直接来自单条授权 | `orgCodeCnt/internalOrgCodeCnt` 的精确定义与异常值处理 |
| `device_status` | `device_check_record` | L3 | 部分充分 | 完全依赖归并统计，不是原始输入透传 | 状态值 `0/1` 在下游页面与导出中的业务语义对照 |
| `scan_info` | `org_run_detail` | L3 | 部分充分 | 展示用时间取首条记录，不等于最近扫码时间，容易误解 | `submitRecordList` 顺序是否稳定（SQL 默认排序） |
| `scan_time_type_a/...` | `org_run_detail` | L3 | 部分充分 | 取分组后的 max 时间，受 appType 拆分与日志归并影响 | 不同 appType 下日志过滤规则导致的“时间缺口”案例 |
| `run_status_a` | `org_run_detail` | L4 | 部分充分 | 当前状态与历史状态双层合并，且 A 口径优先级是 rapid>full | 与 `full_*`/`rapid_*` 的一一映射校验样例（建议列举至少 4 种输入组合） |
| `run_status_b` | `org_run_detail` | L4 | 部分充分 | 同为双层合并，但 B 口径优先级是 full>rapid（与 A 不对称） | 不对称设计的业务理由、是否存在历史兼容包袱 |
| `full_*` / `rapid_*` 全字段族 | `org_run_detail` | L4 | 部分充分 | 由 `checkRunStatus` + appType 专用 actId 列表共同决定 | 4 个 appType 各自 `commonActIds/purchaseActId/removeActIds` 需要逐项表格化 |
| `version_info` / `version_info_a` / `version_info_b` | `org_run_detail` | L2 | 部分充分 | 看似简单拼接，但依赖 `getAppType` 口径拆分（0->3/4） | 授权码前缀与 appType 映射异常时的版本归类偏差 |

### 5.1 建议优先关注的字段（按风险排序）

1. `device_check_record.real_org_code` / `device_check_record.real_org_name`（L4）  
2. `org_run_detail.run_status_a` / `org_run_detail.run_status_b`（L4）  
3. `org_run_detail.full_*` / `rapid_*`（L4）  
4. `auth_check_record.check_status`（L3，信息缺口型风险）  

---

## 6) 输入 -> 输出总览矩阵

| 输入项 | 直接影响输出 | 中间链路 | 输出类型 |
|---|---|---|---|
| `param.app` | `authCode` 前缀、`auth_record.app` | `AppTypeEnum` 映射 + digest 计算 | 返回 + DB |
| `param.deviceCode` | `authCode` 摘要、`auth_record.device_code`、后续设备归并 | `KeyGenUtil` + 异步 `deviceCode` 分组 | 返回 + 多表DB |
| `param.orgCode/orgName` | `auth_record` 初始机构字段 | 异步被主数据映射与设备判定纠偏 | 多表DB |
| `param.clientSource` | `auth_record.client_source` | 为空时可能被兜底/覆盖 | 多表DB |
| `param.version` | `auth_record.version`、`org_run_detail.version_info*` | 授权聚合后拼接 | 多表DB |
| `loginUser` | `auth_record.user_id/tenant_id/operator_name` | 直接透传 | DB |
| 机构主数据表 | `auth_check_record.realOrg*` | 名称<->编码映射 | DB |
| `submit_record.rawData` | `full_*`,`rapid_*`,`scan_*`,`run_status_*` | `checkRunStatus` 动作规则 | DB |
| 配置 `calcTimeLine` | `device_check_record.realOrg*` 选取结果 | `getLastValidAuthCheckBO` | DB |

---

## 7) 待确认与风险

- 待确认项：
  - `authService.getValidAuthRecord` 与 `listByCleanReq` 的 SQL 过滤条件（有效性窗口、去重细节）。
  - `orgRunDetailService.calcOrgRunStatus` 的“删旧插新”精确策略与唯一键定义。
- 风险说明：
  - 当前文档已覆盖代码可见逻辑；若需做到“SQL 级绝对闭环”，建议补扫 Mapper XML 与表索引/唯一键约束。

---

## 8) 结论（一句话）

`generateAuthCode` 的同步输出字段大多由请求与登录态直接生成，但异步链路会把授权信息与主数据、设备归并策略、扫码日志规则进行多轮融合与覆盖，最终在 `auth_check_record`、`device_check_record`、`org_run_detail` 中形成与初始输入不完全同构的“派生输出状态”。
