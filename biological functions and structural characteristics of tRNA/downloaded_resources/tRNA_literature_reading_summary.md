# tRNA 文献阅读总结：功能、结构与图像要点

来源文件夹：`D:\Project\tRNA research\biological functions and structural characteristics of tRNA\downloaded_resources\pdfs`

本报告按 PDF 文件逐篇阅读整理，重点覆盖主文图；Extended Data 图和表格作为补充图证据列在每篇末尾。图像解读主要依据论文正文摘要、结果脉络和图注信息；若要做投稿级综述，建议后续再把重点论文逐段精读。

## 总体结论

这些文献共同显示，tRNA 远不只是翻译适配器，而是一个高度可塑的结构平台：

1. tRNA 的局部结构和修饰决定蛋白识别方式。METTL6、Trbp111/Arc1p、Trl1、Cas12a3 都不是简单识别线性序列，而是读取 tRNA 的 3' 端、反密码子臂、可变臂、受体茎、T 臂或修饰状态。
2. tRNA 可作为调控和免疫靶点。PARIS 和 Cas12a3 都通过切割 tRNA 抑制翻译或触发抗噬菌体防御；氧化脱硫修饰则把氧化压力转化为翻译效率变化。
3. tRNA 可作为装配因子。痘病毒 vRNAP 论文把 tRNA 定义为多蛋白转录-加工复合物的 assembly chaperone，这是非经典功能的强证据。
4. tRNA 工程正在进入治疗场景。两篇 suppressor tRNA/AAV 论文分别证明了视网膜疾病模型和更泛疾病场景中，工程化抑制子 tRNA 可以恢复提前终止密码子造成的蛋白缺失。
5. 技术路线主要集中在 cryo-EM/X-ray 结构、生化结合/活性实验、tRNA 修饰质谱、DMS-MaPseq 结构探针、AAV 体内递送和功能表型验证。

## 1. METTL6-SerRS 识别 tRNASer 并催化 m3C32 修饰

文件：`38918637_Structural_basis_of_tRNA_recognition_by_the_m3C_RNA_methyltransferase_METTL6_in_complex_with_Se.pdf`

核心要点：该文解析了人 METTL6、SerRS 和 tRNASer 的复合物结构。METTL6 负责在 tRNA 反密码子环 C32 上写入 m3C 修饰，但其底物选择依赖 SerRS。SerRS 不只是氨酰化酶，还作为 METTL6 的 tRNASer 选择因子；METTL6 的 m3C 特异 RNA-binding domain 夹持并重塑反密码子臂，使 C32 进入催化位点。作者进一步提出 METTL2/METTL6/METTL8 可能共享类似的 m3C tRNA 识别模式。

主文图：

- Fig. 1：展示 SerRS-tRNA-METTL6 复合物的整体 cryo-EM 结构和结构域安排。图的核心信息是 METTL6、SerRS 二聚体和 tRNASer 形成稳定复合物，SerRS 帮助 METTL6 定位正确的 tRNA 底物。
- Fig. 2：聚焦 METTL6 的 m3C-RBD。该结构域接触 tRNA 反密码子臂，是 METTL6 区分和固定 tRNA 的关键模块。
- Fig. 3：展示 tRNA 反密码子臂被重塑。与游离 tRNA 相比，复合物中的反密码子臂构象发生偏转，使 C32 和 A37 附近修饰能进入被识别/催化的空间位置。
- Fig. 4：展示 METTL6 活性中心。SAH/SAM 结合口袋与 C32 的空间关系说明 methyl transfer 如何发生；突变验证支持关键残基对催化的重要性。
- Fig. 5：展示 METTL6-SerRS-tRNA 可变臂界面。该图说明 SerRS 和 METTL6 共同读取 tRNASer 的可变臂特征，这是底物选择的结构基础。

补充图/表：

- Extended Data Fig. 1：样品纯化、复合物装配和 cryo-EM 初步证据。
- Extended Data Fig. 2：cryo-EM 数据处理流程和重构质量。
- Extended Data Fig. 3：比较不同 METTL6-SerRS-tRNA 界面，说明复合物构象和结合模式。
- Extended Data Fig. 4：m3C RNA methyltransferase 的序列保守性，提示关键识别/催化残基。
- Extended Data Fig. 5：与 METTL11 等甲基转移酶比较，突出 METTL6 的 tRNA 结合特异性。
- Extended Data Fig. 6：分析共纯化 tRNASer 的修饰状态。
- Extended Data Fig. 7：建模 A37 可能修饰如何被识别。
- Extended Data Fig. 8：二维活性中心示意，便于理解 C32、SAH 和关键侧链关系。
- Extended Data Fig. 9：METTL6 突变体功能表征，验证结构推断。
- Extended Data Fig. 10：METTL6-SerRS 接触细节。
- Table 1/2：X-ray 与 cryo-EM 数据收集和模型质量统计。

## 2. OB-fold 蛋白通过 tRNA 3' 端识别成熟 tRNA

文件：`39075051_Structural_basis_of_tRNA_recognition_by_the_widespread_OB_fold..pdf`

核心要点：传统上 Trbp/Arc1p 这类 OB-fold 蛋白被认为识别 tRNA elbow 或反密码子区域。该文通过 Trbp111-tRNAIle 共晶结构显示，Trbp111 主要通过捕获成熟 tRNA 的 3' CA 末端来识别 tRNA。Arc1p 在此基础上还通过邻近碱性区域和 tRNA 主体增加结合强度。这说明一个古老 OB fold 可以用非常简洁的方式读取成熟 tRNA 的通用标志。

主文图：

- Fig. 1：展示 Trbp111 和相关 OB-fold 蛋白结构域，以及 tRNA 结合实验。图的重点是 Trbp111 自身即可结合多种 tRNA。
- Fig. 2：Trbp111 与 E. coli tRNAIle 的共晶结构。核心结论是 Trbp111 二聚体抓住 tRNA 3' 端，而不是主要夹住 elbow 或反密码子。
- Fig. 3：突变分析 tRNA 接触界面。关键接触残基突变削弱结合，证明 3' 端识别不是结构巧合。
- Fig. 4：Arc1p 截短和点突变对 tRNA 结合的影响。说明 Arc1p 的 OB fold 与额外区域协同提升 tRNA 结合。
- Fig. 5：改变全长 tRNA 的 3' 端或相关结构后测结合能力。结果支持 Arc1p/Trbp111 对成熟 tRNA 3' 端结构和序列的敏感识别。
- Fig. 6：用 minihelix、microhelix 和 ssRNA 测 Arc1p 结合。图说明 Arc1p 能读出 3' 末端单链/局部结构，但完整 tRNA 主体仍影响亲和力。
- Fig. 7：比较三类核酸结合 OB-fold。该图把 Trbp/EMAPII-like OB fold 的 tRNA 3' 端识别模式放入更广泛的 OB-fold 识别框架中。

## 3. 病毒编码 tRNA 可逃逸 PARIS 抗病毒系统

文件：`39111359_A_virally_encoded_tRNA_neutralizes_the_PARIS_antiviral_defence_system..pdf`

核心要点：PARIS 是由 AriA ATPase 和 AriB TOPRIM nuclease 组成的抗噬菌体系统。AriA/AriB 形成大型复合物，感知外源抗限制蛋白 Ocr 后释放 AriB，AriB 通过切割宿主 tRNALys 抑制翻译并触发防御。噬菌体 T5 编码一种不易被切割的 tRNALys 变体，从而中和 PARIS 防御并恢复感染。

主文图：

- Fig. 1：展示 PARIS 两组分系统和整体复合物。AriA 六聚体形成类似螺旋桨的支架，AriB 装配在其上，说明 PARIS 是大型蛋白机器而非简单二元酶。
- Fig. 2：解析 AriA ATPase 与 AriB 的关键接触。界面突变会破坏防御，说明 AriA-AriB 装配是 PARIS 功能前提。
- Fig. 3：展示 Ocr 与 AriA ATPase 依赖性相互作用，并导致 AriB 从复合物释放。图说明病毒蛋白 Ocr 是触发 PARIS 的信号。
- Fig. 4：展示 PARIS 激活后的细胞死亡和翻译抑制。读数包括毒性、染色和翻译水平，说明 PARIS 的效应是阻断细胞翻译。
- Fig. 5：证明 PARIS 切割 E. coli tRNALys，而 T5 编码不易切割的 tRNALys。该图是全文和 tRNA 直接相关的关键证据。
- Fig. 6：PARIS 及相关 ABC ATPase 防御系统的系统发育。说明这种 ATPase-TOPRIM 免疫架构广泛存在并发生分化。

补充图：

- Extended Data Fig. 1：AriA/AriB 的 AlphaFold2 预测结构。
- Extended Data Fig. 2：PARIS 同源物结构比较。
- Extended Data Fig. 3：PARIS 结构解析流程。
- Extended Data Fig. 4：AriB 毒性依赖 AriA 关联。
- Extended Data Fig. 5：活化 AriB 的纯化和二聚化证据。
- Extended Data Fig. 6：AriA 纯化和结构相关验证。
- Extended Data Fig. 7：AriA ATPase 活性测定。
- Extended Data Fig. 8：PARIS 激活并不造成总体 RNA/DNA 随机降解。
- Extended Data Fig. 9：PARIS 激活导致 DNA 压缩等细胞状态改变。
- Extended Data Fig. 10：定位 T5 逃逸 PARIS 所需基因区域。
- Extended Data Fig. 11：tRNALys 切割产物与相关系统发育分析。

## 4. PYROXD1 保护人 tRNA ligase complex 免受氧化失活

文件：`40069351_Mechanistic_basis_for_PYROXD1-mediated_protection_of_the_human_tRNA_ligase_complex_against_oxid.pdf`

核心要点：人 tRNA ligase complex 的催化亚基 RTCB 含有易氧化的活性中心半胱氨酸。PYROXD1 是含 FAD 的氧化还原酶，能以 NAD(P)H 依赖方式保护 RTCB。该文解析 RTCB-PYROXD1 结构，发现 PYROXD1 的 C 端尾部直接接触并遮挡 RTCB 催化中心；NADH/FAD 氧化还原状态调控 PYROXD1 构象、RTCB 结合和释放。RTCB 经 Archease guanylylation 后自身也更耐氧化。

主文图：

- Fig. 1：RTCB-PYROXD1 复合物 cryo-EM 结构。显示 PYROXD1 贴近 RTCB 催化中心，并携带 FAD/NAD 相关配体。
- Fig. 2：PYROXD1 的 C-terminal domain/尾部遮挡 RTCB 活性中心。图的核心是“保护”来自物理占位和直接接触。
- Fig. 3：PYROXD1 的变构调控。FAD/NADH 状态改变 loop 区域构象，从而影响 CTC 形成和 RTCB 结合。
- Fig. 4：PYROXD1-RTCB 的定时解离允许 Archease 激活 RTCB。说明 PYROXD1 不是永久抑制 RTCB，而是在保护和催化激活之间切换。

补充图/表：

- Extended Data Fig. 1：RTCB-PYROXD1 复合物形成和 NADH 周转光谱分析。
- Extended Data Fig. 2：cryo-EM 数据处理。
- Extended Data Fig. 3：FADH-/NAD+ 配体相互作用图。
- Extended Data Fig. 4：PYROXD1 loop 对活性的变构控制。
- Extended Data Fig. 5：PYROXD1 的 NADH turnover 动力学。
- Extended Data Fig. 6：RTCB 催化中心结构比较。
- Table 1：cryo-EM 数据和模型验证统计。

## 5. DM-DMS-MaPseq 揭示人细胞 tRNA 结构组和互作组

文件：`40447571_In_vivo_structure_profiling_reveals_human_cytosolic_and_mitochondrial_tRNA_structurome_and_inte.pdf`

核心要点：作者开发 DM-DMS-MaPseq，把 DMS 体内化学探针、demethylase 处理和突变测序结合起来，用于绘制人细胞核编码和线粒体编码 tRNA 的体内结构与相互作用图谱。结果显示 tRNA 体内结构整体稳定，但体内 DMS 图谱与体外差异显著，主要反映 tRNA 与蛋白、核糖体等细胞机器的接触。砷酸盐氧化应激会改变细胞质和线粒体 tRNA 的结构/互作，符合全局翻译抑制和重编程。

主文图：

- Fig. 1：DM-DMS-seq/DM-DMS-MaPseq 方法验证。通过 rRNA 和 tRNA 已知构象证明该方法能在体内捕捉 RNA 可及性。
- Fig. 2：比较染色体编码 tRNA 的体外和体内 DMS 信号。显示不同 isodecoder 在细胞内有差异化保护/暴露模式。
- Fig. 3：把体内 DMS 保护信号与 tRNA-蛋白、tRNA-核糖体互作联系起来。说明许多体内结构差异来自真实互作而非折叠错误。
- Fig. 4：砷酸盐应激下细胞质 tRNA 结构和互作变化。图中 ΔDMS 信号指出哪些位点在应激时更暴露或更受保护。
- Fig. 5：线粒体编码 tRNA 的体外/体内 DMS 图谱。说明 mt-tRNA 的非经典结构也可被该方法系统捕捉。
- Fig. 6：砷酸盐应激下线粒体 tRNA 结构/互作变化。提示线粒体翻译也参与氧化应激响应。

## 6. 真菌 tRNA ligase Trl1 与 RNA 的结构揭示保守底物结合原则

文件：`40563009_Structure_of_fungal_tRNA_ligase_Trl1_with_RNA_reveals_conserved_substrate-binding_principles..pdf`

核心要点：Trl1 是真菌/植物 tRNA 剪接后连接 exon halves 的三功能酶。该文解析了 Chaetomium thermophilum Trl1-LIG 与 tRNA 来源 RNA 底物的晶体结构，捕捉到活化 RNA 中间体，定义了保守的 RNA 结合界面。结果说明 Trl1-LIG 的 NTD/CTD 在腺苷酸化、底物结合、磷酸转移和 2'-phosphate 特异性识别中分工明确。

主文图：

- Fig. 1：概述 Trl1 连接反应和 RNA 底物结构。图把 cP opening、5' phosphorylation、adenylylation 和最终 ligation 串起来。
- Fig. 2：CtTrl1-LIG 与活化 RNA 底物的结构。显示 AMP、RNA 末端和蛋白结构域如何共同定位反应中心。
- Fig. 3：分析 Trl1-LIG 的 RNA 结合界面。表面图和突变实验说明哪些氨基酸负责抓住 RNA 双链和末端。
- Fig. 4：建模 CtTrl1-LIG 与 tRNA-derived substrate 的复合物。把晶体中的短 RNA 接触扩展到真实 tRNA 剪接 exon halves 场景。
- Fig. 5：比较 CtTrl1-LIG-RNA 与 T4 Rnl2-AppDNA。说明不同连接酶共享类似核酸末端定位逻辑。
- Fig. 6：分析 Trl1-LIG C 端结构域在 RNA 连接中的作用。CTD 影响底物结合和连接效率。
- Fig. 7：保守精氨酸残基介导 2'-P 特异性。图解释 Trl1 如何识别真菌 tRNA 剪接特有的 2'-phosphate 产物。

补充图/表：

- Extended Data Fig. 1：TSEN 切割后的 pre-tRNA、环化/连接相关示意。
- Extended Data Fig. 2：CtTrl1-LIG 与 RNA 接触残基二维图。
- Extended Data Fig. 3：RNA duplex 电子密度和体外活性验证。
- Extended Data Fig. 4：Trl1-LIG 结构域和 RNA 结合残基保守性。
- Extended Data Fig. 5：RNA 接触残基对酵母细胞生长/功能影响。
- Extended Data Fig. 6：RNA 进入 CtTrl1-LIG 活性中心的建模。
- Extended Data Fig. 7：与 DNA ligase/Rnl2 类结构的叠合比较。
- Extended Data Fig. 8：CTD 在连接反应中的进一步功能分析。
- Table 1：晶体学数据和模型精修统计。

## 7. tRNA 作为痘病毒 RNA polymerase 复合物装配伴侣

文件：`40908366_tRNA_as_an_assembly_chaperone_for_a_macromolecular_transcription-processing_complex..pdf`

核心要点：该文提出 tRNA 的非经典功能：在痘病毒感染期间，缺少 anticodon mcm5s2U34 修饰的 tRNAGln/Arg 被选择性招募，作为 assembly chaperone 促进多亚基病毒 RNA polymerase 复合物 vRNAP 装配。tRNA 通过诱导适配方式改变反密码子区域构象，帮助招募转录和 mRNA 加工因子，并控制向 preinitiation complex 的转换。Mpox 病毒也有类似机制。

主文图：

- Fig. 1：vRNAP 中间体重构策略。展示如何分离 minimal/core vRNAP、加入 D1/D12、E11、NPH-I 等因子，并检测 tRNA 参与装配。
- Fig. 2：早期 PIC tRNA-chaperoned assembly cycle 的关键 cryo-EM 结构。显示 tRNA 在不同中间体中如何定位和桥接因子。
- Fig. 3：提出 tRNA-chaperoned 装配循环模型。图把结构中间体串成从 core/minimal vRNAP 到完整 PIC 的路径。
- Fig. 4：完整 vRNAP 高分辨率重构。展示所有转录/加工因子和 tRNA 的空间排布。
- Fig. 5：完整 vRNAP 中 tRNAGln(UUG) 的构象和相互作用。重点是反密码子臂的非典型构象和与蛋白因子的多点接触。
- Fig. 6：鉴定 tRNAGln/Arg 修饰及其对复合物形成的影响。说明特定修饰缺失状态是被选择性招募的条件。
- Fig. 7：在 cryo-EM 密度中识别 tRNAGln 修饰。把化学修饰状态和结构密度联系起来。
- Fig. 8：完整 vRNAP 以 en bloc 方式包装入 vaccinia virions。说明这种 tRNA 参与的复合物装配具有病毒生命周期意义。

补充图/表：

- Extended Data Fig. 1：单个转录因子与 vRNAP/tRNA 的相互作用。
- Extended Data Fig. 2：minimal vRNAP cryo-EM 重构。
- Extended Data Fig. 3：Rap94 结构域排列。
- Extended Data Fig. 4：vRNAP assembly intermediate 的 cryo-EM 重构。
- Extended Data Fig. 5：Intermediate 5 重构。
- Extended Data Fig. 6：完整 vRNAP 重构流程。
- Extended Data Fig. 7：tRNAGln isoforms 与 cryo-EM 密度。
- Extended Data Fig. 8：修饰和非经典碱基配对对结构/功能的影响。
- Extended Data Fig. 9：病毒颗粒中 vRNAP 和 tRNAGln(UUG) 含量。
- Table 1：cryo-EM 数据和模型精修统计。

## 8. AAV 递送工程化 suppressor tRNAArg 挽救遗传性视网膜病小鼠视觉功能

文件：`41407712_AAV-delivered_engineered_suppressor_tRNA_rescues_visual_function_in_mice_with_an_inherited_reti.pdf`

核心要点：该研究针对 RPE65-R44X nonsense mutation，工程化 sup-tRNAArg 识别 UGA 提前终止密码子，并通过 scAAV8 递送至 rd12 小鼠视网膜。治疗恢复 RPE65 蛋白表达，改善视网膜电生理和视觉行为，疗效可维持至少 36 周；毒性和全局正常终止密码子 readthrough 较低。

主文图：

- Fig. 1：在 HEK293 细胞中筛选/验证工程化 sup-tRNAArg 对 RPE65-R44X 的抑制效果。显示改变 tRNA body sequence 可提升 readthrough。
- Fig. 2：scAAV8.A4T1 治疗恢复 rd12 小鼠 RPE65 蛋白。图包括载体设计、给药流程、免疫染色/蛋白表达等。
- Fig. 3：scAAV8.A4T1 维持视网膜功能并保护锥细胞。ERG 波形和振幅说明光反应恢复，组织学显示感光细胞保护。
- Fig. 4：视觉 cliff 行为实验显示视觉引导行为改善。治疗组更倾向选择安全区域，证明功能改善延伸到行为层面。
- Fig. 5：安全性评估。H&E、转录组和核糖体 profiling 等显示没有明显组织毒性或广泛异常 readthrough。

## 9. RNA 触发的 Cas12a3 通过切割 tRNA 3' CCA tail 执行细菌免疫

文件：`41501459_RNA-triggered_Cas12a3_cleaves_tRNA_tails_to_execute_bacterial_immunity..pdf`

核心要点：该文发现 Cas12a3 是一类 RNA 触发的 type V CRISPR-Cas 效应核酸酶。crRNA 识别目标 RNA 后，Cas12a3 优先切割多种 tRNA 保守 3' CCA tail，而不是主要切目标 RNA 本身；这会导致生长停滞和抗噬菌体防御。结构显示 Cas12a3 有 tRNA-loading domain，能把 tRNA tail 装入 RuvC 活性位点。作者还利用其底物特异性扩展 CRISPR RNA 检测的多重化能力。

主文图：

- Fig. 1：两个与 Cas12a2 相关的新 clade 具有 RNA 激活的 RNA collateral cleavage，但不切 DNA。该图定义 Cas12a3/Cas12a4 与已知 Cas12a2 的差异。
- Fig. 2：Cas12a3 优先切割 tRNA 保守尾部。时间过程、direct RNA sequencing 和底物分析共同证明 3' CCA tail 是主要靶点。
- Fig. 3：Ba1Cas12a3 捕获 tRNA 的结构基础。crRNA、target RNA 和 tRNA 同时结合的复合物显示 tRNA 如何被加载。
- Fig. 4：Ba1Cas12a3 结合和切割 tRNA 的机制。比较二元、三元、四元和切割前后结构，说明 target RNA 激活后 RuvC 如何处理 tRNA tail。
- Fig. 5：特异底物识别扩展多重 RNA 检测。利用 tRNA-like reporter 设计，Cas12a3 可与现有 CRISPR 检测体系互补。

补充图：

- Extended Data Fig. 1：Cas12a2/3/4 预测结构域组织。
- Extended Data Fig. 2：Cas12a2/3/4 的 RNA targeting 和 growth arrest 验证。
- Extended Data Fig. 3：比较 Cas12a3 与 Cas12a2/Cas13 类 RNA targeting。
- Extended Data Fig. 4：在无 phage 条件下评估 plasmid interference。
- Extended Data Fig. 5：四元复合物结构比较。
- Extended Data Fig. 6：Ba1Cas12a3 与 tRNA 的细节相互作用。
- Extended Data Fig. 7：全长和截短 tRNA/底物的结合亲和力。
- Extended Data Fig. 8：其他 RNA 底物 trans cleavage 测试。
- Extended Data Fig. 9：tRNA trimming 介导免疫防御的模型。

## 10. 工程化 UGA suppressor tRNA 基因用于 disease-agnostic AAV 递送

文件：`41555020_An_engineered_UGA_suppressor_tRNA_gene_for_disease-agnostic_AAV_delivery..pdf`

核心要点：UGA suppressor tRNA 可用于多种由 UGA 提前终止密码子导致的疾病，但强 readthrough 的 sup-tRNA 基因会影响 rAAV 生产。该文通过 NFS regulatory context、CuO-CymR 抑制系统和载体生产优化，构建 AAV-NoSTOP(UGA)。单次给药在两种 lysosomal storage disorder 小鼠模型中恢复约 10% 正常酶活，且不同组织的 sup-tRNA 表达和 charging efficiency 与疗效差异相关。

主文图：

- Fig. 1：NFS context 增强 UGA-sup-tRNAArg 效力。图比较不同启动/调控环境下的 readthrough，说明 NFS 比常规 U6 构建更强。
- Fig. 2：CuO-CymR 通过压低 sup-tRNA 功能改善 rAAV 包装。核心逻辑是生产阶段抑制 sup-tRNA，避免影响包装细胞。
- Fig. 3：优化 rAAV 产量、纯度和 vector genome homogeneity。展示不同 CymR 细胞系/工艺条件对 AAV 质量的影响。
- Fig. 4：AAV-NoSTOP(UGA) 在 IduaKI/KI 小鼠中恢复 IDUA 活性。组织酶活、GAG/病理等读数支持体内疗效。
- Fig. 5：不同组织中 sup-tRNA 表达水平和 aminoacylation/charging efficiency。说明疗效不仅由递送量决定，也由 tRNA 被正确氨酰化的效率决定。

补充图：

- Extended Data Fig. 1：HEK293 细胞中评估 UGA-sup-tRNAArg 候选体。
- Extended Data Fig. 2：low-cis triple transfection 对强 UGA-sup-tRNA 包装的限制。
- Extended Data Fig. 3：CuO-CymR 系统抑制 UGA-sup-tRNA 功能。
- Extended Data Fig. 4：CymR 克隆细胞系的建立和表征。
- Extended Data Fig. 5：CymR 细胞系提高 AAV9 载体产量。
- Extended Data Fig. 6：截短 vector genomes 的表征。
- Extended Data Fig. 7：Idua-W401X(TGA) 小鼠模型建立和验证。
- Extended Data Fig. 8：IduaKI/KI 小鼠 20 周持久疗效。
- Extended Data Fig. 9：AAV-NoSTOP(UGA) 安全性评估。
- Extended Data Fig. 10：AAV-NoSTOP(UGA) 在另一模型中恢复 TPP1 活性。

## 11. 氧化脱硫 tRNA 修饰调控翻译

文件：`41807381_Translational_regulation_by_oxidative_desulfuration_of_tRNA_modifications..pdf`

核心要点：tRNA wobble position 34 的 5-methyl-2-thiouridine 衍生物 xm5s2U 有助于高效解码以嘌呤结尾的二密码子组，但其 thiocarbonyl 基团易在氧化压力下脱硫形成 xm5h2U。该文在人细胞和小鼠组织中检测到这些脱硫产物，并证明 mcm5h2U 会降低 Lys/Glu/Gln 等 tRNA 的氨酰化和密码子识别效率，从而在氧化压力下调控蛋白翻译。cryo-EM 解释了 mcm5s2U34 与 mcm5h2U34 对 AAA/AAG 解码差异的结构基础。

主文图：

- Fig. 1：介绍 tRNA 反密码子中 2-thiouridine 衍生物及其氧化脱硫产物。图建立化学反应和生物学问题。
- Fig. 2：用 tracer tRNA spike-in 实验证明 xm5h2U 可在细胞环境中形成，而非纯粹样品处理伪影。
- Fig. 3：在人/小鼠细胞质和线粒体 tRNA 中检测 h2U 衍生物。XIC 质谱峰证明多类 tRNA 存在脱硫修饰。
- Fig. 4：脱硫 tRNA 修饰影响翻译效率。体外翻译报告系统显示特定 codon context 下翻译输出下降。
- Fig. 5：脱硫影响 aminoacylation。Lys、Gln、Glu 等 tRNA 氨酰化下降，而 Arg 影响较小或不同。
- Fig. 6：脱硫 tRNALys 影响 codon recognition。A-site tRNA binding 实验证明 AAA/AAG 识别受 mcm5h2U34 状态影响。
- Fig. 7：mcm5s2U34 和 mcm5h2U34 解码 AAR 的结构基础。cryo-EM 展示 wobble 位点化学变化如何改变 codon-anticodon geometry。
- Fig. 8：提出机制模型：氧化压力下 xm5s2U34 脱硫为 xm5h2U34，降低氨酰化/解码效率，从而动态重塑翻译。

## 主题归纳：这些图共同支持什么

- 结构识别：METTL6、Trbp111/Arc1p、Trl1、Cas12a3 的结构图共同证明 tRNA 被蛋白识别时，关键不是“整条 tRNA 一样被看见”，而是不同机器读取不同局部标志：C32/反密码子臂、3' CA、剪接末端 2'-P、3' CCA tail。
- 修饰调控：METTL6 的 m3C32、vRNAP 选择未带特定 U34 修饰的 tRNA、氧化脱硫 xm5s2U34 都说明 tRNA 修饰是动态功能开关。
- 免疫与抗病毒：PARIS 和 Cas12a3 都利用 tRNA 切割造成翻译停摆，但 PARIS 主要切 tRNALys，Cas12a3 则广泛切 3' CCA tail；二者都把 tRNA 作为“关闭宿主翻译”的高效节点。
- 治疗工程：两篇 AAV/sup-tRNA 论文说明 tRNA 工程的关键限制从“能不能 readthrough”转向“递送、包装、组织表达、charging efficiency 和安全性”。
- 方法学贡献：DM-DMS-MaPseq 提供了在活细胞中观察 tRNA 结构和互作的工具，可与结构生物学和治疗工程结合，用于判断工程 tRNA 是否形成正确结构、是否进入正确互作网络。

## 建议优先精读顺序

1. 如果目标是“tRNA 结构识别机制”：先读 METTL6、OB-fold、Trl1、Cas12a3。
2. 如果目标是“tRNA 非经典功能”：先读 PARIS、Cas12a3、vRNAP assembly chaperone。
3. 如果目标是“tRNA 修饰与翻译调控”：先读 METTL6、氧化脱硫、DM-DMS-MaPseq。
4. 如果目标是“tRNA 治疗应用”：先读两篇 AAV suppressor tRNA，再回看 DM-DMS-MaPseq 和修饰论文理解安全性/功能机制。

