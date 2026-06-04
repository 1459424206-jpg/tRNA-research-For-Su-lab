# tRNA 修饰指纹库阅读总结

生成日期：2026-05-23  
输入材料：`downloaded_resources/pdfs` 下 7 篇 PDF，`github_repositories_selected.csv/json` 中 8 个 GitHub 项目。  
辅助抽取文件：`paper_extraction.json`、`paper_figure_caption_index.md`。

## 一句话结论

这批材料共同指向一个清晰的数据库设计方向：tRNA 修饰指纹库不应只存“某个位点有什么修饰”，而应把修饰类型、tRNA/反密码子/结构位置、检测技术、测序错误或停顿信号、酶与生物学场景、功能后果和证据等级连成一张可查询的证据图谱。

最值得优先纳入的指纹信号有四类：

1. **化学/质谱指纹**：LC-MS/MS、MLC-seq、核苷/片段质量、修饰频率。
2. **逆转录/测序指纹**：mim-tRNAseq、TRAC-seq、PANDORA-seq、错配率、RT stop、cleavage score、read-through/termination。
3. **纳米孔电信号/碱基识别错误指纹**：RNA002/RNA004 直接 RNA 测序的 basecalling error、indel、read termination、上下文依赖信号。
4. **功能指纹**：氨酰化效率、A-site codon recognition、ribosome occupancy、translation efficiency、stress/virus/衰老/脂代谢表型。

## 数据库字段建议

建议将每条“指纹”拆成可复用记录：

| 字段组 | 推荐字段 |
|---|---|
| tRNA 身份 | species、cell/tissue、tRNA gene、isodecoder、anticodon、amino acid、cytosolic/mitochondrial/viral-associated |
| 位点 | canonical position, Sprinzl position, anticodon loop/D-loop/T-loop/variable arm, local sequence context |
| 修饰 | MODOMICS symbol、short name、chemical class、writer/eraser/reader enzyme、pathway |
| 检测方法 | method、library chemistry、enzyme pretreatment、sequencer、mapper、caller、threshold |
| 指纹特征 | mismatch spectrum、RT stop、cleavage score、basecalling error、indel、termination site、LC-MS fragment、coverage |
| 证据等级 | direct MS / sequencing inferred / structural / perturbation / computational prediction |
| 功能后果 | aminoacylation、codon decoding、ribosome stalling、translation efficiency、RNA stability、stress phenotype |
| 来源 | PMID/DOI、figure、GitHub tool、dataset accession、processing parameters |

## 文献阅读要点

### PMID 38918637

**Structural basis of tRNA recognition by the m3C RNA methyltransferase METTL6 in complex with SerRS seryl-tRNA synthetase.**

核心要点：
- METTL6 对 tRNASer C32 进行 m3C 修饰，SerRS 不是旁观者，而是帮助选择 tRNASer 底物的关键因子。
- cryo-EM 结构显示 METTL6 有一个 m3C-specific RNA-binding domain，识别 anticodon arm、C32 flip-out、A37 修饰和 variable arm。
- 对指纹库的价值：提供“修饰酶-氨酰 tRNA 合成酶-tRNA 结构-目标位点”的高置信结构证据；m3C32 的指纹不应只记录位点，还应记录 SerRS 依赖性、A37 预修饰、variable arm 识别。

每张图说什么：
- Fig. 1：展示 SerRS-tRNA-METTL6 复合物结构和体外甲基化实验；证明 SerRS 增强 METTL6 对 tRNASer 的 m3C 修饰。
- Fig. 2：定义 METTL6 的 m3C-RBD，说明其正电沟槽抓住 tRNA anticodon stem，并通过特定位点接触 C32。
- Fig. 3：显示 tRNA anticodon arm 被重塑，C32 从 C32-A38 配对中翻出，同时 A37 的 i6A 修饰被蛋白域识别。
- Fig. 4：展示 METTL6 活性中心，m3C32 与 SAH 位于甲基转移核心和 m3C-RBD 之间。
- Fig. 5：说明 METTL6-SerRS-tRNA variable arm 接口，指出 SerRS 通过少量关键 loop 帮助选择底物。
- Extended Data Fig. 1：蛋白/RNA 纯化、tRNA 质量控制和体外甲基化活性控制。
- Extended Data Fig. 2：cryo-EM 样品制备和数据处理流程。
- Extended Data Fig. 3：比较不同复合物 stoichiometry 下的 METTL6-SerRS-tRNA 接口。
- Extended Data Fig. 4：m3C RNA methyltransferase 多序列比对，标出保守活性/识别位点。
- Extended Data Fig. 5：与 METTL11 结构比较，强调 m3C-RBD 的特殊性。
- Extended Data Fig. 6：共纯化 tRNASer 的修饰谱，支持 A37/C32 等结构解释。
- Extended Data Fig. 7：模拟不同 A37 修饰如何被 METTL6/METTL2/METTL8 类酶协调。
- Extended Data Fig. 8：二维活性位点示意图，列出 m3C32、SAH 和侧链距离。
- Extended Data Fig. 9：METTL6 突变体功能验证，连接结构位点与甲基化活性。
- Extended Data Fig. 10：SerRS-METTL6 接口细节和 tRNA 结合实验，支持 SerRS 作为选择因子。

对指纹库的建议：
- `modification=m3C`, `position=32`, `enzyme=METTL6`, `cofactor/substrate selector=SerRS`, `required/associated_modification=i6A37/t6A37-like A37 state`, `evidence=cryo-EM + mutagenesis + MS`。

### PMID 38977661

**Perturbation of METTL1-mediated tRNA N7-methylguanosine modification induces senescence and aging.**

核心要点：
- METTL1-WDR4 催化 tRNA m7G46；衰老/老化时 METTL1-WDR4 与 m7G 水平下降。
- METTL1 缺失使一组 m7G-tRNAs 降低，触发 RTD、核糖体停顿、翻译效率下降、ribotoxic stress/ISR/SASP，最终促衰老。
- TRAC-seq 被用于定位 m7G 并评估 tRNA abundance，是指纹库中“化学切割 + 测序”型 m7G 指纹的重要方法。

每张图说什么：
- Fig. 1：显示 RNA m7G 甲基化、METTL1/WDR4 随细胞衰老和小鼠组织老化下降。
- Fig. 2：METTL1 knockdown/knockout 诱导衰老；野生型 METTL1 可 rescue，催化失活突变体不能 rescue。
- Fig. 3：小鼠 Mettl1 缺失导致早衰、寿命缩短、组织衰老标志增加；Mettl1 过表达缓解化疗诱导损伤。
- Fig. 4：TRAC-seq 定义 m7G46 tRNA 集合，显示 METTL1 缺失和衰老共同下调 13 类 m7G-tRNAs。
- Fig. 5：Ribo-seq 发现 METTL1 缺失时 m7G-tRNA 解码 codon 上核糖体停顿增加，WNT 等通路翻译效率下降。
- Fig. 6：METTL1 缺失通过 RPS20 ubiquitination、ISR/RSR 激活和 SASP 因子表达连接到衰老炎症表型。
- Fig. 7：eEF1A/RTD 与 tRNA 稳定性相关；补充 eEF1A 可部分缓解 METTL1 缺失造成的衰老和翻译压力。
- Fig. 8：SP1 调控 METTL1/WDR4 表达；给出 METTL1-m7G-tRNA-翻译-衰老模型图。

对指纹库的建议：
- 收录 `m7G46` 的 TRAC-seq cleavage score、motif、affected tRNA list、METTL1/WDR4 状态、RTD/translation phenotype。
- 为 m7G 指纹建立 `cleavage_score_ratio`, `tRNA_abundance_change`, `codon_ribosome_occupancy` 三个下游字段。

### PMID 40908366

**tRNA as an assembly chaperone for a macromolecular transcription-processing complex.**

核心要点：
- poxvirus vRNAP 装配需要特定 tRNAGln/Arg 作为 assembly chaperone，而不是用于翻译。
- 该 tRNA 的 anticodon loop 和修饰状态被结构性选择，尤其强调缺少 mcm5s2U34 的特定修饰图案。
- 对指纹库的价值：tRNA 修饰图谱不仅影响翻译，还决定非经典 RNP 装配功能；数据库应支持“non-translational function”标签。

每张图说什么：
- Fig. 1：重构 vRNAP 装配中间体，证明 tRNAGln/Arg 与核心 vRNAP 和辅助因子共同形成复合物。
- Fig. 2：展示早期 PIC 装配循环关键 cryo-EM 中间体 I3-I5。
- Fig. 3：提出 tRNA-chaperoned assembly cycle 模型，说明 tRNA 如何引导多个因子逐步组装。
- Fig. 4：高分辨率 complete vRNAP 结构，显示 tRNA 与 E11/NPH-I/VETF 等形成稳定带状装配。
- Fig. 5：解析 complete vRNAP 中 tRNAGln(UUG) 的 anticodon stem-loop 构象和非经典相互作用。
- Fig. 6：用 gel shift 和 LC-MS/MS 鉴定 tRNAGln/Arg 修饰，并测试修饰/突变对 vRNAP 形成的影响。
- Fig. 7：在 cryo-EM 密度中识别 tRNAGln 的 A57、C32、U34 等位置，指出 U34 处缺少 mcm5s2U3 的结构证据。
- Fig. 8：证明 complete vRNAP 与 tRNAGln(UUG) 作为整体被包装进 vaccinia virion。
- Extended Data Fig. 1：辅助转录因子与核心 vRNAP 的相互作用控制实验。
- Extended Data Fig. 2：minimal vRNAP 的 cryo-EM 重构质量控制。
- Extended Data Fig. 3：Rap94 结构域排列。
- Extended Data Fig. 4：vRNAP 中间体 I3/I4 的 cryo-EM 重构。
- Extended Data Fig. 5：中间体 I5 的 cryo-EM 重构。
- Extended Data Fig. 6：complete vRNAP 的 cryo-EM 重构。
- Extended Data Fig. 7：tRNAGln 和 tRNAArg 模型与 cryo-EM 密度拟合比较。
- Extended Data Fig. 8：修饰和非经典碱基配对对 vRNAP 复合物形成的影响。
- Extended Data Fig. 9：定量 vRNAP 和 virion extract 中的 tRNAGln(UUG) 含量。

对指纹库的建议：
- 增加 `functional_context=viral RNP assembly/non-translational chaperone`。
- 记录 `selected_modification_pattern`，包括“缺失某修饰”的状态，因为 absence 也可能是功能性指纹。

### PMID 41398161

**A cholesterol-responsive hepatic tRNA-derived small RNA regulates cholesterol homeostasis and atherosclerosis development.**

核心要点：
- PANDORA-seq 在小鼠肝脏中发现 tsRNA-Glu-CTC 是最丰富 tsRNA，且对胆固醇饮食响应。
- tsRNA-Glu-CTC 促进高胆固醇血症和脂肪肝；ASO knockdown 可降低胆固醇并缓解动脉粥样硬化。
- MLC-seq 显示内源性 tsRNA-Glu-CTC 带有位点特异 RNA 修饰，修饰型比未修饰合成寡核苷酸功能更强。

每张图说什么：
- Fig. 1：PANDORA-seq 比传统 RNA-seq 更好捕获肝脏 tsRNA，锁定 tsRNA-Glu-CTC。
- Fig. 2：高胆固醇饮食诱导 tsRNA-Glu-CTC，显示其 cholesterol-responsive 特征。
- Fig. 3：注射合成 tsRNA-Glu-CTC 导致血胆固醇升高和肝脏脂质沉积。
- Fig. 4：ASO knockdown tsRNA-Glu-CTC 降低高胆固醇饮食小鼠循环胆固醇并改善脂肪肝。
- Fig. 5：RNA-seq 显示 tsRNA-Glu-CTC 调控肝脏脂代谢基因，尤其 Srebp2 相关通路。
- Fig. 6：tsRNA-Glu-CTC 定位于核内/胞质，并与 SREBP2 互作，通过 E-box 调节自身转录。
- Fig. 7：在 Ldlr-/- 小鼠中，ASO 保护其免于饮食诱导的高胆固醇和动脉粥样硬化。
- Fig. 8：人样本中循环 tsRNA-Glu-CTC 与血清胆固醇水平相关。
- Fig. 9：MLC-seq 解析内源 tsRNA-Glu-CTC 修饰；修饰型 tsRNA 生物效应更强。
- Fig. 10：模型图，总结 tsRNA-Glu-CTC-SREBP2-脂质稳态/动脉粥样硬化轴。

对指纹库的建议：
- 指纹库应支持 `tsRNA fragment` 作为实体，并关联其来源 tRNA、片段端点、修饰、组织、疾病表型。
- PANDORA-seq/MLC-seq 可作为“被修饰小 RNA 指纹”的标准方法组合。

### PMID 41611679

**ALKB-1-dependent tRNA methylation is required for efficient paternal mitochondrial elimination.**

核心要点：
- C. elegans ALKB-1 demethylase 失活导致 tRNA m1A 增高。
- tRNA m1A 异常引起翻译紊乱、线粒体蛋白稳态破坏、ROS/SKN-1/UPRmt 激活，最终延迟 paternal mitochondrial elimination。
- 对指纹库的价值：m1A 指纹需要同时记录 demethylase 状态、translation/proteostasis、ROS 和生殖/线粒体遗传表型。

每张图说什么：
- Fig. 1：ALKB-1 RNAi 或 D247A 催化突变导致父源 mtDNA/线粒体清除延迟。
- Fig. 2：ALKB-1 失活使 tRNA m1A 增加，并伴随 RNC-seq/proteomics 显示线粒体蛋白稳态紊乱。
- Fig. 3：PME 延迟与 UPRmt 激活和 mtDNA 扩增相关，测试 ATFS-1 等通路。
- Fig. 4：ROS 增加和 SKN-1 激活参与 ALKB-1 失活导致的 PME 延迟。
- Fig. 5：遗传互作分析 SKN-1 与 ATFS-1，拆解 PME 延迟、UPRmt、ROS 之间的关系。
- Fig. 6：ALKB-1 失活降低雄性生殖能力并提高胚胎死亡率，最后给出调控模型。

对指纹库的建议：
- m1A 记录需区分 writer/eraser；`ALKB-1/ALKBH1-dependent demethylation` 是方向性信息。
- 增加 `organellar_quality_control`、`paternal_mitochondrial_elimination` 等 phenotype ontology。

### PMID 41714626

**Coronaviruses reprogram the tRNA epitranscriptome to favor viral protein expression.**

核心要点：
- 冠状病毒基因组富含 A/U-ending suboptimal codons。
- 病毒感染诱导 DNA damage/oxidative stress，并重塑宿主 tRNA 修饰：I、Q、mcm5U/mcm5s2U、m5C/f5C 等，利于病毒蛋白翻译。
- mim-tRNAseq 和 LC-MS/MS 在该论文中形成互补：一个给修饰/转录本层面的测序信号，一个给总体化学修饰水平。

每张图说什么：
- Fig. 1：RSCU 分析显示冠状病毒 codon usage 与 I/Q/mcm5U/mcm5s2U/m5C 相关解码需求。
- Fig. 2：SARS-CoV-2 和 HCoV-OC43 感染诱导 DNA damage response 和氧化应激。
- Fig. 3：LC-MS/MS 显示感染后 tRNA epitranscriptome 改变，尤其 anticodon loop 修饰。
- Fig. 4：敲低 ELP3、QTRT1、NSUN2 或过表达相关酶，测试这些 tRNA-modifying enzymes 对病毒 NP 蛋白表达的影响。
- Fig. 5：比较病毒和 tRNA modifying enzymes 的 RSCU，提示酶自身编码偏好与修饰反馈回路可能相关。
- Fig. 6：mim-tRNAseq 显示感染导致 type II tRNA transcripts 下降，并给出修饰变化图。

对指纹库的建议：
- 需要支持 `condition=viral infection/stress` 下的动态修饰变化，而不是静态参考表。
- 建议将 `codon_usage_pressure` 与 `required_tRNA_modification` 关联，例如病毒 A/U-ending codons 对 I/Q/mcm5U/mcm5s2U/m5C 的依赖。

### PMID 41807381

**Translational regulation by oxidative desulfuration of tRNA modifications.**

核心要点：
- xm5s2U34 这类 wobble 2-thiouridine 修饰在氧化条件下可脱硫，形成 xm5h2U34。
- mcm5h2U34 会降低 tRNALys/tRNAGln/tRNAGlu 氨酰化和 codon recognition，进而调节翻译。
- 对指纹库的价值：修饰需要记录“化学转化状态”，例如 mcm5s2U 到 mcm5h2U 是氧化应激下的动态指纹。

每张图说什么：
- Fig. 1：介绍 xm5s2U34 的位置、类型及氧化脱硫产物 xm5h2U，并用 LC-MS/CID 验证。
- Fig. 2：用 E. coli tracer tRNA spike-in 排除样品处理过程中人工产生 h2U 的可能。
- Fig. 3：在小鼠细胞质/线粒体 tRNAs 中检测 h2U derivatives，给出 U34 修饰频率。
- Fig. 4：体外翻译实验显示 tRNA 脱硫降低翻译效率。
- Fig. 5：脱硫 tRNA 的氨酰化效率下降，尤其 Gln/Glu/Lys 明显。
- Fig. 6：tRNALys 脱硫削弱 AAA/AAG codon 的 A-site 识别。
- Fig. 7：cryo-EM 解释 mcm5s2U34 与 mcm5h2U34 在 AAR decoding 中的结构差异。
- Fig. 8：模型图，总结氧化应激下 mcm5s2U34 脱硫为 mcm5h2U34，导致 codon-specific translation efficiency 下降。

对指纹库的建议：
- 对 U34 wobble 修饰建立 `redox_state`、`precursor_modification`、`converted_modification` 字段。
- 功能字段需区分 `aminoacylation effect` 和 `ribosome A-site decoding effect`。

## GitHub 项目阅读总结

| 项目 | 类型 | 能为指纹库提供什么 | 局限 |
|---|---|---|---|
| `junchaoshi/sports1.1` | small RNA/tRNA/rRNA-derived RNA 注释 pipeline | PANDORA-seq/小 RNA 数据中识别 tRNA-derived fragments，输出 tRNA 5'/3'/internal fragment、长度分布、reads、mismatch summary | 主要面向小 RNA 注释，不是修饰 caller；mismatch 只能作为候选修饰线索 |
| `nedialkova-lab/mim-tRNAseq` | modification-induced misincorporation tRNA sequencing pipeline | tRNA expression、modification misincorporation signature、coverage QC、3'-CCA completeness、SLAC crosstalk | 依赖 GSNAP/usearch/R/DESeq2 等；需要 mim-tRNAseq 实验设计 |
| `rnabioco/tRNA004` | Nanopore direct tRNA sequencing benchmark/R project | 43 类 RNA 修饰的 nanopore basecalling error benchmark，RNA002/RNA004 对比，MODOMICS 位点映射 | 更像分析项目/论文代码，不是通用一键 caller；原始数据公开状态需随论文检查 |
| `rnabioinfor/TRAC-Seq` | m7G TRAC-seq 项目入口 | 与 m7G single-nucleotide profiling 方法相关，可作为 m7G46 指纹方法来源 | README 几乎为空，需要从论文/脚本/补充材料补方法细节 |
| `jfallmann/tRNA_ngs_mod_map_call_galaxy` | Galaxy 工具集合 | tRNA reference construction、CCA 添加、multimapper phasing、GATK mismatch/variant calling，可组织 NGS 修饰映射 workflow | 老旧，依赖 GATK 3.6；需要本地 Galaxy/GATK 配置 |
| `monimaanam/Modomics_Decoder` | MODOMICS unicode sequence decoder | 将 MODOMICS 序列符号映射到修饰短名和位置，适合导入参考修饰表 | 不是测序分析工具；需要和 tRNA 坐标/物种/证据来源结合 |
| `AteeshaNegi/nanopore-2Read-trna-pipeline` | ONT 2-read tRNA modification analysis pipeline | 基于 basecalling error、polymerase read-through/error、termination events 做 per-read/per-site 修饰候选 | README 概念性较强；需进一步检查脚本完整度和示例数据 |
| `FlorianPichot/tRNA_reference_construction` | tRNA reference construction/validation scripts | 从 genomic tRNA predictions 构建 non-duplicated/merged/optimized tRNA reference，并用 reads 验证 | 路径硬编码较多；主要是参考构建，不负责修饰 calling |

### 项目逐个要点

#### SPORTS1.1

最适合用来处理 PANDORA-seq 或 small RNA-seq 中的 tsRNA/tRF 层面：
- 支持 genome、miRNA、rRNA、tRNA、piRNA、Ensembl ncRNA、Rfam 多库注释。
- 对 tRNA 可区分 pre-tRNA、mature tRNA、mitochondrial tRNA，并自动生成 CCA 版本参考。
- 输出每条 unique sequence 的 reads、length、Match_Genome、Annotation，例如 `tRNA-Glu-CTC_5_end`。
- `-M` 和 `-z` 可产生 mismatch summary，可作为修饰候选信号，但不能直接等同于修饰。

指纹库用途：
- 生成 tsRNA/tRF 实体表：fragment sequence、length、5'/3'/internal class、source tRNA、reads/RPM、condition。
- 与 41398161 的 tsRNA-Glu-CTC 结合，可作为“修饰 tsRNA 功能指纹”的入口。

#### mim-tRNAseq

这是最直接可用的 tRNA 修饰测序 pipeline：
- 从 trimmed fastq 开始，聚类 tRNAs、建立 modification index、用 GSNAP 做 SNP-tolerant alignment。
- 将 cluster-aligned reads deconvolve 到 transcript-level tRNA reads。
- 计算 coverage、expression、DESeq2 differential expression。
- 分析 3'-CCA completeness、modification-induced misincorporation signatures。
- 可用 SLAC 分析修饰-修饰、修饰-氨酰化之间的 single-read crosstalk。

指纹库用途：
- 设计 `method=mim-tRNAseq` 的 evidence record：coverage、misincorporation rate、mutation spectrum、modification pair crosstalk、aminoacylation association。
- 适合收录 41714626 中感染条件下 tRNA transcript 和修饰重编程证据。

#### tRNA004

这是纳米孔直接 tRNA 测序的 benchmark/论文分析项目：
- 比较 RNA002 与 RNA004 chemistry。
- 使用 MODOMICS 中已知 tRNA 修饰，评估 40+ 或 43 类修饰在 nanopore basecaller 中产生的信号。
- `rmd/fig2_RNA_mods.Rmd` 明确说明：把 basecalling error data 映射到 tRNA structure files，并与 modification info 对齐。
- 包含 Rmd、src、bcerror、modplots 等分析产物，用于生成论文图和所有修饰上下文的错误图。

指纹库用途：
- 建立 `nanopore_error_fingerprint` 表：chemistry、basecaller model、modification type、sequence context、coverage、error/indel pattern。
- 适合做“参考训练集/benchmark set”，帮助未来 ONT tRNA 修饰 caller 评估。

#### TRAC-Seq

仓库 README 只有标题，文档不足；但从 38977661 文献可读到 TRAC-seq 的核心：
- AlkB/D135S 处理去除阻碍 RT 的修饰。
- NaBH4 还原 m7G 位点，aniline cleavage 在还原位点切割。
- small RNA library sequencing 后用 cleavage score 定位 m7G。

指纹库用途：
- 把 TRAC-seq 作为 `m7G-specific cleavage-based sequencing` 方法来源。
- 重点字段：G46 cleavage score、control/KO ratio、motif、tRNA abundance。

#### tRNA_ngs_mod_map_call_galaxy

Galaxy workflow 工具集合：
- `addCCA` 给 tRNA 序列加 CCA，得到 mature tRNA 参考。
- `clustering` 聚类完全相同的 tRNA 序列。
- `multimapperPhasing` 允许多重比对 reads，但要求其 misincorporation pattern 一致。
- `gatk_wrapper` 用 GATK/Picard/samtools 对 tRNAmod BAM 做 realignment/variant calling。
- `removeGenomeMapper`、`removePrecursor` 用于过滤基因组/前体 tRNA reads。

指纹库用途：
- 对传统短读长 tRNA-seq 的 mismatch/variant 证据做标准化预处理。
- 适合作为 workflow 参考，不建议原样作为现代生产 pipeline。

#### Modomics_Decoder

这是一个 MODOMICS 符号解析器：
- 内置 unicode/symbol 到修饰名的字典，例如 `7 -> m7G/pm7G`, `? -> m5C/pm5C`, `Ѣ -> m1A/pm1A`, `Щ -> m3C/pm3C`。
- 可输出修饰位置表和全序列位置列表。

指纹库用途：
- 将 MODOMICS 序列批量转为 `position-symbol-short_name` 表。
- 可作为 reference import 的轻量工具，但需要补充物种、tRNA 名称、标准坐标、证据来源和 MODOMICS 版本。

#### nanopore-2Read-trna-pipeline

README 描述的是 ONT 2-read tRNA modification pipeline：
- 通过 direct RNA sequencing、Dorado basecalling、POD5/BAM/FASTQ 转换、BWA-MEM alignment 进行分析。
- 核心信号是 systematic ONT basecalling errors、polymerase read-through/error、5'/3' termination patterns。
- 面向 E. coli、人、酵母 tRNA，强调 per-read/per-site single-nucleotide resolution。

指纹库用途：
- 适合为每个位点存储 `termination_fingerprint` 与 `per-read_error_signature`。
- 可以和 tRNA004 的 benchmark 指纹互补：一个偏 benchmark/Rmd 分析，一个偏 2-read pipeline 思路。

#### tRNA_reference_construction

参考构建工具：
- 从 genomic tRNA predictions 生成 tRNA reference。
- 包括 non-duplicated、merged、optimized references 的分阶段构建。
- 用 Unix/R 脚本和 reads mapping 验证参考质量。

指纹库用途：
- 解决“同一 read 匹配多个 tRNA 基因/等解码 tRNA”的参考归并问题。
- 建议作为数据库 `reference_version` 构建流程的一部分，而不是修饰证据来源。

## 建议的指纹库处理流程

1. **参考层**
   - 用 GtRNAdb/MODOMICS/tRNAscan-SE 构建物种 tRNA reference。
   - 用 `tRNA_reference_construction` 思路处理重复 tRNA、merged reference、mature CCA reference。
   - 用 `Modomics_Decoder` 导入 MODOMICS 已知修饰位置。

2. **短读长/RT 指纹层**
   - 对 mim-tRNAseq 数据运行 mimseq，产出 misincorporation、coverage、expression、CCA、SLAC。
   - 对 m7G 使用 TRAC-seq 风格 cleavage score。
   - 对 small RNA/PANDORA-seq 用 SPORTS1.1 识别 tsRNA/tRF 来源。

3. **纳米孔指纹层**
   - 用 tRNA004 作为 benchmark：为每种修饰/上下文建立 error profile。
   - 用 2-read pipeline 思路记录 per-read termination 和 read-through/error。

4. **功能证据层**
   - 从论文中抽取 functional assays：aminoacylation、codon recognition、Ribo-seq、translation efficiency、stress response、phenotype。
   - 每个功能证据都链接 PMID、Figure、condition 和 perturbation。

5. **数据库查询层**
   - 支持按修饰查：`m7G`, `m3C`, `m1A`, `mcm5s2U`, `mcm5h2U`, `I`, `Q`, `m5C/f5C`。
   - 支持按位置查：U34、C32、G46、A37 等。
   - 支持按方法查：LC-MS/MS、MLC-seq、TRAC-seq、mim-tRNAseq、PANDORA-seq、Nanopore RNA004。
   - 支持按生物学场景查：aging、viral infection、oxidative stress、cholesterol metabolism、PME、viral RNP assembly。

## 最高优先级收录对象

建议第一版先做这些核心条目：

| 优先级 | 条目 |
|---|---|
| P0 | m7G46 / METTL1-WDR4 / TRAC-seq cleavage score / aging-senescence |
| P0 | U34 mcm5s2U 与氧化脱硫 mcm5h2U / codon recognition / oxidative stress |
| P0 | mim-tRNAseq misincorporation signature schema |
| P0 | Nanopore RNA004 43 修饰 benchmark schema |
| P1 | m3C32 / METTL6-SerRS / structural recognition |
| P1 | tsRNA-Glu-CTC / PANDORA-seq + MLC-seq / cholesterol phenotype |
| P1 | coronavirus-induced I/Q/mcm5U/mcm5s2U/m5C/f5C reprogramming |
| P2 | ALKB-1-dependent m1A / PME and mitochondrial proteostasis |
| P2 | poxvirus vRNAP-associated tRNAGln/Arg modification pattern |

## 本次材料的缺口

- TRAC-Seq GitHub 仓库文档极少，真正可用信息主要来自论文方法；后续需要补充脚本、参数或补充材料。
- 多数 GitHub 项目不是统一输入/输出标准，数据库应先定义中间标准表，再写转换器。
- 纳米孔项目的原始 pod5/fastq 与模型版本会强烈影响 error fingerprint，需记录 chemistry/basecaller/model。
- MODOMICS 符号解析需要固定版本，否则同一符号表未来可能漂移。

## 附：本地证据文件

- PDF/HTML 抽取结构：`D:\Project\tRNA research\tRNA mod-fingerprint database\downloaded_resources\analysis_outputs\paper_extraction.json`
- 图注索引：`D:\Project\tRNA research\tRNA mod-fingerprint database\downloaded_resources\analysis_outputs\paper_figure_caption_index.md`
- GitHub README 缓存：`D:\Project\tRNA research\tRNA mod-fingerprint database\downloaded_resources\analysis_outputs\github_raw_readmes`
- 已下载仓库：`D:\Project\tRNA research\tRNA mod-fingerprint database\downloaded_resources\github_repositories`
