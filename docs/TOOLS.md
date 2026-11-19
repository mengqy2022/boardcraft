# 工具与工作方式 / Tools

BoardCraft是规则与证据流程，不自带EDA编辑器、仿真器或第三方插件。宿主决定工具是否可用，项目条件决定是否需要调用。

| 工具 | 何时使用 | 不能据此宣称 |
|---|---|---|
| [嘉立创EDA API Skill](https://github.com/easyeda/easyeda-api-skill) / [Run API Gateway](https://jlc-ext.com/item/oshwhub/run-api-gateway) | 读取工程、编辑副本、原生DRC与导出；实际入口以已安装easyeda-api版本为准 | 安装规则即获得实时连接，或DRC替代工程审查 |
| [原理图增强 Skill](https://github.com/easyeda/easyeda-enhanced-schematic-skill) | 符号/引脚/封装关联及网络扇出方法；按本包已记录取舍应用 | 自动加载全部上游示例或保证其电气正确 |
| [drawio-engineering-mcp](https://github.com/RFingAdam/drawio-engineering-mcp) | 叠层、信号链、射频结构等工程说明图 | 说明图等于PCB布局、场求解或天线实测 |
| [rftools-mcp](https://www.npmjs.com/package/rftools-mcp) / [rftools.io](https://rftools.io) | 记录单位/模型的本地工程计算；按需查询RF计算器 | 解析计算等于实际板厂阻抗、3D EM、VNA或法规验证 |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | 优先复用、最小完整修改、简短证据反馈 | 节省Token可省略DRC和关键验收 |
| [mattpocock-skills](https://github.com/mattpocock/skills) | research定向查原厂资料；writing-for-agents梳理入口/按需引用 | 所有任务必须研究、插件名代表已运行 |

## 当前工作区的已验证范围

`drawio-engineering-mcp`和`rftools`仅在用户指定的嵌入式工作区配置；不随便添加全局服务器。Skill负责选择与调用流程，宿主配置决定暴露范围；cwd不是文件沙箱。

已验证rftools 2.11.3的握手、工具发现和本地LED计算；drawio固定提交8599aeb0d1118ef1d1cc0933812d892030a2c4bf的握手及叠层XML。drawio包1.1.0/握手1.0.0存在版本标识差异；SVG导出为占位实现、PNG额外依赖未验证。未调用远程仿真或上传私人工程。准确边界见[MCP调用参考](../references/mcp-tooling.md)。

## 可选安装

Ponytail与mattpocock-skills的安装命令、版本适配及Hook选择集中见[可选插件](../OPTIONAL_PLUGINS.md)。MCP按上游说明安装到当前项目并配置绝对路径；不同电脑按实际目录和宿主重新配置，仓库不分发第三方源码、密钥或私人配置。

未安装可选插件不妨碍读取BoardCraft规则。需要实时编辑时必须有对应EDA工具；不可用时保存可审查资料和具体未验证项。
