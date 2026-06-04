# mim-tRNAseq 与 Induro-tRNAseq 修饰指纹库对比及三篇文献精读

生成日期：2026-06-03  
范围：仅比较反转录酶/工具本身的修饰指纹规则，不解释具体样本中的修饰丰度差异。  
本地资料来源：
- `D:\Project\tRNA research\new study\mim_tRNAseq_fingerprint_library\mim_tRNAseq_fingerprint_report_cn.md`
- `D:\Project\tRNA research\new study\mim_tRNAseq_fingerprint_library\mim_tRNAseq_fingerprint_tables.xlsx`
- `D:\Project\tRNA research\analysis_induro_modification_fingerprints_20260602\Induro_tRNAseq_modification_fingerprints_reproduction.xlsx`
- `D:\Project\tRNA research\analysis_induro_modification_fingerprints_20260602\papers\Nakano_2025_Induro_tRNAseq_NatCommun.pdf`
- `D:\Project\tRNA research\analysis_induro_modification_fingerprints_20260602\papers\Chen_2016_Science_sperm_tsRNAs.pdf`
- `D:\Project\tRNA research\analysis_induro_modification_fingerprints_20260602\papers\Chen_Yan_Duan_2016_NRG_sperm_RNA_modifications.pdf`

## 一、核心结论

1. `mim-tRNAseq` 与 `Induro-tRNAseq` 不是两个完全同构的“修饰数据库”。`mim-tRNAseq` 的指纹库更偏向源码内置规则：完整修饰字典、可检测修饰集合、人工补充位点、canonical 位点先验。`Induro-tRNAseq` 的指纹库更偏向酶学实测图谱：Induro 在每类 tRNA 修饰上的读穿（readthrough）、反转录停顿（RT stop）和错配掺入（misincorporation）响应。
2. 两者共享一组主要可读修饰：m1A、m1G、m2,2G、m3C、m1I、I34、yW、acp3U、ms2i6A、ms2t6A。它们大多位于 9、20、26/27、32、34、37、58 等经典 tRNA 修饰热点。
3. 主要差异不在“有没有这些修饰名称”，而在“如何把测序错误解释成修饰”。Induro 论文系统测定了每种修饰的 RT stop 与 misincorporation 模式，并指出 Induro 大多数情况下以 0 位错配为主，少数修饰以 +1 RT stop 为主。
4. Induro 对 acp3U20 和 ms2i6A37/ms2t6A37 的表现最有区分度：这两类是 Induro 的主要停顿型例外。acp3U20 上 Induro 的 RT stop 强于 TGIRT；ms2i6A37/ms2t6A37 上 Induro 的停顿弱于 TGIRT，且 Mn2+ 可改善该位点读穿。
5. mim-tRNAseq 源码额外收录了 o2yW 和 OHyW 这两个 wybutosine 家族条目；Induro 论文主要以 yW37 作为实测条目，并没有把 o2yW/OHyW 分拆成单独规则。
6. 两者都不能把所有 tRNA 修饰直接读出来。假尿苷（pseudouridine, Ψ）、二氢尿苷（dihydrouridine, D）、m5C、T/ribothymidine、τm5U 等不改变 Watson-Crick 配对面的修饰，在常规 Mg2+ 条件下不属于稳定 RT-readable 修饰；需要化学处理、酶处理或质谱等互补技术。

## 二、术语速查

| 中文术语 | English | 本报告中的含义 |
|---|---|---|
| 反转录酶 | reverse transcriptase, RT | 把 tRNA 反转录为 cDNA 的酶。不同 RT 面对修饰碱基时会停顿、错配或读穿。 |
| 读穿 | readthrough | RT 从 tRNA 3' 端一路合成到 5' 端附近，未在修饰处终止。 |
| 反转录停顿 | RT stop | RT 在修饰位点或附近停止，产生截短 cDNA。 |
| 错配掺入 | misincorporation | RT 遇到修饰碱基时掺入非标准互补碱基，测序中表现为 mismatch。 |
| 读出身份 | read identity | 在测序读段中，修饰位点被读成 A/C/G/U 的哪一种。 |
| 反密码子茎环 | anticodon stem-loop, ASL | tRNA 识别密码子的结构区域，34/37 位等修饰常在此影响翻译。 |
| tRNA 主体 | tRNA body | ASL 以外、更多参与 L 形三级结构稳定的 tRNA 区域。 |
| 同解码子 | isodecoder | 反密码子相同、解码同一密码子但序列可不同的 tRNA。 |
| 同受体 | isoacceptor | 携带同一氨基酸、但反密码子可不同的一组 tRNA。 |
| wobble 位点 | wobble position | 反密码子的第 34 位，可决定一个 tRNA 能识别哪些同义密码子。 |
| Watson-Crick 配对面 | Watson-Crick face | 参与 A-U、G-C 标准碱基配对的碱基化学面；被修饰后更容易影响 RT。 |

## 三、mim-tRNAseq 与 Induro-tRNAseq：工具层面对比总表

| 比较维度 | mim-tRNAseq / TGIRT | Induro-tRNAseq / Induro | 相同点与差异解释 |
|---|---|---|---|
| 核心 RT | TGIRT，group-II intron-derived RT。 | Induro，新的 group-II intron-encoded RT，商业化试剂 NEB M0681。 | 二者同属 group-II intron RT，整体 misincorporation 图谱相近；Induro 论文将二者并行比较，用于增强修饰预测置信度。 |
| 指纹库的本质 | 源码内置库：`mimseq/modifications`、`Mods + I`、`additionalMods.txt`、`mmQuant.py::mods`。 | 实测酶响应库：每类修饰对应 RT stop、misincorporation、read identity、读穿条件和 Mg2+/Mn2+ 影响。 | mim 更像“规则/注释库”；Induro 更像“酶学行为图谱”。 |
| 完整修饰字典 | 170 个修饰符号条目，可把 MODOMICS 符号还原为未修饰参考碱基。 | 论文不提供等价的 170 项完整字典；重点是 RT-readable 修饰。 | mim 的底层字典覆盖广，但并不表示全部可检测。 |
| 真正可检测核心集合 | 12 类：m1A、m1G、m2,2G、m3C、m1I、yW、o2yW、OHyW、acp3U、ms2i6A、ms2t6A、I/I34。 | 主要实测：m1A9/58、m1G9/37、acp3U20、m2,2G26/27、m3C32、I34、m1I37、yW37、ms2i6A37、ms2t6A37。 | 共同核心高度重叠；mim 额外把 o2yW/OHyW 单列，Induro 主文未单列。 |
| 人工补充位点 | 有。`additionalMods.txt` 主要补 I34，另有少量 m1A9、mcm5s2U34。 | 没有同构的人工补充文件；论文按已知位置和 >10% RT stop/mismatch 标准识别已注释或未注释位点。 | mim 更依赖预定义位点；Induro 更强调从 RT 行为发现/确认。 |
| canonical 位点先验 | 有。9、20、20a、20b、26、32、37、58、e9 等作为修饰干扰热点，避免误判 isodecoder 差异。 | 论文分析聚焦 9、20、26、32、34、37、58 等已知 tRNA 修饰位置，并用 -1/0/+1 窗口报告停顿。 | 两者热点位置高度一致；mim 在去卷积层面硬编码得更明确。 |
| 主要 readout | mismatch / misincorporation，RT stop 也可作为修饰信号，但源码库重点是错配容忍和注释。 | 大多数修饰：0 位 misincorporation；acp3U20a 与 ms2i6A37/ms2t6A37：+1 RT stop 更关键。 | Induro 对每类修饰给了更细的 readout 建议。 |
| 读穿优化 | 资料中主要体现为既有 mim 流程与 TGIRT 数据集。 | Induro 明确优化：37 °C 过夜读穿最高约 90%；42 °C 过夜为论文工作流选择；55 °C 推荐条件反而读穿低。 | Induro 论文的一个重要贡献是把 RT 条件本身系统化。 |
| Mg2+/Mn2+ | mim 资料中无同等系统的 Mg2+/Mn2+ 指纹比较。 | Mn2+ 可特别改善 ms2i6A37/ms2t6A37 的 readthrough，并增强低阈值 m7G 检出；但常规工作流仍用 Mg2+。 | Induro 在金属离子调控方面提供了可操作线索。 |
| 与样本无关的局限 | 依赖 MODOMICS/人工位点与源码规则；不是所有 170 个修饰都能被判读。 | 不改变 Watson-Crick 配对面的修饰在 Mg2+ 条件下仍难读，如 Ψ、D、m5C、T、τm5U；低信号位点仍需谨慎。 | 两者都需要 LC-MS/MS、化学处理或酶处理补证。 |
| 数据分析骨架 | mimseq 管线：BLAST/MODOMICS 注释、聚类、GSNAP 比对、错配和停顿统计。 | Induro 论文的数据处理仍使用 mimseq v1.2 进行映射和部分分析。 | Induro 不是完全另起炉灶；它在 RT 与实验读出层面扩展了 mim/TGIRT 框架。 |
| 最适合的问题 | 快速利用已有 TGIRT/mim 规则做 tRNA 丰度、修饰热点、isodecoder 去卷积。 | 系统比较修饰位点的 RT signature、选择最佳 RT 条件、发现组织/细胞间协调修饰变化。 | 若研究目标是“修饰指纹本身”，Induro 信息更细；若目标是“已有注释库驱动分析”，mim 更成熟。 |

## 四、逐修饰指纹库异同表

| 修饰 | 中文（English） | 经典位置 | mim-tRNAseq 状态 | Induro-tRNAseq 状态 | 异同与解释 |
|---|---|---:|---|---|---|
| m1A | 1-甲基腺苷（1-methyladenosine） | 9、58，也可见 14/16 | 核心可检测条目；源码把它作为经典错配/停顿指纹位点。 | 实测 m1A9/58；位置敏感，m1A9 与 m1A58 的读穿随温度/结构不同。主要看 0 位错配和读穿。 | 共同核心修饰。差异在于 Induro 明确强调“同一化学修饰在不同结构位置有不同 RT signature”。 |
| m1G | 1-甲基鸟苷（1-methylguanosine） | 9、37 | 核心可检测条目，常见于 G9/G37。 | 实测 m1G9/37；m1G37 读穿随温度增加更明显，m1G9 与 m1G37 行为不同。 | 共同核心修饰。Induro 论文还用 Pro(AGG) 的 m1G37/I34 读出解决了此前人/鼠 Pro(AGG) m1G37 是否稳定存在的问题。 |
| m2,2G | N2,N2-二甲基鸟苷（N2,N2-dimethylguanosine） | 26、27 | 核心可检测条目；26 位是 canonical 先验热点。 | 实测 m2,2G26/27；通常以 0 位错配为主，局部结构可影响信号。 | 共同核心修饰。需要注意它与 sperm tsRNA 文献中的 m2G（N2-methylguanosine）不是同一化学物种。 |
| m3C | 3-甲基胞苷（3-methylcytidine） | 32 | 核心可检测条目；32 位是先验热点。 | 实测 m3C32；Induro 可读穿 m3C32，主要以错配而非强停顿读出。 | 共同核心修饰。Induro 的亮点是无需先对 m3C 做化学处理即可读出。 |
| m1I | 1-甲基次黄嘌呤（1-methylinosine） | 37 | 核心可检测条目。 | 实测 m1I37；接近均一的 0 位 misincorporation。 | 共同核心修饰。Induro 给出更明确的 read identity/错配主导判断。 |
| I / I34 | 次黄嘌呤（inosine） | 34 | 源码单独处理 I，人工补充库大量补 I34。 | 实测 I34；几乎完全是 0 位错配，几乎无 RT stop。 | 共同核心修饰。I34 是 wobble 解码研究的高价值位点，两个工具都很重要。 |
| yW | wybutosine | 37 | 核心可检测条目。 | 实测 yW37；与 TGIRT 相比，Induro 的 read identity 可不同，Induro 主要读成 G，而 TGIRT 主要读成 T。 | 共同核心修饰。Induro/TGIRT 的差异可作为区分 yW37 的酶学指纹。 |
| o2yW | 过氧 wybutosine（peroxywybutosine） | 37 | mim 源码单列为可检测条目。 | 主文未作为独立条目系统展开。 | mim 特有/更细分。Induro 可能在 yW 家族相关读出中有信息，但没有主文级独立规则。 |
| OHyW | 羟基 wybutosine（hydroxywybutosine） | 37 | mim 源码单列为可检测条目。 | 主文未作为独立条目系统展开。 | mim 特有/更细分。需要质谱或更精细注释确认具体 wybutosine 衍生物。 |
| acp3U | 3-(3-氨基-3-羧丙基)尿苷（3-(3-amino-3-carboxypropyl)uridine） | 20、20a | 核心可检测条目；20/20a/20b 是 canonical 热点。 | Induro 的主要例外之一，常以 +1 RT stop 为主；Induro 在 acp3U20 的 RT stop 强于 TGIRT。 | 共同核心修饰，但最佳 readout 不同于多数修饰。研究 acp3U20 时，Induro 的停顿信号尤其有用。 |
| ms2i6A | 2-甲硫基-N6-异戊烯基腺苷（2-methylthio-N6-isopentenyladenosine） | 37 | 核心可检测条目。 | 与 ms2t6A37 合并讨论；Induro 的主要停顿型例外之一，常在 +1 RT stop；Mn2+ 可改善读穿。 | 共同核心修饰。Induro 论文将它和 ms2t6A 作为 A37 复杂修饰组合来读。 |
| ms2t6A | 2-甲硫基-N6-苏氨酰氨甲酰腺苷（2-methylthio-N6-threonylcarbamoyladenosine） | 37 | 核心可检测条目。 | 与 ms2i6A37 合并讨论；主要 readout 是 RT stop 窗口，尤其 +1。 | 共同核心修饰。对翻译解码和胚胎/生殖相关研究具有较高优先级。 |
| m7G | 7-甲基鸟苷（7-methylguanosine） | 常见 46 等 | 不是 mim 核心 12 个可检测条目之一。 | 常规 >10% 阈值下不作为主要 RT-readable；Mn2+ 与较低错配阈值可提高检出。 | Induro 论文提供了低阈值探索线索，但不应把 m7G 当作常规高置信核心指纹。 |
| Ψ | 假尿苷（pseudouridine） | 多位点 | 不在 mim 核心 12 个可检测条目。 | Mg2+ 条件下不可稳定 RT-readable；Mn2+ 也未可靠检出。作者建议未来考虑 CMC 或 bisulfite 等化学处理。 | 两者都需要化学处理或其他方法补充。 |
| m5C | 5-甲基胞苷（5-methylcytidine） | 多位点，含 tRNA/tsRNA | 不在 mim 核心 12 个可检测条目。 | 论文明确把 m5C 归入常规 Mg2+ 条件下不 RT-readable 的非 Watson-Crick face 修饰。 | 与 sperm tsRNA 文献高度相关，但不能仅靠这两个 RT 指纹库可靠定位。 |

## 五、如何理解“指纹库”这个词

### 1. mim-tRNAseq 的指纹库

mim-tRNAseq 的“指纹库”至少有四层：

1. 完整修饰字典：170 个修饰符号条目，用于把 MODOMICS 修饰字符转换成修饰名和原始碱基。
2. 可检测核心集合：真正进入 signature 判读的 12 类修饰。
3. 人工补充位点：尤其是多个物种中的 I34，还有少量 m1A9、mcm5s2U34。
4. canonical hotspot 先验：9、20、20a、20b、26、32、37、58、e9 等，用于避免把修饰造成的错配误判为 isodecoder 差异。

所以，mim-tRNAseq 的完整修饰字典不是“全部可检测修饰表”。真正用于判读的核心集合远小于 170 项。

### 2. Induro-tRNAseq 的指纹库

Induro-tRNAseq 的“指纹库”主要来自 Nakano et al. 2025 对 Induro 反转录酶的系统实测：

1. 大多数 RT-readable 修饰以 0 位 misincorporation 为主。
2. I34 几乎纯错配，几乎没有 RT stop。
3. acp3U20a 和 ms2i6A37/ms2t6A37 是两个主要例外，以 +1 RT stop 为主。
4. 同一化学修饰在不同结构位置可有不同酶学响应，例如 m1A9 与 m1A58、m1G9 与 m1G37。
5. Induro 与 TGIRT 整体相似，但 acp3U、ms2i6A/ms2t6A、yW 等处存在可利用差异。

因此，Induro 的价值不只是“多一个 RT”，而是给出了按修饰/位点/局部结构拆开的酶学指纹规则。

## 六、文献精读 1：Nakano et al. 2025, Nature Communications

题目：Genome-wide profiling of tRNA modifications by Induro-tRNAseq reveals coordinated changes  
类型：方法学 + 资源型 + 生物学发现论文  
主题：建立 Induro-tRNAseq，系统定义 Induro 对 tRNA 修饰的 RT signature，并用其分析不同细胞/组织中的协调性 tRNA 修饰变化。

### 1. 背景知识

tRNA 是修饰最密集的 RNA 类型之一。成熟 tRNA 中约 10-20% 的核苷酸可带有转录后修饰（post-transcriptional modifications）。这些修饰大致分两类：

1. 反密码子茎环修饰（ASL modifications）：位于 32、34、37 等位点，直接影响密码子-反密码子配对、解码准确性、移码抑制和翻译效率。
2. tRNA 主体修饰（body modifications）：位于 9、20、26、58 等位点，更多影响 tRNA L 形三级结构、折叠稳定性、成熟和蛋白因子识别。

Illumina tRNA-seq 的核心难题是 RT 很难穿过高度修饰、结构紧密的 tRNA。不同 RT 面对同一修饰时可能有三种行为：停下来、错配读过去、直接读过去。这个行为就是“RT signature”。

已有 TGIRT 被用于 mim-tRNAseq，Marathon 被用于 tRNA structure-seq/ALL-tRNAseq。作者认为目前仍缺少对每类修饰的系统 RT signature 定义，因此引入新的 group-II intron RT：Induro。

### 2. 研究逻辑

论文的逻辑链如下：

1. 先建立一个可多重化（multiplexing）的 Induro-tRNAseq 工作流。
2. 验证该工作流能稳定测 tRNA 丰度、3' CCA 端完整性和 tRNA charging。
3. 系统优化 Induro 反转录温度和时间，找出读穿条件。
4. 在已知 RT-readable tRNA 修饰上建立 Induro 的 RT stop/misincorporation 图谱。
5. 与 TGIRT/mim-tRNAseq 数据并行比较，判断二者在每类修饰上的相同与差异。
6. 把方法应用到 5 种人类细胞系和 3 种小鼠组织，寻找 tRNA 修饰的组织/细胞型变化。
7. 得出一个概念模型：ASL 中直接参与遗传密码读取的修饰更稳定，tRNA body 中参与结构适配的修饰更可变。

### 3. 实验方法

样本与输入：

- 人类细胞系：HEK293T、K562、HeLa、SH-SY5Y、HAP1。
- 小鼠组织：小脑、肾、脾等。
- 输入可为总 RNA（total RNA）或凝胶纯化 tRNA。作者发现总 RNA 输入更简便且效果相近，因此工作流主要使用总 RNA。

文库构建流程：

1. tRNA charging 测定：对未氨酰化 tRNA 的 2',3'-羟基进行高碘酸氧化（periodate oxidation），再通过 β-消除（β-elimination）去除 A76，形成 CC 端；氨酰化 tRNA 先受保护，去酰化后保留 CCA 端。
2. T4 PNK 修复 3' 端。
3. T4 RNA ligase 2（T4 Rnl2）在 DNA splint 辅助下连接带 barcode 的 3' adapter。
4. Induro RT 反转录，标准工作流为 42 °C 过夜 12-16 h。
5. cDNA 凝胶纯化、Circligase 环化、Q5 PCR 扩增。
6. Illumina NextSeq 500 进行 2×75 paired-end sequencing。

优化与验证：

- 温度：25、37、42、55 °C。
- 时间：1、2、16 h。
- 金属离子：Mg2+ 与 Mn2+。
- 定量校准：用含 0%、25%、75%、100% m1G9 的 mt-Leu(TAA) 合成/重构 tRNA 进行线性校准。
- 质谱补证：用 LC-MS/MS 验证小鼠组织 acp3U 水平。

数据分析：

- PEAR 合并 paired-end reads。
- cutadapt 去 barcode/adaptor，并去除 RT 引入的 5' RN 两个核苷酸。
- 用 mimseq v1.2 将人类 reads 映射至 hg38 tRNA 参考，小鼠映射至 mm39。
- GSNAP 比对成熟 tRNA representative cluster。
- mismatch rate：目标位点四种错配碱基计数之和 / 总 reads。
- RT stop frequency：该位点 stops / 该位点总 reads。
- readthrough：1 - RT stop ratio。
- 对每个修饰，RT stop 取 -1、0、+1 三核苷酸窗口最大值，降低误估。
- 已知和未知修饰候选：在已知位置 9、20、26、32、34、37、58 以及非注释位置，RT stop 或 misincorporation >10%。
- 差异丰度：DESeq2 归一化后计算 Pearson correlation。
- 组织/细胞差异：按 tRNA 表达量加权的 misincorporation difference。
- 统计：两侧 Wilcoxon test、Student's t-test 等。

### 4. 主要结果

结果 1：Induro-tRNAseq 工作流可靠。  
Induro 与 TGIRT/mim-tRNAseq 测得的 cytosolic tRNA 和 mitochondrial tRNA 丰度整体高度相关。Induro 对 mt-Ser(GCT) 的检测优于 TGIRT 工作流。3' CCA 完整性较高，说明流程对 tRNA 降解较少。

结果 2：Induro 读穿强烈依赖温度和时间。  
55 °C 是厂家推荐的通用条件，但对 tRNA 修饰读穿并不理想，读穿约 10% 且随时间不改善。37 °C 过夜最高可到约 90% 读穿，42 °C 过夜约 60%。作者最终选择 42 °C 过夜，因为 42 °C 有完整时间梯度数据，且检测到的潜在修饰数量更多。

结果 3：Induro 的读穿提升主要来自减少 RT stop，而不是改变 misincorporation。  
作者发现 misincorporation 频率在时间过程中基本稳定，readthrough 增加来自 RT stops 下降。这说明 misincorporation 更像 Induro 对特定修饰的内在指纹，而 RT stop 更受温度、时间和结构环境调控。

结果 4：不同修饰的 Induro 指纹不同。  
多数 RT-readable 修饰以 0 位 misincorporation 为主，RT stop 较低。I34 几乎只有错配、没有停顿。acp3U20a 和 ms2i6A37/ms2t6A37 是主要例外，常在修饰后 +1 位发生 RT stop。m3C32 可被 Induro 读穿，这是方法学亮点。

结果 5：同一化学修饰在不同位置有不同酶学行为。  
m1A9 与 m1A58 不同，m1G9 与 m1G37 也不同。这说明不能只按“修饰名”解释测序信号，还必须考虑 tRNA 局部结构环境。

结果 6：Mn2+ 主要改善 ms2i6A37/ms2t6A37。  
以 Mn2+ 替代 Mg2+ 后，Induro 对 ms2i6A37/ms2t6A37 的 misincorporation 增加、RT stop 降低。此外，在低错配阈值下，m7G 检出增强；但 Ψ 仍不能可靠检出。

结果 7：Induro 与 TGIRT 总体相似，但可互补。  
两者对多数修饰的 misincorporation 率和可检测注释修饰数量相近。差异主要包括：

- acp3U20：Induro RT stop 强于 TGIRT。
- ms2i6A37/ms2t6A37：Induro RT stop 弱于 TGIRT。
- yW37：read identity 不同，Induro 主要读为 G，TGIRT 主要读为 T。

结果 8：tRNA 修饰变化具有协调性。  
ASL 中参与解码的修饰在不同组织和细胞中更稳定；tRNA body 中稳定 L 形结构的修饰更可变。作者据此提出：tRNA 修饰在满足翻译供应-需求平衡和蛋白稳态（protein homeostasis）中具有协调机制。

### 5. 讨论发散

这篇论文把 tRNA 修饰研究从“一个错配等于一个修饰”推进到“同一修饰在不同位置、不同 RT、不同反应条件下有不同 signature”。它给 tRNA 修饰研究带来的发散方向包括：

1. RT 选择本身可以成为实验设计变量。不要默认厂家推荐温度就是 tRNA 修饰测序最佳条件。
2. Induro 与 TGIRT 可作为双 RT 互证体系：若两个 RT 在同一位点给出符合预期但不同的 read identity/RT stop 图谱，修饰预测更可信。
3. 对低信号修饰，RT stop 与 misincorporation 要同时看，尤其是 acp3U 和 A37 thio/carbamoyl 修饰。
4. tRNA body 修饰的组织差异可能不是噪音，而是细胞型对 tRNA 结构适配的调节。
5. ASL 修饰的稳定性提示这些位点更可能是核心翻译稳态需求，适合做跨组织/跨物种保守性研究。

### 6. 局限

1. 非 Watson-Crick face 修饰仍难以直接读出，如 Ψ、D、m5C、T、τm5U。
2. 未注释修饰的化学身份不能仅靠 RT signature 最终确认，仍需 LC-MS/MS 或化学处理验证。
3. Induro 序列信息不可用，限制了对其结构机制的深入工程化改造。
4. 主要样本是细胞系和少数小鼠组织，生殖细胞、早期胚胎、精子 tsRNA 并不是本论文主体。
5. >10% 阈值适合高置信筛选，但可能漏掉低丰度或低 stoichiometry 修饰。

### 7. 对 tRNA 研究的提示

如果我们要做 tRNA 修饰研究，Induro-tRNAseq 适合用于：

- 建立 tRNA 修饰位点层面的 RT signature。
- 比较不同细胞状态中 ASL 与 non-ASL 修饰的协调变化。
- 重点追踪 I34、m1A58、m1G37、m3C32、acp3U20、ms2i6A/ms2t6A37 等功能位点。
- 与 TGIRT/mim-tRNAseq 联合使用，提高修饰判读置信度。
- 对不能 RT-readable 的修饰，提前设计 LC-MS/MS、化学处理测序或抗体/酶学验证。

## 七、文献精读 2：Chen et al. 2016, Science

题目：Sperm tsRNAs contribute to intergenerational inheritance of an acquired metabolic disorder  
类型：实验性论文  
主题：高脂饮食（high-fat diet, HFD）父代小鼠的精子 tsRNA 可把代谢异常信息传递给 F1 后代，并伴随 tsRNA 表达和 RNA 修饰变化。

### 1. 背景知识

父源获得性性状遗传（paternal inheritance of acquired traits）指父亲在环境暴露、饮食、压力等经历中获得的表型，可通过精子影响后代。传统关注点是 DNA 甲基化（DNA methylation）和组蛋白修饰（histone modifications），但这些标记在受精后会经历大规模重编程，因此是否能稳定传递一直有争议。

精子携带多类小非编码 RNA（small non-coding RNA, sncRNA），包括 miRNA、piRNA、tRNA-derived small RNA。tsRNA 是 tRNA 衍生小 RNA，本文主要关注 5' tRNA halves，长度约 30-34 nt。

### 2. 研究问题

作者想回答：

1. 父代 HFD 诱导的代谢异常能否通过精子传给后代？
2. 精子 RNA 是否足以诱导后代表型？
3. 哪一类精子 RNA 是主要信息载体？
4. tsRNA 的表达和修饰是否受 HFD 改变？
5. 注入 HFD 精子 tsRNA 后，胚胎和后代胰岛的基因表达如何改变？

### 3. 实验设计与方法

动物模型：

- F0 雄鼠从 5 周龄开始喂养 6 个月。
- HFD：60% fat。
- ND：normal diet，10% fat。
- HFD 雄鼠出现肥胖、葡萄糖耐受异常和胰岛素抵抗。

验证精子本身可携带信息：

- 精子头注射（sperm-head injection）进入正常卵母细胞，胚胎移植到代孕母鼠。
- 排除自然交配中的精液因子和雌雄接触因素。
- HFD 精子来源后代出现葡萄糖耐受异常和胰岛素抵抗。

验证精子 RNA 可诱导表型：

- 提取 HFD/ND 精子总 RNA。
- 按约 10 个精子的 RNA 量注入正常合子（zygote）。
- 后代进行体重、葡萄糖耐受试验（glucose tolerance test, GTT）、胰岛素耐受试验（insulin tolerance test, ITT）检测。

分离 RNA 亚群：

- 15% PAGE 分离 15-25 nt、30-40 nt、>40 nt RNA。
- 30-40 nt 组主要是 tsRNA。
- 15-25 nt 组主要是 miRNA。
- 分别注入合子，观察 F1 后代表型。

小 RNA 测序与修饰检测：

- 小 RNA-seq 比较 HFD 与 ND 精子中的 sncRNA。
- LC-MS/MS 同时识别和定量多个 RNA 修饰。
- 比较 30-40 nt tsRNA fraction 与 15-25 nt miRNA fraction 中的修饰变化。

胚胎和后代转录组/甲基化分析：

- F1 后代胰岛进行 RNA-seq 和 RRBS（reduced representation bisulfite sequencing）。
- 注入 tsRNA 后的 8 细胞胚胎和囊胚进行 RNA-seq。
- 分析差异表达基因、GO 富集和 tsRNA 与启动子区域匹配。

### 4. 主要结果

结果 1：HFD 精子头可传递代谢异常。  
HFD 精子头产生的雄性 F1 后代在正常饮食下仍出现葡萄糖耐受异常和胰岛素抵抗，说明精子携带了足够信息。

结果 2：精子总 RNA 可诱导葡萄糖耐受异常。  
注入 HFD 精子总 RNA 后，F1 雄性后代体重无明显差异，但 GTT 中血糖和血清胰岛素升高，提示葡萄糖耐受异常。ITT 不完全复制精子头注射结果，说明 RNA 是重要因素但可能不是唯一因素。

结果 3：30-40 nt RNA/tsRNA 是关键亚群。  
HFD 和 ND 精子 small RNA-seq 显示，tsRNA 的差异比例高于 miRNA。注入 30-40 nt RNA 可以复制总 RNA 诱导的代谢表型；>40 nt RNA 无明显作用；高剂量 15-25 nt RNA 导致胚胎致死，稀释后不诱导代谢表型。

结果 4：合成未修饰 tsRNA 不能复制内源 tsRNA 功能。  
作者合成了占精子 tsRNA 约 70% 的高表达 tsRNA 组合，但注入后不能诱导代谢异常。一个解释是未修饰合成 tsRNA 在合子裂解液中稳定性较差，而内源精子 tsRNA 带有修饰，更稳定。

结果 5：HFD 改变 tsRNA 修饰。  
LC-MS/MS 在 30-40 nt sperm RNA 中稳定检测到 10 类 RNA 修饰。HFD 精子的 tsRNA fraction 中 m5C 和 m2G 显著升高，而 15-25 nt miRNA fraction 中没有显著变化。这说明修饰变化是 tsRNA 特异或至少在 tsRNA fraction 中更明显。

结果 6：HFD tsRNA 改变胚胎和胰岛转录组。  
F1 胰岛 RNA-seq 显示差异基因富集于代谢通路，特别是下调基因。RRBS 发现的 DMR 相关基因与转录变化基因不重叠，提示 DNA 甲基化不是直接解释。8 细胞胚胎和囊胚中，HFD tsRNA 注入导致更多基因下调，并富集于代谢调控、蛋白运输、定位等过程。

结果 7：tsRNA 可能通过启动子匹配影响转录级联。  
差异 tsRNA 更倾向匹配基因启动子区域而非编码区。部分匹配启动子的基因在 8 细胞胚胎中表达，并出现差异表达。作者提出 tsRNA 可能在早期胚胎启动转录级联，最终影响胰岛功能和代谢表型。

### 5. 讨论发散

这篇论文的关键发散是把 sperm tsRNA 从“精子中存在的小 RNA”推进到“具有功能因果性的父源表观遗传信息载体”。尤其重要的是：内源 tsRNA 与合成未修饰 tsRNA 的功能差异，把“RNA 修饰”引入了父源遗传的机制讨论。

对 tRNA 修饰研究而言，它提示：

1. tRNA-derived fragments 继承了 tRNA 母体的部分修饰，这些修饰可能决定 tsRNA 稳定性、靶标识别或蛋白结合。
2. LC-MS/MS 能证明修饰总量变化，但不能定位到具体 tsRNA 序列和具体位点。
3. m5C 与 m2G 是生殖/代谢表型中值得重点跟踪的修饰类别，但它们不等同于 mim/Induro 核心 RT-readable 修饰库中的全部重点。

### 6. 局限

1. m5C 和 m2G 的位点未定位到具体 tsRNA 序列，因此不能判断是哪条 tsRNA 的哪个碱基最关键。
2. 合成 tsRNA 缺乏修饰，不能区分“序列组合不对”与“缺乏修饰导致功能缺失”。
3. 注入实验虽然有因果性，但注入剂量和时空分布不完全等同自然受精。
4. 胚胎转录组变化与启动子匹配是强提示，但具体结合蛋白、靶标机制和直接分子互作未解析。
5. 总 RNA 与精子头注射表型并不完全一致，说明 DNA甲基化、组蛋白、蛋白或其他 RNA 可能协同参与。

### 7. 对 tRNA 研究的提示

如果我们关注 tRNA/tsRNA 与生殖发育：

- 不应只测 tsRNA abundance，还要测修饰。
- m5C/m2G 需要 LC-MS/MS、bisulfite/m5C mapping、AlkB 类处理或其他新技术定位。
- 可以把 Induro/TGIRT 用于 tRNA 母体修饰位点图谱，再结合小 RNA-seq 和质谱推断 tsRNA 继承哪些修饰。
- 功能实验要尽量比较：天然 tsRNA、未修饰合成 tsRNA、带特定位点修饰的合成 tsRNA。

## 八、文献精读 3：Chen, Yan & Duan 2016, Nature Reviews Genetics

题目：Epigenetic inheritance of acquired traits through sperm RNAs and sperm RNA modifications  
类型：综述  
主题：总结精子 RNA 与精子 RNA 修饰在获得性性状遗传中的证据、机制假说、技术偏差和未来方向。

### 1. 综述逻辑

这篇综述按以下逻辑展开：

1. 获得性性状遗传曾被认为有争议，但越来越多动物实验支持父代环境暴露可影响后代。
2. DNA 甲基化作为主要载体的解释不足，因为受精后存在表观遗传重编程，而且多项数据不支持饮食诱导的 sperm methylome 改变可稳定维持。
3. 因此需要寻找其他精子信息载体，尤其是精子 RNA。
4. 精子 RNA 包括 miRNA、piRNA、tsRNA、mitosRNA、lncRNA 等，其中 miRNA 和 tsRNA 已有功能注入证据。
5. 精子 RNA 可通过早期胚胎转录级联、转座元件调控、染色质结构重塑等方式影响后代表型。
6. RNA 修饰为 sperm RNA 功能提供新的调控层，尤其是 tsRNA 中 m5C/m2G 的变化和稳定性作用。
7. RNA 修饰也会导致测序偏差，过去的小 RNA-seq 数据可能漏检高度修饰的 tRNA/tsRNA。
8. 未来需要单细胞多组学、修饰定位、功能性 writer/eraser 操作和严谨动物实验。

### 2. 关键背景与术语

- 获得性性状遗传（inheritance of acquired traits）：个体在环境中获得的表型被后代继承。
- 非孟德尔遗传（non-Mendelian inheritance）：不按 DNA 序列等位基因分离规律解释的遗传现象。
- 表观遗传重编程（epigenetic reprogramming）：受精后和原始生殖细胞中大规模清除/重置表观遗传标记。
- 转座元件（transposable elements, TEs）：可移动遗传元件，常与早期胚胎转录调控相关。
- 胞外囊泡（extracellular vesicles, EVs）：可在附睾等环境中向精子转运 RNA。
- RNA 修饰酶（RNA modification enzymes）：添加、去除或编辑 RNA 修饰的酶，如 DNMT2、APOBEC1 等。

### 3. 综述中的核心论点

论点 1：DNA 甲基化不是唯一、也未必是初始载体。  
作者指出环境暴露确实可能改变 sperm DNA methylation，但许多变化不能稳定传到后代或与转录变化直接对应。因此 sperm RNA 成为重要候选。

论点 2：精子 RNA 有功能证据。  
早期精神压力、高脂饮食、高脂高糖饮食等模型中，注入精子总 RNA 或特定小 RNA 可部分或完全复制父代表型。

论点 3：tsRNA 是精子小 RNA 的重点。  
成熟精子中 tsRNA 丰富，主要来源于 tRNA 5' 端，长度约 29-34 nt。tsRNA 在高脂饮食、低蛋白饮食、环境暴露和人类肥胖中可变化，提示其是敏感环境响应标记。

论点 4：附睾成熟可能重塑精子 RNA。  
精子在附睾成熟过程中获得大量 tsRNA，可能来自附睾上皮细胞 EVs。这意味着精子 RNA 不是只由睾丸内转录决定，还可能被体细胞环境后天装载。

论点 5：RNA 修饰可能决定 tsRNA 功能。  
精子 tsRNA 含大量修饰。HFD 可使 tsRNA m5C 和 m2G 升高；修饰可能提高 RNA 稳定性、改变二级结构、改变与 DNA/RNA/蛋白的结合特异性。

论点 6：修饰会造成测序偏差。  
tRNA/tsRNA 高度修饰，部分修饰会阻断 RT，导致常规 RNA-seq 文库中漏检。AlkB 去甲基化处理可恢复部分被漏检 tRNA/tsRNA。因此旧数据需要谨慎重解读。

### 4. 对机制的梳理

机制 A：早期胚胎转录级联。  
精子 RNA 进入合子后，即使产生很小的初始表达偏差，也可能在 2-cell、8-cell、囊胚等阶段被放大，影响谱系和代谢程序。

机制 B：miRNA-AGO 靶向 mRNA。  
精子 miRNA 可通过 Argonaute（AGO）调控 mRNA 稳定性或降解，这是相对经典的 post-transcriptional regulation。

机制 C：tsRNA 与启动子/转座元件关联。  
tsRNA 可能匹配基因 promoter，很多 promoter 与 TE 相关。tsRNA 可能通过未知蛋白或 RNA-DNA/RNA-RNA 互作影响早期胚胎转录。

机制 D：lncRNA 调控染色质三维结构。  
精子 lncRNA 可能影响长程染色质互作和 3D genome organization，但证据相对推测性。

机制 E：RNA 修饰稳定和重定向 sperm RNA。  
m5C、m2G 等修饰可能延长 tsRNA 半衰期，改变二级结构，改变与靶 DNA/RNA/蛋白的结合。

### 5. 综述指出的缺陷与未来方向

1. 具体 RNA 序列与具体表型之间的“编码机制”不清楚。
2. 一个性状究竟由单个 RNA、RNA 组合，还是 RNA 与 DNA/组蛋白协同编码，尚未解决。
3. RNA 修饰位点图谱不完整，尤其是 sperm tsRNA/miRNA 的位点级修饰图谱。
4. LC-MS/MS 有修饰类型定量能力，但缺少位点信息。
5. 常规 RNA-seq 会漏检高度修饰 RNA，需要 AlkB、化学处理和新测序技术。
6. 需要早期胚胎和精子的单细胞多组学：transcriptomics、DNA methylomics、ChIP-seq、Hi-C 等。

### 6. 对 tRNA 研究的提示

这篇综述对 tRNA 研究最大的提示是：tRNA 修饰研究不能只停留在成熟 tRNA 全长分子，也要关注 tRNA-derived small RNAs。尤其在生殖和早期胚胎场景中，真正进入合子并发挥调控作用的可能是 tsRNA，而其功能又可能由 tRNA 母体修饰遗传下来。

## 九、三篇文献之间的关系

| 论文 | 类型 | 核心贡献 | 与 mim/Induro 指纹库的关系 |
|---|---|---|---|
| Nakano et al. 2025 | 方法学/资源型实验论文 | 建立 Induro-tRNAseq，定义 Induro 对多类 tRNA 修饰的 RT signature。 | 直接回答“Induro 反转录酶可读哪些修饰、如何读”。是 Induro 指纹库的主要依据。 |
| Chen et al. 2016 Science | 实验性功能论文 | 证明 HFD 精子 tsRNA 可诱导后代代谢异常，并发现 tsRNA m5C/m2G 升高。 | 提示 tRNA/tsRNA 修饰有生殖功能意义；但 m5C/m2G 不一定能由 mim/Induro 常规 RT 指纹直接定位。 |
| Chen, Yan & Duan 2016 NRG | 综述 | 梳理 sperm RNA/RNA modification 介导获得性遗传的证据与假说。 | 给出研究框架：精子 RNA、RNA 修饰、测序偏差、早期胚胎机制。 |

## 十、如果我们要做 tRNA 相关研究，可得到的提示

### 1. 技术路线建议

1. 若目标是全长 tRNA 修饰指纹：优先考虑 Induro-tRNAseq + mim/TGIRT 双 RT 互证。
2. 若目标是 m1A、m1G、m2,2G、m3C、I34、m1I、yW、acp3U、ms2i6A/ms2t6A：可用 RT signature 作为初筛。
3. 若目标是 m5C、m2G、Ψ、D、m7G、T 等：不要单靠常规 Induro/mim 指纹，应加入 LC-MS/MS、化学处理测序、AlkB/engineered AlkB 处理或靶向验证。
4. 若研究 sperm tsRNA：全长 tRNA-seq 与 small RNA-seq 要配套，否则难以判断 tsRNA 修饰来自哪条 tRNA 母体。
5. 若研究早期胚胎：需要在合子、2-cell、8-cell、blastocyst 等阶段做时间序列，而不是只看成体组织。

### 2. 优先修饰/位点

| 优先级 | 修饰/位点 | 理由 |
|---|---|---|
| 高 | I34 | wobble 解码核心，Induro/mim 均可读；对密码子偏好和早期胚胎翻译调控有强生物学意义。 |
| 高 | m1A58 / m1A9 | tRNA 结构稳定、成熟、ALKBH1/ALKBH3 相关；与生殖/胚胎发育有潜在连接。 |
| 中高 | m1G37 | 反密码子环稳定和移码抑制，Induro 论文指出 Pro(AGG) m1G37 保守存在。 |
| 中高 | ms2i6A37/ms2t6A37 | A37 解码修饰，Induro 中是特殊停顿型信号；可能与高翻译需求状态有关。 |
| 中高 | m5C / m2G in sperm tsRNA | Science/NRG 文献直接关联 HFD 精子 tsRNA；但需要非标准定位方法。 |
| 中 | acp3U20 | Induro 指纹强，组织差异明显；更偏结构调节和神经/组织特异性。 |
| 中 | m3C32 | ASL 稳定修饰，在 Induro 中可读；可作为解码稳定性研究位点。 |

### 3. 关键实验组合

推荐组合 A：全长 tRNA 修饰图谱  
Induro-tRNAseq + mim/TGIRT 数据交叉验证 + LC-MS/MS 总量验证。

推荐组合 B：sperm tsRNA 功能研究  
small RNA-seq + LC-MS/MS + 修饰定位方法 + 合成修饰/未修饰 tsRNA 注入或细胞模型比较。

推荐组合 C：writer/eraser 因果验证  
敲低/敲除或过表达 TRMT6/TRMT61A、TRMT10、TRMT1、METTL2/METTL6、ADAT2/3、DNMT2/NSUN2、ALKBH1/ALKBH3 等，再检测 tRNA/tsRNA 修饰和胚胎/翻译表型。

推荐组合 D：早期胚胎机制  
tsRNA 注入 + 2-cell/8-cell/blastocyst RNA-seq + TE/promoter 分析 + DNA methylome/ATAC/Hi-C 或 CUT&Tag，判断 RNA 信号是否转化为染色质或转录级联。

### 4. 研究设计中最容易踩的坑

1. 把“修饰总量变化”误解为“某个 tRNA 位点变化”。LC-MS/MS 需要位点定位补充。
2. 把 m2G 与 m2,2G 混为一谈。二者化学结构和生物学含义不同。
3. 只看 mismatch，不看 RT stop。acp3U 和 ms2i6A/ms2t6A 这类会被漏判。
4. 用未修饰合成 tsRNA 否定天然 tsRNA 功能。未修饰 RNA 稳定性和互作可能完全不同。
5. 把样本差异当作工具差异。比较 RT 指纹库时应固定“修饰类别/位点/酶行为”，不要把某个样本丰度差异混入。

## 十一、最终建议

如果下一步要围绕 tRNA 修饰与生殖发育做研究，我建议把问题拆成两层：

1. 工具层：用 Induro 与 TGIRT/mim 建立全长 tRNA 修饰位点的可靠指纹，重点锁定 I34、m1A58、m1G37、m3C32、acp3U20、ms2i6A/ms2t6A37。
2. 生物学层：在精子和早期胚胎中追踪 tsRNA abundance + tsRNA modification，尤其补上 m5C/m2G 的位点级证据和功能因果验证。

这样可以避免只做“相关性列表”，而是形成一条更完整的证据链：tRNA 母体修饰变化 -> tsRNA 修饰继承/稳定性变化 -> 合子/胚胎转录或翻译改变 -> 后代表型。
