# 借助 AI 适配 / 调试设备指南

本指南面向希望借助 AI 编程助手（Trae、ChatGPT、Claude、Cursor 等）为 **midea_smart_home** 集成适配新设备或调试现有设备的用户。你不需要精通 Python，但需要会复制日志、编辑文件和重启 Home Assistant。

> 普通安装配置请先阅读 [SETUP_GUIDE.md](SETUP_GUIDE.md)，向作者反馈问题请阅读 [CONTRIBUTING.md](../../CONTRIBUTING.md)。

---

## 目录

1. [先判断你的设备属于哪种情况](#1-先判断你的设备属于哪种情况)
2. [5 分钟理解工作原理](#2-5-分钟理解工作原理)
3. [关键文件与目录地图](#3-关键文件与目录地图)
4. [第一步：为 AI 准备调试材料](#4-第一步为-ai-准备调试材料)
5. [场景一：适配 ⏳ 待支持的新设备类型](#5-场景一适配--待支持的新设备类型)
6. [场景二：已支持设备的实体增删改](#6-场景二已支持设备的实体增删改)
7. [场景三：Lua 协议层问题](#7-场景三lua-协议层问题)
8. [设备分类与失败原因对照表](#8-设备分类与失败原因对照表)
9. [调试工具箱](#9-调试工具箱)
10. [提交前的格式与排序检查（CI 必过）](#10-提交前的格式与排序检查ci-必过)
11. [Commit 与 PR 规范](#11-commit-与-pr-规范)
12. [可直接复制给 AI 的提示词模板](#12-可直接复制给-ai-的提示词模板)
13. [必须转告 AI 的项目规则](#13-必须转告-ai-的项目规则)
14. [适配完成之后](#14-适配完成之后)

---

## 1. 先判断你的设备属于哪种情况

扫描设备后，设备列表会把设备分为三类（详见 [第 8 节](#8-设备分类与失败原因对照表)）：

| 列表中的表现 | 含义 | 你能做什么 |
|---|---|---|
| `名称 \| 型号 \| T0xXX \| V3`（可勾选） | ✅ 已支持 | 如实体缺失/数值不对，走[场景二](#6-场景二已支持设备的实体增删改) |
| `名称 \| 型号 \| T0xXX \| V3 ⏳ 待支持` | ⏳ 通信完全正常，只缺类型映射 | 走[场景一](#5-场景一适配--待支持的新设备类型)，这是最容易适配的一类 |
| 列表下方 `- [不支持] ... \| 原因` | ❌ 协议/token/Lua/初始化查询有问题 | 对照[第 8 节](#8-设备分类与失败原因对照表)，走[场景三](#7-场景三lua-协议层问题)或反馈作者 |

**请记下设备条目中的 4 个关键信息**：名称、型号、`T0xXX` 类型码、协议版本（V1/V2/V3）。与 AI 的所有沟通都围绕 `T0xXX` 展开。

---

## 2. 5 分钟理解工作原理

把下面这段原理连同你的问题一起发给 AI，能显著减少它的猜测：

```
midea_smart_home 集成的设备数据链路：

设备(局域网 TCP 6444)
  → DeviceController：8370 协议加解密（V3 需要 token/key）
  → MideaCodec（Lua 运行时）：调用厂商 Lua 文件的 dataToJson，
    把原始报文 hex 解码成 status JSON 字段（如 {"power":"on","temperature":26}）
  → ExpressionEvaluator：按 device_mapping 的 calculate 表达式做二次计算
  → DeviceLogicHandler（midea_lib/extras.py）：设备特例修正
  → MideaCoordinator：推送给 HA 实体平台（sensor/switch/climate...）

控制链路（HA → 设备）相反：
实体 → 按 mapping 的 options/command 组装 control dict
  → MideaCodec.build_control 调用 Lua 的 jsonToData 编码成 hex
  → 8370 加密后发给设备

两层解耦：
1. Lua 文件（厂商协议）：负责字节 ↔ JSON，决定"能解析出哪些字段"
2. device_mapping/T0xXX.py：负责 JSON 字段 → HA 实体，决定"显示成什么、怎么控制"
```

**核心结论**：

- 设备**能通信但没有实体 / 实体不对** → 改 `device_mapping/T0xXX.py`（纯 Python，AI 最擅长）。
- 日志里 status 字段本身就缺失 / 是乱码 / 控制下发无反应 → Lua 协议层问题（[场景三](#7-场景三lua-协议层问题)）。
- V2 `0x0110` 新协议变体目前**无法本地通信**，不属于适配能解决的范围。

---

## 3. 关键文件与目录地图

HA 配置目录记为 `CONFIG`（含 `configuration.yaml` 的目录），集成安装目录记为 `COMP`（`custom_components/midea_smart_home`）。

| 路径 | 作用 | 适配时是否需要改 |
|---|---|---|
| `COMP/const.py` → `DEVICE_TYPES` | 已注册的 T0x 类型码字典 | 新类型需要加一行 |
| `COMP/device_mapping/T0xXX.py` | 某类型的实体映射（核心文件） | **主要修改对象** |
| `COMP/device_mapping/__init__.py` | 映射加载与选型（model → sn8 → category → default） | 一般不改 |
| `COMP/device_mapping/_common.py` | 所有 mapping 共用的 HA 常量导入 | 缺常量时在这里加 |
| `COMP/lua/T0xXX.lua`、`T0xXX_SN8.lua` | **自定义 Lua 覆盖文件**（随集成分发） | Lua 修复时放这里 |
| `COMP/midea_lib/lua.py` | Lua 运行时（`MideaCodec`、加解密辅助） | 一般不改 |
| `COMP/midea_lib/device.py` | TCP 通信、status 解码、控制下发、轮询 | 一般不改，调试时看日志 |
| `COMP/midea_lib/extras.py` | 各类型的特殊数据修正逻辑 | 有设备特例时在这里加 |
| `COMP/midea_lib/setup.py` | 添加设备时的连接/初始化校验 | 一般不改 |
| `COMP/translations/zh-Hans.json`、`en.json` | 实体中文名/英文名 | 新增实体名时补翻译 |
| `COMP/icons.json` | 实体图标（按平台 → translation_key 索引） | 新实体需要专属图标时补一行 |
| 仓库根目录 `scripts/format_code.py` | Python/Lua 代码格式化（CI 强制） | 提交前运行 |
| 仓库根目录 `scripts/sort_device_mapping.py` | mapping 中 Platform 排序规范化（CI 强制） | 提交前运行 |
| 仓库根目录 `scripts/sort_translations.py` | 翻译与 icons.json 排序规范化（CI 强制） | 提交前运行 |
| `CONFIG/.storage/midea_smart_home/lua_devices/T0xXX[_SN8].lua` | 云端自动下载的设备 Lua | 只读，分析协议用 |
| `CONFIG/.storage/midea_smart_home/lua_common/` | 云端下载的公共 Lua 依赖 | 只读 |
| `CONFIG/.storage/midea_smart_home/json_files/T0xXX_<设备ID>[_sn8].json` | 每台设备缓存的 token/key | 只读 |

**Lua 文件选取优先级**（运行时）：集成目录 `COMP/lua/T0xXX[_SN8].lua`（自定义） → `.storage` 云端下载文件（带 sn8 的新文件名优先）。想让 AI 修改 Lua 逻辑时，把改好的文件放进 `COMP/lua/` 即可覆盖，升级也不会被云端文件顶掉。

**device_mapping 选型优先级**：格式化后的型号名（小写、非字母数字转下划线）→ SN8 → `default_<category>` → `default`。同一型号的特殊差异可以单独开一个型号 key，不影响其他型号。

---

## 4. 第一步：为 AI 准备调试材料

信息越全，AI 一次成功率越高。请收集以下材料：

### 4.1 设备基本信息

- 添加设备列表里的完整条目：`名称 | 型号 | T0xXX | 协议`
- 设备在美居 App 里的产品类型截图（帮助判断它属于风扇/净化器/热水器等哪一类）

### 4.2 开启 debug 日志

在 `CONFIG/configuration.yaml` 加入（修改后重启或调用 `logger.set_level` 服务生效）：

```yaml
logger:
  default: warning
  logs:
    custom_components.midea_smart_home: debug
```

debug 级别下日志会包含：

- `Raw response hex (N bytes): ...`：设备原始报文
- `[DeviceType:0xXX] Received status: ...`：Lua 解码后的 status 字段（**适配 mapping 最重要的依据**）
- `Status update: ...`：经计算/修正后的数据
- `Setting attribute ... / Setting attributes: ...`：下发的控制指令

### 4.3 导出诊断包（推荐）

集成页面 → **配置** → **🔬 获取日志与设备属性**，会生成一个 zip（通过 `/local/...` 链接下载，**10 分钟后自动删除**），内含：

- `midea_debug.log`：最近的集成日志（开启 debug 后内容最全）
- `device_attributes.json`：每台设备的元数据 + **当前全部属性值快照**（适配新类型时直接把里面对应设备的 `attributes` 整段发给 AI）

### 4.4 抓取操作报文

需要分析控制功能时：

1. 开启 debug 日志；
2. 在**美居 App** 或集成里操作设备一次（开关、调温度、切模式等）；
3. 等待设备状态变化，把操作时间点前后的日志保存下来；
4. 如 Lua 解码失败，把 `Raw response hex` 原始报文一并提供。

### 4.5 参考文件

让 AI 阅读一个**同类已适配设备**的 mapping，例如：

| 你的设备类型 | 参考文件 |
|---|---|
| 风扇 | `device_mapping/T0xFA.py`（结构最简单，适合入门） |
| 空气净化器 / 加湿器 | `T0xFC.py`、`T0xFD.py` |
| 空调 / 中央空调网关 | `T0xAC.py`、`T0xCC.py` |
| 电热水器 / 燃气热水器 | `T0xE2.py`、`T0xE3.py` |
| 洗衣机 / 烘干机 | `T0xDA.py`、`T0xDB.py`、`T0xDC.py`、`T0xD9.py`（双筒最复杂） |
| 冰箱 | `T0xCA.py` |

---

## 5. 场景一：适配 ⏳ 待支持的新设备类型

⏳ 设备表示通信、token、Lua、初始化查询全部通过，仅仅因为类型码不在 `DEVICE_TYPES` 中而没有实体。适配通常只需改 2~3 个文件。

### 步骤 1：注册类型码

在 [const.py](../../custom_components/midea_smart_home/const.py) 的 `DEVICE_TYPES` 中新增一行：

```python
0xB7: "Your Device Type English Name",
```

### 步骤 2：让设备先用 default 映射跑出原始属性

把设备添加进 HA（⏳ 设备可以勾选添加）。添加后即使没有实体，诊断包 `device_attributes.json` 里也能看到 Lua 解出的**全部原始字段名和值**——这就是 mapping 的字段来源。

### 步骤 3：新建 `device_mapping/T0xXX.py`

最小骨架（让 AI 仿照同类参考文件填写）：

```python
from custom_components.midea_smart_home.device_mapping._common import *

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "initial_query": [
            {}
        ],
        "entities": {
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SENSOR: {
                # key 必须与 Lua 解出的 status 字段同名
                "temperature_feedback": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                }
            }
        }
    }
}
```

文件名中的 `XX` 必须与类型码一致（大写十六进制），文件放好后重启 HA 即自动加载，无需注册。

### 步骤 4：补实体中文名与图标

- 新实体的显示名在 [translations/zh-Hans.json](../../custom_components/midea_smart_home/translations/zh-Hans.json) 与 `en.json` 的 `entity.<平台>` 段添加；若实体配置了 `translation_key`，翻译键要与之相同，不配置则默认与字段名相同。
- 需要专属图标的实体，在 [icons.json](../../custom_components/midea_smart_home/icons.json) 的 `entity.<平台>.<translation_key>` 下添加一行，格式固定为 `{ "default": "mdi:图标名" }`（图标在 [Material Design Icons](https://pictogrammers.com/library/mdi/) 查询）；有 `device_class` 的实体（如温度、功率、门锁）通常无需配图标。
- 翻译与图标文件都有**排序要求**，手工添加后运行一次 `python scripts/sort_translations.py` 自动排序（见[第 10 节](#10-提交前的格式与排序检查ci-必过)）。

### 步骤 5：重启验证

1. 重启 Home Assistant；
2. 检查设备页面实体是否出现、数值是否正常；
3. 逐个操作实体，结合 debug 日志确认控制下发正确；
4. 有问题就把日志和 `device_attributes.json` 再发给 AI 迭代。

### mapping 配置速查

```python
"default": {
    "rationale": ["off", "on"],          # 开关类字段的原始值约定（[关, 开]）
    "initial_query": [ {}, {"run_status"} ],  # 启动时依次发送的状态查询；{} 为全量查询
    "polling_query": [ {"run_status"} ],      # 定时轮询查询；不写则仅靠设备主动上报
    "default_values": {"power": "off"},       # 属性初始默认值
    "centralized": ["mode", "temperature"],   # 需合并下发的字段（中央空调多联机场景）
    "calculate": {                            # 二次计算（解析后、显示前）
        "get": [
            {"lvalue": "[remain_time_min]",   # 左边为生成的新字段
             "rvalue": "int(([remain_time] + 59) / 60)"}  # [字段名] 引用原始值
        ]
    },
    "entities": {
        Platform.SENSOR: {
            "字段名": {
                "device_class": SensorDeviceClass.TEMPERATURE,
                "unit_of_measurement": UnitOfTemperature.CELSIUS,
                "state_class": SensorStateClass.MEASUREMENT,
                "translation_key": "cur_temperature",   # 可选，翻译键（默认用字段名）
                "default_value": 0                      # 可选，写入 default_values
            }
        },
        Platform.SWITCH: {
            "字段名": {
                "device_class": SwitchDeviceClass.SWITCH,
                "rationale": ["off", "on"],              # 可选，覆盖全局 rationale
                "command": {"mode": "auto"}              # 可选，按下时附带的固定指令
            }
        },
        Platform.SELECT: {
            "mode": {
                "options": {                              # 选项名 → 下发的 control 片段
                    "auto": {"mode": "auto"},
                    "sleep": {"mode": "sleep"}
                }
            }
        },
        Platform.NUMBER: {
            "target_temp": {
                "min": 16, "max": 30, "step": 1, "mode": "box"
            }
        },
        Platform.FAN: {
            "fan": {
                "power": "power",                         # 电源字段名
                "speeds": [{"gear": 1}, {"gear": 2}],     # 风速档位 → 下发值
                "oscillate": "swing",                     # 摆头字段名
                "preset_modes": {
                    "normal": {"mode": "normal", "speeds": [{"gear": 1}, {"gear": 2}]}
                }
            }
        },
        Platform.CLIMATE: {
            "air_conditioner": {
                "power": "power",
                "precision": PRECISION_HALVES,
                "hvac_modes": {
                    "off":  {"power": "off"},
                    "cool": {"power": "on", "mode": "cool"}
                }
            # 还有 fan_modes、温度上下限等，参考 T0xAC.py / T0xCC.py
            }
        }
    }
}
```

要点：

- 实体配置的 **key 默认就是 Lua status 里的字段名**；字段名不同时可用 `"attribute"` 指定。
- 不同型号差异大时，按**型号**或 **SN8** 再开一个同级 key（如 `"560011AH": {...}`），不要在 `default` 里堆条件。
- 需要单位/枚举等新常量时，统一在 [device_mapping/_common.py](../../custom_components/midea_smart_home/device_mapping/_common.py) 里加并放进 `__all__`，不要在 T0x 文件里写本地常量。
- 字段值需要复杂修正（保持上次有效值、位图解析进度、关机联动等）时，在 [midea_lib/extras.py](../../custom_components/midea_smart_home/midea_lib/extras.py) 的 `DeviceLogicHandler.apply_special_handling` 中按 `device_type` 增加分支，并让 AI 参考已有写法。

---

## 6. 场景二：已支持设备的实体增删改

设备已能添加，但实体有问题时，90% 的工作只在 `device_mapping/T0xXX.py`：

| 现象 | 处理方式 |
|---|---|
| 某个传感器/开关缺失，但 `device_attributes.json` 里有对应字段 | 在对应平台下新增实体配置 |
| 实体存在但一直 `unknown` / 不可用 | 字段名与 Lua status 不一致，用诊断包核对真实字段名 |
| 数值需要换算（秒→分钟、mV→V 等） | 用 `calculate.get` 表达式生成新字段，参考 `T0xB6.py`、`T0x9C.py` |
| 枚举值显示成原始英文/数字 | 改用 `Platform.SELECT` + `options`，或在 `extras.py` 做映射 |
| 某些字段只在特定工作状态下有效 | 给实体配置 `condition` 控制可用性：`{"eq": ["mode", "auto"]}`（字段等于某值时可用）或 `{"not": ["error_code"]}`（字段为假值时可用） |
| 关机后状态残留、进度位图需要解析 | 在 `extras.py` 增加设备特例 |
| 状态不主动刷新 | 配置 `polling_query` 并在集成选项里开启轮询 |
| 改完不生效 | 确认改的是 `COMP/device_mapping/` 且**重启了 HA**；必要时在集成选项中"清理本地配置文件"后重新加载 |

修改后务必双向验证：**显示**（HA 实体值与设备/App 一致）和**控制**（HA 操作后设备真实动作，且 debug 日志中 `Setting attributes` 的内容正确）。

---

## 7. 场景三：Lua 协议层问题

### 7.1 Lua 文件的接口契约

厂商 Lua 必须实现两个全局函数（见 [midea_lib/lua.py](../../custom_components/midea_smart_home/midea_lib/lua.py)）：

| 函数 | 方向 | 输入（JSON 字符串） | 输出 |
|---|---|---|---|
| `dataToJson` | 解码上报 | `{"deviceinfo": {...}, "msg": {"data": "<报文hex>"}}` | `{"status": {字段...}}` 形式的 JSON 字符串 |
| `jsonToData` | 编码查询/控制 | 查询：`{"deviceinfo":..., "query": {...}}`；控制：`{"deviceinfo":..., "control": {...}, "status": {...}}` | 报文字节的 **hex 字符串** |

硬性要求：**`dataToJson` 必须始终返回合法 JSON 字符串**；解析失败时返回兜底值 `{"status":{"version":0}}`，不能返回 `nil`/空串，否则上层解析会直接报错。初始化校验只认 `available`、`version` 之外的真实数据字段。

### 7.2 常见情况与对策

| 现象 / 列表原因 | 排查与处理 |
|---|---|
| `无法获取 Lua 文件`（no_lua） | 云端没有该型号 Lua；可在用户群/Issue 寻找同型号 Lua，放入 `COMP/lua/T0xXX_SN8.lua` 后重新添加 |
| 日志 `decode_status Lua error` | Lua 执行报错，把完整报错栈发给 AI；通常是新版报文分支没处理 |
| 日志 `decode_status JSON parse error` | Lua 返回了非法 JSON，按上面的接口契约修复 |
| 只有 `Raw response hex` 没有 `Received status` | Lua 没认出这条报文；让 AI 结合 App 操作对照 hex 补充分支 |
| 上报能解、控制无效 | 检查 `jsonToData` 的 control 编码，用日志中 `Setting attributes` 与 App 抓的 hex 对比 |
| `V3 无法获取有效 token/key`（no_token） | 网络/云端问题，与适配无关；确认能访问美居服务器，必要时删除集成重新添加 |
| `V2 0x0110 协议暂不支持`（protocol） | 新协议变体，目前无法本地通信，适配 mapping/Lua 均无法解决 |
| `初始化查询数据长度不足`（no_status） | 连接成功但设备没回有效数据：Lua 不匹配、设备处于休眠/未配网状态都会导致；先尝试唤醒设备再扫 |

### 7.3 用自定义 Lua 覆盖云端文件

1. 从 `CONFIG/.storage/midea_smart_home/lua_devices/` 找到当前 Lua，复制给 AI 修改；
2. 改好后命名为 `T0xXX.lua` 或 `T0xXX_SN8.lua`，放入 `COMP/lua/`（该目录已有示例）；
3. 重启 HA，运行时会优先加载自定义文件；
4. 在集成选项中执行"清理本地配置文件"可排除旧云端文件干扰（清理前会自动备份到 `.storage/midea_smart_home-backup`）。

---

## 8. 设备分类与失败原因对照表

分类逻辑见 [config_flow.py](../../custom_components/midea_smart_home/config_flow.py) 的 `_classify_discovered_devices`，按顺序短路判定：

| 顺序 | 判定 | 归类 | 界面文案 |
|---|---|---|---|
| 1 | 设备上报 V2 `0x0110` 协议变体 | ❌ 不支持 | V2 0x0110 协议暂不支持 |
| 2 | V3 设备拿不到 token/key（云端与本地缓存均失败） | ❌ 不支持 | V3 无法获取有效 token/key |
| 3 | 云端下载与本地均无 Lua 文件 | ❌ 不支持 | 无法获取 Lua 文件 |
| 4 | 初始化状态查询无真实字段（5 秒超时） | ❌ 不支持 | 初始化查询数据长度不足 |
| 5 | 探测全通过，但类型码不在 `DEVICE_TYPES` | ⏳ 待支持 | 条目带 `⏳ 待支持` 后缀 |
| 6 | 其余（V1/V2 及 V3 验证通过且类型已知） | ✅ 支持 | 正常条目 |

---

## 9. 调试工具箱

### 9.1 日志配置

```yaml
logger:
  default: warning
  logs:
    custom_components.midea_smart_home: debug
```

### 9.2 常用排查动作

- **集成 → 配置 → 🔬 获取日志与设备属性**：一键打包日志 + 全部设备属性（zip 10 分钟有效）。
- **集成 → 配置 → 🗑️ 清理本地配置文件**：Lua/JSON 缓存异常、协议更新后使用；清理前自动备份到 `.storage/midea_smart_home-backup`。
- **重新扫描**：只重新发现局域网设备，不会重新登录云端。
- 删除集成条目重新添加前，建议先清理本地配置文件。

### 9.3 日志关键词速查

| 关键词 | 含义 |
|---|---|
| `Raw response hex` | 设备原始报文（Lua 之前） |
| `Received status` | Lua 解码结果（mapping 字段依据） |
| `Status update` | 经计算和特例修正后的最终数据 |
| `Setting attribute(s)` | 下发给设备的控制字段 |
| `Initialization query failed` | 添加设备时初始化校验失败 |
| `decode_status Lua/JSON ... error` | Lua 协议层错误 |
| `Connection error / Authentication error / Invalid token` | 网络或 token/key 问题 |
| `INITIALIZED` / `CHANGE ... sending notification` | 设备上线/离线状态变化 |

### 9.4 反馈时请脱敏

日志与诊断包可能包含 token、key、账号、SN 等敏感信息，提交 Issue 或发到群里前请打码。

---

## 10. 提交前的格式与排序检查（CI 必过）

仓库的 GitHub Actions（`.github/workflows/validate.yml`）在每次 push / PR 时执行 5 项检查：**hassfest**、**HACS 校验**，以及 3 个脚本的 `--check`。任何一项不过都会在 CI 报红。适配完成后、提交或发给作者前，请在**仓库根目录**依次运行三个脚本（不带参数即自动修复）：

```bash
python scripts/format_code.py            # 格式化所有 .py 和 .lua
python scripts/sort_device_mapping.py    # 规范化 device_mapping 平台顺序
python scripts/sort_translations.py      # 排序翻译文件与 icons.json
```

只想检查不修改，加 `--check`（CI 就是这种模式）。

### 10.1 `format_code.py`：代码格式规则

作用范围：`custom_components/midea_smart_home` 下**全部 `.py` 和 `.lua`**（包括你新增的 `T0xXX.py` 和自定义 Lua）。

- 缩进统一 4 个空格，禁止 Tab；
- 删除行尾多余空格；
- 文件末尾保留且只保留一个换行；
- 类内部方法之间空 1 行；
- 顶层 class / 顶层函数之间空 2 行；
- 不允许连续多个空行；
- Lua 文件同样要求去行尾空格、Tab 转 4 空格、末尾换行。

### 10.2 `sort_device_mapping.py`：mapping 平台顺序规则

每个 `T0x*.py` 中 `entities` 字典里的 `Platform.*` 条目必须按以下固定顺序排列，且每个条目末尾除最后一个外都要有逗号：

```
CLIMATE → COVER → FAN → HUMIDIFIER → LIGHT → TEXT → TIME →
VACUUM → WATER_HEATER → BUTTON → LOCK → NUMBER → SWITCH →
SELECT → BINARY_SENSOR → SENSOR
```

即"控制类平台在前、传感类平台在后"。新建 mapping 时直接按这个顺序写；没把握就写完跑脚本自动排。

### 10.3 `sort_translations.py`：翻译与图标排序规则

作用文件：`translations/en.json`、`translations/zh-Hans.json`、`icons.json`。

- 所有 JSON 键按**自然顺序**递归排序（数字按数值排，如 `mode2` 在 `mode10` 前面）；
- 例外：`data` 和 `data_description` 两个键的内部顺序保持不动（对应表单字段展示顺序）；
- `icons.json` 使用紧凑格式，每个实体独占一行：
  `"translation_key": { "default": "mdi:xxx" }`；
- 因此**不要手工纠结键的插入位置**——在正确的层级里加好内容，然后运行脚本排序即可。

### 10.4 hassfest / HACS 校验要点

这两项是 HA 官方与 HACS 的校验，无法用脚本自动修复，适配时注意：

- 翻译文件的 flow step 内只能有标准键（`title` / `description` / `data` / `data_description` / `menu_options` 等），自定义键会报 `not a valid option`；
- `manifest.json`、`icons.json` 必须是合法 JSON；
- Python 文件不能有语法/导入错误（mapping 里引用的 `_common` 常量必须存在）。

---

## 11. Commit 与 PR 规范

以下约束与 [CONTRIBUTING.md](../../CONTRIBUTING.md) 完全一致。让 AI 帮你写 commit message 和 PR 描述时，把本节规则一并发给它。

### 11.1 分支与提交粒度

1. Fork 仓库后，**从 `staging` 分支**切出功能分支（不要基于 `main`）；
2. 一个 PR 只解决**一个**设备适配 / 一个问题，不要把多台设备、无关重构混在一起；
3. 只 stage 本次适配相关的文件（用 `git add <具体文件>`），**不要 `git add -A`**，
   绝不提交 `.storage/` 下的个人配置、token/key、日志、诊断包等；
4. 提交前必须在真机本地验证通过，且[第 10 节](#10-提交前的格式与排序检查ci-必过)的三个 `--check` 全部为 `[OK]`。

### 11.2 Commit message 格式

```
<type>: <subject>
<空行>
<body>
<空行>
<footer>
```

**type**（小写，必填）：

| type | 用途 |
|---|---|
| `feat` | 新功能 / 新设备适配 |
| `fix` | 修复 bug |
| `docs` | 仅文档改动（可省略 body） |
| `style` | 不改变语义的格式调整（空格、换行等） |
| `refactor` | 既不修 bug 也不加功能的重构 |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 构建、脚本、杂项 |
| `revert` | 回滚历史提交 |

**subject**：祈使句、现在时；首字母**不大写**；结尾**不加句号**；尽量简短（如 `add T0xB7 device mapping`）。

**body**：除 `docs` 类型外为必填，说明改动内容与原因，每行不要过长。

**footer**（可选）：引用关联的 Issue / PR，如 `Closes #123`。

设备适配的示例：

```
feat(device_mapping): add T0xB7 dehumidifier mapping

Register 0xB7 in DEVICE_TYPES and add default mapping with
power switch, humidity sensor and target humidity number.
Include translation keys for zh-Hans/en and mdi icons.

Closes #123
```

修复的示例：

```
fix(setup): require real status data before validation passes
```

> 注意：**不要**让 AI 使用 `--amend`、`--no-verify`、`--force` 等方式绕过检查或改写已推送的历史。

### 11.3 代码风格要求

- 遵循 [Google Python Style Guide](https://google.github.io/pyguide.html)，格式以 `scripts/format_code.py` 的输出为准；
- 代码注释一律使用**英文**；
- 中英文混排时，中文与英文/数字之间留一个空格（如"支持 T0xAC 空调"），文档中也保持这一习惯；
- 变量命名要准确表达语义；同类方法风格保持一致、优先早返回。

### 11.4 PR 描述自查清单

提交 PR 前确认：

- [ ] 基于 `staging` 分支，且只包含本次适配的相关文件；
- [ ] 三个格式/排序检查通过，hassfest / HACS 无报错；
- [ ] 真机验证：实体显示正确、控制双向可用、开关机与上下线正常；
- [ ] PR 描述写清：**问题/需求 → 解决方案 → 测试方式**；
- [ ] 附上设备四要素：型号、SN8、T0x 类型码、协议版本，以及测试截图或日志（脱敏后）；
- [ ] 如有配套改动（Lua、常量、特例逻辑、文档），在描述中列明；
- [ ] 有测试则运行并通过。

PR 描述可以直接套用：

```
## 背景
设备：<型号> / SN8: <SN8> / T0xXX / V3，扫描显示 ⏳ 待支持（或：某实体异常）。

## 改动
- const.py 注册 0xXX
- 新增 device_mapping/T0xXX.py（default + 型号差异 key）
- 补充 zh-Hans/en 翻译与 icons.json 图标
- （如有）extras.py 增加 xxx 特例

## 验证
- [ ] 传感器读数与美居 App 一致
- [ ] 各开关/模式/数值控制双向生效
- [ ] format_code / sort_device_mapping / sort_translations --check 全部通过
```

---

## 12. 可直接复制给 AI 的提示词模板

> 把【】中的内容替换成你的实际信息。建议在 Trae / VS Code 中直接打开集成源码目录后使用，AI 可以自行查阅参考文件。

### 模板 A：适配 ⏳ 新设备类型

```
我在适配 Home Assistant 的 midea_smart_home 集成（美的美居局域网协议）。
我的设备：名称【】，型号【】，类型码 T0x【】，协议 V【】，设备类别类似【风扇/净化器/热水器...】。
该设备扫描时显示"⏳ 待支持"，说明通信与 Lua 均正常，只是缺少 device_mapping。

附件是诊断包中的 device_attributes.json（该设备的 attributes 段）：
【粘贴 attributes JSON】

请你：
1. 阅读 device_mapping/T0xFA.py（或我指定的同类参考文件 T0x【】.py）了解 mapping 结构；
2. 在 const.py 的 DEVICE_TYPES 注册 0x【】；
3. 新建 device_mapping/T0x【】.py，基于 attributes 中真实存在的字段配置实体，
   不确定用途的字段先保留为 sensor 并加英文注释说明，不要臆造字段；
   entities 内 Platform 顺序遵循 CLIMATE...SENSOR 的固定顺序；
4. 在 translations/zh-Hans.json 和 en.json 补充新实体名称，
   需要专属图标的在 icons.json 补 mdi 图标；
5. 完成后按 CI 要求自检：4 空格缩进、方法间空 1 行/顶层间空 2 行、
   末尾单换行，并提醒我依次运行
   scripts/format_code.py、scripts/sort_device_mapping.py、scripts/sort_translations.py；
6. 按项目规范生成 commit message（从 staging 切分支，格式
   `feat(device_mapping): add T0x【】 ...`，subject 小写祈使句、无句号，
   body 说明改动与原因），并给出 PR 描述草稿（型号/SN8/类型码/协议/验证项）；
7. 告诉我需要如何验证。
```

### 模板 B：修正已支持设备的实体 / 数值

```
midea_smart_home 集成，设备 T0x【】 型号【】。
问题：【哪个实体，现象是什么，例如"湿度在关机后显示 0 / 缺少 xxx 开关 / 风速档位不对"】。

附件：
1. device_attributes.json 中该设备的 attributes：【粘贴】
2. 操作前后的 debug 日志（含 Received status 和 Status update）：【粘贴】
3. 期望的正确行为：【】

请先阅读 device_mapping/T0x【】.py 判断问题在 mapping、calculate 表达式
还是 midea_lib/extras.py 的特例逻辑，先说明根因再修改，并给出验证步骤。
如改动了 Python/翻译/icons 文件，完成后提醒我运行
scripts/format_code.py 和 scripts/sort_translations.py。
```

### 模板 C：Lua 层解码 / 控制问题

```
midea_smart_home 集成，设备 T0x【】 SN8【】。Lua 解码异常 / 控制无效。
debug 日志：
- 原始报文 Raw response hex：【粘贴 hex 与时间点】
- Lua 报错（如有）：【粘贴 decode_status Lua error 完整栈】
- App 操作【什么功能】后期望 status 出现字段【】，实际：【】
厂商 Lua 文件如下：【粘贴 .storage/midea_smart_home/lua_devices/ 里的 T0x【】*.lua】

请对照 dataToJson/jsonToData 的接口契约定位问题。
注意 dataToJson 失败时必须返回 '{"status":{"version":0}}'，不能返回 nil。
修复后的文件我会放到 custom_components/midea_smart_home/lua/T0x【】_【SN8】.lua 覆盖。
```

### 模板 D：添加设备失败

```
midea_smart_home 添加设备时该设备显示"[不支持] | 【原因文案】"。
设备条目：【名称 | 型号 | T0xXX | 协议】
debug 日志中从扫描到分类完成的片段：【粘贴】
请根据日志判断属于 protocol/no_token/no_lua/no_status 中哪一种，
是配置/网络问题、Lua 缺失，还是代码问题，并给出下一步。
```

---

## 13. 必须转告 AI 的项目规则

把以下规则贴给 AI，可以避免常见返工：

1. 新建 `T0xXX.py` 时第一行固定为
   `from custom_components.midea_smart_home.device_mapping._common import *`，
   所需 HA 常量统一从 `_common.py` 获取，**不要在 mapping 文件里定义本地类型常量**，保持文件清爽。
2. mapping 中只能引用 Lua status **真实存在**的字段；字段依据是诊断包 / `Received status` 日志，不允许猜。
3. 代码注释用英文；实体翻译走 `translations/*.json`。
4. 翻译文件的 flow step 内**只能使用标准键**（`title`/`description`/`data`/`menu_options` 等），
   自定义键无法通过 HACS 翻译校验；运行时标记/原因类文案放代码内置常量。
5. `pre_mode` 等空调专属配置仅适用于具有 `mode` 属性的设备（如 T0xAC、T0xCC）；
   没有 `mode` 的设备（如 T0xCA、T0xE6）禁止添加。
6. 修改设备特例逻辑放 `midea_lib/extras.py`，按 `device_type` 分支，沿用已有方法的代码风格（早返回、同类方法风格一致）。
7. 初始化校验成功的标准是解出真实数据字段（温度、湿度等），`available`、`version` 不算。
8. 不要改动 token/key 获取、UDP 发现等与适配无关的链路；不要提交 `.storage` 下的个人文件。
9. 实体命名遵循项目惯例（如"室内环境温度""水泵运行状态"等简洁中文名）。
10. **CI 格式红线**（详见[第 10 节](#10-提交前的格式与排序检查ci-必过)）：
    - 4 空格缩进、无行尾空格、文件末尾单个换行、方法间空 1 行 / 顶层间空 2 行、无连续空行；Lua 同理；
    - mapping 中 `entities` 的 `Platform.*` 必须按
      `CLIMATE, COVER, FAN, HUMIDIFIER, LIGHT, TEXT, TIME, VACUUM, WATER_HEATER, BUTTON, LOCK, NUMBER, SWITCH, SELECT, BINARY_SENSOR, SENSOR`
      顺序排列；
    - 翻译 JSON 与 `icons.json` 的键保持自然排序（`data`/`data_description` 除外），
      新增内容后由脚本排序，不要手工重排已有键；
    - 新增图标的 `icons.json` 条目格式为 `"translation_key": { "default": "mdi:xxx" }`，
      键与实体的 `translation_key`（无则与字段名）一致；
    - 提交前依次运行 `scripts/format_code.py`、`scripts/sort_device_mapping.py`、
      `scripts/sort_translations.py`（均可自动修复），必要时用 `--check` 自查。
11. **提交规范**（详见[第 11 节](#11-commit-与-pr-规范)）：
    功能分支从 `staging` 切出；commit message 遵循 `<type>: <subject>`
    （如 `feat: add T0xXX ...`，subject 小写祈使句、无句号），
    body 说明改动与原因；一个 PR 只做一件事，不提交 `.storage/` 个人文件；
    禁止使用 `--amend`、`--no-verify`、`--force` 绕过检查。

---

## 14. 适配完成之后

1. 在真机上完整验证一轮：所有传感器读数、每个可控实体的双向控制、开关机/离线再上线。
2. 自查日志无 `Lua error`、`JSON parse error`、未知字段告警。
3. 在仓库根目录运行三个脚本的 `--check` 确认格式/排序全部通过（与 CI 一致）：
   `python scripts/format_code.py --check`、`python scripts/sort_device_mapping.py --check`、
   `python scripts/sort_translations.py --check`。
4. 适配成果欢迎回馈：
   - 在群里分享 `T0xXX.py` 与验证结论；
   - 或按 [CONTRIBUTING.md](../../CONTRIBUTING.md) 与[第 11 节](#11-commit-与-pr-规范)的规范，
     从 `staging` 分支提交 PR，附上设备型号、SN8、类型码与测试情况；
   - 自定义 Lua（如获得授权）可放入集成 `lua/` 目录随版本分发。
5. 遇到无法解决的问题，带上**诊断包 + 操作时间点 + 设备四要素**到 [GitHub Issues](https://github.com/Cyborg2017/midea_smart_home/issues) 反馈。
