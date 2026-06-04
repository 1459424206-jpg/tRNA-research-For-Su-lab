from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

import fitz
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "analysis_induro_modification_fingerprints_20260602" / "papers"
OUT = ROOT / "analysis_induro_modification_fingerprints_20260602" / "ppt_output_20260604"
ASSETS = OUT / "assets" / "figures"
PPTX = OUT / "final_presentation_cn.pptx"
QA = OUT / "qa_report.md"
MANIFEST = OUT / "asset_manifest.md"

W, H = Inches(13.333), Inches(7.5)

INK = RGBColor(31, 41, 55)
MUTED = RGBColor(95, 108, 125)
LIGHT = RGBColor(247, 249, 252)
LINE = RGBColor(213, 221, 230)
TEAL = RGBColor(20, 125, 140)
BLUE = RGBColor(45, 90, 170)
GREEN = RGBColor(42, 126, 92)
GOLD = RGBColor(167, 116, 37)
RED = RGBColor(181, 73, 73)
PURPLE = RGBColor(112, 86, 160)


def ensure_dirs() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)


def find_reading_pdf() -> Path:
    for p in ROOT.glob("*.pdf"):
        if "指纹库" in p.name:
            return p
    raise FileNotFoundError("Could not find reading-note PDF in workspace root")


def paper(name: str) -> Path:
    p = PAPER_DIR / name
    if not p.exists():
        raise FileNotFoundError(p)
    return p


def crop_pdf_page(pdf: Path, page_no: int, rel: tuple[float, float, float, float], out_name: str, zoom: float = 2.4) -> Path:
    doc = fitz.open(pdf)
    page = doc[page_no - 1]
    r = page.rect
    x0, y0, x1, y1 = rel
    clip = fitz.Rect(r.x0 + x0 * r.width, r.y0 + y0 * r.height, r.x0 + x1 * r.width, r.y0 + y1 * r.height)
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)
    target = ASSETS / out_name
    pix.save(target)
    return target


def render_note_page(pdf: Path, page_no: int, out_name: str, zoom: float = 1.8) -> Path:
    return crop_pdf_page(pdf, page_no, (0.03, 0.05, 0.97, 0.92), out_name, zoom=zoom)


def extract_text_summary() -> dict[str, str]:
    note_pdf = find_reading_pdf()
    doc = fitz.open(note_pdf)
    pages = []
    for i in range(doc.page_count):
        text = re.sub(r"\s+", " ", doc[i].get_text("text")).strip()
        pages.append(text[:3200])
    return {"note_pdf": note_pdf.name, "pages": pages}


def prepare_assets() -> dict[str, Path]:
    ensure_dirs()
    note = find_reading_pdf()
    nakano = paper("Nakano_2025_Induro_tRNAseq_NatCommun.pdf")
    chen = paper("Chen_2016_Science_sperm_tsRNAs.pdf")
    nrg = paper("Chen_Yan_Duan_2016_NRG_sperm_RNA_modifications.pdf")

    assets = {
        "note_summary": render_note_page(note, 1, "note_p1_core_conclusions.png"),
        "note_compare_table": render_note_page(note, 2, "note_p2_mim_induro_table.png"),
        "note_mod_table": render_note_page(note, 3, "note_p3_modification_table.png"),
        "nakano_workflow": crop_pdf_page(nakano, 3, (0.02, 0.04, 0.98, 0.76), "nakano_fig1_workflow.png"),
        "nakano_readthrough": crop_pdf_page(nakano, 5, (0.03, 0.03, 0.97, 0.68), "nakano_fig3_readthrough.png"),
        "nakano_signature": crop_pdf_page(nakano, 8, (0.03, 0.03, 0.97, 0.72), "nakano_fig5_signatures.png"),
        "nakano_tissue": crop_pdf_page(nakano, 10, (0.03, 0.03, 0.97, 0.72), "nakano_fig6_tissues.png"),
        "nakano_coord": crop_pdf_page(nakano, 12, (0.03, 0.03, 0.97, 0.72), "nakano_fig7_coordination.png"),
        "chen_tsRNA": crop_pdf_page(chen, 2, (0.42, 0.04, 0.98, 0.92), "chen_science_fig2_fig3.png"),
        "chen_mod": crop_pdf_page(chen, 3, (0.03, 0.04, 0.98, 0.52), "chen_science_fig4_modification.png"),
        "nrg_model": crop_pdf_page(nrg, 7, (0.03, 0.06, 0.55, 0.74), "nrg_fig4_sperm_rna_mechanism.png"),
    }
    return assets


def add_bg(slide, color: RGBColor = RGBColor(255, 255, 255)) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_text(slide, x, y, w, h, text: str, size=14, bold=False, color: RGBColor = INK, align=None, font="Microsoft YaHei"):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.alignment = align or PP_ALIGN.LEFT
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box


def add_title(slide, title: str, kicker: str = "") -> None:
    add_text(slide, Inches(0.52), Inches(0.28), Inches(11.65), Inches(0.42), title, 25, True, INK)
    if kicker:
        add_text(slide, Inches(0.55), Inches(0.72), Inches(11.0), Inches(0.25), kicker, 8.5, False, MUTED)
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.52), Inches(0.98), Inches(12.2), Inches(0.018))
    line.fill.solid()
    line.fill.fore_color.rgb = LINE
    line.line.fill.background()


def add_pill(slide, x, y, text, color=TEAL, w=None):
    width = w or Inches(1.55)
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, width, Inches(0.34))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    add_text(slide, x + Inches(0.05), y + Inches(0.055), width - Inches(0.1), Inches(0.18), text, 8.5, True, RGBColor(255, 255, 255), PP_ALIGN.CENTER)
    return shape


def add_takeaway(slide, text: str, color=TEAL):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(6.82), Inches(12.22), Inches(0.38))
    shape.fill.solid()
    shape.fill.fore_color.rgb = LIGHT
    shape.line.color.rgb = LINE
    add_text(slide, Inches(0.72), Inches(6.9), Inches(11.9), Inches(0.2), f"Take-home: {text}", 10.5, True, color)


def add_bullets(slide, x, y, w, h, bullets: list[str], size=13, color: RGBColor = INK, gap=0.05):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.06)
    tf.margin_top = Inches(0.02)
    for idx, bullet in enumerate(bullets):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = bullet
        p.level = 0
        p.font.name = "Microsoft YaHei"
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(gap * 72)
    return box


def add_image_fit(slide, path: Path, x, y, w, h, frame=True):
    img = Image.open(path)
    iw, ih = img.size
    box_ratio = w / h
    img_ratio = iw / ih
    if img_ratio > box_ratio:
        width = w
        height = w / img_ratio
        left = x
        top = y + (h - height) / 2
    else:
        height = h
        width = h * img_ratio
        left = x + (w - width) / 2
        top = y
    pic = slide.shapes.add_picture(str(path), left, top, width=width, height=height)
    if frame:
        rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        rect.fill.background()
        rect.line.color.rgb = LINE
        rect.line.width = Pt(0.8)
        slide.shapes._spTree.remove(rect._element)
        slide.shapes._spTree.insert(pic._element.getparent().index(pic._element), rect._element)
    return pic


def add_source(slide, text: str) -> None:
    add_text(slide, Inches(0.58), Inches(7.23), Inches(12.1), Inches(0.18), text, 7.3, False, MUTED)


def add_notes(slide, notes: str) -> None:
    tf = slide.notes_slide.notes_text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = notes


def image_slide(prs, title, asset, bullets, takeaway, source, notes, layout="right_rail", accent=TEAL):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_title(slide, title)
    if layout == "right_rail":
        add_image_fit(slide, asset, Inches(0.58), Inches(1.24), Inches(8.65), Inches(5.35))
        add_pill(slide, Inches(9.55), Inches(1.24), "怎么读这张图", accent, Inches(2.15))
        add_bullets(slide, Inches(9.48), Inches(1.72), Inches(3.05), Inches(4.6), bullets, 12.2)
    elif layout == "wide":
        add_bullets(slide, Inches(0.65), Inches(1.18), Inches(11.8), Inches(0.68), bullets, 12.2)
        add_image_fit(slide, asset, Inches(0.72), Inches(1.9), Inches(11.85), Inches(4.75))
    else:
        add_image_fit(slide, asset, Inches(0.7), Inches(1.42), Inches(6.35), Inches(4.95))
        add_bullets(slide, Inches(7.35), Inches(1.42), Inches(5.0), Inches(4.95), bullets, 12.8)
    add_takeaway(slide, takeaway, accent)
    add_source(slide, source)
    add_notes(slide, notes)
    return slide


def build_deck(assets: dict[str, Path]) -> None:
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H

    # 1 cover
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide, RGBColor(250, 252, 253))
    add_text(slide, Inches(0.7), Inches(0.7), Inches(11.8), Inches(0.45), "mim-tRNAseq 与 Induro-tRNAseq", 19, True, TEAL)
    add_text(slide, Inches(0.7), Inches(1.22), Inches(11.7), Inches(1.2), "修饰指纹库对比与三篇文献精读", 34, True, INK)
    add_text(slide, Inches(0.72), Inches(2.35), Inches(10.9), Inches(0.52), "把“测序错误”拆成可解释的 RT signature：mismatch、RT stop、readthrough 与位点结构环境", 15.5, False, MUTED)
    for i, (label, color, x) in enumerate([
        ("规则库：mim/TGIRT", BLUE, 0.82),
        ("酶学图谱：Induro", TEAL, 3.05),
        ("生殖场景：sperm tsRNA", GREEN, 5.3),
        ("研究设计：双RT + 质谱", GOLD, 8.05),
    ]):
        add_pill(slide, Inches(x), Inches(3.24), label, color, Inches(2.0 if i < 2 else 2.35))
    add_image_fit(slide, assets["note_summary"], Inches(0.75), Inches(3.9), Inches(11.9), Inches(2.45))
    add_source(slide, "Sources: 本地阅读版 PDF；Nakano et al., Nature Communications 2025；Chen et al., Science 2016；Chen, Yan & Duan, Nature Reviews Genetics 2016")
    add_notes(slide, "开场先说明本报告不比较具体样本的修饰丰度，而是比较工具层面的修饰指纹规则。核心问题是：RT 遇到修饰时产生什么可测信号，以及这些信号如何变成可用的修饰判读。")

    # 2 agenda
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_title(slide, "报告问题：不是“谁的数据库更大”，而是谁能解释哪类 RT 信号")
    boxes = [
        ("1", "指纹库边界", "mim 是源码规则/注释库；Induro 是反转录酶响应图谱。", BLUE),
        ("2", "共同核心", "m1A、m1G、m2,2G、m3C、I34、yW、acp3U、A37 复杂修饰等。", TEAL),
        ("3", "关键差异", "多数修饰看 0 位 mismatch；acp3U20 和 ms2i6A/ms2t6A37 要看 +1 RT stop。", RED),
        ("4", "生物学落点", "sperm tsRNA 的 m5C/m2G 有功能意义，但不能直接等同于 RT-readable 指纹。", GREEN),
    ]
    for i, (num, head, body, color) in enumerate(boxes):
        x = Inches(0.72 + (i % 2) * 6.1)
        y = Inches(1.42 + (i // 2) * 2.22)
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.55), Inches(1.65))
        shape.fill.solid(); shape.fill.fore_color.rgb = LIGHT
        shape.line.color.rgb = LINE
        add_pill(slide, x + Inches(0.18), y + Inches(0.18), num, color, Inches(0.45))
        add_text(slide, x + Inches(0.78), y + Inches(0.2), Inches(4.45), Inches(0.3), head, 15.5, True, color)
        add_text(slide, x + Inches(0.28), y + Inches(0.75), Inches(4.95), Inches(0.55), body, 12.2, False, INK)
    add_takeaway(slide, "本报告按“工具规则 -> 证据图谱 -> 生物学应用 -> 研究设计”展开。")
    add_notes(slide, "这一页给听众一个路线图：先澄清数据库/指纹库的语义，再进入 Induro 论文的证据，最后回到 sperm tsRNA 场景。")

    # 3 comparison
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_title(slide, "mim 与 Induro 的核心差异在“指纹来源”")
    add_image_fit(slide, assets["note_compare_table"], Inches(0.65), Inches(1.22), Inches(7.45), Inches(5.4))
    add_pill(slide, Inches(8.45), Inches(1.28), "mim-tRNAseq / TGIRT", BLUE, Inches(2.25))
    add_bullets(slide, Inches(8.35), Inches(1.75), Inches(4.2), Inches(1.55), [
        "源码内置规则：modifications、Mods + I、additionalMods",
        "包含完整修饰字典，但真正可检测集合远小于 170 项",
        "canonical hotspot 先验用于避免 isodecoder 误判",
    ], 11.4)
    add_pill(slide, Inches(8.45), Inches(3.72), "Induro-tRNAseq", TEAL, Inches(2.1))
    add_bullets(slide, Inches(8.35), Inches(4.18), Inches(4.2), Inches(1.45), [
        "来自系统酶学实测：RT stop、mismatch、read identity",
        "按修饰、位点、温度/时间、金属离子拆分规则",
        "不是重写 mim，而是在 RT 行为层面扩展框架",
    ], 11.4)
    add_takeaway(slide, "mim 更像“注释规则库”，Induro 更像“修饰-酶响应图谱”。")
    add_source(slide, "Source: 本地阅读版 PDF p2；Nakano et al., Nat Commun 2025")
    add_notes(slide, "强调这里的比较不是工具优劣，而是知识组织方式不同。mim 的强项是成熟注释和热点先验，Induro 的强项是把每类修饰的反转录行为拆开。")

    # 4 modification map
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_title(slide, "共同核心高度重叠，但可读边界必须逐修饰判断")
    add_image_fit(slide, assets["note_mod_table"], Inches(0.58), Inches(1.18), Inches(8.8), Inches(5.45))
    add_bullets(slide, Inches(9.62), Inches(1.28), Inches(2.95), Inches(4.85), [
        "共同核心：m1A、m1G、m2,2G、m3C、m1I、I34、yW、acp3U、ms2i6A、ms2t6A",
        "mim 额外单列 o2yW / OHyW；Induro 主文以 yW37 为实测条目",
        "m5C、Ψ、D、T、τm5U 等通常不能靠常规 RT signature 稳定定位",
    ], 11.2)
    add_takeaway(slide, "“有修饰名称”不等于“能被这套 RT 指纹可靠读出”。", RED)
    add_source(slide, "Source: 本地阅读版 PDF p3")
    add_notes(slide, "这一页需要提醒两个常见误区：第一，完整修饰字典不是可检测清单；第二，生物学上重要的修饰未必是 RT-readable。")

    # 5 workflow
    image_slide(
        prs,
        "Induro-tRNAseq 把 tRNA 修饰测序做成可多重化工作流",
        assets["nakano_workflow"],
        ["总 RNA 可直接进入流程，兼顾 charged / uncharged tRNA", "3' 端处理、barcode adapter、Induro RT、环化和 PCR 构成核心流程", "流程还能同时评估丰度、CCA 完整性和 charging"],
        "方法学贡献不只是换一个 RT，而是建立可复用的 tRNA modification profiling workflow。",
        "Source: Nakano et al., Nat Commun 2025, Fig. 1",
        "介绍工作流时不用讲每个酶反应细节，重点说它如何把 tRNA 的长度、结构和修饰障碍转化成可测读段。",
        "right_rail",
        TEAL,
    )

    # 6 readthrough
    image_slide(
        prs,
        "Induro 读穿提升来自减少 RT stop，而不是改变 mismatch 指纹",
        assets["nakano_readthrough"],
        ["37 °C 过夜读穿最高可接近 90%；42 °C 过夜是论文主工作流", "55 °C 推荐条件并不适合 tRNA 修饰读穿", "misincorporation 频率相对稳定，RT stop 更受时间和温度调控"],
        "mismatch 更像修饰的内在读出；RT stop 更像受条件调节的障碍。",
        "Source: Nakano et al., Nat Commun 2025, Fig. 3",
        "这里要把 experimental condition 作为主角。厂家条件不等于 tRNA 修饰测序的最佳条件，这对以后设计实验很重要。",
        "wide",
        BLUE,
    )

    # 7 signatures
    image_slide(
        prs,
        "多数修饰以 0 位错配为主，少数修饰必须看 +1 RT stop",
        assets["nakano_signature"],
        ["I34 几乎是纯 0 位 mismatch，几乎无 RT stop", "acp3U20a 与 ms2i6A37/ms2t6A37 是主要停顿型例外", "m1A/m1G 等同一化学修饰在不同位置可有不同 signature"],
        "不能只按修饰名解释测序信号，必须把“修饰 + 位点 + 局部结构”作为最小判读单位。",
        "Source: Nakano et al., Nat Commun 2025, Fig. 5",
        "这是全场核心证据页。mim/Induro 差异的关键不是名字列表，而是同一信号如何被解释成修饰。",
        "right_rail",
        RED,
    )

    # 8 coordinated tissues
    image_slide(
        prs,
        "Induro 还把指纹库推到组织/细胞型层面的协调变化",
        assets["nakano_tissue"],
        ["三种小鼠组织中修饰信号不是随机漂移", "ASL 解码相关位点更稳定，tRNA body 位点更可变", "body 修饰差异可能反映组织对 tRNA 结构适配的需求"],
        "工具层面的 signature 最终服务于生物学问题：哪些修饰随细胞状态协调变化？",
        "Source: Nakano et al., Nat Commun 2025, Fig. 6",
        "这一页从方法学过渡到生物学。重点不是每个组织哪条 tRNA 变了，而是作者提出的稳定 ASL 与可变 body 的组织逻辑。",
        "right_rail",
        GREEN,
    )

    # 9 concept model
    image_slide(
        prs,
        "作者提出：ASL 修饰稳定，body 修饰更像结构调节层",
        assets["nakano_coord"],
        ["ASL 位点承担遗传密码读取，跨细胞/组织更保守", "body 位点影响 L 形结构、Mg2+ 配位和局部折叠，可随组织需求变化", "这一模型为后续筛选功能位点提供优先级"],
        "Induro 的生物学结论是“修饰变化有组织逻辑”，不是一张无序差异列表。",
        "Source: Nakano et al., Nat Commun 2025, Fig. 7",
        "可以把这一页当作 Nakano 论文的小结：signature 是手段，coordinated changes 是生物学出口。",
        "right_rail",
        TEAL,
    )

    # 10 sperm tsRNA
    image_slide(
        prs,
        "Chen 2016 Science 把 sperm tsRNA 修饰带入功能因果链",
        assets["chen_tsRNA"],
        ["HFD 父代精子 RNA 可诱导 F1 葡萄糖耐受异常", "30-40 nt RNA fraction 主要为 tsRNA，是关键功能亚群", "内源 tsRNA 与未修饰合成 tsRNA 的功能差异提示修饰很关键"],
        "sperm tsRNA 让“tRNA 修饰图谱”从技术问题变成生殖表观遗传问题。",
        "Source: Chen et al., Science 2016, Fig. 2-3",
        "这页只保留背景证据，不展开所有代谢表型。目的是说明为什么要关心 tsRNA 的修饰，而不是只关心全长 tRNA。",
        "right_rail",
        GREEN,
    )

    # 11 m5C/m2G caution
    image_slide(
        prs,
        "HFD sperm tsRNA 中 m5C/m2G 升高，但这不是 Induro/mim 可直接解决的问题",
        assets["chen_mod"],
        ["LC-MS/MS 在 30-40 nt sperm RNA 中检测到 10 类修饰", "HFD 组 m5C 与 m2G 显著升高，miRNA fraction 中未见同样变化", "LC-MS/MS 给总量，不给具体 tsRNA 序列和位点"],
        "m5C/m2G 是生殖功能重点，但需要质谱、化学定位和功能实验补证。",
        "Source: Chen et al., Science 2016, Fig. 4",
        "这里要明确区分 m2G 与 m2,2G，也要说明 m5C 不是常规 Induro/mim 核心 RT-readable 修饰。",
        "right_rail",
        GOLD,
    )

    # 12 NRG model
    image_slide(
        prs,
        "NRG 综述给出 sperm RNA 与 RNA modification 的机制框架",
        assets["nrg_model"],
        ["精子 RNA 可来自睾丸发生过程，也可在附睾成熟中被重塑", "tsRNA、miRNA 等可能在早期胚胎触发转录级联", "RNA 修饰既影响功能，也会造成常规测序漏检"],
        "未来研究必须同时处理 abundance、modification 和测序偏差三件事。",
        "Source: Chen, Yan & Duan, Nat Rev Genet 2016, Fig. 4",
        "这一页用作讨论框架，不需要解释综述每个例子。核心是把 sperm RNA 的来源、作用和修饰偏差连起来。",
        "right_rail",
        PURPLE,
    )

    # 13 relationships
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_title(slide, "三篇文献之间的关系：方法、功能、框架")
    rows = [
        ("Nakano 2025", "方法学/资源", "定义 Induro 对 tRNA 修饰的 RT signature", "回答 Induro 能读哪些修饰、如何读"),
        ("Chen 2016 Science", "功能实验", "HFD sperm tsRNA 可诱导代谢异常，m5C/m2G 升高", "提示 tRNA/tsRNA 修饰有生殖功能意义"),
        ("Chen/Yan/Duan 2016 NRG", "综述框架", "整理 sperm RNA / RNA modification 的机制假说", "提示测序偏差和位点级证据缺口"),
    ]
    x0, y0 = Inches(0.72), Inches(1.35)
    widths = [Inches(2.15), Inches(1.45), Inches(4.45), Inches(4.25)]
    headers = ["文献", "类型", "核心贡献", "对本报告的作用"]
    for j, htxt in enumerate(headers):
        add_text(slide, x0 + sum(widths[:j]), y0, widths[j], Inches(0.35), htxt, 11, True, RGBColor(255,255,255), PP_ALIGN.CENTER)
        hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x0 + sum(widths[:j]), y0, widths[j], Inches(0.4))
        hdr.fill.solid(); hdr.fill.fore_color.rgb = TEAL
        hdr.line.color.rgb = RGBColor(255,255,255)
        slide.shapes._spTree.remove(hdr._element)
        slide.shapes._spTree.insert(2, hdr._element)
    for i, row in enumerate(rows):
        y = y0 + Inches(0.45 + i * 1.25)
        for j, cell in enumerate(row):
            rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x0 + sum(widths[:j]), y, widths[j], Inches(1.12))
            rect.fill.solid(); rect.fill.fore_color.rgb = LIGHT if i % 2 == 0 else RGBColor(255,255,255)
            rect.line.color.rgb = LINE
            add_text(slide, x0 + sum(widths[:j]) + Inches(0.08), y + Inches(0.16), widths[j] - Inches(0.16), Inches(0.62), cell, 10.4, j == 0, INK)
    add_takeaway(slide, "Nakano 解决“怎么读”，Chen Science 提供“为什么值得读”，NRG 提供“怎样设计下一步”。")
    add_source(slide, "Source: 本地阅读版 PDF p10；三篇原文")
    add_notes(slide, "这页把三篇文献在报告里的角色压实，避免听众觉得它们是三个并列但松散的阅读笔记。")

    # 14 research design
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_title(slide, "下一步研究设计：把全长 tRNA 指纹与 sperm tsRNA 功能接起来")
    cols = [
        ("A. 全长 tRNA 指纹", ["Induro-tRNAseq + mim/TGIRT 双 RT 互证", "重点：I34、m1A58、m1G37、m3C32、acp3U20、A37 复杂修饰", "RT stop 与 mismatch 同时建模"], TEAL),
        ("B. tsRNA 修饰定位", ["small RNA-seq 配套 LC-MS/MS", "m5C/m2G 需要 bisulfite、AlkB 或靶向修饰定位", "区分修饰总量、具体位点和具体 tsRNA 序列"], GOLD),
        ("C. 功能因果验证", ["天然 tsRNA vs 未修饰/定点修饰合成 tsRNA", "writer/eraser 操作：NSUN2/DNMT2、TRMT、ALKBH 等", "合子到 2-cell/8-cell/blastocyst 时间序列"], GREEN),
    ]
    for i, (head, bullets, color) in enumerate(cols):
        x = Inches(0.72 + i * 4.18)
        rect = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.32), Inches(3.68), Inches(4.82))
        rect.fill.solid(); rect.fill.fore_color.rgb = LIGHT
        rect.line.color.rgb = LINE
        add_pill(slide, x + Inches(0.22), Inches(1.58), head, color, Inches(2.62))
        add_bullets(slide, x + Inches(0.25), Inches(2.18), Inches(3.12), Inches(3.2), bullets, 11.2)
    add_takeaway(slide, "推荐证据链：tRNA 母体修饰变化 -> tsRNA 修饰继承/稳定性 -> 胚胎转录或翻译改变 -> 后代表型。", RED)
    add_source(slide, "Synthesized from local reading PDF and cited papers")
    add_notes(slide, "收束到可执行研究路线。这里可以结合自己的样本体系，把技术层与生物学层分开设计，避免把相关性列表误当因果链。")

    # 15 pitfalls and conclusion
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_title(slide, "结论：指纹库是解释规则，不是万能修饰探测器")
    add_bullets(slide, Inches(0.82), Inches(1.28), Inches(11.9), Inches(3.05), [
        "mim/TGIRT 的强项是成熟注释规则和 canonical hotspot；Induro 的强项是位点化、条件化的 RT signature 图谱。",
        "多数 Induro-readable 修饰看 0 位 mismatch；acp3U20 与 ms2i6A/ms2t6A37 等必须把 +1 RT stop 纳入判读。",
        "m5C/m2G 在 sperm tsRNA 功能研究中很重要，但需要 LC-MS/MS、化学/酶处理定位和功能实验补证。",
        "最稳妥路线是双 RT 互证 + 质谱总量验证 + 位点级修饰定位 + 胚胎时间序列功能读出。",
    ], 14.2)
    for x, label, color in [
        (0.9, "不要把 170 项字典当可检测表", BLUE),
        (3.85, "不要只看 mismatch", RED),
        (6.25, "不要混淆 m2G 与 m2,2G", GOLD),
        (9.05, "不要用未修饰 tsRNA 否定天然 tsRNA", GREEN),
    ]:
        add_pill(slide, Inches(x), Inches(5.18), label, color, Inches(2.55))
    add_takeaway(slide, "下一步最有价值的问题，是把工具层 signature 变成生殖发育中的位点级因果证据。")
    add_source(slide, "Prepared from local source package, 2026-06-04")
    add_notes(slide, "结尾回到一句话：这套 PPT 的目的不是证明某个工具更好，而是帮助设计一个可被验证的 tRNA/tsRNA 修饰研究路径。")

    prs.save(PPTX)


def write_manifest(assets: dict[str, Path]) -> None:
    rows = [
        ("note_summary", "reading note PDF p1", "cover/core conclusion"),
        ("note_compare_table", "reading note PDF p2", "mim vs Induro comparison"),
        ("note_mod_table", "reading note PDF p3", "modification-level comparison"),
        ("nakano_workflow", "Nakano 2025 Fig. 1", "workflow slide"),
        ("nakano_readthrough", "Nakano 2025 Fig. 3", "readthrough optimization"),
        ("nakano_signature", "Nakano 2025 Fig. 5", "RT signature rules"),
        ("nakano_tissue", "Nakano 2025 Fig. 6", "mouse tissue modification changes"),
        ("nakano_coord", "Nakano 2025 Fig. 7", "coordinated change model"),
        ("chen_tsRNA", "Chen 2016 Science Fig. 2-3", "sperm tsRNA functional evidence"),
        ("chen_mod", "Chen 2016 Science Fig. 4", "tsRNA modification evidence"),
        ("nrg_model", "Chen/Yan/Duan 2016 NRG Fig. 4", "sperm RNA mechanism framework"),
    ]
    lines = ["# Asset Manifest", "", "| asset | source | intended use | file |", "|---|---|---|---|"]
    for key, src, use in rows:
        lines.append(f"| {key} | {src} | {use} | `{assets[key].name}` |")
    MANIFEST.write_text("\n".join(lines), encoding="utf-8")


def verify() -> dict[str, object]:
    prs = Presentation(PPTX)
    media = []
    with zipfile.ZipFile(PPTX) as z:
        media = [n for n in z.namelist() if n.startswith("ppt/media/")]
    notes = sum(1 for s in prs.slides if s.notes_slide.notes_text_frame.text.strip())
    too_large = []
    for p in ASSETS.glob("*.png"):
        img = Image.open(p)
        if min(img.size) < 400:
            too_large.append(p.name)
    return {
        "pptx": str(PPTX),
        "slides": len(prs.slides),
        "embedded_media": len(media),
        "slides_with_notes": notes,
        "small_assets": too_large,
    }


def write_qa(info: dict[str, object]) -> None:
    rendered_pdf = PPTX.with_suffix(".pdf")
    rendered_sheet = OUT / "rendered_contact_sheet.jpg"
    lines = [
        "# QA Report",
        "",
        "- PPTX creation status: success",
        f"- Output file: `{PPTX}`",
        f"- Slide count: {info['slides']}",
        f"- Embedded media count: {info['embedded_media']}",
        f"- Slides with speaker notes: {info['slides_with_notes']}",
        "- Verification method: reopened with python-pptx; inspected PPTX package media entries; checked extracted asset dimensions.",
        f"- Rendered PDF available: {'yes' if rendered_pdf.exists() else 'not generated by this script'}",
        f"- Rendered contact sheet available: {'yes' if rendered_sheet.exists() else 'not generated by this script'}",
        "- Missing or placeholder figures: none",
        "- Known limitations: figure assets are cropped from PDF page renderings rather than publisher-original image files; very dense original panels may still need manual zoom/cropping if used for a long oral discussion.",
    ]
    if info["small_assets"]:
        lines.append(f"- Small assets flagged: {', '.join(info['small_assets'])}")
    QA.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assets = prepare_assets()
    build_deck(assets)
    write_manifest(assets)
    info = verify()
    write_qa(info)
    (OUT / "source_text_summary.json").write_text(json.dumps(extract_text_summary(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
