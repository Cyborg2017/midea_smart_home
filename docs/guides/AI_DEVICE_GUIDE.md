# 借助 AI 适配 / 调试设备指南

面向希望借助 AI 编程助手（Trae、ChatGPT、Claude、Cursor 等）为 **midea_smart_home** 适配新设备或调试现有设备的用户。不需要精通 Python，但需要会复制日志、编辑文件、重启 Home Assistant。

> 安装配置请看 [SETUP_GUIDE.md](SETUP_GUIDE.md)，提交反馈请看 [CONTRIBUTING.md](../../CONTRIBUTING.md)。

## 目录

1. [先定位问题类型](#1-先定位问题类型)
2. [5 分钟理解工作原理](#2-5-分钟理解工作原理)
3. [文件地图](#3-文件地图)
4. [准备调试材料](#4-准备调试材料)
5. [三个典型场景](#5-三个典型场景)
6. [提交前检查与 PR 规范](#6-提交前检查与-pr-规范)
7. [AI 提示词模板](#7-ai-提示词模板)
8. [必须转告 AI 的规则](#8-必须转告-ai-的规则)
9. [适配完成之后](#9-适配完成之后)

---

## 1. 先定位问题类型

添加设备时，列表条目只会落在三类：

| 界面表现 | 含义 | 下一步 |
|---|---|---|
| `名称 \| 型号 \| T0xXX \| V3`（可勾选） | ✅ 已支持 | 实体缺失/数值不对 → 场景二 |
| 条目带 `⏳ 待支持` | ⏳ 通信、Lua 全通过，只缺类型映射 | 场景一，最容易适配 |
| `- [不支持] ... \| 原因` | ❌ 协议 / token / Lua / 初始化查询有问题 | 对照下表 → 场景三 |

分类判定顺序（[config_flow.py](../../custom_components/midea_smart_home/config_flow.py) 的 `_classify_discovered_devices`，按序短路）：

| 顺序 | 条件 | 界面文案 |
|---|---|---|
| 1 | 上报 V2 `0x0110` 协议变体 | V2 0x0110 协议暂不支持 |
| 2 | V3 设备拿不到 token/key | V3 无法获取有效 token/key |
| 3 | 云端与本地均无 Lua 文件 | 无法获取 Lua 文件 |
| 4 | 初始化状态查询 5 秒内无真实字段 | 初始化查询数据长度不足 |
| 5 | 探测全通过，但类型码不在 `DEVICE_TYPES` | ⏳ 待支持 |
| 6 | 其余（V1/V2 及 V3 验证通过且类型已知） | ✅ 支持 |

请记下设备四要素：**名称、型号、`T0xXX` 类型码、协议版本（V1/V2/V3）**，与 AI 沟通都围绕 `T0xXX` 展开。

---

## 2. 5 分钟理解工作原理

把这段原理连同问题一起发给 AI，能显著减少它的猜测：

```
设备(局域网 TCP 6444)
  → DeviceController：8370 协议加解密（V3 需要 token/key）
  → MideaCodec（Lua 运行时）：调用厂商 Lua 的 dataToJson，
    把原始报文 hex 解码成 status JSON 字段（如 {"power":"on","temperature":26}）
  → ExpressionEvaluator：按 device_mapping 的 calculate 表达式二次计算
  → DeviceLogicHandler（midea_lib/extras.py）：设备特例修正
  → MideaCoordinator：推送给 HA 实体平台（sensor/switch/climate...）

控制链路（HA → 设备）相反：
实体 → 按 mapping 的 options/command 组装 control dict
  → MideaCodec.build_control 调用 Lua 的 jsonToData 编码成 hex
  → 8370 加密后发给设备

两层解耦：
1. Lua 文件（厂商协议）：字节 ↔ JSON，决定"能解析出哪些字段"
2. device_mapping/T0xXX.py：JSON 字段 → HA 实体，决定"显示成什么、怎么控制"
```

核心结论：

- 能通信但**没有实体 / 实体不对** → 改 `device_mapping/T0xXX.py`（纯 Python，AI 最擅长）。
- 日志里 status 字段缺失 / 乱码 / 控制无反应 → Lua 协议层问题（场景三）。
- V2 `0x0110` 新协议变体目前**无法本地通信**，调 mapping / Lua 都解决不了。

---

## 3. 文件地图

HA 配置目录记为 `CONFIG`（含 `configuration.yaml`），集成目录记为 `COMP`（`custom_components/midea_smart_home`）。

| 路径 | 作用 | 是否要改 |
|---|---|---|
| `COMP/const.py` → `DEVICE_TYPES` | 已注册的 T0x 类型码 | 新类型加一行 |
| `COMP/device_mapping/T0xXX.py` | 某类型的实体映射 | **主要修改对象** |
| `COMP/device_mapping/__init__.py` | 映射加载与选型 | 一般不改 |
| `COMP/device_mapping/_common.py` | mapping 共用的 HA 常量 | 缺常量时加 |
| `COMP/lua/T0xXX[_SN8].lua` | 自定义 Lua 覆盖（随集成分发） | Lua 修复放这里 |
| `COMP/midea_lib/lua.py` | Lua 运行时、加解密辅助 | 一般不改 |
| `COMP/midea_lib/device.py` | TCP 通信、解码、控制、轮询 | 一般不改 |
| `COMP/midea_lib/extras.py` | 各类型特殊数据修正 | 有设备特例时加 |
| `COMP/midea_lib/setup.py` | 添加设备时的连接/初始化校验 | 一般不改 |
| `COMP/translations/zh-Hans.json`、`en.json` | 实体中文名/英文名 | 新增实体补 |
| `COMP/icons.json` | 实体图标 | 需要专属图标时补 |
| `scripts/format_code.py` 等 3 个脚本 | CI 格式/排序检查 | 提交前运行 |
| `CONFIG/.storage/midea_smart_home/` | 云端下载的 Lua、token 缓存 | 只读，分析协议用 |

**Lua 选取优先级**：`COMP/lua/T0xXX[_SN8].lua`（自定义） → `.storage` 云端下载文件（带 sn8 的优先）。改好的 Lua 放进 `COMP/lua/` 即可覆盖，升级不会被云端文件顶掉。

**mapping 选型优先级**：格式化型号名（小写、非字母数字转下划线）→ SN8 → `default_<category>` → `default`。型号差异大时单独开一个型号 key，不影响其他型号。

参考同类已适配设备：

| 你的设备类型 | 参考文件 |
|---|---|
| 风扇（结构最简单，适合入门） | `device_mapping/T0xFA.py` |
| 空气净化器 / 加湿器 | `T0xFC.py`、`T0xFD.py` |
| 空调 / 中央空调网关 | `T0xAC.py`、`T0xCC.py` |
| 电热水器 / 燃气热水器 | `T0xE2.py`、`T0xE3.py` |
| 洗衣机 / 烘干机 | `T0xDA.py`、`T0xDB.py`、`T0xDC.py`、`T0xD9.py` |
| 冰箱 | `T0xCA.py` |

---

## 4. 准备调试材料

信息越全，AI 一次成功率越高。

### 4.1 设备基本信息

- 添加设备列表里的完整条目：`名称 | 型号 | T0xXX | 协议`
- 设备在美居 App 里的产品类型截图（帮助判断属于风扇/净化器/热水器…）

### 4.2 开启 debug 日志

在 `CONFIG/configuration.yaml` 加入（重启或调用 `logger.set_level` 生效）：

```yaml
logger:
  default: warning
  logs:
    custom_components.midea_smart_home: debug
```

常见日志关键词：

| 关键词 | 含义 |
|---|---|
| `Raw response hex` | 设备原始报文（Lua 之前） |
| `Received status` | Lua 解码结果（**适配 mapping 最重要的依据**） |
| `Status update` | 经计算与特例修正后的最终数据 |
| `Setting attribute(s)` | 下发给设备的控制字段 |
| `Initialization query failed` | 添加设备时初始化校验失败 |
| `decode_status Lua/JSON ... error` | Lua 协议层错误 |
| `Connection error / Authentication error / Invalid token` | 网络或 token/key 问题 |
| `INITIALIZED` / `CHANGE ... notification` | 设备上线 / 离线 |

### 4.3 导出诊断包（推荐）

集成页面 → **配置** → **🔬 获取日志与设备属性**，生成可下载的 zip（`/local/...` 链接，10 分钟后自动删除），内含：

- `midea_debug.log`：最近的集成日志
- `device_attributes.json`：每台设备的元数据 + **当前全部属性值快照**（适配新类型时把对应设备的 `attributes` 整段发给 AI）

### 4.4 抓取操作报文

需要分析控制功能时：

1. 开启 debug 日志；
2. 在美居 App 或集成里操作设备一次（开关、调温、切模式等）；
3. 保存操作前后的日志；Lua 解码失败时一并提供 `Raw response hex`。

### 4.5 脱敏

日志与诊断包可能含 token、key、账号、SN，提交 Issue 或发群前请打码。

---

## 5. 三个典型场景

### 场景一：适配 ⏳ 待支持的新类型

通信、token、Lua、初始化查询全部通过，只是类型码未注册，通常只改 2~3 个文件。

**步骤 1：注册类型码**（[const.py](../../custom_components/midea_smart_home/const.py) 的 `DEVICE_TYPES`）

```python
0xB7: "Your Device Type English Name",
```

**步骤 2：先用 default 映射跑出原始属性**

把设备添加进 HA（⏳ 设备可以勾选）。即使没有实体，诊断包里也能看到 Lua 解出的**全部原始字段名和值**——这是 mapping 的字段来源。

**步骤 3：新建 `device_mapping/T0xXX.py`**

```python
from custom_components.midea_smart_home.device_mapping._common import *

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "initial_query": [{}],
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
            },
        },
    }
}
```

文件名 `XX` 必须与类型码一致（大写十六进制），放好后重启 HA 自动加载。

**步骤 4：补翻译与图标**

- 实体显示名加到 `translations/zh-Hans.json` 与 `en.json` 的 `entity.<平台>` 段；配置了 `translation_key` 时翻译键与之相同，否则默认用字段名。
- 需要专属图标时在 `icons.json` 的 `entity.<平台>.<translation_key>` 下加 `{ "default": "mdi:图标名" }`（图标查 [MDI](https://pictogrammers.com/library/mdi/)）；有 `device_class` 的实体通常无需配图标。
- 两个文件都有排序要求，加完运行 `python scripts/sort_translations.py`。

**步骤 5：重启验证**

实体是否出现、数值是否正常 → 逐个操作实体并对照 `Setting attributes` → 有问题把日志和 `device_attributes.json` 再发给 AI 迭代。

**mapping 配置速查**

```python
"default": {
    "rationale": ["off", "on"],               # 开关字段原始值约定（[关, 开]）
    "initial_query": [{}, {"run_status"}],    # 启动查询，{} 为全量
    "polling_query": [{"run_status"}],        # 定时轮询；不写则仅靠主动上报
    "default_values": {"power": "off"},
    "centralized": ["mode", "temperature"],   # 需合并下发的字段（多联机）
    "calculate": {
        "get": [
            {"lvalue": "[remain_time_min]",
             "rvalue": "int(([remain_time] + 59) / 60)"}
        ]
    },
    "entities": {
        Platform.SENSOR: {
            "字段名": {
                "device_class": SensorDeviceClass.TEMPERATURE,
                "unit_of_measurement": UnitOfTemperature.CELSIUS,
                "state_class": SensorStateClass.MEASUREMENT,
                "translation_key": "cur_temperature",  # 可选
            }
        },
        Platform.SWITCH: {
            "字段名": {
                "device_class": SwitchDeviceClass.SWITCH,
                "rationale": ["off", "on"],            # 可选，覆盖全局
                "command": {"mode": "auto"},           # 可选，固定附带指令
            }
        },
        Platform.SELECT: {
            "mode": {
                "options": {
                    "auto": {"mode": "auto"},
                    "sleep": {"mode": "sleep"},
                }
            }
        },
        Platform.NUMBER: {
            "target_temp": {"min": 16, "max": 30, "step": 1, "mode": "box"}
        },
        Platform.FAN: {
            "fan": {
                "power": "power",
                "speeds": [{"gear": 1}, {"gear": 2}],
                "oscillate": "swing",
                "preset_modes": {
                    "normal": {"mode": "normal", "speeds": [{"gear": 1}]}
                },
            }
        },
        Platform.CLIMATE: {
            "air_conditioner": {
                "power": "power",
                "precision": PRECISION_HALVES,
                "hvac_modes": {
                    "off": {"power": "off"},
                    "cool": {"power": "on", "mode": "cool"},
                },
            }
        },
    },
}
```

要点：

- 实体 key 默认就是 Lua status 字段名；不同名时用 `"attribute"` 指定。
- 型号差异大时按型号或 SN8 再开一个同级 key，不要在 `default` 里堆条件。
- 新常量统一加到 `device_mapping/_common.py` 并放进 `__all__`。
- 需要保持上次有效值、位图解析、关机联动等复杂修正时，在 `extras.py` 的 `apply_special_handling` 按 `device_type` 加分支。

### 场景二：已支持设备实体 / 数值问题

90% 的工作只在 `device_mapping/T0xXX.py`：

| 现象 | 处理方式 |
|---|---|
| 实体缺失，但诊断包里有对应字段 | 在对应平台下新增实体配置 |
| 实体一直 `unknown` / 不可用 | 字段名与 Lua status 不一致，用诊断包核对 |
| 需要换算（秒→分钟、mV→V 等） | 用 `calculate.get` 生成新字段，参考 `T0xB6.py`、`T0x9C.py` |
| 枚举显示成原始英文/数字 | 改用 `Platform.SELECT` + `options`，或在 `extras.py` 映射 |
| 指定工作状态下才有效 | 实体加 `condition`：`{"eq": ["mode", "auto"]}` 或 `{"not": ["error_code"]}` |
| 关机后状态残留、进度位图 | 在 `extras.py` 增加设备特例 |
| 状态不主动刷新 | 配置 `polling_query` 并在集成选项里开启轮询 |
| 改完不生效 | 确认改的是 `COMP/device_mapping/` 且已重启；必要时"清理本地配置文件"后重载 |

修改后务必双向验证：**显示**（与设备/App 一致）和**控制**（设备真实动作，且 `Setting attributes` 正确）。

### 场景三：Lua 协议层问题

厂商 Lua 必须实现两个全局函数（见 [midea_lib/lua.py](../../custom_components/midea_smart_home/midea_lib/lua.py)）：

| 函数 | 方向 | 输入（JSON 字符串） | 输出 |
|---|---|---|---|
| `dataToJson` | 解码上报 | `{"deviceinfo": {...}, "msg": {"data": "<hex>"}}` | `{"status": {字段...}}` 的 JSON |
| `jsonToData` | 编码查询/控制 | 查询：`{"deviceinfo":..., "query": {...}}`；控制：`{"deviceinfo":..., "control": {...}, "status": {...}}` | 报文字节 hex 字符串 |

硬性要求：`dataToJson` **必须始终返回合法 JSON**；失败时返回 `{"status":{"version":0}}`，不能返回 `nil`/空串。初始化校验只认 `available`、`version` 之外的真实数据字段。

| 现象 / 原因 | 处理 |
|---|---|
| `无法获取 Lua 文件` | 云端无该型号 Lua；找到同型号 Lua 放入 `COMP/lua/T0xXX_SN8.lua` 后重新添加 |
| `decode_status Lua error` | Lua 执行报错，把完整栈发给 AI（多为新版报文分支未处理） |
| `decode_status JSON parse error` | 返回了非法 JSON，按接口契约修复 |
| 只有 `Raw response hex` 没有 `Received status` | Lua 没识别该报文，对照 App 操作补分支 |
| 上报能解、控制无效 | 检查 `jsonToData` 编码，对比 `Setting attributes` 与 App 抓包 |
| `V3 无法获取有效 token/key` | 网络/云端问题，确认能访问美居服务器，必要时删除重加 |
| `V2 0x0110 协议暂不支持` | 目前无法本地通信，改 mapping / Lua 都无效 |
| `初始化查询数据长度不足` | 连接成功但无有效数据：Lua 不匹配、设备休眠/未配网，先唤醒再扫 |

用自定义 Lua 覆盖云端文件：

1. 从 `CONFIG/.storage/midea_smart_home/lua_devices/` 复制当前 Lua；
2. 改好后命名为 `T0xXX.lua` 或 `T0xXX_SN8.lua` 放入 `COMP/lua/`；
3. 重启 HA（运行时优先加载自定义文件）；
4. 必要时执行"清理本地配置文件"排除旧云端文件干扰（会自动备份到 `.storage/midea_smart_home-backup`）。

---

## 6. 提交前检查与 PR 规范

CI（`.github/workflows/validate.yml`）会执行 hassfest、HACS 校验与 3 个脚本的 `--check`，任何一项不过都会报红。在仓库根目录依次运行（不带参数即自动修复）：

```bash
python scripts/format_code.py            # 格式化全部 .py 与 .lua
python scripts/sort_device_mapping.py    # 规范化 mapping 平台顺序
python scripts/sort_translations.py      # 排序翻译文件与 icons.json
```

常用规则：

- **格式**：4 空格缩进、无 Tab、无行尾空格、文件末尾单个换行；类内方法间空 1 行、顶层之间空 2 行、禁止连续空行；Lua 同理。
- **Platform 顺序**：`CLIMATE → COVER → FAN → HUMIDIFIER → LIGHT → TEXT → TIME → VACUUM → WATER_HEATER → BUTTON → LOCK → NUMBER → SWITCH → SELECT → BINARY_SENSOR → SENSOR`（控制类在前、传感类在后）。
- **排序**：翻译与 `icons.json` 按自然顺序递归排序，例外是 `data`/`data_description` 内部保持不动；新内容加好后跑脚本排序，不要手工重排已有键。
- **hassfest / HACS**：翻译的 flow step 内只能用标准键（`title`/`description`/`data`/`data_description`/`menu_options` 等）；`manifest.json`、`icons.json` 必须是合法 JSON；Python 不能有语法/导入错误。

提交规范（与 [CONTRIBUTING.md](../../CONTRIBUTING.md) 一致）：

- 从 `staging` 切功能分支（不要基于 `main`）；一个 PR 只做一件事；只 `git add <具体文件>`，绝不提交 `.storage/`、token/key、日志、诊断包。
- Commit 格式：`<type>: <subject>` + 空行 + body（可选 footer）。type：`feat` / `fix` / `docs` / `style` / `refactor` / `perf` / `test` / `chore` / `revert`；subject 用祈使句、小写开头、不加句号。
- 示例：

```
feat(device_mapping): add T0xB7 dehumidifier mapping

Register 0xB7 in DEVICE_TYPES and add default mapping with power
switch, humidity sensor and target humidity number.

Closes #123
```

- 不允许用 `--amend`、`--no-verify`、`--force` 绕过检查或改写已推送的历史。

PR 描述按"问题/需求 → 解决方案 → 测试方式"写，并附设备四要素（型号、SN8、类型码、协议）与脱敏截图/日志；自查清单：真机显示正确、控制双向可用、上下线正常、3 个 `--check` 全部 `[OK]`、hassfest/HACS 无报错。

---

## 7. AI 提示词模板

> 把【】替换为实际信息。建议在 Trae / VS Code 中打开集成源码目录后使用，AI 可自行查阅参考文件。

**模板 A：适配 ⏳ 新设备类型**

```
我在适配 Home Assistant 的 midea_smart_home 集成（美的美居局域网协议）。
设备：名称【】，型号【】，类型码 T0x【】，协议 V【】，类别类似【风扇/净化器/热水器…】。
扫描显示"⏳ 待支持"，说明通信与 Lua 均正常，只缺 device_mapping。

诊断包中该设备的 attributes：
【粘贴 JSON】

请你：
1. 阅读 device_mapping/T0xFA.py（或我指定的 T0x【】.py）了解 mapping 结构；
2. 在 const.py 的 DEVICE_TYPES 注册 0x【】；
3. 新建 device_mapping/T0x【】.py，只使用 attributes 中真实存在的字段，
   不确定用途的字段先保留为 sensor 并加英文注释，不要臆造；
   entities 内 Platform 顺序遵循规范；
4. 补充 translations/zh-Hans.json、en.json 名称，需要时补 icons.json；
5. 提醒我运行三个 scripts 下的检查脚本，并按规范给出 commit message 与 PR 描述；
6. 说明如何验证。
```

**模板 B：修正已支持设备的实体 / 数值**

```
midea_smart_home 集成，设备 T0x【】，型号【】。
问题：【哪个实体，现象是什么，例如"湿度关机后显示 0 / 缺少 xxx 开关"】。

附件：
1. device_attributes.json 中该设备的 attributes：【粘贴】
2. 操作前后 debug 日志（含 Received status、Status update）：【粘贴】
3. 期望行为：【】

请先阅读 device_mapping/T0x【】.py 判断问题在 mapping、calculate 还是 extras.py，
先说明根因再修改，并给出验证步骤。
```

**模板 C：Lua 层解码 / 控制问题**

```
midea_smart_home 集成，设备 T0x【】 SN8【】。Lua 解码异常 / 控制无效。
- Raw response hex：【粘贴 hex 与时间点】
- Lua 报错（如有）：【粘贴完整栈】
- App 操作【功能】后期望字段【】，实际：【】
厂商 Lua 文件：【粘贴 .storage/midea_smart_home/lua_devices/ 下的 T0x【】*.lua】

请对照 dataToJson/jsonToData 契约定位问题；dataToJson 失败必须返回
'{"status":{"version":0}}' 而不是 nil。修复后我放到 COMP/lua/T0x【】_【SN8】.lua 覆盖。
```

**模板 D：添加设备失败**

```
midea_smart_home 添加设备时显示"[不支持] | 【原因文案】"。
设备条目：【名称 | 型号 | T0xXX | 协议】
扫描到分类完成的 debug 日志：【粘贴】
请判断属于 protocol/no_token/no_lua/no_status 中的哪一种，
说明是网络配置问题、Lua 缺失还是代码问题，并给出下一步。
```

---

## 8. 必须转告 AI 的规则

1. 新建 `T0xXX.py` 第一行固定为 `from custom_components.midea_smart_home.device_mapping._common import *`，HA 常量统一从 `_common.py` 获取，**不在 mapping 内定义本地常量**。
2. mapping 只能引用 Lua status **真实存在**的字段，依据是诊断包或 `Received status` 日志，不允许猜。
3. 代码注释用英文；实体名称走 `translations/*.json`。
4. 翻译 flow step 内只能用标准键，自定义键无法通过 HACS 校验；运行时文案放代码常量。
5. `pre_mode` 等空调专属配置只适用于有 `mode` 属性的设备（如 T0xAC、T0xCC），禁止加到 T0xCA、T0xE6 等。
6. 设备特例逻辑放 `midea_lib/extras.py`，按 `device_type` 分支，沿用已有风格（早返回）。
7. 初始化校验的成功标准是解出真实数据字段，`available`、`version` 不算。
8. 不要改动 token/key 获取、UDP 发现等无关链路；不要提交 `.storage` 下的个人文件。
9. 实体命名沿用项目惯例（如"室内环境温度""水泵运行状态"），简洁准确。
10. 遵守第 6 节的格式、排序、commit 与 PR 规范；改动完成前必须跑完三个脚本。

---

## 9. 适配完成之后

1. 真机完整验证一轮：全部传感器读数、每个可控实体的双向控制、开关机与离线再上线。
2. 日志无 `Lua error`、`JSON parse error`、未知字段告警。
3. 仓库根目录运行三个脚本的 `--check`，确认与 CI 结果一致。
4. 成果欢迎回馈：群里分享 `T0xXX.py` 与验证结论，或按 CONTRIBUTING 提交 PR（附型号、SN8、类型码、测试情况）；自定义 Lua 可放入 `COMP/lua/` 随版本分发。
5. 无法解决时，带**诊断包 + 操作时间点 + 设备四要素**到 [GitHub Issues](https://github.com/Cyborg2017/midea_smart_home/issues) 反馈。
