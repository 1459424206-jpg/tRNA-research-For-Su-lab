# -*- coding: utf-8 -*-
from pathlib import Path
import zipfile
import textwrap

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor


BASE = Path(r"D:\Project\tRNA research\tRNA mod-fingerprint database\downloaded_resources")
FIG = BASE / "figures"
FIG_ALL = BASE / "figures_all"
OUT = BASE / "analysis_outputs" / "paper2ppt_output" / "fingerprint_strategy_deck"
ASSETS = OUT / "assets"
OUT.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

PPTX = OUT / "tRNA_modification_fingerprint_database_strategy_deck.pptx"
QA = OUT / "qa_report.md"
MANIFEST = OUT / "asset_manifest.md"


def font(size, bold=False):
    candidates = [
        "msyhbd.ttc" if bold else "msyh.ttc",
        "simhei.ttf",
        "arial.ttf",
    ]
    for f in candidates:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()


F_TITLE = font(34, True)
F_HEAD = font(26, True)
F_TEXT = font(22)
F_SMALL = font(17)


def wrap_text(text, width=32):
    lines = []
    for seg in str(text).split("\n"):
        if len(seg) <= width:
            lines.append(seg)
        else:
            lines.extend(textwrap.wrap(seg, width=width, break_long_words=True, replace_whitespace=False))
    return lines


def make_flow(path, title, steps, footer=None):
    w, h = 1600, 900
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline="black", width=3)
    d.text((55, 35), title, fill="black", font=F_TITLE)
    top = 150
    box_h = 92
    gap = 35
    x = 110
    bw = w - 220
    for i, step in enumerate(steps):
        y = top + i * (box_h + gap)
        d.rounded_rectangle([x, y, x + bw, y + box_h], radius=8, outline="black", width=3, fill="white")
        yy = y + 15
        for line in wrap_text(step, 48)[:2]:
            d.text((x + 28, yy), line, fill="black", font=F_TEXT)
            yy += 30
        if i < len(steps) - 1:
            cx = w // 2
            d.line([cx, y + box_h + 6, cx, y + box_h + gap - 14], fill="black", width=4)
            d.polygon([(cx - 10, y + box_h + gap - 14), (cx + 10, y + box_h + gap - 14), (cx, y + box_h + gap + 1)], fill="black")
    if footer:
        d.text((55, h - 62), footer, fill="black", font=F_SMALL)
    img.save(path, quality=95)
    return path


def make_matrix(path, title, headers, rows, foot=None, col_widths=None):
    w, h = 1800, 1000
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline="black", width=3)
    d.text((45, 32), title, fill="black", font=F_TITLE)
    x0, y0 = 45, 120
    table_w = w - 90
    if col_widths is None:
        col_widths = [table_w // len(headers)] * len(headers)
    else:
        total = sum(col_widths)
        col_widths = [int(table_w * c / total) for c in col_widths]
    row_h = int((h - y0 - 95) / (len(rows) + 1))
    xs = [x0]
    for cw in col_widths:
        xs.append(xs[-1] + cw)
    # header
    for j, head in enumerate(headers):
        d.rectangle([xs[j], y0, xs[j + 1], y0 + row_h], outline="black", width=2, fill="white")
        d.text((xs[j] + 12, y0 + 16), head, fill="black", font=F_HEAD)
    # rows
    for i, row in enumerate(rows):
        y = y0 + (i + 1) * row_h
        for j, cell in enumerate(row):
            d.rectangle([xs[j], y, xs[j + 1], y + row_h], outline="black", width=2, fill="white")
            yy = y + 10
            width_chars = max(10, int(col_widths[j] / 24))
            for line in wrap_text(cell, width_chars)[:4]:
                d.text((xs[j] + 10, yy), line, fill="black", font=F_SMALL if len(row) > 7 else F_TEXT)
                yy += 23
    if foot:
        d.text((45, h - 55), foot, fill="black", font=F_SMALL)
    img.save(path, quality=95)
    return path


def make_map(path, title):
    w, h = 1600, 900
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline="black", width=3)
    d.text((55, 35), title, fill="black", font=F_TITLE)
    # simplified cloverleaf
    cx, cy = 660, 470
    d.line([cx, cy, cx, 220], fill="black", width=5)
    d.line([cx, cy, cx, 725], fill="black", width=5)
    d.arc([cx - 210, cy - 160, cx - 40, cy + 10], 90, 360, fill="black", width=5)
    d.arc([cx + 40, cy - 160, cx + 210, cy + 10], 180, 450, fill="black", width=5)
    d.arc([cx - 125, cy + 40, cx + 125, cy + 290], 180, 360, fill="black", width=5)
    labels = [
        ("D-loop", cx - 330, cy - 95, "D, m1A, m2G"),
        ("Anticodon loop", cx - 210, cy + 250, "U34: mcm5s2U/Q/I/k2C\n37: t6A/i6A/yW/ms2i6A"),
        ("Variable arm", cx + 190, cy + 35, "m3C32识别相关\n结构选择"),
        ("T-loop", cx + 230, cy - 95, "T/m5U, Ψ, m1A"),
        ("Acceptor stem/3' CCA", cx + 40, cy - 275, "氨酰化与CCA完整性"),
    ]
    for name, x, y, detail in labels:
        d.rectangle([x, y, x + 330, y + 105], outline="black", width=2, fill="white")
        d.text((x + 12, y + 8), name, fill="black", font=F_HEAD)
        yy = y + 45
        for line in detail.split("\n"):
            d.text((x + 12, yy), line, fill="black", font=F_SMALL)
            yy += 23
    d.text((55, h - 70), "位置比修饰名更重要：同一化学类型在不同环区会产生完全不同的检测和功能指纹。", fill="black", font=F_TEXT)
    img.save(path, quality=95)
    return path


def make_title_visual(path):
    return make_flow(
        path,
        "tRNA 修饰指纹库：从化学修饰到可计算证据",
        [
            "修饰全景：>170 RNA 修饰；tRNA 子集约 >100，实验可稳定识别的更少",
            "检测指纹：LC-MS/MS、RT/mismatch、chemical cleavage、Nanopore error/termination",
            "功能指纹：氨酰化、codon decoding、ribosome stalling、RNA stability、stress phenotype",
            "数据库目标：把修饰-位点-方法-信号-表型-来源连成证据图谱",
        ],
        "白底黑字版：每页一张图，图文严格对应。",
    )


VISUALS = {
    "title": make_title_visual(ASSETS / "00_title_architecture.png"),
    "mod_count": make_matrix(
        ASSETS / "01_modification_count_landscape.png",
        "tRNA 修饰全景：总数、子集和可识别指纹不要混在一起",
        ["层级", "数量/范围", "对指纹库的含义"],
        [
            ["RNA 修饰总库", "MODOMICS 2023 update：所有 RNA 类别 >170 种修饰", "作为全量字典和命名体系，不等于每种都在 tRNA 中高置信出现。"],
            ["tRNA 修饰子集", "文献常用表述：tRNA 有 >100 种修饰；单条 tRNA 通常有多个修饰位点", "需要按物种、细胞器、tRNA family 和位点拆分。"],
            ["实验可识别集合", "tRNA004 benchmark：43 种修饰；mim-tRNAseq/TRAC-seq 各有适用范围", "数据库必须记录 method-specific detectability，而不是只存“有/无”。"],
            ["优先版目标", "先覆盖 m7G、m1A、m3C、Ψ、I/Q、mcm5U/mcm5s2U、mcm5h2U、ac4C、k2C、t6A/i6A/yW", "覆盖关键位点、检测差异和表型证据，随后从 MODOMICS 扩展。"],
        ],
    ),
    "families": make_matrix(
        ASSETS / "02_modification_families.png",
        "修饰家族：每种修饰的“样子”先按化学类型编码",
        ["家族", "代表修饰", "结构/化学特征", "常见指纹"],
        [
            ["甲基化", "m1A, m1G, m3C, m5C, m7G, Gm/Cm/Um", "碱基或核糖加甲基；可能影响配对、RT、稳定性", "RT mismatch/stop、TRAC cleavage、MS mass shift"],
            ["异构/还原", "Ψ, D", "U 的异构化或还原，改变氢键和柔性", "结构稳定、RT/化学选择性弱，常需特异方法或MS"],
            ["硫化/氧化转换", "s2U, mcm5s2U, τm5s2U, mcm5h2U", "U34 硫代基增强解码；氧化可脱硫", "氨酰化/解码下降、Nanopore error、MS片段"],
            ["超修饰 wobble", "Q, k2C/lysidine, I, mcm5U/ncm5U", "反密码子第一位的碱基替换或复杂侧链", "codon specificity、AUG avoidance、病毒 codon pressure"],
            ["A37 hypermods", "t6A, i6A, ms2i6A, yW", "反密码子邻位大体积修饰，稳定 reading frame", "结构识别、frameshift/翻译精度表型"],
            ["乙酰化", "ac4C", "胞苷 N4 乙酰化；NAT10 相关", "RNA稳定/染色质相关tRNA/转录调控表型"],
        ],
        col_widths=[1.2, 1.8, 2.4, 2.5],
    ),
    "position": make_map(ASSETS / "03_position_map.png", "tRNA 修饰位点：位置决定检测和表型"),
    "fingerprint": make_matrix(
        ASSETS / "04_fingerprint_signal_layers.png",
        "“修饰指纹”不是一个信号，而是四层证据的组合",
        ["证据层", "可观测信号", "优点", "风险"],
        [
            ["化学层", "LC-MS/MS、MLC-seq、核苷/片段质量", "化学特异性最高", "普通核苷MS丢失位点信息"],
            ["测序层", "RT stop、mismatch、cleavage score、read-through", "可定位到tRNA/位点", "受RT酶、预处理、结构和mapping影响"],
            ["纳米孔层", "basecalling error、indel、current shift、termination", "理论上保留原分子和单读段信息", "受chemistry、basecaller、上下文、coverage影响"],
            ["功能层", "氨酰化、ribosome occupancy、TE、表型", "解释为什么修饰重要", "因果链长，需要扰动/救援证据"],
        ],
        col_widths=[1.3, 2.4, 2.0, 2.5],
    ),
    "detectability": make_matrix(
        ASSETS / "05_detectability_readthrough.png",
        "识别率 / 通读率差异：本质是修饰如何扰动酶或孔道",
        ["因素", "导致什么差异", "数据库字段"],
        [
            ["修饰化学体积与配对能力", "m1A/m1G/m3C 等可阻碍 Watson-Crick 配对，造成 RT stop/mismatch；Ψ/D 可能更隐蔽", "modification_class, expected_RT_effect"],
            ["位点与上下文", "U34/A37/C32/G46 的结构环境不同；同一修饰在不同 tRNA context 下信号不同", "position, local_context, structural_region"],
            ["预处理", "AlkB、DM、NaBH4/aniline、PANDORA-seq 会改变通读率或切割率", "pretreatment, cleavage_score, readthrough_rate"],
            ["测序平台", "Illumina 读 RT 产物；Nanopore 读原分子，RNA004 与 RNA002 的错误谱不同", "platform, chemistry, basecaller_model"],
            ["参考与多重比对", "tRNA 多拷贝和等解码 tRNA 使 reads 归属困难", "reference_version, multi_mapping_policy"],
        ],
        col_widths=[1.5, 3.2, 2.0],
    ),
    "selection": make_matrix(
        ASSETS / "06_selected_evidence_map.png",
        "本次PPT筛选标准：能贡献“数据库字段”的文献和工具优先",
        ["保留对象", "贡献", "数据库问题"],
        [
            ["METTL1/TRAC-seq", "m7G46 定位、tRNA abundance、衰老表型", "怎么记录 cleavage score 与表型链？"],
            ["mcm5s2U/m6A 与氧化脱硫", "U34 解码、通读、翻译效率", "同一位点的动态化学转换如何建模？"],
            ["Nanopore/tRNA004/2-Read", "43修饰 benchmark、error/termination", "如何存 method-specific detection profile？"],
            ["mim-tRNAseq / SPORTS / MODOMICS", "RT错配、tsRNA捕获、修饰字典", "如何从工具输出进入统一 schema？"],
            ["结构机制文献", "METTL6、PUS3、lysidine、vRNAP", "修饰为什么产生特异表型？"],
        ],
        col_widths=[1.7, 3.0, 2.6],
    ),
    "schema": make_flow(
        ASSETS / "99_database_schema.png",
        "指纹库最小可行 schema",
        [
            "Reference layer：species / tRNA gene / anticodon / mature CCA / structure position",
            "Modification layer：MODOMICS symbol / short name / chemical family / writer-eraser",
            "Evidence layer：method / pretreatment / signal / coverage / threshold / source figure",
            "Function layer：decoding / aminoacylation / stability / stress / disease phenotype",
            "Query layer：按修饰、位点、方法、表型、工具输出追踪证据",
        ],
        "关键原则：同一修饰可以有多个方法指纹；同一方法对不同修饰的识别率不同。",
    ),
}


TOOL_VISUALS = {
    "modomics": make_flow(
        ASSETS / "tool_modomics_decoder.png",
        "MODOMICS_Decoder：把修饰符号变成数据库字段",
        ["MODOMICS unicode sequence", "symbol → short name dictionary", "position enumeration", "position-symbol-modification table", "join species / tRNA / evidence source"],
    ),
    "reference": make_flow(
        ASSETS / "tool_reference_construction.png",
        "tRNA reference construction：解决归属和版本问题",
        ["genomic tRNA predictions", "remove duplicates / merge references", "mature CCA and genomic coordinates", "validate by reads mapping", "store reference_version"],
    ),
    "sports": make_flow(
        ASSETS / "tool_sports.png",
        "SPORTS1.1：从小RNA数据中识别 tsRNA/tRF",
        ["small RNA / PANDORA-seq reads", "adapter + length filtering", "Bowtie mapping to tRNA/rRNA/miRNA/genome", "fragment class: 5 end / 3 end / internal", "reads/RPM + mismatch summary"],
    ),
    "mim": make_flow(
        ASSETS / "tool_mimseq.png",
        "mim-tRNAseq：RT错配型修饰指纹",
        ["trimmed tRNA-seq reads", "tRNA clustering + modification index", "SNP-tolerant GSNAP alignment", "deconvolution to transcript-level tRNAs", "coverage / expression / mismatch / SLAC"],
    ),
    "trac": make_flow(
        ASSETS / "tool_tracseq.png",
        "TRAC-Seq：m7G46 的化学切割型指纹",
        ["AlkB/D135S 去除RT阻碍", "NaBH4 还原 m7G", "aniline cleavage", "small RNA sequencing", "cleavage score / m7G abundance"],
    ),
    "trna004": make_flow(
        ASSETS / "tool_trna004.png",
        "tRNA004：Nanopore RNA004 修饰 benchmark",
        ["direct RNA nanopore tRNA reads", "RNA002 vs RNA004 chemistry", "known MODOMICS sites as truth anchors", "basecalling error mapped to structure", "43 modifications × contexts error profiles"],
    ),
    "tworead": make_flow(
        ASSETS / "tool_2read.png",
        "Nanopore 2-Read：termination/read-through 指纹",
        ["ONT direct RNA", "Dorado basecalling + BWA-MEM", "per-read mismatch/indel", "5'/3' termination and read-through", "per-site candidate modification confidence"],
    ),
    "galaxy": make_flow(
        ASSETS / "tool_galaxy.png",
        "Galaxy tRNAmod workflow：传统NGS错配证据整理",
        ["add CCA / cluster tRNA references", "preprocess reads", "multimapper phasing by same mismatch pattern", "GATK / samtools / Picard wrappers", "SAM/BAM/VCF-like evidence"],
    ),
}


def img(name):
    return name


SLIDES = [
    ("tRNA 修饰指纹库：重做后的汇报主线", "目标：围绕修饰种类、检测指纹、通读/识别差异、表型和工具输出构建数据库方案。", VISUALS["title"],
     ["这版不是逐资料摘要，而是把文献和GitHub工具合并成一个数据库设计故事。", "每页一张图：原始论文图、工具流程图或数据库结构图。", "核心问题：什么修饰、在哪里、怎么被识别、识别率为何不同、有什么表型。"]),
    ("修饰数量：全量字典、tRNA子集、实验可识别集合必须分开", "MODOMICS/NAR 2023 update；tRNA review；tRNA004 README/manuscript description。", VISUALS["mod_count"],
     ["全量 RNA 修饰 >170；tRNA 子集通常表述为 >100 种。", "实验可稳定识别的数量远小于理论总数，且强烈依赖方法。", "指纹库应从 MODOMICS 导入全量字典，再用 evidence layer 标注可检测性。"]),
    ("修饰家族：数据库先按化学类型组织“每种修饰是什么样”", "用于替代在PPT中硬塞 >100 个修饰名；全量清单留给数据库导入。", VISUALS["families"],
     ["同一类修饰常产生类似检测问题，例如甲基化导致 RT mismatch/stop。", "U34 wobble 和 A37 hypermodifications 对翻译影响最大。", "数据库字段应包括 chemical_family、base、position、expected_signal。"]),
    ("位点决定表型：U34、A37、C32、G46 是第一版重点", "tRNA cloverleaf 结构位置图。", VISUALS["position"],
     ["U34 常决定 codon recognition 和读码效率。", "A37 常稳定 reading frame；C32/G46 更多连接结构识别和tRNA稳定。", "同一修饰换位置，检测指纹和功能解释都会改变。"]),
    ("什么叫修饰指纹：化学、测序、纳米孔和功能四层证据", "数据库概念图。", VISUALS["fingerprint"],
     ["一条记录不是“有m7G”，而是“某方法在某位点观察到某信号”。", "同一位点可同时有MS、TRAC、mim-seq、Ribo-seq和表型证据。", "证据等级需要和实验方法绑定。"]),
    ("识别率/通读率为何不同：修饰在扰动RT酶、孔道和比对", "方法差异解释图。", VISUALS["detectability"],
     ["通读率低不一定代表修饰多；也可能是结构、RT酶、预处理或参考造成。", "Nanopore 的错误谱不是Illumina错配谱的简单替代。", "每个工具输出都要记录参数、阈值、coverage和reference版本。"]),
    ("筛选标准：能贡献数据库字段的文献和工具优先", "证据地图。", VISUALS["selection"],
     ["保留：能解释修饰、方法信号、功能表型或工具输出的材料。", "弱相关：只讲普通tRNA生物学、与修饰指纹无直接关系的材料降级。", "新增/强化：MODOMICS、tRNA004/Nanopore、mim-tRNAseq、m7G/TRAC、U34动态转换。"]),

    ("文献精读｜METTL1/m7G46：假说是m7G-tRNA下降会导致翻译衰老", "PMID 38977661 | Fig.4 TRAC-seq 定位 m7G-tRNAs", FIG_ALL / "38977661_41467_2024_49796_Fig4_HTML.jpg",
     ["逻辑：衰老中METTL1-WDR4下降，推测tRNA m7G46减少影响翻译。", "方法：TRAC-seq 用 NaBH4/aniline 产生m7G位点切割，计算 cleavage score。", "结果：定义一组m7G-tRNAs，并在METTL1 KO/衰老中下降。", "讨论：m7G46 应作为第一版数据库的标准化化学切割指纹。"]),
    ("文献精读｜METTL1/m7G46：结果是核糖体停顿与SASP衰老表型", "PMID 38977661 | Fig.5 Ribo-seq uncover ribosome stalling", FIG_ALL / "38977661_41467_2024_49796_Fig5_HTML.jpg",
     ["方法步骤：puromycin、polysome、Ribo-seq、RNC-qPCR验证翻译效率。", "结果：m7G-tRNA解码的codon上A-site ribosome occupancy升高。", "表型：WNT等通路翻译下降，ISR/RSR/SASP被激活。", "数据库字段：codon_occupancy、translation_efficiency、RTD、senescence phenotype。"]),
    ("文献精读｜m6A与mcm5s2U：假说是mRNA和tRNA表观转录组相互读码", "PMID 40311619 | Fig.4 mcm5s2U facilitates decoding of m6A codons", FIG_ALL / "40311619_nihms-2074120-f0005.jpg",
     ["逻辑：m6A在CDS中会让相应codon变成低效翻译位点。", "假说：tRNA anticodon loop 的 mcm5s2U 可抵消m6A codon带来的解码障碍。", "方法：translation/decay assays、ribosome profiling、tRNA pathway扰动。", "意义：指纹库要能连接mRNA修饰、tRNA修饰和codon-specific translation。"]),
    ("文献精读｜m6A与mcm5s2U：结果是修饰状态改变mRNA decay和肿瘤通路", "PMID 40311619 | Fig.6 mRNA and tRNA modifications affect ribosomal decoding", FIG_ALL / "40311619_nihms-2074120-f0007.jpg",
     ["结果：mcm5s2U水平改变会改变m6A修饰codon的翻译和mRNA稳定性。", "表型：癌症中m6A和mcm5s2U通路失衡与更强侵袭性相关。", "讨论：U34修饰是“解码补偿指纹”，不只是tRNA自身属性。", "数据库字段：mRNA_mod_context、decoded_codon、tRNA_U34_state、decay_effect。"]),
    ("文献精读｜氧化脱硫：假说是氧化应激把U34修饰转成另一种指纹", "PMID 41807381 | Fig.1 xm5s2U → xm5h2U", FIG / "PMC12976133_41467_2026_70126_Fig1_HTML.jpg",
     ["逻辑：xm5s2U34 是解码purine-ending codons的重要wobble修饰。", "假说：氧化条件使xm5s2U脱硫为xm5h2U，形成可逆/动态翻译调控。", "方法：LC-MS/CID 验证脱硫产物，spike-in排除处理伪影。", "数据库字段：precursor_mod、converted_mod、redox_state、MS_fragment。"]),
    ("文献精读｜氧化脱硫：结果是氨酰化和A-site识别下降", "PMID 41807381 | Fig.2 spike-in 控制；Fig.4-7 为功能验证", FIG / "PMC12976133_41467_2026_70126_Fig2_HTML.jpg",
     ["方法步骤：spike-in tracer tRNA、体外翻译、氨酰化、A-site binding、cryo-EM。", "结果：mcm5h2U降低tRNALys/Gln/Glu氨酰化，并削弱AAA/AAG识别。", "讨论：同一U34位点可能随氧化应激在“高效解码”和“低效解码”状态间切换。", "数据库字段：readthrough/recognition_rate、aminoacylation_effect、stress_condition。"]),
    ("文献精读｜冠状病毒：假说是病毒codon usage利用宿主tRNA修饰", "PMID 41714626 | Fig.1 RSCU and modification pathways", FIG / "PMC13031925_41467_2026_69700_Fig1_HTML.jpg",
     ["逻辑：冠状病毒富含A/U-ending suboptimal codons。", "假说：感染重编程I、Q、mcm5U/mcm5s2U、m5C/f5C来提高病毒蛋白翻译。", "方法：RSCU、LC-MS/MS、mim-tRNAseq、酶敲低/过表达。", "数据库字段：condition=virus、codon_usage_pressure、required_modification。"]),
    ("文献精读｜冠状病毒：结果是感染触发tRNA epitranscriptome重塑", "PMID 41714626 | Fig.3 LC-MS/MS modification landscape", FIG / "PMC13031925_41467_2026_69700_Fig3_HTML.jpg",
     ["结果：SARS-CoV-2和HCoV-OC43感染改变anticodon loop修饰。", "功能测试：ELP3/QTRT1/NSUN2等通路扰动会影响病毒NP蛋白表达。", "讨论：病毒不是只“消耗”tRNA，而是改写宿主修饰景观。", "数据库字段：enzyme_expression、infection_time、mod_fold_change、viral_translation_output。"]),
    ("文献精读｜tRNA004/Nanopore：问题是43种修饰在孔道中有不同错误指纹", "GitHub rnabioco/tRNA004 | README + Rmd analysis", TOOL_VISUALS["trna004"],
     ["逻辑：已知tRNA修饰位点可作为天然benchmark。", "方法：RNA002/RNA004直接RNA测序，basecalling error映射到MODOMICS位点和结构坐标。", "结果目标：比较43种修饰在不同上下文下的错误谱、yield和basecalling accuracy。", "数据库字段：platform、chemistry、basecaller、error_profile、context_coverage。"]),
    ("文献精读｜PUS3/Ψ38-39：结构选择性解释为什么同类修饰不等价", "PMID 38996458 | Figure 2/3 PUS3-tRNA structure", FIG_ALL / "38996458_gr2.jpg",
     ["逻辑：Ψ广泛存在，但PUS3只修饰特定tRNA 38/39位点。", "方法：apo和tRNA-bound PUS3 cryo-EM，突变验证，Pseudo-seq定位。", "结果：PUS3二聚体定位tRNA并把目标U放到活性位点。", "讨论：数据库不能只记录“Ψ”，还要记录writer、target position和selectivity evidence。"]),
    ("文献精读｜METTL6/m3C32：SerRS决定底物选择，A37和variable arm也重要", "PMID 38918637 | Fig.1 METTL6-SerRS-tRNA complex", FIG / "PMC11479938_41594_2024_1341_Fig1_HTML.jpg",
     ["逻辑：m3C32影响翻译精度，但METTL6如何选择tRNASer不清楚。", "方法：cryo-EM、体外甲基化、mutagenesis、MS。", "结果：SerRS是底物选择因子；C32 flip-out进入METTL6活性中心。", "数据库字段：writer、cofactor/substrate_selector、structure_state、associated_A37_mod。"]),
    ("文献精读｜lysidine/k2C34：一个wobble修饰决定AUA而避开AUG", "PMID 38538914 | Fig.2 role of lysidine 34", FIG_ALL / "38538914_nihms-2030058-f0002.jpg",
     ["逻辑：tRNAIle CAU 需要识别AUA但避开AUG。", "假说：C34的lysidine改变碱基几何，排斥AUG。", "方法：70S ribosome + EF-Tu + Ile-tRNA cryo-EM。", "结果：L34在第三位形成特殊几何，削弱AUG ternary complex稳定性。", "数据库字段：codon_specificity、avoidance_codon、structural_decoding_evidence。"]),
    ("文献精读｜tsRNA-Glu-CTC：修饰型tsRNA的表型强于未修饰合成体", "PMID 41398161 | Fig.9 endogenous modified tsRNA", FIG_ALL / "41398161_41467_2025_67387_Fig9_HTML.jpg",
     ["逻辑：tsRNA不仅是降解片段，可能是带修饰的功能分子。", "方法：PANDORA-seq识别tsRNA，MLC-seq解析内源tsRNA修饰。", "结果：修饰型tsRNA-Glu-CTC更强地影响胆固醇和肝脂质。", "数据库字段：fragment_start/end、source_tRNA、modification_pattern、lipid phenotype。"]),
    ("文献精读｜ALKB-1/m1A：eraser失活会改变翻译和线粒体表型", "PMID 41611679 | Fig.2 tRNA m1A and proteostasis", FIG_ALL / "41611679_41467_2026_68813_Fig2_HTML.jpg",
     ["逻辑：tRNA methylation 是否影响 paternal mitochondrial elimination 未知。", "方法：ALKB-1 D247A/RNAi、LC-MS、m1A-seq、RNC-seq、proteomics。", "结果：tRNA m1A升高，线粒体蛋白稳态和ROS通路改变。", "数据库字段：eraser_state、m1A_level、translation_imbalance、PME phenotype。"]),
    ("文献精读｜vRNAP-associated tRNA：缺失修饰也可能是功能指纹", "PMID 40908366 | Fig.6 modification impact for vRNAP formation", FIG_ALL / "40908366_41594_2025_1653_Fig6_HTML.jpg",
     ["逻辑：poxvirus vRNAP装配需要特定tRNAGln/Arg作为assembly chaperone。", "方法：重构装配、gel shift、LC-MS/MS、cryo-EM。", "结果：特定tRNA修饰图案和缺失mcm5s2U34参与选择。", "讨论：数据库应允许记录absence_of_modification和non-translational_function。"]),
    ("文献精读｜NAT10/ac4C chromatin-associated tRNA：修饰影响染色质与转移", "PMID 41344331 | Fig.2 NAT10 modifies RNAs and metastasis complex", FIG_ALL / "41344331_nihms-2122374-f0003.jpg",
     ["逻辑：NAT10是ac4C writer，但其促转移机制不清楚。", "方法：NAT10扰动、RNA ac4C、chromatin-associated tRNA、p300/CBP功能分析。", "结果：染色质相关tRNA ac4C变化扰动p300/CBP和enhancer组织。", "数据库字段：subcellular_context、chromatin_associated_tRNA、ac4C、metastasis phenotype。"]),
    ("文献精读｜LIDAR：捕获被3'端修饰阻断的tRNA-derived RNAs", "PMID 39096899 | Method logic reconstructed from abstract and local metadata", make_flow(ASSETS / "paper_lidar.png", "LIDAR：ligation-independent detection of blocked-end tDRs", ["quasi-random priming", "template switching", "capture RNAs regardless of 3' blocking modifications", "detect more tRNA-derived RNAs than ligation-dependent methods", "store terminal chemistry / capture bias"], "没有可用本地图；用方法流程图表示。"),
     ["逻辑：传统ligation-dependent small RNA-seq会漏掉3'端被修饰/阻断的RNA。", "方法：quasi-random priming + template switching，避免3' ligation依赖。", "结果：发现更多tDRs，包括3' blocked species。", "数据库字段：terminal_state、library_method、capture_bias、tDR class。"]),

    ("工具精读｜MODOMICS_Decoder：修饰字典导入，不是caller", "GitHub monimaanam/Modomics_Decoder", TOOL_VISUALS["modomics"],
     ["输入：MODOMICS unicode sequence。", "输出：position、symbol、short names，例如7=m7G、?=m5C、Ѣ=m1A。", "用途：把“每种修饰是什么样”标准化为数据库字段。", "局限：不提供实验识别率或表型，需要和证据层join。"]),
    ("工具精读｜tRNA reference construction：先解决参考坐标", "GitHub FlorianPichot/tRNA_reference_construction", TOOL_VISUALS["reference"],
     ["目标：从genomic tRNA predictions构建非重复、合并、优化参考。", "方法：R脚本构建，Unix脚本用reads验证。", "数据库意义：所有修饰位点必须锚定reference_version。", "风险：路径硬编码，需要工程化重写。"]),
    ("工具精读｜SPORTS1.1：tsRNA/tRF层面的指纹入口", "GitHub junchaoshi/sports1.1", TOOL_VISUALS["sports"],
     ["处理small RNA/PANDORA-seq，输出tRNA-derived fragment annotation。", "可识别tRNA-Glu-CTC_5_end等片段类别。", "mismatch summary可作为候选修饰线索。", "数据库用途：fragment entity、RPM、length、source tRNA、condition。"]),
    ("工具精读｜mim-tRNAseq：最完整的RT错配型tRNA修饰pipeline", "GitHub nedialkova-lab/mim-tRNAseq", TOOL_VISUALS["mim"],
     ["步骤：cluster/index、GSNAP alignment、deconvolution、coverage/QC、DESeq2。", "输出：expression、misincorporation、3'-CCA completeness、SLAC crosstalk。", "识别率受coverage、RT通读、修饰类型和remap参数影响。", "数据库用途：method-specific mismatch spectrum 和 crosstalk evidence。"]),
    ("工具精读｜TRAC-Seq：专门服务m7G46的高特异方法", "GitHub rnabioinfor/TRAC-Seq + METTL1论文方法", TOOL_VISUALS["trac"],
     ["化学逻辑：m7G还原后可特异切割。", "信号：cleavage score，而不是普通mismatch。", "优点：m7G位点特异；局限：主要适用于m7G。", "数据库字段：chemical_treatment、cleavage_position、score_ratio。"]),
    ("工具精读｜tRNA004：把Nanopore错误率变成修饰benchmark", "GitHub rnabioco/tRNA004", TOOL_VISUALS["trna004"],
     ["核心贡献：43种已知修饰的basecalling error profiles。", "RNA004相对RNA002改善短tRNA测序产量/准确性，但每种修饰信号不同。", "识别差异原因：修饰化学体积、序列上下文、basecaller训练、coverage。", "数据库用途：nanopore_signature_reference。"]),
    ("工具精读｜Nanopore 2-Read：通读率和终止位点成为指纹", "GitHub AteeshaNegi/nanopore-2Read-trna-pipeline", TOOL_VISUALS["tworead"],
     ["利用ONT basecalling errors、polymerase read-through/error和termination events。", "强调per-read/per-site解析，适合记录分子层异质性。", "需要补充脚本完整性、示例数据、阈值和验证集。", "数据库字段：readthrough_rate、termination_site、per_read_signature。"]),
    ("工具精读｜Galaxy tRNAmod：传统NGS错配证据的workflow参考", "GitHub jfallmann/tRNA_ngs_mod_map_call_galaxy", TOOL_VISUALS["galaxy"],
     ["addCCA、clustering、multimapperPhasing、GATK wrapper等工具。", "核心思路：多重比对reads只有错配图案一致时才保留。", "优点：体现tRNA多拷贝mapping问题；局限：依赖旧GATK/Galaxy。", "数据库用途：multi_mapping_policy 和 mismatch evidence 规范化。"]),

    ("数据库设计｜第一版优先收录这些修饰和字段", "从精选文献和工具反推最小可行数据模型。", make_matrix(ASSETS / "priority_mods.png", "第一版优先修饰集合", ["修饰/位点", "代表证据", "核心字段"], [
        ["m7G46", "METTL1/TRAC-seq/衰老", "cleavage_score, METTL1-WDR4, RTD, ribosome_stalling"],
        ["mcm5s2U34 / mcm5h2U34", "m6A decay、氧化脱硫、病毒", "redox_state, decoding_rate, aminoacylation_effect"],
        ["m1A", "ALKB-1/PME", "writer/eraser_state, m1A_level, mitochondrial phenotype"],
        ["m3C32", "METTL6-SerRS结构", "writer, cofactor, structure_state, substrate_tRNA"],
        ["Ψ38/39", "PUS3结构选择性", "writer, target_position, selectivity_evidence"],
        ["Q/I/m5C/f5C/k2C", "病毒/解码/lysidine", "codon_specificity, infection_condition, AUG_avoidance"],
    ], col_widths=[1.7, 2.5, 3.0]),
     ["先覆盖强证据和强表型修饰，不追求一开始覆盖>100全部。", "每个修饰至少要有：位点、方法、信号、来源、表型字段。", "后续用MODOMICS批量扩展全量修饰字典。"]),
    ("数据库设计｜指纹库schema把文献与工具输出连接起来", "最小可行schema。", VISUALS["schema"],
     ["Reference、Modification、Evidence、Function 四层分离。", "工具输出只进入Evidence层；文献表型进入Function层。", "同一修饰允许多方法、多条件、多表型证据并存。"]),
    ("数据库设计｜识别率/通读率需要按方法存储，而不是全局值", "方法特异字段建议。", make_matrix(ASSETS / "method_specific_metrics.png", "方法特异指标", ["方法", "建议指标", "不能混淆的地方"], [
        ["mim-tRNAseq", "mismatch_rate, RT_stop, coverage, remap_mismatch", "错配率不是绝对修饰率"],
        ["TRAC-seq", "cleavage_score, score_ratio, NaBH4/aniline parameters", "只适合m7G等特定化学逻辑"],
        ["Nanopore", "basecalling_error, indel, termination, readthrough_rate", "受chemistry和basecaller强烈影响"],
        ["LC-MS/MS", "nucleoside abundance, fragment mass, modification frequency", "核苷MS通常缺少tRNA位点来源"],
        ["PANDORA/LIDAR", "capture_gain, terminal_state, fragment class", "捕获率反映library bias和末端化学"],
    ], col_widths=[1.5, 3.2, 2.8]),
     ["同一修饰在不同工具中指标不等价。", "数据库查询界面应显示方法、阈值和coverage，避免误读。", "通读率/readthrough_rate必须绑定RT酶或Nanopore chemistry。"]),
    ("最终结论｜tRNA修饰指纹库应是证据图谱，不是静态修饰表", "综合模型。", make_flow(ASSETS / "final_conclusion.png", "从精读材料得到的数据库原则", [
        "用MODOMICS定义“修饰是什么”",
        "用reference版本定义“修饰在哪里”",
        "用mim/TRAC/Nanopore/MS定义“如何被识别”",
        "用Ribo-seq/氨酰化/表型定义“为什么重要”",
        "每条记录保留来源文献、图号、工具参数和证据等级",
    ]),
     ["第一版优先做U34/G46/C32/A37等关键位点。", "识别率差异来自化学结构、上下文、平台和预处理，不应被简化为一个百分比。", "下一步可以把现有CSV/JSON整理成schema原型，再接入工具输出。"]),
]


def add_textbox(slide, x, y, w, h, text, size=18, bold=False, align=PP_ALIGN.LEFT):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.03)
    tf.margin_right = Inches(0.03)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.name = "Microsoft YaHei"
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = RGBColor(0, 0, 0)
    return shape


def add_bullets(slide, x, y, w, h, bullets, size=13):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = b
        p.level = 0
        p.space_after = Pt(5)
        p.font.name = "Microsoft YaHei"
        p.font.size = Pt(size)
        p.font.color.rgb = RGBColor(0, 0, 0)
    return shape


def fit_picture(slide, image_path, x, y, w, h):
    image_path = Path(image_path)
    with Image.open(image_path) as im:
        iw, ih = im.size
    box_ratio = w / h
    im_ratio = iw / ih
    if im_ratio > box_ratio:
        dw = w
        dh = w / im_ratio
    else:
        dh = h
        dw = h * im_ratio
    px = x + (w - dw) / 2
    py = y + (h - dh) / 2
    pic = slide.shapes.add_picture(str(image_path), Inches(px), Inches(py), width=Inches(dw), height=Inches(dh))
    pic.line.color.rgb = RGBColor(0, 0, 0)
    pic.line.width = Pt(0.75)
    return pic


def build():
    prs = Presentation()
    prs.slide_width = Inches(13.333333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    for i, (title, source, image, bullets) in enumerate(SLIDES, 1):
        slide = prs.slides.add_slide(blank)
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = RGBColor(255, 255, 255)
        add_textbox(slide, 0.32, 0.16, 12.7, 0.42, title, 20, True)
        add_textbox(slide, 0.36, 0.62, 12.4, 0.25, source, 8.8)
        fit_picture(slide, image, 0.45, 0.98, 7.25, 5.95)
        add_bullets(slide, 7.95, 1.02, 4.95, 5.75, bullets, 12.5)
        add_textbox(slide, 12.45, 7.14, 0.55, 0.18, str(i), 8, align=PP_ALIGN.RIGHT)

    prs.save(PPTX)
    reopened = Presentation(str(PPTX))
    bad = []
    for i, slide in enumerate(reopened.slides, 1):
        for shape in slide.shapes:
            if hasattr(shape, "text") and "????" in shape.text:
                bad.append(i)
                break
    with zipfile.ZipFile(PPTX) as zf:
        names = zf.namelist()
        media = [n for n in names if n.startswith("ppt/media/")]
        slide_xml = [n for n in names if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
    MANIFEST.write_text(
        "# Asset Manifest\n\n"
        + f"PPTX: `{PPTX}`\n\n"
        + "\n".join(f"- Slide {i}: `{image}` | {source}" for i, (_, source, image, _) in enumerate(SLIDES, 1))
        + "\n",
        encoding="utf-8",
    )
    result = "PASS" if len(reopened.slides) == len(SLIDES) and len(media) >= len(SLIDES) and not bad else "CHECK"
    QA.write_text(
        "# QA Report\n\n"
        + f"- PPTX: `{PPTX}`\n"
        + f"- Slides: {len(reopened.slides)} / expected {len(SLIDES)}\n"
        + f"- Embedded media: {len(media)}\n"
        + f"- Slide XML files: {len(slide_xml)}\n"
        + f"- Slides containing literal `????`: {bad or 'none'}\n"
        + "- Style: white background, black text, one visual per slide.\n"
        + f"\nValidation result: {result}\n",
        encoding="utf-8",
    )
    print(f"WROTE {PPTX}")
    print(f"WROTE {QA}")
    print(f"slides={len(reopened.slides)} media={len(media)} bad={bad}")


if __name__ == "__main__":
    build()
