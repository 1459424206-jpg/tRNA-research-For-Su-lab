# mim-tRNAseq 指纹库整理

这个文件夹汇总了我从 `mim-tRNAseq` 官方源码中整理出的指纹库相关内容，方便后续阅读、引用和继续加工。

## 建议先看

1. `mim_tRNAseq_fingerprint_report_cn.md`
2. `mim_tRNAseq_fingerprint_biological_functions_cn.md`
3. `mim_tRNAseq_detectable_fingerprint_set.xlsx`
4. `mim_tRNAseq_modifications_full.xlsx`

## 这里包含什么

- `mim_tRNAseq_fingerprint_report_cn.md`
  - 源码层面的“指纹库”拆解，说明完整修饰字典、可识别集合、人工补充位点库、canonical 热点先验库分别是什么。
- `mim_tRNAseq_fingerprint_biological_functions_cn.md`
  - 对 `m1A、m1G、m2,2G、m3C、m1I、yW、o2yW、OHyW、acp3U、ms2i6A、ms2t6A、I` 的中文名、常见位点、主要结合/作用界面、生物学功能逐项解释。
- `mim_tRNAseq_modifications_full.xlsx`
  - 完整修饰字典。
- `mim_tRNAseq_modifications_full_ascii_safe.xlsx`
  - 完整修饰字典的安全版，额外提供 `U+XXXX` 编码。
- `mim_tRNAseq_detectable_fingerprint_set.xlsx`
  - 真正被源码当作可识别指纹的核心集合。
- `mim_tRNAseq_detectable_fingerprint_set_ascii_safe.xlsx`
  - 核心集合的安全版。
- `mim_tRNAseq_additional_manual_mods.xlsx`
  - 人工补充位点库。
- `mim_tRNAseq_canonical_site_priors.xlsx`
  - canonical 热点先验库。

## 关键结论

- `mim-tRNAseq` 不是把完整 `MODOMICS` 字典中的所有修饰都直接当成“可检测指纹”。
- 真正参与指纹判读的是一个更小的核心集合，重点集中在：
  - `m1A`
  - `m1G`
  - `m2,2G`
  - `m3C`
  - `m1I`
  - `yW / OHyW / o2yW`
  - `acp3U`
  - `ms2i6A`
  - `ms2t6A`
  - `I34`
- 这些修饰大多集中在 `34` 位和 `37` 位附近，核心作用是：
  - 扩展 wobble 解码范围
  - 稳定反密码环
  - 抑制移码
  - 维持 tRNA 正确折叠和三级结构稳定
