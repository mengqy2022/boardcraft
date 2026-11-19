# 工具路由与工作区配置

Skill提供任务判断与使用指令；宿主MCP配置决定服务器和工具是否可见，服务器实现决定其能力与边界。Skill无法越过宿主权限，也不提供进程/网络隔离。配置仅在嵌入式工作区的`.codex/config.toml`中，默认不修改全局配置；stdio `cwd`限定启动目录，不是文件系统沙箱。

| 场景 | 工具 | 必须记录 |
|---|---|---|
| 原理图/PCB/封装实时操作、原生DRC | 嘉立创EDA + easyeda-api | 实际窗口/工程/文档身份、工具版本、修改前后读回及网表 |
| 限流、压降、阻抗、RF基础计算 | rftools本地run_calculation | schema、单位、输入、公式/模型、版本、结果及适用范围 |
| 系统框图、叠层说明、RF信号链/EMC接线图 | drawio-engineering | 参数、可编辑XML及实际渲染检查 |
| 场求解、S参数、天线/PDN等远程仿真 | rftools远程工具按任务启用 | 工程需要、外发数据、模型、配额/费用及结果边界 |

当前工作区默认暴露rftools的5个本地查询/计算工具；`solve_calculation`及simulate/job工具未默认开放，不因安装MCP自动上传文件、运行计费服务或配置密钥。需要时使用当前宿主配置流程，记录范围。工具缺失时普通EDA工作继续；需要的专项计算保持未验证并提供替代方法。

安装版本：rftools-mcp 2.11.3（MIT），drawio-engineering-mcp固定提交8599aeb0d1118ef1d1cc0933812d892030a2c4bf（包1.1.0，AGPL-3.0-or-later，握手1.0.0）。第三方代码独立安装，不重新授权或复制进规则包。依赖锁文件保存在工作区。

已实测限制：drawio该提交的SVG exporter只输出占位说明并嵌入XML，不能称为渲染图；PNG路径要求另配浏览器依赖，尚未验证。原理图/PCB动图从实际EDA设计阶段采集；完整图纸/板框必须在裁切内，固定尺寸，去除UI。重放时注明“设计过程回放”，不冒充首次连续屏幕录像。

嘉立创EDA V4.1.60本轮发现：枚举未注入、原理图getAllNets可能为空、截图/缓存可能滞后、otherProperty替换可破坏库关联、孔参数有缩放差异。通过准确签名、源文件/库ID、网表、保存后的新读取、真实屏幕和生产钻孔交叉确认；不能将某次修正倍数推广至所有API/版本。写后留足实际同步时间再读回，不盲目重放失败批次。

来源：[rftools npm](https://www.npmjs.com/package/rftools-mcp)、[drawio固定源码](https://github.com/RFingAdam/drawio-engineering-mcp/tree/8599aeb0d1118ef1d1cc0933812d892030a2c4bf)、[Codex项目配置](https://developers.openai.com/codex/config-basic)。
