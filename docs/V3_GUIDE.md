# v3：内容、使用与更新

v3.0.0把原理图和PCB规则、证据门槛、专项模块与工具路由连接起来。主入口保持`boardcraft`；SCH/PCB历史规则编号保留。安装规则不自动安装MCP，不自动取得EDA权限。

## 包含什么

| 模块 | 用途 |
|---|---|
| HW-01～07 | 需求、接口、计算、研究/仿真、制造、实测与反馈 |
| SCH-01～34 | 原理图功能分区、排版、真实引脚/封装、连接、标签、可读性及自动化读回 |
| PCB布局/电源/差分/晶振 | 锁定机械、装配空间、供电和完整回地、连续参考、按实际条件确定参数 |
| PCB-V07/V08/V09 | 分阶段证据覆盖；规则门禁与原生DRC分别运行；六类工程审查 |
| v3模块路由 | 逐器件/网络分类，按证据选择模块，未知项阻止分类完成 |
| 丝印、RF、FPC | 独立按需参考，区分通用原则与器件/制造专用条件 |
| MCP说明 | 嘉立创EDA编辑/DRC、rftools计算、drawio说明图各自边界 |

## 每次如何使用

```text
使用 $boardcraft 处理当前嘉立创EDA工程。
先读取工程和约束，生成有证据的器件/网络分类与本次规则清单。
保留锁定机械和未授权网络，先完成布局审查再布线。
按当前修订分别提交规则门禁、原生DRC及适用工程核验，未测项单列。
```

配置工作区AGENTS的默认使用入口后，硬件任务可隐式选用；每次仍核对首次实际版本/规则声明。缺资料时保留未知，继续无依赖工作。无RF/FPC的简单板无需加载其全部正文。一次示例只验证其覆盖范围，不能证明所有板型能力。

工程inventory包含`project/revision/source_sha256/layers/components/nets/features`，详见[路由契约](../references/task-routing.md)。

```powershell
python scripts/route_rules.py inventory.json --stage layout --output task_rules.json
python scripts/route_rules.py inventory.json --check task_rules.json --source current.epcb
python scripts/check_pcb_stage.py review.json --pcb current.epcb --stage final
```

路由脚本、阶段检查器与EDA DRC各自验收，互不替代。模块里的规则仍需对象级证据和真实审查。RF/FPC当前是入口和审查方法，具体器件、工艺、弯折寿命与天线性能需专项验证。

## 如何更新规则

新资料先分类：物理原则、器件专用要求、项目工艺/偏好或待核查经验。记录来源版本/页码、适用触发条件、验收证据和替代关系；相冲突的数值回查原厂，不默认挑更宽松值。公开仓库只含原创摘要/链接及获授权例子，密钥、私人项目和第三方原文不进入包。

更新模块正文→更新catalog路由→补能发现遗漏/误路由的测试→运行脚本/包检查→同步工作区与安装副本。日常修正累计CHANGELOG；大版本/关键修正正式Release，README摘要与实际版本一起生成。已发布附件不可原地替换。

## 从旧名和v2.4.2迁移

先将旧名embedded-hardware-design安装目录备份到宿主扫描目录之外，安装新名boardcraft；保留v2.4.2历史包。v3新增inventory与任务路由；旧项目不批量补“通过”，从当前快照重新分类，原有核验只在差异确认后复用。没有新增专项对象时保持既有电气规则，不自动改变旧板。MCP只在指定工作区配置，移动到其他电脑时按其真实路径重装依赖。

完整示例见[按键LED板教程](DEMO.md)，更新记录见[CHANGELOG](../CHANGELOG.md)。

第二个实例见[GD32E230开发板对比](GD32E230.md)，工具职责与上游链接见[工具页](TOOLS.md)。
