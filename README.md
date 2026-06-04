# tRNA research For Su lab

本仓库用于整理 Su lab tRNA 研究相关材料，覆盖文献检索、论文精读、分析流程、工具调研、实验设想、汇报 PPT、图表资产和阶段性输出。仓库目标是把分散的阅读材料、脚本和报告集中保存，方便后续继续迭代 tRNA 修饰、tRNA-seq/纳米孔测序、胚胎与精子发育、冷冻保存损伤机制等方向。

## 仓库内容

| 路径 | 主要内容 |
| --- | --- |
| `biological functions and structural characteristics of tRNA/` | tRNA 生物学功能、结构特征、早期胚胎相关综述、文献阅读记录和 PPT 输出。 |
| `tRNA mod-fingerprint database/` | tRNA 修饰指纹库方向的文献、数据库、工具仓库调研、分析输出和汇报材料。 |
| `tRNA analysis tools and algorithms/` | tRNA 分析工具、算法、测序策略和软件流程调研材料。 |
| `tRNA-related wet-lab experiments/` | tRNA 相关湿实验方向的文献、实验设计线索、报告、图表和汇报材料。 |
| `tRNA_embryo_sperm_cryo_literature_20260604/` | 胚胎、精子、冷冻保存和 tRNA 修饰相关的文献地图、阅读笔记和项目设想。 |
| `analysis_induro_modification_fingerprints_20260602/` | Induro/MIM tRNA-seq 修饰指纹对比、文献精读、分析图表和汇报输出。 |
| `new study/` | 新研究方向的阶段性整理材料。 |
| `scripts/` | 本地分析、绘图、文献整理、PPT/报告生成和上传辅助脚本。 |
| `output/`, `outputs/` | 已生成的报告、PPT 预览、图表资产、中间结果和质量检查记录。 |
| 根目录文件 | 综合汇报 PPT、结构示意图、文献精读 PDF 和材料生成脚本。 |

## 推荐阅读顺序

1. 先阅读根目录综合汇报和本 README，快速了解材料边界。
2. 如果关注研究问题和项目构思，优先看 `tRNA_embryo_sperm_cryo_literature_20260604/`、`new study/` 和各目录下的 `bilingual_topic_report.md`、`README.md`。
3. 如果关注方法学和数据分析，优先看 `tRNA analysis tools and algorithms/`、`tRNA mod-fingerprint database/` 和 `scripts/`。
4. 如果关注已有汇报结果，优先看各目录中的 `.pptx`、`qa_report.md`、`asset_manifest.md` 和 `output/` 文件夹。

## 材料类型

仓库中主要包含以下类型文件：

- 文献与网页资料：PDF、HTML、下载清单、文献表格和阅读笔记。
- 分析与整理结果：Markdown 报告、CSV/TSV 表格、JSON 索引、图表资产和 QA 记录。
- 汇报材料：PPTX、PDF 预览和结构示意图。
- 脚本与流程：Python、R、Shell/PowerShell 脚本和少量第三方工具仓库快照。

## 本地环境说明

本仓库不上传本地虚拟环境和依赖目录。`.gitignore` 已排除：

- `.venv/`
- `.venv_paper2ppt/`
- `node_modules/`
- Python 缓存、Office 临时锁文件、日志文件和本地环境变量文件

如需重新运行脚本，请根据对应脚本导入的包自行创建 Python/R 环境。大型 PPT、PDF 和图表文件已经作为阶段性结果保存在仓库中。

## 上传与维护建议

- 当前仓库包含较多二进制材料，首次上传采用分批提交，避免单次 Git pack 过大导致网络中断。
- 后续新增大文件时，建议按主题目录分批提交和推送。
- 若单个文件接近或超过 GitHub 100 MB 限制，建议改用 Git LFS、数据仓库或云盘保存原始文件，并在仓库中保留索引与说明。
- 若只更新文字说明、脚本或表格，建议单独提交，方便追踪修改历史。

完整复刻与上传流程见 [`docs/reproduce_workflow.md`](docs/reproduce_workflow.md)。

## 版权与使用提醒

仓库内包含下载的论文 PDF、网页 HTML、第三方工具仓库快照和示例数据。若本仓库保持公开状态，请在继续扩展或分享前确认相关材料的版权、开放获取许可和第三方代码许可证。对于不适合公开分发的原文 PDF 或数据文件，建议改为保留引用信息、下载链接和阅读笔记。
