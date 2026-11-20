# 变更记录

## Unreleased

- 规则维护继续累计到下一里程碑；本次板层可行性门槛记录在 3.0.2 待发布版本中，不创建新的 Release。

### English

- Routine changes continue to accumulate toward the next milestone; the layer-feasibility gate is recorded in the unreleased 3.0.2 version and creates no new Release.

## 3.0.2 — 2026-11-20

- 新增 PCB-P12 板层数可行性与成本门槛：既有板以当前层数为基线，新板先评估最低可行层数；增加层数必须有低层方案的具体阻碍、关键通道试布/计算或制造依据、替代方案及成本影响。
- 阶段检查器新增 `layer_decision` 结构化字段和行为测试；没有层数候选证据，或二层可行却直接选择四层时，布局阶段不通过。
- GD32E230 案例的四层副本保留为多层探索对照，不能被解释为成本优化或二层不可行的证明。

### English

- Add PCB-P12 for layer-count feasibility and cost justification: use the current layer count as the baseline for existing boards, start new boards from the lowest feasible count, and require concrete lower-layer blockers, critical-channel trial routing/calculation or fabrication evidence, alternatives and cost impact before adding layers.
- Extend the stage checker with a structured `layer_decision` field and behavioral tests; a layout is blocked when candidate evidence is missing or four layers are selected while two layers remain feasible.
- Keep the GD32E230 four-layer copy as a multilayer exploration comparison, not as evidence that the two-layer board was infeasible or cost-optimized.

## 3.0.1 — 2026-11-19

- 更名为 **BoardCraft（板匠）**，调用名 `$boardcraft`；原 `embedded-hardware-design` 的规则编号、阶段门槛与来源保留，提供安装迁移说明。
- 新增 GD32E230 MCU 开发板 PCB 对比案例：P1和原PCB保持不变，副本保持相同板框／接口基准，记录去耦、晶振、装配、供地与实际DRC差异，附图纸范围GIF。
- 重排双语首页为“开始使用→选择规则→看例子→检查证据→扩展工具”，新增统一工具引用页，补齐 drawio-engineering-mcp、rftools、Ponytail、mattpocock-skills 与嘉立创EDA工具链接和边界。
- 按用户明确要求复用现有v3.0.0发布页；先归档原附件及哈希，再更新3.0.1附件与说明。保留原v3.0.0标签，不新增Release、不用旧标签冒充新源码。
- 案例结果按实际证据填写；计算、EDA检查、制造输出、样机与EMC状态分别报告。

### English

- Rename to **BoardCraft**, invoked as `$boardcraft`, preserving the existing rule IDs, evidence gates and migration history.
- Add a PCB-only GD32E230 development-board comparison, protecting the original schematic/PCB and matching the board outline and interface baseline; include cropped GIFs and evidence-based differences.
- Simplify bilingual navigation and document EasyEDA tooling, drawio-engineering-mcp, rftools, Ponytail and mattpocock-skills with upstream links and limitations.
- Refresh the existing v3.0.0 release page at the user's explicit request after archiving previous assets. Keep the original tag immutable and identify the 3.0.1 attachment edition and source commit separately; create no new Release.
- Keep calculations, native EDA checks, manufacturing review and unmeasured prototype performance distinct.

## 3.0.0 — 2026-11-19

- 引入有证据的器件/网络分类、profile目录和任务规则清单；按真实叠层、接口、边沿/传播、RF/FPC对象组合模块，未知项不能默认为不存在。
- 新增只读规则路由器及覆盖/快照检查，拒绝缺失分类证据、遗漏模块和过期源文件；不修改EDA、自动放宽DRC或把分类检查当电气认证。
- 新增丝印、RF、FPC专项入口，审查用户资料中的比例/数值/绝对化说法；板厂限定数值保留待核查状态，不把附件原文/图片放入发布包。
- 接入工作区级rftools-mcp 2.11.3和固定提交的drawio-engineering-mcp：本地计算、图示、EDA编辑各自路由，远程仿真/文件上传不默认开放；记录实际版本差异和SVG占位导出限制。
- 新增独立嘉立创EDA按键LED板实例、器件和选值说明、逐段原理图连线/PCB布线动图及能力评估；动态图仅保留图纸/板框，回放如实标注，不冒充首次录屏。
- 保留SCH/PCB编号与V07/V08/V09独立核验，补充库关联、真实引脚/焊盘、API缓存/孔径与生产文件交叉检查。旧项目按当前修订重分类，不追溯批量填通过。
- 更新双语README、完整使用指南、迁移和发布说明；发布包不含密钥、第三方MCP源码及私人历史工程。RF/FPC实板、制造放行与样机实测未由本版证明。

### English

- Add evidence-backed component/net inventories and composable task modules. Unknown high-speed, RF and FPC classifications remain unresolved instead of silently disabling checks.
- Add a read-only rule router and snapshot/coverage validator, with regression tests for mixed boards, missing evidence, stale snapshots and tampered module selections. Routing is separate from native DRC and engineering acceptance.
- Add silkscreen, RF and FPC review entrypoints, triaging context-dependent manufacturing numbers and rejecting unsupported universal claims. Original attachments and third-party images are excluded.
- Document workspace-scoped rftools 2.11.3 and pinned drawio MCP integration, local calculation defaults, remote-service boundaries, observed version mismatch and placeholder SVG export.
- Add a real EasyEDA button LED tutorial with component explanations, electrical calculations, wiring/routing replay GIFs and a bounded capability assessment. Refresh bilingual documentation, migration and checksummed release packaging.
- Preserve existing rule IDs and independent V07/V08/V09 reviews. No retroactive project approvals, RF/FPC board validation, fabricated measurement results or manufacturing release claims.

## 2.4.2 — 2026-11-16

- 新增 PCB-V09 六类工程审查：电气连接、电源完整性、信号完整性、EMC 风险、热及制造/装配；按项目风险选择审查、计算、仿真和实测，明确各自结论边界。
- 修正 PCB-V07 阶段检查器：布局/最终阶段要求 RULE_GATE、PCB-P09/P10/P11，最终补齐 PI/SI/EMC/THERMAL 等证据；规则门禁及最终 DRC 不可用“不适用”跳过。旧记录缺项或证据过期必须重审补证，不能批量填通过。
- 新增 PCB-V08 双门槛：规则门禁与当前修订版 EDA DRC 分别运行、分别留证并同时通过；检查器只验证覆盖和文件新鲜度，不替代实际工程判断。
- 整合三批 PCB 学习资料，以 TI ADS8860、SLVA680A 和 JLCPCB 官方资料定向核查；补强完整供电/回流、换流回路、ADC 建立、ESD 泄放、时钟/差分时序及盘中孔工艺，剔除缺条件的固定数值与图片评级。只分发原创总结与来源链接。
- 明确 PCB-P09/P10：记录真实层类型；允许有据的四层 SIGNAL 和规则几何电源铜区，区分原生 PLANE。参考地按实际差分所在层确定，90 Ω 参数依据实际制造叠层计算。
- 补充 PCB-P11 锁定机械基准、PCB-V02 Arial 与丝印避让、PCB-V04 独立同网焊盘分离；更新模板、双语首页和可携带安装包。
- 升级提示：旧阶段记录需要补齐新增适用项及当前修订证据。保持现有规则编号和 JSON 结构；不修改用户 PCB，不追溯升级历史板卡检查结论，也不代表任何板卡通过 DRC、性能实测或制造放行。

### English

- Add PCB-V09 reviews for electrical connectivity, power integrity, signal integrity, EMC risk, thermal, and fabrication/assembly; select reviews, calculations, simulation and measurements proportionately to project risk and state their limits.
- Correct the PCB-V07 stage checker: require RULE_GATE and PCB-P09/P10/P11 at layout/final, plus PI/SI/EMC/THERMAL and existing evidence at final. Neither the rule gate nor final DRC can be waived as not applicable. Re-review incomplete or stale records rather than bulk-marking them passed.
- Add PCB-V08: run the rule gate and current-revision EDA DRC independently, retain separate evidence, and require both to pass. Coverage and freshness checks do not replace engineering judgment.
- Consolidate three PCB article batches with focused checks against TI ADS8860, SLVA680A and JLCPCB. Strengthen complete supply/return and commutation loops, ADC settling, ESD discharge, clock/differential timing, and via-in-pad fabrication; reject context-free numerical rules and diagram rankings. Distribute original summaries and source links only.
- Clarify actual SIGNAL/PLANE layer semantics, documented regular power zones and four-SIGNAL-layer boards under PCB-P09/P10. Select the reference from the actual differential routing layer and calculate 90 ohm geometry from the fabrication stackup.
- Extend PCB-P11 mechanical baselines, PCB-V02 Arial/silkscreen clearances and PCB-V04 separate same-net solder lands; refresh templates, bilingual documentation and portable packages.
- Upgrade: existing stage records need newly required applicable items and current-revision evidence. Preserve rule identifiers and JSON structure. No user PCB changes, retroactive board approvals, or claims of DRC, measured performance or fabrication release.

## 2.4.1 — 2026-11-04

- 显式允许按任务自动选用，读取实际版本/适用参考后提示使用状态；交付区分实际检查、未验证项及证据。
- 补充跨工作区指令、普通ChatGPT使用及安装升级说明；包校验不等于EDA或实测通过。

### English

- Explicitly allow implicit selection and announce the actual skill version and applicable references after reading them; report completed checks, unverified items and evidence at delivery.
- Document workspace/user instruction entrypoints and ordinary ChatGPT usage; avoid unrelated tasks, disclose missing files, and distinguish usage announcements from engineering results.
- Refresh bilingual release docs, packages and local instructions without changing v2.4.0 electrical rules. Configuration checks do not prove future invocation or board correctness.

## 2.4.0 — 2026-11-04

- 新增HW-01～07工程闭环：量化需求/验收、共享接口、计算与边界条件、按风险研究/仿真、装配/测试接入、样机测试及经验反馈。
- 新增精简设计依据模板，复用已有记录并关联需求、器件/网络、计算、模型与实测证据；新板/电气/接口变更读取，纯排版和局部修复只核验受影响项。
- 区分设计检查、制造输出、样机和合规结论；仿真记录模型边界，未测项保持未验证。延续PCB-V07及全部既有规则，更新双语首页、安装包和聊天合并规则；未修改EDA或追溯认证旧板。

### English

- Added HW-01–07 for measurable requirements, shared interfaces, bounded calculations, risk-based research/simulation, assembly/test access, prototype tests, and feedback.
- Added a compact evidence template linking requirements, design objects, calculations, models, and measurements; reuse existing records and limit cosmetic/local changes to affected checks.
- Report design, manufacturing, prototype, and compliance states separately; state model limits and keep unmeasured items unverified. Preserve PCB-V07 and existing rules, refresh bilingual release docs and portable packages; no EDA edits or retroactive board certification.

## 2.3.2 — 2026-11-04

- 新增PCB-L22：MLCC封装与有效电容选型；不将0201/0402/0603/0805绑定固定容值上限，也不把经验范围当合格保证。
- 按准确MPN、实际偏压/温度/容差/老化核对有效容量、额定电压及ESR/稳定性；新增Murata与ADI原厂依据，区分典型曲线和保证下限。
- 将选型证据接入电源/去耦、阶段核验及项目/BOM审查入口；同步双语首页与发布说明。未改动既有EDA工程，历史板级验证不追溯升级。

### English

- Added PCB-L22 for MLCC package and effective-capacitance selection; package sizes do not impose universal capacitance ceilings or define a safe selection window.
- Check exact-part DC bias, temperature, tolerance and aging against required capacitance, voltage ratings and ESR/stability; cite Murata and ADI and distinguish typical curves from guaranteed limits.
- Route this evidence into power/decoupling, stage reviews and project/BOM checks; refresh bilingual release summaries. No EDA designs were edited or retroactively revalidated.

## 2.3.1 — 2026-11-03

- 重做中英文 README：增加原创封面、最新版本摘要、规则导航、安装升级入口和工具适用边界，修正首页版本滞后。
- 新增贡献指南、问题/规则建议与 PR 模板、安装及发布文档，延续现有来源归属与 CC BY-SA 4.0 许可。
- 从版本元数据和 CHANGELOG 自动生成双语首页摘要与 Release 说明；CI 检查版本、链接、包指纹和辅助脚本，并在匹配标签时构建发布附件及 SHA-256 校验文件。
- 设计规则与 PCB-V07 行为沿用 2.3.0，本版聚焦文档和发布维护，不代表任何板卡新增验证通过。

### English

- Redesigned both READMEs with an original cover, current release highlights, rule navigation, and clear installation and tool boundaries.
- Added contribution guidance, issue/PR templates, installation and release documentation, preserving attribution and CC BY-SA 4.0.
- Generate README summaries and release notes from version metadata and this changelog; CI checks consistency, links, package hashes, and helper tests, then builds checksummed assets for matching tags.
- Design rules and PCB-V07 behavior remain those of 2.3.0; this documentation and maintenance release does not revalidate any board.

## 2.3.0 — 2026-11-03

- 新增PCB-V07：大规模布线前和交付前分阶段检查，全器件装配及逐电源脚去耦/完整回地均须留证，不用DRC或文档编号检查替代。
- 新增可携带记录模板及检查器，缺规则项、缺器件/电源脚覆盖、失败、无依据的不适用或文件哈希过期均阻止阶段通过；保留真实EDA/人工审查边界。
- PCB布局布线入口必读电源与接地；修正工作区模板残留的强制大小电容串行表述，保持并联拓扑和准确器件优先。

## 2.2.3 — 2026-11-03

- PCB-V04补充同网焊盘和真实焊接/返修空间检查，不以DRC零错误代替装配审查。
- PCB-L01/L17/L20补充逐电源脚的实际供电和回地路径证据，关键去耦回路在普通布线前预留空间。
- 保留器件专用紧凑布局和并联去耦边界，不推广固定装配间距或宣称几何检查证明实测性能。

## 2.2.2 — 2026-11-03

- PCB-L21：记录外接排针靠板边的用户偏好，按项目确定边距、孔/螺钉避让、插拔空间及逐脚丝印。
- 成对模块插座保留真实配合尺寸，冲突先确认；移位后的核验不继承旧位置 DRC。
- 同步核验项和项目模板；本次规则发布不代表任何板卡制造放行。

## 2.2.1 — 2026-11-02

- PCB-V06 明确首次完整零错误 DRC 后设计适用泪滴、重铺铜、再次完整 DRC，局部修复后重复至零错误再导出。
- 记录关键网络/细间距例外、关联网络/铜形与制造边界，接口丝印同步实际脚序。
- 更新技能入口和核验/项目模板；版本发布只证明规则包完整，不代替板级验证。

## 2.2.0 — 2026-11-02

- 从9工程84张图页的概览和21张代表页局部观察完善既有SCH编号，增加多板导航、重复通道、合法多单元、字段显隐与装配矩阵。
- 澄清去耦归属、图上距离、单标签与分框的边界，保留用户偏好，记录样本标题错配、拥挤和待验证建议。
- 新增按需样本取舍参考及检查项；只发布原创方法总结，不包含原生工程、截图、网表或私人空间标识。
- 只读采集不等于电气认证；没有编辑样本或运行ERC/DRC。

## 2.1.0 — 2026-11-02

- 安装并阅读 easyeda-enhanced-schematic-skill 固定提交，原版独立保留为 easyeda-schematic-net-fanout；完整核对3个上游文件字节。
- 新增嘉立创自动化工作方式及 SCH-28～34，整合批量查料、真实引脚、功能分框、按需标记、局部对象清理与批次读回。
- 按 SCH-25 修正上游逐脚重复标签策略，补充端口方向、EP/NC及共享分支保护；不照搬示例电路/固定间距。
- 对上游Y轴/旋转说明不一致及原始导线属性与当前API方法的差异记录版本边界，未宣称实时API验证通过。
- 更新安装提示、来源、打包/聊天合并版与检查模板。


## 2.0.0 — 2026-11-02

- Skill 改名为 embedded-hardware-design，原 pcb-design-rules 的 PCB 内容保留，增加原理图绘制/排版/审查的按需入口。
- 完整纳入 SCH-01～27 和可复用原理图检查模板，保留用户手动排版提炼；不公开原图或工程。
- 区分原理图直角导线与 PCB 转角偏好，保留纯排版网表不变及原理图/PCB 授权范围。
- 纠正 1.2.0 的去耦过度约束：正常平面直供不代表电容失效，各电源域不统一套用 100 nF，大小排序不能优先于低电感回路、稳压稳定性及原厂布局。
- 修复工作区重复 PCB-L20 与误用 PCB-R18，增加原理图来源归属；包、聊天合并版和本机安装迁移至新名。


## 1.2.0 — 2026-11-02

- PCB-L17：逐个核对 MCU 的 VDD/VDDA/VBAT 等电源域，默认同层并在对应引脚附近布置 100 nF；大到小指物理铜路顺序，电容仍为并联旁路。
- PCB-L20：新增 LDO/BUCK/BOOST/负载开关的输入、输出滤波与不可绕过检查；项目电容值不推广为通用默认。
- V9 的 ME6210A33M3G 与 TPS2553DBVR 电容配置记录为需按准确数据手册、有效容量和启动负载复核的项目例子。

## 1.1.1 — 2026-11-01

- PCB-P09：核对物理用途、原生EDA层类型和平面对象；明确内电层时验证原生类型，转换后重验连接/DRC/Gerber。
- PCB-R07：允许受约束的相切圆弧，核验网络端点、真实弧长、连续线宽、全弧间距、差分耦合和回流；独立检查须覆盖ARC/CARC。
- 用户指正后同步维护源、项目、Skill安装副本及经授权的GitHub，记录版本与提交；公开内容保持项目数据边界。

## 1.1.0 — 2026-11-01

- PCB-G08：非GND飞线优先；GND按铺铜→缝合孔→重铺/DRC→残余短线处理，继续保证去耦与换层回流。
- PCB-L19：从用户手动样本提炼差分器件沿逃线方向成对放置、短直主干和局部过渡，以及晶振按完整敏感回路勾勒禁铜/外围接地的做法。
- 明确COPPER禁布不自动禁止TRACK/VIA，已完成通道需与保护基线比较。
- 样本的剩余DRC错误与布局方法分开记录，未复制用户工程或将其具体参数作为通用阈值。

## 1.0.0 — 2026-11-01

- 从已有规范及核读记录提炼可携带规则，按布局、电源/GND、差分/晶振和核验分开按需读取。
- 保留用户默认：GND过孔优先、非过孔位置无90°转角、20→10→20mil节点间分段同宽、MCU同层去耦与大小电容连接点顺序。
- V9专用阻抗、线宽/间距、偏斜、位号与机械方向保留项目范围，不设为新板默认。
- 补充实际铜皮回流、端到端网络/串阻检查、用户手动接管后的状态重读及证据边界。
- 提供跨电脑使用、ChatGPT规则导出、可选插件安装及校验打包方法。

本版本为规则整理与分发；没有恢复或编辑任何暂停的PCB，也未为任何现有PCB重新执行DRC。
