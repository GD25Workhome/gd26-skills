# Python 注释规范 — 示例

## 标准示例：docstring 缩进 + 流程步骤（推荐对照）

以下形态为本技能的标准写法（与用户提供的 `load_providers` 一致）：

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
    # 1. 确定配置文件路径
    if config_path is None:
        config_path = cls._get_config_path()
    else:
        cls._config_path = config_path

    if not config_path.exists():
        raise FileNotFoundError(f"模型供应商配置文件不存在: {config_path}")

    logger.info(f"加载模型供应商配置: {config_path}")

    try:
        # 2. 读取 YAML 并校验顶层结构
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)

        if not config_data or "providers" not in config_data:
            raise ValueError("配置文件格式错误：缺少 'providers' 字段")

        providers_list = config_data.get("providers", [])
        if not isinstance(providers_list, list):
            raise ValueError("配置文件格式错误：'providers' 必须是列表")

        # 3. 重置注册表，准备写入本次加载结果
        provider_registry.clear()

        # 4~5. 逐条解析并注册供应商
        for provider_data in providers_list:
            if not isinstance(provider_data, dict):
                logger.warning(f"跳过无效的供应商配置: {provider_data}")
                continue

            provider_name = provider_data.get("provider")
            api_key = provider_data.get("api_key", "")
            base_url = provider_data.get("base_url", "")
            default_model = provider_data.get("default_model")

            if not provider_name:
                logger.warning(f"跳过缺少 provider 名称的配置: {provider_data}")
                continue

            # _resolve_env_var：将 ${ENV} 占位符替换为环境变量实际值
            api_key = cls._resolve_env_var(api_key)
            base_url = cls._resolve_env_var(base_url)

            if not api_key:
                logger.warning(f"供应商 {provider_name} 的 API 密钥为空，跳过注册")
                continue

            provider_registry.register(
                provider=provider_name,
                api_key=api_key,
                base_url=base_url,
                default_model=default_model,
            )
            logger.info(f"已注册模型供应商: {provider_name} (base_url: {base_url})")

        # 6. 完成加载
        cls._loaded = True
        logger.info(f"成功加载 {len(provider_registry.get_all())} 个模型供应商配置")

    except yaml.YAMLError as e:
        raise ValueError(f"配置文件 YAML 格式错误: {e}")
    except Exception as e:
        raise ValueError(f"加载模型供应商配置失败: {e}")
```

要点：

- **多行** docstring 开闭 `"""` 与函数体同级，**正文再缩进 4 格**；**单行** docstring 写在一行内。
- 方法体用 **`# 1.` … `# 6.`** 标步骤；可合并为 **`# 4~5.`**。
- 步骤注释已覆盖的阶段内， obvious 调用不必重复注释；**不直观**的调用（如 `_resolve_env_var`）单独一行说明。

---

## 反例：多行 docstring 正文未缩进

```python
def load_providers(cls, config_path: Optional[Path] = None) -> None:
    """从 YAML 加载模型供应商配置并写入内存注册表。

    Args:
        config_path: 配置文件路径
    """
    ...
```

`Args:` 与摘要应相对 `"""` **再缩进 4 格**，见标准示例。

---

## 反例：顶格写在 def 外

```python
# 从 YAML 加载模型供应商配置   ← 禁止
@classmethod
def load_providers(cls, config_path: Optional[Path] = None) -> None:
    ...
```

方法级说明应写在 **docstring** 内，而非 `def` 上方顶格注释。

---

## 反例：流程复杂却无步骤注释

```python
def load_providers(cls, config_path: Optional[Path] = None) -> None:
    """
        从 YAML 加载模型供应商配置。
    """
    if config_path is None:
        config_path = cls._get_config_path()
    with open(config_path) as f:
        config_data = yaml.safe_load(f)
    provider_registry.clear()
    for provider_data in config_data["providers"]:
        provider_registry.register(...)
    cls._loaded = True
```

应拆为 `# 1.` 确定路径、`# 2.` 读取校验、`# 3.` 重置注册表、`# 4~5.` 解析注册、`# 6.` 完成加载。

---

## 简单方法：单行 docstring，不必编号

```python
def is_active(user: User) -> bool:
    """判断用户是否处于活跃状态。"""
    return user.status == "ACTIVE" and user.deleted_at is None
```
