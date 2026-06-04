# tRNA 分析工具文献精读矩阵

## 1. PMID 34417604 | tRNAscan-SE 2.0: improved detection and functional classification of transfer RNA genes
- Status: 主线新增
- Theme: 基因识别
- Article logic: 先用高速候选扫描缩小搜索空间，再用协方差模型和特征分类确认 tRNA 基因、伪基因与功能类别。
- Hypothesis: tRNA 的保守二级结构和身份元件足以支持跨基因组、高灵敏度的自动识别与分类。
- Methods: 候选区域扫描; Infernal/协方差模型评分; isotype 与 anticodon 分类; 伪基因和线粒体 tRNA 过滤
- Results: 提升复杂基因组中 tRNA 与 tRNA-like 元件的识别能力，是后续 tRNA-seq 注释与参考库构建的上游基础。
- Discussion/Direction: 局限在于表达状态、修饰和样本特异性无法由基因组序列直接推断；后续应与测序证据和 pangenome/reference graph 结合。

## 2. PMID 32796835 | Quantitative tRNA-sequencing uncovers metazoan tissue-specific tRNA regulation.
- Status: 主线保留
- Theme: 丰度定量
- Article logic: QuantM-tRNA-seq 通过成熟 tRNA 建库、环化/接头策略与全长读段来量化组织间 tRNA 表达差异。
- Hypothesis: 成熟 tRNA 的丰度与修饰差异可通过专门建库和比对策略从常规测序偏差中恢复。
- Methods: tRNA 末端处理与接头连接; RT 与 PCR 建库; tRNA 专用参考比对; 组织/等解码 tRNA 差异比较
- Results: 小鼠组织间 isodecoder 表达和修饰痕迹差异显著，但 anticodon pool 受到缓冲。
- Discussion/Direction: 短读长仍受多重比对、RT stop 与高相似序列限制；需要 spike-in、UMI 与概率分配模型提升绝对定量。

## 3. PMID 33581077 | High-resolution quantitative profiling of tRNA abundance and modification status in eukaryotes by mim-tRNAseq.
- Status: 主线保留
- Theme: 修饰诱导错配
- Article logic: mim-tRNAseq 将修饰导致的 misincorporation 从噪声转化为定量特征，同时估计丰度和修饰状态。
- Hypothesis: 不同修饰在逆转录时形成可重复的错配/停顿指纹，能用于高分辨率地追踪 tRNA 修饰状态。
- Methods: 全长 cDNA 建库; 错配/RT-stop 统计; isodecoder 层级归并; 跨物种可迁移分析工具包
- Results: 在酵母、果蝇和人细胞中量化 tRNA abundance 与 modification status，发现细胞系特异 isodecoder pool 和位点间修饰联动。
- Discussion/Direction: 优点是短读长平台可用；缺陷是对 RT 酶、参考注释和修饰指纹库依赖强，未知修饰难以唯一归因。

## 4. PMID 37024678 | Quantitative analysis of tRNA abundance and modifications by nanopore RNA sequencing.
- Status: 主线保留
- Theme: 纳米孔全长读段
- Article logic: Nano-tRNAseq 直接读取 native tRNA，并通过 raw signal 重处理恢复被默认流程丢弃的短 tRNA 读段。
- Hypothesis: 原始电流信号中保留了 tRNA 丰度和修饰状态；定制处理能减少长度和修饰造成的系统偏差。
- Methods: native tRNA 纳米孔测序; raw signal reprocessing; tRNA mapping; 错配/信号异常推断修饰
- Results: 重处理使可用 tRNA reads 增加约 12 倍，并捕获氧化应激下 tRNA 丰度与修饰联动。
- Discussion/Direction: 纳米孔优势是长读段和单分子层级；短 tRNA、接头效率、basecaller 偏差和修饰训练集仍是主要瓶颈。

## 5. PMID 39865096 | Genome-wide profiling of tRNA modifications by Induro-tRNAseq reveals coordinated changes.
- Status: 主线保留
- Theme: RT readthrough 修饰图谱
- Article logic: Induro-tRNAseq 选择更强 readthrough 的 group-II intron RT，将 RT stop 降低但保留 misincorporation 信号。
- Hypothesis: 改变 RT 酶的停顿行为可以把“读不穿”的修饰位点转化为可比较的错配信号。
- Methods: Induro RT 时间梯度; Induro 与对照 RT 平行比较; 错配频率矩阵; 组织/细胞间修饰差异分析
- Results: 在多个人细胞系和小鼠组织中绘制 tRNA 修饰，显示遗传密码读取相关修饰更稳定，其他位点更动态。
- Discussion/Direction: 强项是全基因组修饰 profiling；短板是修饰类别归因仍需标准品/酶缺失验证，适合发展联合修饰 caller。

## 6. PMID 40835813 | Nanopore sequencing of intact aminoacylated tRNAs.
- Status: 主线保留
- Theme: 氨酰化状态
- Article logic: aa-tRNA-seq 用化学连接保留 aminoacylated tRNA，再用纳米孔信号和机器学习识别单分子氨基酸身份。
- Hypothesis: 氨基酸夹在 tRNA 与接头之间会产生可学习的电流扰动，可在单分子层面解析 charging fidelity。
- Methods: aminoacyl-tRNA 化学保护/连接; nanopore sequencing; 特征提取; 机器学习 amino acid classifier
- Results: 能识别 tRNA 所携带氨基酸，并用于分析修饰酶缺失导致的 hypomodification 和 tRNA 稳定性变化。
- Discussion/Direction: 方法打开 charging 分析入口；局限是模型训练、氨基酸类别泛化、化学处理效率和复杂样本校准。

## 7. PMID 40447571 | In vivo structure profiling reveals human cytosolic and mitochondrial tRNA structurome and interactome in response to stress.
- Status: 主线保留
- Theme: 结构与互作
- Article logic: DM-DMS-MaPseq 将体内 DMS 化学探针、demethylase 处理和 mutational profiling 结合，解析 tRNA structurome/interactome。
- Hypothesis: 体内 DMS 反应性不仅反映结构可及性，也反映蛋白/核糖体互作遮蔽，可用于追踪应激调控。
- Methods: in vivo DMS probing; DM 去甲基化处理; MaP-seq 突变读出; 胞质/线粒体 tRNA 结构比较
- Results: 体内 tRNA 结构总体稳定，但与体外谱差异显著；砷酸盐应激改变胞质和线粒体 tRNA 互作。
- Discussion/Direction: 结构读出与互作读出耦合是优势也是混杂来源；未来需联合 Ribo-seq/IP 或扰动实验解卷积。

## 8. PMID 42062277 | Deciphering tRNA repertoires and translation coordination during mouse early embryogenesis by ORACLE-tRNAseq.
- Status: 主线保留
- Theme: 低输入 tRNA-seq
- Article logic: ORACLE-tRNAseq 面向极少量卵母细胞/早期胚胎，优化低输入捕获并与多组学和 Ribo-seq 联合分析。
- Hypothesis: 早期胚胎 tRNA pool 的动态变化可与 ZGA、染色质重塑和翻译效率相互协调。
- Methods: 低输入建库; tRNA repertoire 定量; pseudogene activation 分析; Ribo-seq/组蛋白修饰整合
- Results: 从 oocyte 到 blastocyst 绘制 tRNA landscape，发现 4-cell 阶段 tRNA pseudogene 上调和 translation machinery 建立。
- Discussion/Direction: 低输入是突出贡献；算法挑战在于 dropout、批次效应和跨组学时间点对齐。

## 9. PMID 39096899 | A ligation-independent sequencing method reveals tRNA-derived RNAs with blocked 3' termini.
- Status: 主线保留
- Theme: tDR 捕获
- Article logic: LIDAR 通过 quasi-random priming 与 template switching 绕开 3' 端连接依赖，捕获有 blocked 3' termini 的 tDR。
- Hypothesis: 传统 ligation-based small RNA-seq 系统性漏检末端被修饰或封闭的 RNA，小 RNA 组成被低估。
- Methods: ligation-independent 建库; quasi-random RT primer; template switching; tDR 与 miRNA/read coverage 对比
- Results: LIDAR 检出更多 tRNA-derived RNA，尤其是传统方法难以捕获的 blocked 3' end tDR。
- Discussion/Direction: 适合发现层面；但 tDR 起源解析仍需要 tDRnamer/tRAX、tRNA reference 和多重比对模型支持。

## 10. PMID 36869120 | A standardized ontology for naming tRNA-derived RNAs based on molecular origin
- Status: 主线新增
- Theme: tDR 命名与注释
- Article logic: tDRnamer 把 tRNA-derived RNA 的命名锚定到分子来源、起止位置和 tRNA 层级，减少跨研究不可比。
- Hypothesis: 统一 ontology 是 tDR 定量、差异分析和数据库整合的前提，而不是报告阶段的格式问题。
- Methods: tRNA 来源层级定义; 片段坐标规则; 多等位/多位点歧义处理; 标准化名称输出
- Results: 为 tDR/tRF 结果提供机器可读、可比较的命名体系，能作为 LIDAR、small RNA-seq 和 tRAX 的下游桥梁。
- Discussion/Direction: 命名不能替代准确 mapping；未来应把命名不确定性传递到差异分析和功能富集。

## 11. PMID 39952700 | Analyzing, visualizing, and annotating tRNA-derived RNAs using tRAX and tDRnamer
- Status: 主线新增
- Theme: tRAX/tDR 分析协议
- Article logic: tRAX/tDRnamer 将 small RNA reads 的 tRNA 来源识别、注释、可视化和命名整合为可复现流程。
- Hypothesis: tDR 分析需要同时解决 read trimming、非 tRNA 污染、tRNA 参考归属和标准命名。
- Methods: small RNA QC/trimming; 多级参考比对; tRNA/tDR 分类; coverage、长度、片段类别可视化
- Results: 使 tDR 数据从单纯 counts 表转为可解释的来源、位置、类型和样本间变化。
- Discussion/Direction: 短读长与重复 tRNA 家族仍限制唯一定位；应引入概率归属、UMI 与 full-length evidence 校正。

## 12. PMID 35032425 | tRNA modification dynamics from individual organisms to metaepitranscriptomics of microbiomes.
- Status: 背景保留
- Theme: 修饰动态综述
- Article logic: 综述 tRNA modification dynamics 从单生物体扩展到微生物群落 metaepitranscriptomics。
- Hypothesis: tRNA 修饰不是静态装饰，而是环境响应、翻译调控和 tRF 生成的动态调节层。
- Methods: 汇总测序方法; 动态修饰功能框架; microbiome/metaepitranscriptomics 概念; 方法学瓶颈归纳
- Results: 强调修饰测序需要同时处理物种组成、tRNA 同源性、修饰读出和群落差异。
- Discussion/Direction: 作为工具路线图很有价值；但不提供新算法，需要转化为 benchmark 和标准化 workflow。

## 13. PMID 37802077 | tRNA renovatio: Rebirth through fragmentation.
- Status: 背景保留
- Theme: tDR 生物学综述
- Article logic: tRNA fragmentation 被定义为受调控的再利用过程，为 tDR 分析提供生物问题边界。
- Hypothesis: tsRNA/tDR 不是随机降解片段，而是具有来源、结构和互作特征的功能分子。
- Methods: 整合 biogenesis; 结构与互作机制; 疾病/病毒相关功能; AI 与结构预测方向
- Results: 提出未来需要全长序列、修饰、结构和互作的综合方法，支撑 tDR 功能解释。
- Discussion/Direction: 适合作为问题背景；不宜作为工具性能证据，主线中应降权。

## 14. PMID 37173525 | Quantifying tRNA abundance by sequencing.
- Status: 背景保留
- Theme: 定量方法评论
- Article logic: 从方法评论角度强调 tRNA abundance 测序的主要技术壁垒和新方法价值。
- Hypothesis: tRNA 结构、修饰和序列相似性使常规 RNA-seq 不能直接替代 tRNA-seq。
- Methods: 比较建库偏差; 讨论修饰阻断; 解释定量瓶颈; 指出 benchmark 需求
- Results: 为 QuantM/mim 等方法提供背景定位，说明为什么定量 tRNA 需要专门工具。
- Discussion/Direction: 没有新数据或算法，因此作为导读/过渡文献，不占主线证据页。

## 15. PMID 35322228 | AAV-delivered suppressor tRNA overcomes a nonsense mutation in mice.
- Status: 删出主线，保留附录
- Theme: 治疗应用
- Article logic: AAV-delivered suppressor tRNA 主要回答基因治疗可行性，而不是分析工具本身。
- Hypothesis: 工程化 sup-tRNA 可在 premature stop codon 处恢复蛋白表达，同时不过度扰动全局终止密码子读穿。
- Methods: sup-tRNA 设计; AAV 递送; ribosome profiling; tRNA-seq 检查内源稳态
- Results: 小鼠模型中长期恢复功能，全球正常 stop codon readthrough 有限。
- Discussion/Direction: 分析启发在于 tRNA-seq/ribo-seq 可作为安全性 readout；但不应作为工具算法主线。

## 16. PMID 37944512 | Design, construction, and functional characterization of a tRNA neochromosome in yeast.
- Status: 删出主线，保留附录
- Theme: 合成基因组
- Article logic: tRNA neochromosome 是合成生物学工程，使用 tRNA-seq、多组学和 Hi-C 评估构建体功能。
- Hypothesis: 将全部核编码 tRNA 转移到设计染色体上仍可维持酵母生长并用于扰动 tRNA gene organization。
- Methods: neochromosome 设计; SCRaMbLE; tRNA-seq/transcriptomics/proteomics; FISH/Hi-C/replication profiling
- Results: 构建体可存活但出现倍性变化等适应性压力，提示 tRNA 基因组织具有系统效应。
- Discussion/Direction: 可作为 tRNA reference 和功能验证案例；但不是通用分析工具论文。

## 17. PMID 35654044 | A pro-metastatic tRNA fragment drives Nucleolin oligomerization and stabilization of its bound metabolic mRNAs.
- Status: 删出主线，保留附录
- Theme: tRF 功能机制
- Article logic: 研究 5'-tRFCys 促进转移的机制，数据分析侧重 tRF 差异表达和靶蛋白/代谢通路验证。
- Hypothesis: 特定 tRF 可通过促进 Nucleolin oligomerization 稳定代谢 mRNA，从而增强癌细胞转移。
- Methods: small RNA profiling; 差异 tRF 筛选; RBP 互作鉴定; 动物/细胞功能验证
- Results: 5'-tRFCys 上调并驱动促转移代谢网络。
- Discussion/Direction: 说明 tDR 差异分析需要可靠命名和来源解析；但本文贡献是生物机制而非工具。

## 18. PMID 41501459 | RNA-triggered Cas12a3 cleaves tRNA tails to execute bacterial immunity.
- Status: 删出主线，保留启发
- Theme: CRISPR-tRNA 识别机制
- Article logic: Cas12a3 被靶 RNA 激活后切割 tRNA 3' CCA tail，证明 tRNA tail 可以成为可编程识别/报告位点。
- Hypothesis: 部分 type V CRISPR effector 通过 target RNA 触发非靶 tRNA 裂解实现抗噬菌体防御。
- Methods: cell-based/biochemical assay; direct RNA sequencing; cryo-EM; synthetic tRNA-tail reporter
- Results: 发现 tRNA-loading domain 定位 tRNA tail 至 RuvC active site，并扩展 CRISPR RNA 检测能力。
- Discussion/Direction: 对 tRNA tail 识别和纳米孔/direct RNA readout 有启发；但不是 tRNA 分析算法论文。

