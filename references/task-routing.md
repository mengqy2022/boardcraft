# 工程识别与规则分配

先读取真实项目、原理图、PCB、板层/制造条件和锁定对象，再生成inventory。`scripts/route_rules.py`读取已审查的inventory并确定模块；脚本不连接EDA，不根据网络名猜电气功能，不自动修改DRC。

1. 从当前EDA导出原生快照、器件、全部网络、真实铜层和锁定机械基线。记录工程/图页UUID、修订和SHA-256。
2. 对每个器件确定角色，对每个网络确定类别。电源、普通数字、差分/高速、晶振、模拟、开关电源、RF可同时存在；FPC另核对板材及弯折用途。网络名与MPN只产生候选；分类用准确器件/接口、引脚连接、实际板层及项目资料确认。
3. features每项使用`present/absent/unknown`，确定状态带evidence。未知不能当不存在；未识别器件/网络进入待审。边沿、传播延迟与接口要求决定高速约束，不按板子时钟频率二选一。
4. 生成任务规则清单：`python scripts/route_rules.py inventory.json --stage routing --output task_rules.json`。common常开；PCB阶段加载PCB、电源/回流和丝印；超过两层加载multilayer；专项按features加载。新板并读HW-01～07。
5. 复核触发理由、引用、冲突和缺失资料。`--check task_rules.json --source current.epcb`检查清单完整性、分类证据字段与源文件哈希。未分类项阻止完成路由；可以继续不依赖它的工作。
6. 布局、布线、交付继续执行PCB-V07/V08/V09。路由检查通过只说明模块选择/字段/快照一致，不证明分类内容、装配、供地路径或DRC正确。每条适用规则仍须实际检查。

inventory字段：`project/revision/source_sha256/layers/components/nets/features`。components项含`ref/role/evidence`，nets项含`name/class/evidence`；features键为power/high_speed/differential/crystal/analog/switching_power/rf/fpc，每项含state及evidence。evidence引用本项目真实文档及对象，不填空泛的“已确认”。完整流程与示例见[入门案例](../docs/DEMO.md)。

冲突按性质处理：用户决定任务范围和可修改对象；器件绝对限制、制造能力和安全条件需满足，不能以偏好豁免。项目确认参数优先于通用默认；锁定机械冲突报告具体对象。规则未知或相互冲突时记录待确认项，不擅自选择更宽松值。

工具按[mcp-tooling](mcp-tooling.md)选择；RF/FPC模块当前提供审查入口，不宣称全面覆盖所有射频、柔性可靠性或合规规范。修改后重建受影响分类；用户手动接管后重读当前快照。只加载已启用模块正文并复用经差异确认的证据。
