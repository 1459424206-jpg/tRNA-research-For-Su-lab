# tRNA research 四个子项目中英文资料报告

检索日期：2026-05-23（Asia/Shanghai）。

筛选说明：PubMed 文献以 2020-2026 年为时间窗，优先选择 Nature、Science、Cell、Nature Biotechnology、Nature Methods、Molecular Cell、Nucleic Acids Research、Nature Communications 等高影响力期刊；若某主题不足 15 篇，则按题名/摘要相关性补齐。这里的“影响因子最高”采用期刊层级代理分，不等同于 Clarivate 官方 JIF。

Selection note: PubMed records were searched from 2020-2026, prioritizing high-impact journals such as Nature, Science, Cell, Nature Biotechnology, Nature Methods, Molecular Cell, Nucleic Acids Research, and Nature Communications. If fewer than 15 records were available for a topic, relevance-based fallback records were added. Journal impact was approximated by a journal-tier proxy, not official Clarivate JIF values.

## tRNA 的生物功能与结构特征
**English:** Biological functions and structural characteristics of tRNA

### 中文详细阐述
- tRNA 不只是“接头分子”，而是连接遗传密码、翻译速度、细胞应激、免疫防御和疾病治疗的调控节点。
- 结构层面从三叶草二级结构、L 型三级结构、修饰核苷到氨酰化/核糖体复合物共同决定读取精度。
- 近期高影响力研究集中在 suppressor tRNA、tRNA 尾部切割、tRNA 片段和 tRNA 结构互作组。

### Detailed English Explanation
- tRNA functions as more than an adaptor: it links genetic decoding, translation kinetics, stress response, immunity, and therapeutic engineering.
- Its cloverleaf secondary structure, L-shaped tertiary fold, modified nucleosides, and aminoacylation state jointly determine decoding fidelity.
- Recent high-impact work emphasizes suppressor tRNAs, tRNA-tail cleavage, tRNA-derived fragments, and in vivo tRNA structurome/interactome maps.

### 最新高影响力文献 / Recent high-impact literature
1. RNA-triggered Cas12a3 cleaves tRNA tails to execute bacterial immunity. | Nature (2026) | PMID 41501459 | DOI 10.1038/s41586-025-09852-9
2. A virally encoded tRNA neutralizes the PARIS antiviral defence system. | Nature (2024) | PMID 39111359 | DOI 10.1038/s41586-024-07874-3
3. tRNA modifications tune m6A-dependent mRNA decay. | Cell (2025) | PMID 40311619 | DOI 10.1016/j.cell.2025.04.013
4. An engineered UGA suppressor tRNA gene for disease-agnostic AAV delivery. | Nature biotechnology (2026) | PMID 41555020 | DOI 10.1038/s41587-025-02982-5
5. AAV-delivered UGA suppressor tRNA for disease-agnostic in vivo gene therapy. | Nature biotechnology (2026) | PMID 41629463 | DOI 10.1038/s41587-026-02999-4
6. tRNA as an assembly chaperone for a macromolecular transcription-processing complex. | Nature structural & molecular biology (2025) | PMID 40908366 | DOI 10.1038/s41594-025-01653-y
7. Structural basis of tRNA recognition by the m3C RNA methyltransferase METTL6 in complex with SerRS seryl-tRNA synthetase. | Nature structural & molecular biology (2024) | PMID 38918637 | DOI 10.1038/s41594-024-01341-3
8. A methyltransferase-independent role for METTL1 in tRNA aminoacylation and oncogenic transformation. | Molecular cell (2025) | PMID 39892392 | DOI 10.1016/j.molcel.2025.01.003
9. Translational regulation by oxidative desulfuration of tRNA modifications. | Nature communications (2026) | PMID 41807381 | DOI 10.1038/s41467-026-70126-7
10. Structure of fungal tRNA ligase Trl1 with RNA reveals conserved substrate-binding principles. | Nature structural & molecular biology (2025) | PMID 40563009 | DOI 10.1038/s41594-025-01589-3
11. In vivo structure profiling reveals human cytosolic and mitochondrial tRNA structurome and interactome in response to stress. | Nature communications (2025) | PMID 40447571 | DOI 10.1038/s41467-025-59435-5
12. Structural basis of tRNA recognition by the widespread OB fold. | Nature communications (2024) | PMID 39075051 | DOI 10.1038/s41467-024-50730-1
13. Deciphering tRNA repertoires and translation coordination during mouse early embryogenesis by ORACLE-tRNAseq. | Nature communications (2026) | PMID 42062277 | DOI 10.1038/s41467-026-72603-5
14. Mechanistic basis for PYROXD1-mediated protection of the human tRNA ligase complex against oxidative inactivation. | Nature structural & molecular biology (2025) | PMID 40069351 | DOI 10.1038/s41594-025-01516-6
15. AAV-delivered engineered suppressor tRNA rescues visual function in mice with an inherited retinal disease. | Nature communications (2025) | PMID 41407712 | DOI 10.1038/s41467-025-66176-y

### GitHub/数据库资源 / GitHub and database resources
- junchaoshi/sports1.1 | stars=57 | updated=2026-05-20T12:32:20Z | https://github.com/junchaoshi/sports1.1
- UCSC-LoweLab/tDRnamer | stars=2 | updated=2024-10-16T03:49:08Z | https://github.com/UCSC-LoweLab/tDRnamer

### 图像来源 / Figure source
- Source: RNA-triggered Cas12a3 cleaves tRNA tails to execute bacterial immunity.; Nature, 2026; PMID 41501459; PMCID PMC12851939

## tRNA 分析工具与算法
**English:** tRNA analysis tools and algorithms

### 中文详细阐述
- 算法核心难点来自 tRNA 的短序列、多拷贝、强修饰、结构相似性以及测序逆转录停顿/错配。
- 工具链通常包括基因识别、参考库构建、读段比对、修饰信号建模、表达定量和可视化解释。
- tRNAscan-SE、mim-tRNAseq、nanopore direct tRNA sequencing 等代表了从注释到定量修饰的关键路线。

### Detailed English Explanation
- Algorithmic challenges arise from short length, multi-copy genes, heavy modification, structural similarity, and modification-induced RT stops or mismatches.
- A practical toolchain covers gene detection, reference construction, read alignment, modification-signal modeling, abundance quantification, and visualization.
- tRNAscan-SE, mim-tRNAseq, and direct nanopore tRNA sequencing represent major routes from annotation to quantitative modification profiling.

### 最新高影响力文献 / Recent high-impact literature
1. RNA-triggered Cas12a3 cleaves tRNA tails to execute bacterial immunity. | Nature (2026) | PMID 41501459 | DOI 10.1038/s41586-025-09852-9
2. AAV-delivered suppressor tRNA overcomes a nonsense mutation in mice. | Nature (2022) | PMID 35322228 | DOI 10.1038/s41586-022-04533-3
3. Design, construction, and functional characterization of a tRNA neochromosome in yeast. | Cell (2023) | PMID 37944512 | DOI 10.1016/j.cell.2023.10.015
4. Quantitative analysis of tRNA abundance and modifications by nanopore RNA sequencing. | Nature biotechnology (2024) | PMID 37024678 | DOI 10.1038/s41587-023-01743-6
5. Quantifying tRNA abundance by sequencing. | Nature genetics (2023) | PMID 37173525 | DOI 10.1038/s41588-023-01404-z
6. High-resolution quantitative profiling of tRNA abundance and modification status in eukaryotes by mim-tRNAseq. | Molecular cell (2021) | PMID 33581077 | DOI 10.1016/j.molcel.2021.01.028
7. A ligation-independent sequencing method reveals tRNA-derived RNAs with blocked 3' termini. | Molecular cell (2024) | PMID 39096899 | DOI 10.1016/j.molcel.2024.07.008
8. A pro-metastatic tRNA fragment drives Nucleolin oligomerization and stabilization of its bound metabolic mRNAs. | Molecular cell (2022) | PMID 35654044 | DOI 10.1016/j.molcel.2022.05.008
9. Deciphering tRNA repertoires and translation coordination during mouse early embryogenesis by ORACLE-tRNAseq. | Nature communications (2026) | PMID 42062277 | DOI 10.1038/s41467-026-72603-5
10. In vivo structure profiling reveals human cytosolic and mitochondrial tRNA structurome and interactome in response to stress. | Nature communications (2025) | PMID 40447571 | DOI 10.1038/s41467-025-59435-5
11. Genome-wide profiling of tRNA modifications by Induro-tRNAseq reveals coordinated changes. | Nature communications (2025) | PMID 39865096 | DOI 10.1038/s41467-025-56348-1
12. tRNA renovatio: Rebirth through fragmentation. | Molecular cell (2023) | PMID 37802077 | DOI 10.1016/j.molcel.2023.09.016
13. tRNA modification dynamics from individual organisms to metaepitranscriptomics of microbiomes. | Molecular cell (2022) | PMID 35032425 | DOI 10.1016/j.molcel.2021.12.007
14. Nanopore sequencing of intact aminoacylated tRNAs. | Nature communications (2025) | PMID 40835813 | DOI 10.1038/s41467-025-62545-9
15. Quantitative tRNA-sequencing uncovers metazoan tissue-specific tRNA regulation. | Nature communications (2020) | PMID 32796835 | DOI 10.1038/s41467-020-17879-x

### GitHub/数据库资源 / GitHub and database resources
- UCSC-LoweLab/tRNAscan-SE | stars=89 | updated=2026-04-26T23:55:31Z | https://github.com/UCSC-LoweLab/tRNAscan-SE
- nedialkova-lab/mim-tRNAseq | stars=24 | updated=2026-04-29T07:30:44Z | https://github.com/nedialkova-lab/mim-tRNAseq
- merenlab/tRNA-seq-tools | stars=11 | updated=2025-10-06T10:55:16Z | https://github.com/merenlab/tRNA-seq-tools
- rnabioco/tRNA004 | stars=8 | updated=2025-12-02T13:46:48Z | https://github.com/rnabioco/tRNA004
- rnabioinfor/TRAC-Seq | stars=5 | updated=2024-04-29T07:40:55Z | https://github.com/rnabioinfor/TRAC-Seq
- UCSC-LoweLab/tDRnamer | stars=2 | updated=2024-10-16T03:49:08Z | https://github.com/UCSC-LoweLab/tDRnamer

### 图像来源 / Figure source
- Source: Quantitative analysis of tRNA abundance and modifications by nanopore RNA sequencing.; Nature biotechnology, 2024; PMID 37024678; PMCID PMC10791586

## tRNA 修饰指纹数据库
**English:** tRNA mod-fingerprint database

### 中文详细阐述
- tRNA 修饰指纹把“哪一种 tRNA、哪个位点、哪类修饰、在哪个条件下变化”组织为可查询的证据结构。
- 数据库建设需要统一 tRNA 坐标、修饰命名、物种来源、实验技术、置信度和可视化字段。
- MODOMICS、RNAcentral 及测序/质谱分析项目可作为设计本地数据库的外部锚点。

### Detailed English Explanation
- A tRNA modification fingerprint organizes which tRNA, which position, which modification, and which condition into a queryable evidence model.
- Database design requires harmonized tRNA coordinates, modification nomenclature, species metadata, experimental technology, confidence scores, and visualization fields.
- MODOMICS, RNAcentral, and sequencing/mass-spectrometry projects can anchor a local database schema.

### 最新高影响力文献 / Recent high-impact literature
1. tRNA modifications tune m6A-dependent mRNA decay. | Cell (2025) | PMID 40311619 | DOI 10.1016/j.cell.2025.04.013
2. Alanyl-tRNA synthetase, AARS1, is a lactate sensor and lactyltransferase that lactylates p53 and contributes to tumorigenesis. | Cell (2024) | PMID 38653238 | DOI 10.1016/j.cell.2024.04.002
3. A cholesterol-responsive hepatic tRNA-derived small RNA regulates cholesterol homeostasis and atherosclerosis development. | Nature communications (2025) | PMID 41398161 | DOI 10.1038/s41467-025-67387-z
4. Transfer RNA modifications and cellular thermotolerance. | Molecular cell (2024) | PMID 38181765 | DOI 10.1016/j.molcel.2023.11.041
5. NAT10 promotes cancer metastasis by modulating p300/CBP activity through chromatin-associated tRNA. | Molecular cell (2025) | PMID 41344331 | DOI 10.1016/j.molcel.2025.11.010
6. tRNA as an assembly chaperone for a macromolecular transcription-processing complex. | Nature structural & molecular biology (2025) | PMID 40908366 | DOI 10.1038/s41594-025-01653-y
7. A ligation-independent sequencing method reveals tRNA-derived RNAs with blocked 3' termini. | Molecular cell (2024) | PMID 39096899 | DOI 10.1016/j.molcel.2024.07.008
8. Structural basis of tRNA recognition by the m3C RNA methyltransferase METTL6 in complex with SerRS seryl-tRNA synthetase. | Nature structural & molecular biology (2024) | PMID 38918637 | DOI 10.1038/s41594-024-01341-3
9. Structures of the ribosome bound to EF-Tu-isoleucine tRNA elucidate the mechanism of AUG avoidance. | Nature structural & molecular biology (2024) | PMID 38538914 | DOI 10.1038/s41594-024-01236-3
10. tRNA renovatio: Rebirth through fragmentation. | Molecular cell (2023) | PMID 37802077 | DOI 10.1016/j.molcel.2023.09.016
11. Translational regulation by oxidative desulfuration of tRNA modifications. | Nature communications (2026) | PMID 41807381 | DOI 10.1038/s41467-026-70126-7
12. ALKB-1-dependent tRNA methylation is required for efficient paternal mitochondrial elimination. | Nature communications (2026) | PMID 41611679 | DOI 10.1038/s41467-026-68813-6
13. The molecular basis of tRNA selectivity by human pseudouridine synthase 3. | Molecular cell (2024) | PMID 38996458 | DOI 10.1016/j.molcel.2024.06.013
14. Perturbation of METTL1-mediated tRNA N7- methylguanosine modification induces senescence and aging. | Nature communications (2024) | PMID 38977661 | DOI 10.1038/s41467-024-49796-8
15. Coronaviruses reprogram the tRNA epitranscriptome to favor viral protein expression. | Nature communications (2026) | PMID 41714626 | DOI 10.1038/s41467-026-69700-w

### GitHub/数据库资源 / GitHub and database resources
- junchaoshi/sports1.1 | stars=57 | updated=2026-05-20T12:32:20Z | https://github.com/junchaoshi/sports1.1
- nedialkova-lab/mim-tRNAseq | stars=24 | updated=2026-04-29T07:30:44Z | https://github.com/nedialkova-lab/mim-tRNAseq
- rnabioco/tRNA004 | stars=8 | updated=2025-12-02T13:46:48Z | https://github.com/rnabioco/tRNA004
- rnabioinfor/TRAC-Seq | stars=5 | updated=2024-04-29T07:40:55Z | https://github.com/rnabioinfor/TRAC-Seq
- jfallmann/tRNA_ngs_mod_map_call_galaxy | stars=3 | updated=2024-06-09T18:47:45Z | https://github.com/jfallmann/tRNA_ngs_mod_map_call_galaxy
- monimaanam/Modomics_Decoder | stars=1 | updated=2024-06-09T19:02:47Z | https://github.com/monimaanam/Modomics_Decoder
- AteeshaNegi/nanopore-2Read-trna-pipeline | stars=0 | updated=2026-03-10T03:08:29Z | https://github.com/AteeshaNegi/nanopore-2Read-trna-pipeline
- FlorianPichot/tRNA_reference_construction | stars=0 | updated=2020-12-10T09:49:52Z | https://github.com/FlorianPichot/tRNA_reference_construction

### 图像来源 / Figure source
- Source: Translational regulation by oxidative desulfuration of tRNA modifications.; Nature communications, 2026; PMID 41807381; PMCID PMC12976133

## tRNA 相关湿实验
**English:** tRNA-related wet-lab experiments

### 中文详细阐述
- 湿实验围绕样本质量、tRNA 富集、修饰保真、氨酰化状态保护和测序/质谱平台兼容性展开。
- 常见实验包括 Northern blot、氨酰化测定、LC-MS/MS、去修饰/酶处理、small RNA-seq 与 nanopore direct RNA sequencing。
- 关键质控包括 spike-in、去氨酰化对照、酶切效率、RT-stop/mismatch 校准以及 tRNA 片段与成熟 tRNA 的区分。

### Detailed English Explanation
- Wet-lab work depends on sample integrity, tRNA enrichment, modification preservation, aminoacylation protection, and platform compatibility.
- Common assays include Northern blotting, aminoacylation assays, LC-MS/MS, demodification/enzyme treatment, small RNA-seq, and direct nanopore RNA sequencing.
- Key controls include spike-ins, deacylation controls, enzyme-efficiency checks, RT-stop/mismatch calibration, and discrimination between tRNA fragments and mature tRNAs.

### 最新高影响力文献 / Recent high-impact literature
1. RNA-triggered Cas12a3 cleaves tRNA tails to execute bacterial immunity. | Nature (2026) | PMID 41501459 | DOI 10.1038/s41586-025-09852-9
2. AAV-delivered suppressor tRNA overcomes a nonsense mutation in mice. | Nature (2022) | PMID 35322228 | DOI 10.1038/s41586-022-04533-3
3. Design, construction, and functional characterization of a tRNA neochromosome in yeast. | Cell (2023) | PMID 37944512 | DOI 10.1016/j.cell.2023.10.015
4. Quantitative analysis of tRNA abundance and modifications by nanopore RNA sequencing. | Nature biotechnology (2024) | PMID 37024678 | DOI 10.1038/s41587-023-01743-6
5. An engineered UGA suppressor tRNA gene for disease-agnostic AAV delivery. | Nature biotechnology (2026) | PMID 41555020 | DOI 10.1038/s41587-025-02982-5
6. Quantifying tRNA abundance by sequencing. | Nature genetics (2023) | PMID 37173525 | DOI 10.1038/s41588-023-01404-z
7. Translational regulation by oxidative desulfuration of tRNA modifications. | Nature communications (2026) | PMID 41807381 | DOI 10.1038/s41467-026-70126-7
8. RelA-SpoT Homolog toxins pyrophosphorylate the CCA end of tRNA to inhibit protein synthesis. | Molecular cell (2021) | PMID 34174184 | DOI 10.1016/j.molcel.2021.06.005
9. A ligation-independent sequencing method reveals tRNA-derived RNAs with blocked 3' termini. | Molecular cell (2024) | PMID 39096899 | DOI 10.1016/j.molcel.2024.07.008
10. tRNA m1A modification regulate HSC maintenance and self-renewal via mTORC1 signaling. | Nature communications (2024) | PMID 38977676 | DOI 10.1038/s41467-024-50110-9
11. A methyltransferase-independent role for METTL1 in tRNA aminoacylation and oncogenic transformation. | Molecular cell (2025) | PMID 39892392 | DOI 10.1016/j.molcel.2025.01.003
12. Nanopore sequencing of intact aminoacylated tRNAs. | Nature communications (2025) | PMID 40835813 | DOI 10.1038/s41467-025-62545-9
13. tRNA modification dynamics from individual organisms to metaepitranscriptomics of microbiomes. | Molecular cell (2022) | PMID 35032425 | DOI 10.1016/j.molcel.2021.12.007
14. High-resolution quantitative profiling of tRNA abundance and modification status in eukaryotes by mim-tRNAseq. | Molecular cell (2021) | PMID 33581077 | DOI 10.1016/j.molcel.2021.01.028
15. In vivo structure profiling reveals human cytosolic and mitochondrial tRNA structurome and interactome in response to stress. | Nature communications (2025) | PMID 40447571 | DOI 10.1038/s41467-025-59435-5

### GitHub/数据库资源 / GitHub and database resources
- nedialkova-lab/mim-tRNAseq | stars=24 | updated=2026-04-29T07:30:44Z | https://github.com/nedialkova-lab/mim-tRNAseq
- merenlab/tRNA-seq-tools | stars=11 | updated=2025-10-06T10:55:16Z | https://github.com/merenlab/tRNA-seq-tools
- rnabioco/tRNA004 | stars=8 | updated=2025-12-02T13:46:48Z | https://github.com/rnabioco/tRNA004
- rnabioinfor/TRAC-Seq | stars=5 | updated=2024-04-29T07:40:55Z | https://github.com/rnabioinfor/TRAC-Seq
- rnabioco/aa-tRNA-seq | stars=2 | updated=2025-10-08T16:32:14Z | https://github.com/rnabioco/aa-tRNA-seq
- trypchromics/trnaExpCodAdapt | stars=0 | updated=2025-08-11T16:40:47Z | https://github.com/trypchromics/trnaExpCodAdapt

### 图像来源 / Figure source
- Source: Nanopore sequencing of intact aminoacylated tRNAs.; Nature communications, 2025; PMID 40835813; PMCID PMC12368100
