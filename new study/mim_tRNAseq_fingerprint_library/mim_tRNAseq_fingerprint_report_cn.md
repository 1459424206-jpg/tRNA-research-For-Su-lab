# mim-tRNAseq 指纹库提取与解释

## 我怎么界定“指纹库”

在 `mim-tRNAseq` 源码里，和“指纹”直接相关的内置库其实有 4 层：

1. `mimseq/modifications`：完整修饰字典。负责把 MODOMICS 的单字符符号翻译成修饰名、简称和来源碱基。
2. `tRNAtools.py` 里的 `Mods` + `I`：真正参与“已知可识别修饰位点”登记的可检测集合。
3. `data/additionalMods.txt`：人工补充的物种/转录本级位点库，用来补 MODOMICS 缺口，尤其是 I34。
4. `mmQuant.py` 顶部的 `mods`：去卷积时用的 canonical hotspot 先验库，不是修饰名字典，而是“哪些保守位置本来就容易因修饰出现错配”的规则表。

## 这 4 层分别做什么

### 1. 完整修饰字典 `mimseq/modifications`

- 总条目数：170
- 作用：给每个符号提供 `full name / short name / originating base`，并用于把 MODOMICS 序列里的修饰字符还原成未修饰参考碱基。
- 输出文件：`mim_tRNAseq_modifications_full.tsv`
- 阅读建议：这张表适合查“某个字符究竟代表什么修饰”，但它不等于“都会被 mim-tRNAseq 直接拿来做 signature 判读”。

### 2. 真正可识别的指纹集合

- 条目数：12
- 来源：`tRNAtools.py` 里 `Mods = ['"', 'K', 'R', "'", 'O', 'Y', 'W', '⊆', 'X', '*', '[']`，以及单独处理的 `I`。
- 作用：这些条目会被登记为已知修饰位点，进入 SNP-tolerant alignment 和后续 misincorporation 解释流程。
- 输出文件：`mim_tRNAseq_detectable_fingerprint_set.tsv`

可识别集合逐项解释：

- `"` -> `m1A` / 1-methyladenosine：m1A。mim-tRNAseq 把它当作经典 misincorporation/RT-stop 指纹位点之一，常见于 A9、A58 等保守位点。
- `K` -> `m1G` / 1-methylguanosine：m1G。属于强读穿但会留下错配信号的甲基化 G 位点，常见于 G9/G37 一类位置。
- `R` -> `m2,2G` / N2,N2-dimethylguanosine：m2,2G。双甲基化 G，常在 26 位产生明显 signature，是 mim-tRNAseq 重点监测位点。
- `'` -> `m3C` / 3-methylcytidine：m3C。3-甲基胞苷，常见于 32 位，能造成稳定的错配模式。
- `O` -> `m1I` / 1-methylinosine：m1I。1-甲基次黄嘌呤，代码中列入已知可识别修饰集合。
- `Y` -> `yW` / wybutosine：yW。wybutosine，常位于 37 位，属于强结构性解码相关修饰。
- `W` -> `o2yW` / peroxywybutosine：o2yW。peroxywybutosine，是 yW 通路衍生物；代码把它也视作可容忍/可识别 signature。
- `⊆` -> `OHyW` / hydroxywybutosine：OHyW。hydroxywybutosine，同样属于 yW 家族衍生物；这是源码里额外支持的 wybutosine 类条目。
- `X` -> `acp3U` / 3-(3-amino-3-carboxypropyl)uridine：acp3U。3-(3-amino-3-carboxypropyl)uridine，论文与代码都把它视作典型可读出 signature 的修饰。
- `*` -> `ms2i6A` / 2-methylthio-N6-isopentenyladenosine：ms2i6A。2-methylthio-N6-isopentenyladenosine。源码把它纳入可识别集合，说明作者允许其作为已知 signature 位点处理。
- `[` -> `ms2t6A` / 2-methylthio-N6-threonylcarbamoyladenosine：ms2t6A。2-methylthio-N6-threonylcarbamoyladenosine。和 `*` 类似，属于源码层面额外纳入的 A37 类复杂修饰。
- `I` -> `I` / inosine：Inosine。与上面 11 个普通“修饰符号”不同，代码单独追踪 `I`，重点是 anticodon wobble 位点 I34。

### 3. 人工补充位点库 `additionalMods.txt`

- 总条目数：56
- 作用：把 MODOMICS 不完整、但作者明确知道应该存在的位点手工补进去。
- 这个文件里最主要的是 `I34`，另外还有少量 `m1A9` 与 `mcm5s2U34`。
- 输出文件：`mim_tRNAseq_additional_manual_mods.tsv`

按物种统计：
- `Homo sapiens`：9 条；Ala-AGC:I34, Arg-ACG:I34, Ile-AAT:I34, Leu-AAG:I34, Pro-AGG:I34, Ser-AGA:I34, Thr-AGT:I34, Val-AAC:I34, Asp-GTC:m1A9
- `Mus musculus`：5 条；Ala-AGC:I34, Pro-AGG:I34, Thr-AGT:I34, Ser-AGA:I34, Leu-AAG:I34
- `Saccharomyces cerevisiae`：1 条；Gln-TTG:mcm5s2U34
- `Schizosaccharomyces pombe`：9 条；Gln-TTG:mcm5s2U34, Pro-AGG:I34, Thr-AGT:I34, Arg-ACG:I34, Leu-AAG:I34, Ser-AGA:I34, Ala-AGC:I34, Ile-AAT:I34, Val-AAC:I34
- `Danio rerio`：8 条；Ala-AGC:I34, Arg-ACG:I34, Ile-AAT:I34, Leu-AAG:I34, Pro-AGG:I34, Ser-AGA:I34, Thr-AGT:I34, Val-AAC:I34
- `Gorilla gorilla`：8 条；Ala-AGC:I34, Arg-ACG:I34, Ile-AAT:I34, Leu-AAG:I34, Pro-AGG:I34, Ser-AGA:I34, Thr-AGT:I34, Val-AAC:I34
- `Rattus norvegicus`：8 条；Ala-AGC:I34, Arg-ACG:I34, Ile-AAT:I34, Leu-AAG:I34, Pro-AGG:I34, Ser-AGA:I34, Thr-AGT:I34, Val-AAC:I34
- `Caenorhabditis elegans`：8 条；Ala-AGC:I34, Arg-ACG:I34, Ile-AAT:I34, Leu-AAG:I34, Pro-AGG:I34, Ser-AGA:I34, Thr-AGT:I34, Val-AAC:I34

逐类解释：

- `I34`：最重要的 wobble 位点补充规则。代码在 `additionalModsParser()` 里把它直接映射到 anticodon 的第 34 位，并单独走 inosine 逻辑。
- `m1A9`：这里是对 `Homo sapiens Asp-GTC` 的人工补丁，说明作者知道这个位点会影响 signature，但单靠自动匹配未必能稳定补上。
- `mcm5s2U34`：针对酵母 Gln-TTG 的 34 位 wobble 超修饰补丁，用来弥补数据库或匹配流程对该位点的不完整覆盖。

### 4. canonical hotspot 先验库 `mmQuant.py::mods`

- 条目数：9
- 作用：当某个 read 和 cluster parent 有差异时，程序会先检查差异是否正好落在这些“本来就常被修饰扰动”的保守位点上；如果是，就尽量不要把它当成真正的 isodecoder 差异。
- 输出文件：`mim_tRNAseq_canonical_site_priors.tsv`

逐项解释：
- `9` / bases `G,A`：作为去卷积时的“已知易受修饰干扰位点”先验，避免把这些错配误认成 isodecoder 真突变。
- `20` / bases `C,T`：同上；20/20a/20b 是可变环附近的保守修饰热点，源码单独保留。
- `20a` / bases `T`：20 位插入编号之一，用于处理经典 tRNA 编号中的扩展位点。
- `20b` / bases `T`：20 位插入编号之一，和 20/20a 一起构成可变环先验列表。
- `26` / bases `G`：26 位是 m2,2G 高发位点；源码在去卷积时把这里当成“可能由修饰引起”的错配位置。
- `32` / bases `C`：32 位常见 m3C 等 anticodon-loop 邻近修饰，因此被设为先验热点。
- `37` / bases `G,A`：37 位是解码相关超修饰核心位点，包含 yW、i6A、ms2i6A、ms2t6A 等重要条目。
- `58` / bases `A`：58 位典型对应 m1A58，一般会显著影响 RT 行为。
- `e9` / bases `C`，仅匹配 `Leu-CAG|Ser-AGA|Ser-CGA|Ser-GCT|Ser-TGA`：扩展位点的特例规则，仅对部分 Leu/Ser 家族生效，用来避免这些特定转录本在去卷积时被误拆分。

## 你最该怎么理解 mim-tRNAseq 的“指纹库”

- 如果你问“这个工具把哪些修饰名字收进库里了”，答案看 `mim_tRNAseq_modifications_full.tsv`。
- 如果你问“这个工具真正把哪些修饰当成可识别 signature 来处理”，重点看 `mim_tRNAseq_detectable_fingerprint_set.tsv`。
- 如果你问“它为了提高物种覆盖率额外硬编码了哪些位点”，看 `mim_tRNAseq_additional_manual_mods.tsv`。
- 如果你问“它去卷积时默认把哪些位置当成修饰干扰热点”，看 `mim_tRNAseq_canonical_site_priors.tsv`。

## 关键结论

- `mim-tRNAseq` 不是把 `modifications` 里的所有修饰都一视同仁地当作“可检测指纹”。
- 真正参与 signature 判读的是一个更小的核心集合：m1A、m1G、m2,2G、m3C、m1I、yW/o2yW/OHyW、acp3U、ms2i6A、ms2t6A，加上单独处理的 I34。
- 代码还用 `additionalMods.txt` 和 canonical hotspot 规则，补偿 MODOMICS 注释不全以及 isodecoder 去卷积时的误判风险。

## 源码定位

- `mimseq/modifications`：完整修饰字典
- `mimseq/tRNAtools.py`：`processModomics()`、`Mods = [...]`、`additionalModsParser()`
- `mimseq/data/additionalMods.txt`：人工补充位点
- `mimseq/mmQuant.py`：`mods = {...}` 与未知修饰/去卷积逻辑