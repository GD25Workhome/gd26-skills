---
name: python-comments
description: >-
  编写或补全 Python 代码注释时，在通用规范（简体中文、docstring、类型提示）之上，
  强制多行 docstring 正文相对开闭引号再缩进 4 格以便编辑器折叠，单行 docstring 写在一行内；
  方法内流程较多时
  按 # N. 步骤注释；调用其它方法时在调用处添加简短说明。在用户编写/重构 Python、要求
  补注释、代码审查注释风格，或提及 python 注释规范时启用。
---

# Python 注释规范

## 何时启用

- 新建或修改 **Python** 代码，需要编写、补全或统一注释风格。
- 用户要求按团队注释规范写代码，或明确提到 **python 注释**、**注释折叠**。
- 代码审查中需要检查注释是否可读、可折叠、能反映流程。

## 基础规范（沿用默认规则）

在应用本技能额外约束前，须同时满足：

| 项 | 要求 |
|----|------|
| **语言** | 注释、docstring 均使用 **简体中文** |
| **类型提示** | 函数、方法参数与返回值须有完整类型提示 |
| **docstring** | 模块、类、公开函数/方法须有 docstring，说明职责、参数、返回值、异常（如有） |
| **注释原则** | 解释「为什么」与业务含义；避免复述代码字面意思；仅对非显而易见逻辑加注释 |

---

## 额外约束 1：方法级 docstring

**目的**：多行 docstring 正文相对 `"""` 再缩进 4 格，折叠函数/方法时说明与实现一并收起；单行摘要则保持一行，避免无意义换行。

### 规则

1. **方法级说明**写在 **docstring** 中；`"""` 与函数体第一行代码 **同级缩进**（相对 `def` 向右 4 格）。
2. **多行 docstring**：正文每一行（摘要、空行、`Args` / `Returns` / `Raises` 及其条目）相对开闭引号 **再向右缩进 4 格**，全文保持同一正文缩进。
3. **单行 docstring**：摘要 **写在一行内**，不换行、不拆成三行形式，例如 `"""判断用户是否处于活跃状态。"""`。
4. **禁止**在 docstring 外、`def` 上方用顶格 `#` 块重复写方法说明。
5. **禁止**多行 docstring 正文与 `"""` 左对齐（无额外 4 格），否则折叠体验不符合本规范。

### 示例

```python
@classmethod
def load_providers(cls, config_path: Optional[Path] = None) -> None:
    """
        从 YAML 加载模型供应商配置并写入内存注册表。

        Args:
            config_path: 配置文件路径；为 None 时使用 settings.MODEL_PROVIDERS_CONFIG

        Raises:
            FileNotFoundError: 配置文件不存在
            ValueError: YAML 格式错误或 providers 结构不合法
    """
    ...
```

### 反例

```python
def load_providers(cls, config_path: Optional[Path] = None) -> None:
    """从 YAML 加载模型供应商配置并写入内存注册表。

    Args:
        config_path: 配置文件路径
    """                              # 多行 docstring 正文未相对 """ 再缩进 4 格
    ...

# 从 YAML 加载配置                   # 顶格写在 def 外，禁止
def load_providers(cls) -> None:
    ...
```

---

## 额外约束 2：方法内流程步骤注释

当方法内 **分支较多、步骤 ≥ 3 个、或跨多个子系统** 时，在方法体中用 `#` 按流程添加步骤注释。

### 规则

1. 使用 **`# N. 步骤摘要`** 编号（N 从 1 递增），一行说清该步做什么。
2. 步骤注释与对应代码 **同一缩进层级**，紧贴该步代码块 **上方**。
3. 相邻两步逻辑紧密、适合合并讲解时，可用 **`# N~M. 步骤摘要`**（如 `# 4~5. 逐条解析并注册供应商`）。
4. 简单方法（≤2 步、无复杂分支）不必强行编号，docstring 摘要即可。

### 示例

```python
    # 1. 确定配置文件路径
    if config_path is None:
        config_path = cls._get_config_path()
    else:
        cls._config_path = config_path

    ...

    try:
        # 2. 读取 YAML 并校验顶层结构
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
        ...

        # 3. 重置注册表，准备写入本次加载结果
        provider_registry.clear()

        # 4~5. 逐条解析并注册供应商
        for provider_data in providers_list:
            ...

        # 6. 完成加载
        cls._loaded = True
```

---

## 额外约束 3：调用其它方法时的简短说明

在方法内 **调用其它函数/方法**（尤其跨模块、有副作用、远程/异步调用）时，若该调用的职责 **无法从当前步骤注释一眼看出**，在调用语句 **正上方** 增加一行 `#` 说明。

### 规则

1. 格式：**`# 方法名：一句话说明做什么`**（写被调方职责，而非重复参数列表）。
2. 调用已包含在某步 `# N.` 注释所描述的动作范围内、且方法名语义清晰时，**不必**再单独注释（如步骤 `# 4~5. 逐条解析并注册` 内的 `register()`）。
3. 标准库或语义极 obvious 的调用（如 `len()`、`str.strip()`、`open()`）不必注释。
4. 与步骤注释并存时：步骤注释概括 **阶段**，调用注释说明 **该步内具体、不直观的调用**。

### 示例

```python
        # 2. 读取 YAML 并校验顶层结构
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)

        ...

        # 4~5. 逐条解析并注册供应商
        for provider_data in providers_list:
            ...
            # _resolve_env_var：将 ${ENV} 占位符替换为环境变量实际值
            api_key = cls._resolve_env_var(api_key)
            ...
            provider_registry.register(...)
```

---

## 执行检查清单

编写或审查 Python 注释时，逐项确认：

- [ ] docstring + 类型提示齐全（基础规范）
- [ ] **多行** docstring 正文相对 `"""` **再缩进 4 格**；**单行** docstring 写在一行内
- [ ] 流程复杂处有用 **`# N.`** 或 **`# N~M.`** 标出的步骤注释
- [ ] 不直观的方法调用上方有 **一行简短说明**（ obvious 调用可省略）
- [ ] 无顶格写在 `def` 外的重复方法说明
- [ ] 注释为简体中文，无冗余复述代码

## 与其它规范的关系

- 用户/项目若已有 **cursor rules** 中的 Python 注释要求，本技能在其上 **追加** docstring 缩进、步骤、调用说明三条约束，冲突时以 **更严格且更具体** 者为准。
- 本技能 **不替代** 测试、日志、异常信息设计；仅规范注释形态与密度。

## 更多示例

完整对照示例见 [examples.md](examples.md)。
