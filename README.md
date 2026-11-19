<div align="center">

![Embedded Hardware Design — Schematic. Layout. Routing. Evidence.](assets/cover.svg)

# Embedded Hardware Design

**让原理图清楚易读，让 PCB 设计有据可查。**

面向 AI 辅助嵌入式硬件设计的可携带规则、检查模板与证据门槛。

[![Release](https://img.shields.io/github/v/release/mengqy2022/embedded-hardware-design-skill?style=flat-square&color=0f766e)](https://github.com/mengqy2022/embedded-hardware-design-skill/releases/latest)
[![CI](https://github.com/mengqy2022/embedded-hardware-design-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/mengqy2022/embedded-hardware-design-skill/actions/workflows/ci.yml)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-334155?style=flat-square)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-334155?style=flat-square)](https://www.python.org/downloads/)

**简体中文** · [English](README.en.md) · [快速安装](docs/INSTALLATION.md) · [版本记录](CHANGELOG.md) · [提出建议](https://github.com/mengqy2022/embedded-hardware-design-skill/issues/new/choose)

</div>

## 最新进展

**v3.0.0：** 逐对象分类与规则模块路由，新增丝印/FPC/RF入口及工作区MCP使用边界；包含嘉立创EDA按键LED板动图教程。详见[完整使用指南](docs/V3_GUIDE.md)、[设计实例与评估](docs/DEMO.md)和[更新日志](CHANGELOG.md)。

<!-- release:start -->
**[v3.0.0](https://github.com/mengqy2022/embedded-hardware-design-skill/releases/tag/v3.0.0) · 2026-11-19**

- 引入有证据的器件/网络分类、profile目录和任务规则清单；按真实叠层、接口、边沿/传播、RF/FPC对象组合模块，未知项不能默认为不存在。
- 新增只读规则路由器及覆盖/快照检查，拒绝缺失分类证据、遗漏模块和过期源文件；不修改EDA、自动放宽DRC或把分类检查当电气认证。
- 新增丝印、RF、FPC专项入口，审查用户资料中的比例/数值/绝对化说法；板厂限定数值保留待核查状态，不把附件原文/图片放入发布包。
- 接入工作区级rftools-mcp 2.11.3和固定提交的drawio-engineering-mcp：本地计算、图示、EDA编辑各自路由，远程仿真/文件上传不默认开放；记录实际版本差异和SVG占位导出限制。
- 新增独立嘉立创EDA按键LED板实例、器件和选值说明、逐段原理图连线/PCB布线动图及能力评估；动态图仅保留图纸/板框，回放如实标注，不冒充首次录屏。
- 保留SCH/PCB编号与V07/V08/V09独立核验，补充库关联、真实引脚/焊盘、API缓存/孔径与生产文件交叉检查。旧项目按当前修订重分类，不追溯批量填通过。
- 更新双语README、完整使用指南、迁移和发布说明；发布包不含密钥、第三方MCP源码及私人历史工程。RF/FPC实板、制造放行与样机实测未由本版证明。

[完整变更记录](CHANGELOG.md) · [安装包与校验文件](https://github.com/mengqy2022/embedded-hardware-design-skill/releases/tag/v3.0.0)
<!-- release:end -->

## 能解决什么

把原理图排版、PCB 布局布线和交付检查串成可复用的工作方式。规则按任务读取，复用现有工程与已验证记录，减少重复解释和无关修改。

| 设计环节 | 关注内容 | 入口 |
| --- | --- | --- |
| 新板与电气变更 | 量化需求、共享接口、计算与风险验证、样机反馈 | [HW-01～07](references/design-workflow.md) · [记录模板](assets/DESIGN_EVIDENCE.md) |
| 原理图 | 功能分区、引脚与符号一致、连线清晰、标签与字体不重叠 | [SCH 规范](references/schematic-style.md) |
| PCB 布局 | 锁定机械条件、器件装配间距、接口位置、丝印可读性 | [布局与制造](references/layout-manufacturing.md) |
| 供电与回流 | 逐电源脚去耦、输入/输出电容、低电感回路、真实 GND 铜路 | [电源与接地](references/power-ground.md) |
| 敏感网络 | 差分耦合、连续参考、必要等长、晶振敏感区域 | [差分与晶振](references/differential-crystal.md) |
| 阶段验收 | 器件/电源脚覆盖、当前修订证据、原生 DRC、制造输出 | [PCB-V07](references/pcb-stage-review.md) |

**适用范围：** 常见低压嵌入式硬件。器件参数、叠层、阻抗、电流和制造工艺按项目确定；高压、隔离、DDR及RF/FPC专用参数另查准确指南。v3的专项模块提供审查入口，不宣称覆盖所有专用设计。规则包提供设计方法，实时操作由独立的 EDA 工具完成。

## 完整设计示例

[按键LED板：器件、原理、电路图、PCB、检查与能力评估](docs/DEMO.md)。动态图只保留真实EDA图纸/板框内容，包含逐段连接过程回放。

![原理图连线](assets/demo/schematic-wiring.gif)

![PCB布线](assets/demo/pcb-routing.gif)

## 三步开始

### 1. 安装规则

在 [最新 Release](https://github.com/mengqy2022/embedded-hardware-design-skill/releases/latest) 下载 `embedded-hardware-design.zip`；Windows PowerShell **首次安装**：

```powershell
$skillArchive = Join-Path $env:TEMP 'embedded-hardware-design.zip'
Invoke-WebRequest 'https://github.com/mengqy2022/embedded-hardware-design-skill/releases/latest/download/embedded-hardware-design.zip' -OutFile $skillArchive
Expand-Archive -LiteralPath $skillArchive -DestinationPath "$env:USERPROFILE/.codex/skills"
```

新建会话核对 Skill 列表。已有安装或旧名 `pcb-design-rules` 时，按 [升级与迁移](docs/INSTALLATION.md#升级与迁移) 先备份再替换。发布附件附带 `SHA256SUMS.txt`。

普通 ChatGPT 可上传 Release 中的 `HARDWARE_DESIGN_RULES_CHATGPT.md`；工具连接和可选插件见 [完整安装说明](docs/INSTALLATION.md)。

### 2. 带上工程与约束

提供当前工程、项目规则、准确器件资料，以及板框、锁定器件、叠层和板厂条件。示例：

```text
使用 $embedded-hardware-design 优化当前原理图与 PCB。
先读取项目说明、规则和现有核验报告；保持未授权的网络与锁定机械对象不变。
新板或电气/接口变更按 HW-01～07 关联需求、计算与验收；仿真按风险选择，实测状态单独记录。
先完成布局和逐电源脚供电/回地审查，再布线；按 PCB-V07 留下当前修订证据。
```

项目 `AGENTS.md` 可加入：

```text
原理图或 PCB 任务使用 embedded-hardware-design；按任务读取 SCH/PCB 细则，
遵循项目约束。首次回复说明正在使用的实际版本及规则范围；交付时给实际检查、待验证项和证据。
```

Skill已显式允许按任务自动选用。跨工作区默认约定、版本提示与缺失处理见[自动选用与可见提示](docs/INSTALLATION.md#自动选用与可见提示)；普通ChatGPT使用合并规则文档及项目指令。

### 3. 以证据完成验收

```mermaid
flowchart LR
  A[读取工程与约束] --> B[布局与关键回路]
  B --> C[布局阶段门槛]
  C --> D[关键及普通布线]
  D --> E[铺铜与 GND 收尾]
  E --> F[DRC · 适用泪滴 · 重铺铜 · DRC]
  F --> G[最终门槛与生产文件检查]
```

```powershell
python scripts/check_pcb_stage.py review.json --pcb current.epcb --stage layout
python scripts/check_pcb_stage.py review.json --pcb current.epcb --stage final
```

记录格式见 [阶段模板](assets/PCB_STAGE_REVIEW.json)。检查器验证覆盖、阶段和证据文件哈希；几何、电气、原生 DRC 与人工判断仍须真实执行。历史结论只对应其原有修订。

## 规则与模板导航

| 我现在需要…… | 阅读或复用 |
| --- | --- |
| 建立需求、计算和样机验证闭环 | [HW-01～07](references/design-workflow.md) · [精简模板](assets/DESIGN_EVIDENCE.md) |
| 了解 Skill 的执行入口 | [SKILL.md](SKILL.md) |
| 绘制/整理原理图 | [排版规则](references/schematic-style.md) · [检查清单](assets/SCHEMATIC_REVIEW.md) |
| 借鉴工程版式、处理规则冲突 | [样本方法与取舍](references/schematic-examples.md) |
| 使用嘉立创原理图自动化 | [SCH-28～34 与 API 工作方式](references/easyeda-schematic.md) |
| 配置新项目并记录例外 | [项目规则模板](assets/PROJECT_RULES.md) |
| 完成核验与交付 | [核验与证据](references/verification.md) · [阶段审查](references/pcb-stage-review.md) |
| 查明来源与适用边界 | [来源表](references/sources.md) · [来源指纹](provenance.json) |
| 安装 Ponytail / mattpocock-skills | [可选插件](OPTIONAL_PLUGINS.md) |

规则区分电气原则、用户偏好、项目参数和待验证建议。例如，去耦电容通常并联，物理上的“大到小”排列须服从准确器件要求、低电感回路与稳定性；100 nF 或 20 mil 不是所有设计的通用答案。

## 工具兼容与边界

| 环境 | 用法 |
| --- | --- |
| Codex / 支持 Skill 的宿主 | 安装完整目录，显式调用或由宿主按任务选用 |
| 普通 ChatGPT / 项目知识文件 | 上传合并规则与项目资料；读取规则不等于模型永久训练 |
| 嘉立创 EDA 专业版 | 配合另行安装、连接的 `easyeda-api` 等工具 |
| 其他 EDA | 复用设计原则，使用该工具支持的原生编辑与核验方式 |

Ponytail 与 mattpocock-skills 是可选工作方式插件。上游原理图增强 Skill 的已审阅方法及修正见 [集成说明](references/easyeda-schematic.md)；安装本规则包不自动安装其他插件，也不附带用户工程。

## 参与与维护

- **报告问题 / 提议规则：** 使用 [Issue 模板](https://github.com/mengqy2022/embedded-hardware-design-skill/issues/new/choose)，附准确来源、适用范围与最小证据。
- **贡献内容：** 见 [贡献指南](https://github.com/mengqy2022/embedded-hardware-design-skill/blob/main/CONTRIBUTING.md)，保留 SCH/PCB 编号及来源归属。
- **发布维护：** [发布流程](https://github.com/mengqy2022/embedded-hardware-design-skill/blob/main/docs/RELEASING.md) 使用变更记录生成双语首页摘要，并在 CI 核对版本、链接、测试和包哈希。
- **敏感信息：** 按 [安全说明](https://github.com/mengqy2022/embedded-hardware-design-skill/blob/main/SECURITY.md) 处理；公开内容只保留可复用方法。

## 许可与致谢

文档与原创辅助代码采用 [CC BY-SA 4.0](LICENSE)。[来源表](references/sources.md) 保留作者、链接及适用边界；SparkFun Electronics / jimblom 等来源的归属继续保留。厂商文档、第三方插件和原始工程遵循各自许可，不随本包重新授权。
