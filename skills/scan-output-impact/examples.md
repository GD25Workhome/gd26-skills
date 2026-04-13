# 示例接口 输出扫描（脱敏）

## 1. 扫描范围与输出定义

- 入口：`POST /api/example/auth-code`（`ExampleController#generateAuthCode`）。
- 本文“输出”仅按定义统计：
  - 返回结果（HTTP 响应体）；
  - 对数据库的变更（含该入口触发的异步分支）。

---

## 2. 返回结果输出

### 2.1 成功返回对象

- 返回类型：`AuthCodeResponse`
- 字段清单：
  - `authCode`：授权码（形如“前缀 + 6位摘要”，前缀来自 `AppTypeEnum.prefixValue`）
  - `validInfo`：有效期文案（`有效期截至YYYY-MM-DD`，当前日期 +365 天）

### 2.2 异常返回

- 当 `app` 无法映射到 `AppTypeEnum`、摘要生成失败、数据库写入异常等情况发生时：
  - 抛出业务异常：`BusinessException("获取授权码失败")`
  - 实际 HTTP 包装格式由全局异常处理决定（本方法本身不包 `Result`）。

---

## 3. 数据库变更输出（主链路）

## 3.1 表：`auth_record`

### 变更类型

- `INSERT` 1 条授权记录（`authRecordMapper.insert(entity)`）。

### 本次会写入/赋值的字段

- `app`：来自请求 `param.app`
- `source`：固定 `"external"`
- `user_id`：来自登录用户 `loginUser.userId`
- `org_code`：来自请求 `param.orgCode`
- `tenant_id`：来自登录用户 `loginUser.tenantId`
- `record_id`：来自请求 `param.recordId`
- `operator_name`：来自登录用户 `loginUser.name`
- `auth_date`：当天 00:00:00
- `invalid_date`：当天 +365 天 00:00:00
- `device_code`：来自请求 `param.deviceCode`
- `auth_code`：本次生成的授权码
- `org_name`：来自请求 `param.orgName`
- `client_source`：来自请求 `param.clientSource`
- `hostname`：来自请求 `param.hostname`
- `sn`：来自请求 `param.sn`
- `region`：来自请求 `param.region`
- `version`：来自请求 `param.version`

### 简要概述

- 每次调用生成一条新的授权记录，并把请求与登录态信息完整落到 `auth_record`，用于授权追溯与后续运行状态计算。

---

## 4. 数据库变更输出（异步分支）

`createAuthRecord` 在主写入后会异步执行 `qualityManager.calcOrgRunStatus(deviceCode)`，该分支会继续产生数据库变更。

## 4.1 表：`auth_check_record`

### 变更类型

- `saveOrUpdateBatch`（新增或更新校验记录）
- `updateBatchById`（批量更新校验结果）

### 该链路中可被更新的字段

- `auth_record_id`
- `real_client_source`
- `real_org_code`
- `real_org_name`
- `check_status`

### 简要概述

- 基于 `auth_record` 与机构映射规则，回填/修正授权记录对应的“真实机构与终端来源”校验信息。

## 4.2 表：`device_check_record`

### 变更类型

- `saveBatch`（新设备码）
- `updateBatchById`（已有设备码）
- 以及后续 `updateAuthCheck(deviceCodeSet)` 联动更新

### 该链路中可被更新的字段

- `device_code`
- `source`
- `real_org_name`
- `real_org_code`
- `client_source`
- `device_status`

### 简要概述

- 按设备码聚合授权信息后，重算“内部/外部终端”与设备有效性状态，为后续授权清洗和机构运行状态计算提供依据。

## 4.3 表：`org_run_detail`

### 变更类型

- 先按机构+时间维度删除旧明细（`removeByIds`）
- 再批量插入新明细（`saveBatch`）

### 该链路中会写入的字段

- 维度字段：
  - `quarter`
  - `year`
  - `time_type`
  - `org_code`
- 扫码类：
  - `scan_type_a`
  - `scan_type_b`
  - `scan_type_a_ext`
  - `scan_type_b_ext`
  - `scan_time_type_a`
  - `scan_time_type_b`
  - `scan_time_type_a_ext`
  - `scan_time_type_b_ext`
  - `scan_info`
- 版本类：
  - `version_info`
  - `version_info_a`
  - `version_info_b`
- 运行状态类：
  - `run_status_a`
  - `run_status_b`
  - `rapid_a`
  - `rapid_b`
  - `rapid_a_ext`
  - `rapid_b_ext`
  - `full_a`
  - `full_b`
  - `full_a_ext`
  - `full_b_ext`

### 简要概述

- 对当前设备码关联机构执行“运行状态重算”，并以“删旧插新”方式重建机构季度/年度运行明细快照。

---

## 5. 本入口输出总览（一句话）

- 该接口同步输出 `AuthCodeResponse` 并插入 `auth_record` 授权记录，随后异步触发授权校验与机构运行状态重算，进一步更新 `auth_check_record`、`device_check_record`、`org_run_detail`。
