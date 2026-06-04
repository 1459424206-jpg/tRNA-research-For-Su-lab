from pathlib import Path
import json
import re
import textwrap

import fitz
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


ROOT = Path(r"D:\Project\tRNA research\biological functions and structural characteristics of tRNA\downloaded_resources")
PDF_DIR = ROOT / "pdfs"
DEV_DIR = ROOT / "development_added_sources"
DEV_FIG_DIR = DEV_DIR / "figures"
OUT_DIR = ROOT / "paper2ppt_integrated_review"
ASSET_DIR = OUT_DIR / "assets"
PPTX_PATH = OUT_DIR / "tRNA_physiology_structure_early_embryo_integrated_review.pptx"
QA_PATH = OUT_DIR / "QA_report.md"
MANIFEST_PATH = OUT_DIR / "slide_manifest.json"
TRNA_SCHEMATIC = Path(r"D:\Project\tRNA research\tRNA_structure_schematic_clean.png")


WHITE = RGBColor(255, 255, 255)
BLACK = RGBColor(0, 0, 0)
GREY = RGBColor(80, 80, 80)
LIGHT_GREY = RGBColor(230, 230, 230)


LOCAL_PDFS = {
    "METTL6": "38918637_Structural_basis_of_tRNA_recognition_by_the_m3C_RNA_methyltransferase_METTL6_in_complex_with_Se.pdf",
    "OBfold": "39075051_Structural_basis_of_tRNA_recognition_by_the_widespread_OB_fold..pdf",
    "PARIS": "39111359_A_virally_encoded_tRNA_neutralizes_the_PARIS_antiviral_defence_system..pdf",
    "PYROXD1": "40069351_Mechanistic_basis_for_PYROXD1-mediated_protection_of_the_human_tRNA_ligase_complex_against_oxid.pdf",
    "Structurome": "40447571_In_vivo_structure_profiling_reveals_human_cytosolic_and_mitochondrial_tRNA_structurome_and_inte.pdf",
    "Trl1": "40563009_Structure_of_fungal_tRNA_ligase_Trl1_with_RNA_reveals_conserved_substrate-binding_principles..pdf",
    "vRNAP": "40908366_tRNA_as_an_assembly_chaperone_for_a_macromolecular_transcription-processing_complex..pdf",
    "Cas12a3": "41501459_RNA-triggered_Cas12a3_cleaves_tRNA_tails_to_execute_bacterial_immunity..pdf",
    "Desulfuration": "41807381_Translational_regulation_by_oxidative_desulfuration_of_tRNA_modifications..pdf",
}

BIB = {
    "METTL6": ("Structural basis of tRNA recognition by the m3C RNA methyltransferase METTL6 in complex with SerRS seryl-tRNA synthetase", "38918637"),
    "OBfold": ("Structural basis of tRNA recognition by the widespread OB fold", "39075051"),
    "PARIS": ("A virally encoded tRNA neutralizes the PARIS antiviral defence system", "39111359"),
    "PYROXD1": ("Mechanistic basis for PYROXD1-mediated protection of the human tRNA ligase complex against oxidative inactivation", "40069351"),
    "Structurome": ("In vivo structure profiling reveals human cytosolic and mitochondrial tRNA structurome and interactome in response to stress", "40447571"),
    "Trl1": ("Structure of fungal tRNA ligase Trl1 with RNA reveals conserved substrate-binding principles", "40563009"),
    "vRNAP": ("tRNA as an assembly chaperone for a macromolecular transcription-processing complex", "40908366"),
    "Cas12a3": ("RNA-triggered Cas12a3 cleaves tRNA tails to execute bacterial immunity", "41501459"),
    "Desulfuration": ("Translational regulation by oxidative desulfuration of tRNA modifications", "41807381"),
    "PheCNV": ("Copy number variation in tRNA isodecoder genes impairs mammalian development and balanced translation", "37072429"),
    "Zebrafish": ("The dynamics and functional impact of tRNA repertoires during early embryogenesis in zebrafish", "39402326"),
    "MouseORACLE": ("Deciphering tRNA repertoires and translation coordination during mouse early embryogenesis by ORACLE-tRNAseq", "not indexed; DOI: 10.1038/s41467-026-72603-5"),
    "SpermRNA": ("Small RNAs gained during epididymal transit of sperm are essential for embryonic development in mice", "30057276"),
}


def source_label(key=None, extra=None):
    if key in BIB:
        title, pmid = BIB[key]
        return f"来源：{title}. PMID: {pmid}" + (f" | {extra}" if extra else "")
    return "来源：根据本汇报所列文献综合整理" + (f" | {extra}" if extra else "")


def font_path():
    for p in [r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\calibri.ttf", r"C:\Windows\Fonts\segoeui.ttf"]:
        if Path(p).exists():
            return p
    return None


def pil_font(size):
    fp = font_path()
    if fp:
        return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def wrap_lines(text, width=42):
    lines = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, width=width) or [""])
    return lines


def make_diagram(name, title, nodes, footer=None, cols=3):
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    path = ASSET_DIR / f"diagram_{name}.png"
    if path.exists():
        return path
    W, H = 1500, 900
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    f_title = pil_font(42)
    f_node = pil_font(28)
    f_small = pil_font(22)
    d.text((45, 35), title, font=f_title, fill=(0, 0, 0))
    d.line((45, 92, W - 45, 92), fill=(210, 210, 210), width=3)
    rows = (len(nodes) + cols - 1) // cols
    box_w = (W - 100 - (cols - 1) * 30) // cols
    box_h = 170 if rows <= 2 else 145
    y0 = 150
    for idx, node in enumerate(nodes):
        col = idx % cols
        row = idx // cols
        x = 50 + col * (box_w + 30)
        y = y0 + row * (box_h + 65)
        d.rounded_rectangle((x, y, x + box_w, y + box_h), radius=18, fill=(248, 248, 248), outline=(30, 30, 30), width=3)
        node_title, node_text = node if isinstance(node, tuple) else (f"Step {idx+1}", node)
        d.text((x + 22, y + 18), node_title, font=f_node, fill=(0, 0, 0))
        yy = y + 60
        for line in wrap_lines(node_text, width=max(24, box_w // 18))[:4]:
            d.text((x + 22, yy), line, font=f_small, fill=(35, 35, 35))
            yy += 28
        if idx < len(nodes) - 1:
            # Arrow to next node, horizontally when possible.
            if col < cols - 1 and idx + 1 < len(nodes):
                d.line((x + box_w, y + box_h // 2, x + box_w + 26, y + box_h // 2), fill=(0, 0, 0), width=3)
                d.polygon([(x + box_w + 26, y + box_h // 2), (x + box_w + 12, y + box_h // 2 - 9), (x + box_w + 12, y + box_h // 2 + 9)], fill=(0, 0, 0))
    if footer:
        d.text((55, H - 70), footer, font=f_small, fill=(70, 70, 70))
    img.save(path, quality=94)
    return path


def find_label_page(pdf_path, label):
    doc = fitz.open(pdf_path)
    esc = re.escape(label).replace(r"\ ", r"\s+")
    patterns = [
        re.compile(rf"(?m)^{esc}\s*\|"),
        re.compile(rf"(?m)^{esc}\b"),
    ]
    first_loose = None
    for i, page in enumerate(doc):
        text = page.get_text("text") or ""
        if any(p.search(text) for p in patterns):
            return i
        if first_loose is None and re.search(esc, text):
            first_loose = i
    return first_loose if first_loose is not None else 0


def render_local_figure(key, label):
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = PDF_DIR / LOCAL_PDFS[key]
    safe = re.sub(r"[^A-Za-z0-9]+", "_", f"{key}_{label}").strip("_")
    path = ASSET_DIR / f"local_{safe}.jpg"
    if path.exists():
        return path
    doc = fitz.open(pdf_path)
    page_idx = find_label_page(pdf_path, label)
    pix = doc[page_idx].get_pixmap(matrix=fitz.Matrix(1.8, 1.8), alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    max_w = 1500
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, int(img.height * ratio)), Image.Resampling.LANCZOS)
    img.save(path, quality=92)
    return path


def dev_fig(name):
    return DEV_FIG_DIR / name


def set_bg(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = WHITE


def add_text(slide, x, y, w, h, text_value, size=18, bold=False, color=BLACK, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = MSO_ANCHOR.TOP
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text_value
    run.font.name = "Microsoft YaHei"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box


def add_bullets(slide, x, y, w, h, items, size=14):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.font.name = "Microsoft YaHei"
        p.font.size = Pt(size)
        p.font.color.rgb = BLACK
        p.space_after = Pt(4)
    return box


def add_rule(slide, y):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45), Inches(y), Inches(12.45), Inches(0.012))
    shape.fill.solid()
    shape.fill.fore_color.rgb = LIGHT_GREY
    shape.line.fill.background()


def add_picture_fit(slide, image_path, x, y, w, h):
    img = Image.open(image_path)
    iw, ih = img.size
    box_ratio = w / h
    img_ratio = iw / ih
    if img_ratio > box_ratio:
        pic_w = w
        pic_h = w / img_ratio
    else:
        pic_h = h
        pic_w = h * img_ratio
    left = x + (w - pic_w) / 2
    top = y + (h - pic_h) / 2
    return slide.shapes.add_picture(str(image_path), Inches(left), Inches(top), Inches(pic_w), Inches(pic_h))


def add_slide(prs, title, image, bullets, subtitle=None, source=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide)
    if source is None and isinstance(subtitle, str) and subtitle.startswith("来源："):
        source = subtitle
        subtitle = None
    add_text(slide, 0.42, 0.22, 12.45, 0.42, title, size=19, bold=True)
    if subtitle:
        add_text(slide, 0.43, 0.62, 12.1, 0.25, subtitle, size=10, color=GREY)
    add_rule(slide, 0.88)
    add_picture_fit(slide, image, 0.42, 1.04, 6.75, 6.05)
    add_bullets(slide, 7.45, 1.08, 5.25, 5.8, bullets, size=13)
    add_text(slide, 0.45, 6.78, 12.2, 0.48, source or source_label(), size=7.2, color=GREY)
    return slide


def build_slides():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)

    slides = []
    def diag(name, title, nodes, footer=None, cols=3):
        return make_diagram(name, title, nodes, footer=footer, cols=cols)

    # Intro
    slides.append(("tRNA 的广谱生理功能与结构特征：从分子识别到早期胚胎发育",
                   TRNA_SCHEMATIC,
                   [
                       "汇报围绕一个核心问题组织：tRNA 的结构特征如何支持多种生理功能，并如何参与早期胚胎发育调控。",
                       "主线分为四层：结构识别、加工与修饰、非经典生理功能、早期胚胎发育与 MZT/ZGA。",
                       "每页只放一张图或一张示意图；右侧文字解释该图在整篇文献逻辑中的位置。",
                   ],
                   "Integrated review deck | white background | one figure per slide",
                   None))
    slides.append(("文献构成与汇报模块",
                   diag("selection", "Evidence modules used in this report", [
                       ("Structure", "tRNA recognition, processing, modification and interactome"),
                       ("Physiology", "immune defense, viral counter-defense and noncanonical chaperone roles"),
                       ("Development", "embryonic tRNA pools, sperm tRNA fragments and tRNA gene dosage"),
                       ("Integration", "molecular structure to early-embryo translation control"),
                   ], cols=2),
                   [
                       "结构模块用于说明 tRNA 的受体茎、反密码子臂、可变环、3' CCA 和修饰位点如何被蛋白识别。",
                       "生理模块用于说明 tRNA 在翻译关闭、抗病毒防御、病毒逃逸和大分子复合物装配中的非经典功能。",
                       "发育模块聚焦 MZT/ZGA、胚胎 tRNA repertoire、tRNA gene dosage 和父源 tRNA fragments。",
                   ],
                   None, None))
    slides.append(("总假说：tRNA 的结构信息层决定其广谱生理功能",
                   diag("central_hypothesis", "Central hypothesis", [
                       ("Structure", "Acceptor stem, D/T loops, anticodon arm, variable loop, 3' CCA"),
                       ("Chemical layer", "m3C32, U34 sulfur modifications, pseudouridine, aminoacylation"),
                       ("Interaction layer", "aaRS, methyltransferases, ligases, ribosome, immune nucleases"),
                       ("Development", "Maternal-to-zygotic transition requires matched tRNA pools and translation programs"),
                   ], cols=2),
                   [
                       "tRNA 的生理功能不是“一个分子一种用途”，而是由结构域、修饰、末端成熟状态和互作蛋白共同决定。",
                       "早期胚胎发育是检验这一假说的理想场景：转录沉默到 ZGA 的窗口期高度依赖母源 RNA、翻译和 RNA 稳定性。",
                       "因此，tRNA repertoire、修饰和 small RNA fragment 都可能影响 MZT、ZGA、裂解节律和胚胎发育潜能。",
                   ], None, None))

    # Structurome paper
    slides += [
        ("文献精读 1｜DM-DMS-MaPseq：活细胞中的 tRNA structurome/interactome",
         diag("structurome_logic", "Paper logic: in vivo tRNA structure is not just folded RNA", [
             ("Problem", "In vitro tRNA structures miss cellular binding and ribosome protection"),
             ("Hypothesis", "DMS accessibility can report tRNA structure plus interaction state in vivo"),
             ("Method", "Demethylase treatment + DMS-MaPseq enables tRNA-wide profiling"),
             ("Meaning", "A tool to connect tRNA structure with stress and developmental translation"),
         ], cols=2),
         ["文章逻辑：先解决测序障碍，再比较体外/体内 DMS 信号，最后用 stress perturbation 证明互作图谱动态变化。",
          "该研究提供了在细胞状态下解析 tRNA 结构与互作的技术基础。",
          "与胚胎发育连接：MZT 期间 tRNA 结构与互作是否重排，理论上可用类似策略检测。"], source_label("Structurome"), None),
        ("DM-DMS-MaPseq 的关键方法步骤",
         render_local_figure("Structurome", "Fig. 1"),
         ["Fig. 1 是方法验证图：demethylase 先去除阻碍 RT 的 tRNA 修饰，再用 DMS-MaPseq 读出可及性。",
          "核心读数不是单纯丰度，而是碱基在体内是否被蛋白/核糖体/结构保护。",
          "这使 tRNA 从“序列/丰度对象”变成“结构-互作状态对象”。"], source_label("Structurome", "Fig. 1"), None),
        ("体内 tRNA 图谱明显不同于体外折叠状态",
         render_local_figure("Structurome", "Fig. 2"),
         ["Fig. 2 比较 chromosomal-encoded tRNA 的 in vitro 与 in vivo DMS signals。",
          "结论：同一种 tRNA 在细胞内有特定保护/暴露模式，不同 isodecoder 也可能不同。",
          "这对早期胚胎尤其重要：发育阶段改变的不只是 tRNA 数量，也可能是 tRNA 互作状态。"], source_label("Structurome", "Fig. 2"), None),
        ("氧化应激会重排 tRNA 结构和互作，提示翻译程序可被 tRNA 层调节",
         render_local_figure("Structurome", "Fig. 4"),
         ["Fig. 4 展示 arsenite stress 下细胞质 tRNA 的 ΔDMS signal。",
          "stress 后某些位点更暴露或更受保护，说明 tRNA 与翻译机器/蛋白的接触被重排。",
          "讨论意义：如果早期胚胎处在氧化、代谢或细胞周期压力下，tRNA interactome 也可能参与翻译重编程。"], source_label("Structurome", "Fig. 4"), None),
    ]

    # OB-fold
    slides += [
        ("文献精读 2｜OB-fold：成熟 tRNA 的 3' CA 末端是可被蛋白读取的结构标志",
         diag("obfold_logic", "Paper logic: identify a universal mature-tRNA recognition mode", [
             ("Old view", "Trbp/Arc1p may bind elbow or anticodon regions"),
             ("Question", "Which structural feature is directly read by OB-fold?"),
             ("Structure", "Trbp111-tRNA co-crystal reveals 3' CA capture"),
             ("Physiology", "Mature tRNA trafficking, aminoacylation, folding and localization"),
         ], cols=2),
         ["假说：OB-fold 蛋白可能通过一个成熟 tRNA 的通用标志进行识别。",
          "结果将识别焦点从 tRNA 主体/反密码子转向 3' 端成熟状态。",
          "与胚胎发育连接：成熟 tRNA pool 的质量控制会影响翻译可用性。"], source_label("OBfold"), None),
        ("Trbp111-tRNA 共晶结构证明 3' 端捕获是核心识别模式",
         render_local_figure("OBfold", "Fig. 2"),
         ["Fig. 2 是全文最关键结构图：Trbp111 二聚体结合两个 tRNA 分子，接触集中在 3' 端。",
          "这说明 tRNA 的 3' CA 不只是氨基酸连接末端，也可作为蛋白识别标志。",
          "结构特征：单链末端位置、CA 序列和末端几何共同决定识别。"], source_label("OBfold", "Fig. 2"), None),
        ("突变和竞争实验把结构接触转化为功能证据",
         render_local_figure("OBfold", "Fig. 3"),
         ["Fig. 3 通过界面突变和底物竞争证明 3' 端接触是结合所必需。",
          "结果说明 Trbp111 的 tRNA 识别不是晶体偶然现象，而是可被生化验证的功能界面。",
          "讨论意义：tRNA 末端成熟度可能是细胞调控 tRNA 互作网络的一层质量控制。"], source_label("OBfold", "Fig. 3"), None),
    ]

    # METTL6
    slides += [
        ("文献精读 3｜METTL6-SerRS：tRNA 修饰酶如何选择正确底物",
         diag("mettl6_logic", "Paper logic: substrate selection for anticodon-loop m3C32", [
             ("Problem", "METTL6 methylates tRNASer C32 but substrate selection was unclear"),
             ("Hypothesis", "SerRS acts as a tRNASer selection factor for METTL6"),
             ("Structure", "Cryo-EM captures METTL6-SerRS-tRNASer complex"),
             ("Function", "m3C32 supports translation fidelity and tRNA identity"),
         ], cols=2),
         ["文章逻辑：先构建复合物结构，再定位 m3C-RBD 和活性中心，最后用突变/活性验证底物选择机制。",
          "生理意义：tRNA 修饰写入依赖蛋白 cofactor，而不是酶单独识别所有序列信息。",
          "发育连接：胚胎翻译保真度和 codon-biased translation 可能依赖修饰酶和 aaRS 协同。"], source_label("METTL6"), None),
        ("METTL6、SerRS 与 tRNASer 形成可解释底物选择的复合物",
         render_local_figure("METTL6", "Fig. 1"),
         ["Fig. 1 显示 SerRS-tRNA-METTL6 整体结构。",
          "SerRS 把 tRNASer 带到 METTL6 附近，使 METTL6 不必单独完成全部底物选择。",
          "这提示 aaRS 可作为 tRNA 修饰网络中的身份读取器。"], source_label("METTL6", "Fig. 1"), None),
        ("反密码子臂重塑把 C32 送入可催化构象",
         render_local_figure("METTL6", "Fig. 3"),
         ["Fig. 3 展示 tRNA anticodon arm 在复合物中发生构象变化。",
          "C32 和 A37 附近区域被重新排列，为 m3C32 写入提供空间基础。",
          "这说明 tRNA 修饰不是简单识别单个碱基，而是对局部 RNA 构象的读取和重塑。"], source_label("METTL6", "Fig. 3"), None),
        ("METTL6 活性中心把结构重塑转化为化学修饰",
         render_local_figure("METTL6", "Fig. 4"),
         ["Fig. 4 展示 METTL6 active site 中 C32 与 SAH/SAM 结合口袋关系。",
          "催化位点位于 methyltransferase core 与 m3C-RBD 界面，体现结构域协同。",
          "讨论意义：C32、A37、U34 等反密码子环附近修饰可作为翻译效率和保真度的细粒度调节器。"], source_label("METTL6", "Fig. 4"), None),
    ]

    # Trl1 and PYROXD1 processing
    slides += [
        ("文献精读 4｜Trl1：tRNA 剪接后的 exon halves 如何被精确连接",
         render_local_figure("Trl1", "Fig. 1"),
         ["Fig. 1 将 fungal Trl1 的三步化学反应串起来：cP opening、5' phosphorylation、adenylylation/ligation。",
          "假说：Trl1-LIG 的结构域必须同时读取 RNA 末端几何和 2'-phosphate 化学状态。",
          "生理意义：tRNA splicing 是 tRNA 成熟和 UPR 相关 RNA processing 的核心步骤。"], source_label("Trl1", "Fig. 1"), None),
        ("CtTrl1-LIG-RNA 结构捕捉 activated RNA intermediate",
         render_local_figure("Trl1", "Fig. 2"),
         ["Fig. 2 是结构核心图：RNA 末端、AMP 和 LIG 结构域共同定位反应中心。",
          "方法逻辑：用晶体结构捕捉反应中间体，再用突变和模型解释真实 tRNA substrate。",
          "与结构特征连接：tRNA 剪接后的末端化学状态本身就是底物识别信息。"], source_label("Trl1", "Fig. 2"), None),
        ("PYROXD1：tRNA ligase 复合物需要抗氧化保护",
         render_local_figure("PYROXD1", "Fig. 1"),
         ["Fig. 1 展示 human RTCB-PYROXD1 cryo-EM 结构。",
          "RTCB 是人 tRNA-LC 的催化亚基，活性中心半胱氨酸容易被氧化失活。",
          "该研究将 tRNA processing 与细胞氧化还原状态连接起来。"], source_label("PYROXD1", "Fig. 1"), None),
        ("PYROXD1 C 端尾部遮挡 RTCB 活性中心，实现可逆保护",
         render_local_figure("PYROXD1", "Fig. 2"),
         ["Fig. 2 说明 PYROXD1 的 CTD/尾部直接贴近并遮挡 RTCB catalytic center。",
          "保护不是通过远端信号，而是通过物理占位和红氧状态控制。",
          "发育连接：早期胚胎经历代谢转换，RNA processing 酶的氧化保护可能影响 RNA homeostasis。"], source_label("PYROXD1", "Fig. 2"), None),
    ]

    # Desulfuration
    slides += [
        ("文献精读 5｜U34 氧化脱硫：tRNA 修饰把 stress 转换成翻译调控",
         render_local_figure("Desulfuration", "Fig. 1"),
         ["Fig. 1 建立化学问题：wobble U34 的 2-thiouridine 衍生物可被氧化脱硫。",
          "假说：xm5s2U34 到 xm5h2U34 的变化会改变 codon recognition 和 aminoacylation。",
          "生理意义：tRNA 修饰可作为氧化压力感受层，而不是静态结构装饰。"], source_label("Desulfuration", "Fig. 1"), None),
        ("质谱证明细胞质和线粒体 tRNA 中存在脱硫产物",
         render_local_figure("Desulfuration", "Fig. 3"),
         ["Fig. 3 用 XIC/LC-MS 检测 h2U derivatives。",
          "结果说明脱硫修饰不是体外伪影，而是可在细胞/组织中观察到的真实状态。",
          "与胚胎连接：早期胚胎的氧化还原环境变化可能通过 U34 修饰影响翻译选择性。"], source_label("Desulfuration", "Fig. 3"), None),
        ("cryo-EM 解释 U34 化学变化如何改变 AAA/AAG 解码",
         render_local_figure("Desulfuration", "Fig. 7"),
         ["Fig. 7 从结构上比较 mcm5s2U34 与 mcm5h2U34 在 ribosomal A-site 的解码几何。",
          "脱硫降低部分 tRNA 的 aminoacylation 和 codon recognition。",
          "讨论意义：这给出 tRNA 修饰-密码子偏好-翻译输出 的直接机制链。"], source_label("Desulfuration", "Fig. 7"), None),
    ]

    # Immune/noncanonical
    slides += [
        ("文献精读 6｜Cas12a3：CRISPR 免疫可通过切 tRNA tail 关闭翻译",
         render_local_figure("Cas12a3", "Fig. 2"),
         ["Fig. 2 是关键结果：target RNA 激活 Cas12a3 后，优先切割 tRNA 的 3' CCA tail。",
          "假说转变：某些 CRISPR effector 并非只清除入侵核酸，而是通过 tRNA inactivation 触发生长停滞。",
          "结构特征：3' CCA tail 成为免疫 nuclease 的广谱底物标志。"], source_label("Cas12a3", "Fig. 2"), None),
        ("Cas12a3 四元结构解释 tRNA 如何被装入 RuvC 活性位点",
         render_local_figure("Cas12a3", "Fig. 3"),
         ["Fig. 3 展示 Ba1Cas12a3-crRNA-target RNA-tRNA complex。",
          "activated Cas12a3 读取 tRNA acceptor stem、T-arm 和 tail，把 3' 端送入 RuvC。",
          "生理意义：tRNA 的保守结构使其成为快速、广谱的翻译关闭目标。"], source_label("Cas12a3", "Fig. 3"), None),
        ("PARIS：病毒 tRNA 变体可以反制宿主/卫星病毒防御系统",
         render_local_figure("PARIS", "Fig. 5"),
         ["Fig. 5 证明 PARIS cleaves E. coli tRNALys，而 T5 编码 non-cleavable tRNALys。",
          "文章逻辑：AriA 识别病毒 Ocr，释放 AriB；AriB 切 tRNALys 抑制翻译。",
          "意义：tRNA 是宿主防御与病毒逃逸共同争夺的生理节点。"], source_label("PARIS", "Fig. 5"), None),
        ("vRNAP：tRNA 可作为大型转录-加工复合物的 assembly chaperone",
         render_local_figure("vRNAP", "Fig. 3"),
         ["Fig. 3 提出 tRNA-chaperoned assembly cycle。",
          "该研究将 tRNA 的功能范围从翻译适配器扩展至病毒转录机器装配伴侣。",
          "关键点：被选择的是特定修饰状态的 tRNAGln/Arg，说明修饰和结构共同决定非经典功能。"], source_label("vRNAP", "Fig. 3"), None),
        ("vRNAP 中 tRNAGln 的非经典构象说明 tRNA 可被重塑成装配支架",
         render_local_figure("vRNAP", "Fig. 5"),
         ["Fig. 5 展示完整 vRNAP 中 tRNAGln(UUG) 的构象与相互作用。",
          "反密码子区域被内化/重塑，形成非经典 tRNA 结构。",
          "讨论意义：tRNA 的结构可塑性允许它在翻译之外承担 scaffold/chaperone 功能。"], source_label("vRNAP", "Fig. 5"), None),
    ]

    # Development added: tRNA-Phe CNV
    slides += [
        ("发育专题 1｜tRNA-Phe gene copy number variation 会破坏哺乳动物发育",
         dev_fig("tRNA_Phe_CNV_mammalian_development_fig1.jpg"),
         ["该研究直接将 tRNA gene dosage 与 mammalian development 联系起来。",
          "研究问题：哺乳动物扩增的 tRNA isodecoder gene copies 是否有具体生理必要性？",
          "策略：CRISPR 删除 tRNA-Phe isodecoder gene cluster，观察胚胎/个体发育和翻译平衡。"], source_label("PheCNV", "Fig. 1"), None),
        ("tRNA-Phe CNV 的核心假说：tRNA 供给量必须匹配 codon demand",
         dev_fig("tRNA_Phe_CNV_mammalian_development_fig2.jpg"),
         ["图中遗传操作和表型读数用于验证 tRNA-Phe copy number 对生理发育的贡献。",
          "结果方向：删除多个 tRNA-Phe gene copies 会扰动 translation homeostasis。",
          "与早期发育连接：胚胎快速分裂期对翻译平衡特别敏感，tRNA gene dosage 可能影响发育阈值。"], source_label("PheCNV", "Fig. 2"), None),
        ("tRNA gene dosage 影响 balanced translation，而不是只影响某个单一蛋白",
         dev_fig("tRNA_Phe_CNV_mammalian_development_fig5.jpg"),
         ["该图系结果组图的一部分，用于连接 tRNA copy number、codon translation 和生理表型。",
          "讨论意义：tRNA repertoire 是 translation system 的供给端，改变供给端会造成广谱 proteome 后果。",
          "这为解释胚胎发育阶段 tRNA repertoire 重排提供了遗传学支撑。"], source_label("PheCNV", "Fig. 5"), None),
    ]

    # Zebrafish
    slides += [
        ("发育专题 2｜zebrafish 早期胚胎发生中 tRNA repertoire 是动态变化的",
         dev_fig("zebrafish_tRNA_repertoire_2024_fig1.jpg"),
         ["该研究聚焦早期胚胎：MZT 期间 mRNA translation 与 turnover 快速重编程。",
          "核心问题：codon identity 影响 mRNA stability 已知，但 tRNA availability 是否同步变化？",
          "Fig. 1 通常用于建立测序/时间点/总体 repertoire 分析框架。"], source_label("Zebrafish", "Fig. 1"), None),
        ("tRNA repertoires 与胚胎发育阶段相匹配",
         dev_fig("zebrafish_tRNA_repertoire_2024_fig3.jpg"),
         ["结果逻辑：比较不同早期发育时间点的 tRNA abundance/isodecoder composition。",
          "重要性：tRNA pool 并非固定背景，而是随 MZT 和胚胎程序发生变化。",
          "这把 tRNA 从翻译被动底物提升为发育调控变量。"], source_label("Zebrafish", "Fig. 3"), None),
        ("tRNA availability 可能参与 codon-dependent maternal mRNA decay",
         dev_fig("zebrafish_tRNA_repertoire_2024_fig5.jpg"),
         ["该图组通常用于连接 tRNA abundance、codon usage 和 mRNA stability/translation。",
          "主线意义：早期胚胎中 mRNA fate 不只由 RNA-binding protein 和 miRNA 决定，也可能受 tRNA-codon 匹配影响。",
          "这是将 tRNA 结构/丰度与 MZT 机制联系起来的关键发育证据。"], source_label("Zebrafish", "Fig. 5"), None),
    ]

    # Mouse ORACLE
    slides += [
        ("发育专题 3｜mouse ORACLE-tRNAseq：低输入条件下解析 oocyte-to-blastocyst tRNA pools",
         diag("oracle_logic", "ORACLE-tRNAseq: low-input embryonic tRNA profiling", [
             ("Need", "Embryos contain little RNA; conventional tRNA-seq is difficult"),
             ("Method", "Optimized capture enables profiling from as few as five oocytes"),
             ("Map", "Oocyte -> zygote -> 2-cell -> 4-cell -> morula -> blastocyst"),
             ("Integrate", "tRNA-seq + chromatin + transcriptome + Ribo-seq"),
         ], cols=2),
         ["该研究将 tRNA repertoire 直接置于 mouse early embryogenesis 过程进行分析。",
          "核心发现：4-cell stage 出现 distinct embryonic tRNA repertoire 和 tRNA pseudogene upregulation。",
          "与 ZGA 连接：zygotic tRNA gene activation 与 H3K4me3 establishment/chromatin remodeling 同步。"], source_label("MouseORACLE"), None),
        ("mouse early embryo 中 tRNA anticodon pools 与翻译效率基因池协调",
         diag("oracle_result", "Embryonic tRNA pools coordinate with translation efficiency", [
             ("tRNA pool", "Anticodon abundance changes across stages"),
             ("ZGA", "Zygotic tRNA genes activate around genome activation"),
             ("Ribo-seq", "High translation-efficiency genes show codon-tRNA coordination"),
             ("Outcome", "Zygotic translation machinery is preferentially established"),
         ], cols=2),
         ["结果意义：早期胚胎不是简单继承母源 tRNA，而是在 ZGA 过程中建立新的 tRNA-translation coordination。",
          "这为 zebrafish 和 mammalian tRNA-Phe gene dosage 证据提供了共同解释框架。",
          "核心观点：tRNA repertoire 是 MZT/ZGA 期间翻译控制的一部分。"], source_label("MouseORACLE"), None),
    ]

    # Sperm small RNAs
    slides += [
        ("发育专题 4｜sperm small RNAs：精子获得的 tRNA fragments 对胚胎发育必需",
         dev_fig("sperm_small_RNAs_epididymal_transit_fig1.jpg"),
         ["该研究关注 sperm 在 epididymal transit 中获得 small RNA cargo 的过程。",
          "核心问题：精子 small RNAs 是旁观者，还是参与受精后胚胎程序？",
          "Fig. 1 建立精子成熟过程中 small RNA payload 改变的总体框架。"], source_label("SpermRNA", "Fig. 1"), None),
        ("epididymal transit 过程中 tRNA fragments 是精子 RNA cargo 的重要组成",
         dev_fig("sperm_small_RNAs_epididymal_transit_fig2.jpg"),
         ["Fig. 2 展示不同成熟阶段 sperm small RNA composition 的变化。",
          "多个 tRNA fragments 在附睾成熟过程中被加入精子。",
          "这把 tRNA 的生理功能从胚胎自身扩展到父源 RNA 输入和受精后早期调控。"], source_label("SpermRNA", "Fig. 2"), None),
        ("缺失成熟 sperm small RNA cargo 会影响胚胎发育",
         dev_fig("sperm_small_RNAs_epididymal_transit_fig5.jpg"),
         ["该图组支持：精子在附睾获得的 small RNAs 对正常 embryonic development 是必需的。",
          "与 tRNA 主线的关系：tRNA fragments 可作为父源信息载体，影响受精后早期发育轨迹。",
         "这为 sperm tsRNA 介导代际表型和早期胚胎基因调控提供机制入口。"], source_label("SpermRNA", "Fig. 5"), None),
    ]

    # Paper-by-paper close reading cards. These make the logic/method/result/discussion
    # explicit for every selected source, without turning the deck back into a raw
    # figure dump.
    cards = [
        ("DM-DMS-MaPseq tRNA structurome", [
            ("Hypothesis", "In vivo tRNA accessibility reflects both folding and cellular interactions"),
            ("Methods", "Demethylase treatment, DMS probing, MaP sequencing, stress perturbation"),
            ("Results", "In vivo and in vitro profiles differ; stress changes cytosolic and mitochondrial tRNA interactions"),
            ("Discussion", "Embryos may regulate translation by changing tRNA interaction states, not only tRNA abundance"),
        ]),
        ("OB-fold tRNA recognition", [
            ("Hypothesis", "An ancient OB-fold can recognize a universal mature tRNA feature"),
            ("Methods", "Co-crystal structure, mutagenesis, FP/ITC, minihelix competition"),
            ("Results", "Trbp111 captures the 3' CA end; Arc1p adds multivalent contacts"),
            ("Discussion", "Mature 3' ends act as structural identity marks for tRNA trafficking and metabolism"),
        ]),
        ("METTL6-SerRS m3C32 writing", [
            ("Hypothesis", "SerRS selects tRNASer for METTL6-mediated anticodon-loop methylation"),
            ("Methods", "Cryo-EM, X-ray structures, methylation assays, interface mutants"),
            ("Results", "METTL6 remodels anticodon arm; SerRS and METTL6 jointly read tRNASer features"),
            ("Discussion", "aaRS enzymes can be cofactor-like identity readers for tRNA modification pathways"),
        ]),
        ("Trl1 tRNA ligation", [
            ("Hypothesis", "Trl1-LIG reads the chemical geometry of TSEN-cleaved tRNA exon halves"),
            ("Methods", "Crystal structure of LIG-RNA intermediate, MD modeling, biochemical ligation assays"),
            ("Results", "RNA end positioning and 2'-phosphate specificity depend on conserved CTD residues"),
            ("Discussion", "tRNA processing enzymes use both structure and end chemistry as substrate identity"),
        ]),
        ("PYROXD1-RTCB protection", [
            ("Hypothesis", "RTCB needs redox-dependent protection to remain active in aerobic cells"),
            ("Methods", "Cryo-EM, NADH/FAD biochemistry, pull-down, guanylylation assays"),
            ("Results", "PYROXD1 tail occludes RTCB active site; release permits Archease activation"),
            ("Discussion", "tRNA ligation is embedded in redox homeostasis, relevant to stress-sensitive developmental stages"),
        ]),
        ("U34 oxidative desulfuration", [
            ("Hypothesis", "Oxidative conversion of xm5s2U34 to xm5h2U34 changes decoding and aminoacylation"),
            ("Methods", "LC-MS/MS, spike-in tracer tRNA, in vitro translation, A-site binding, cryo-EM"),
            ("Results", "Desulfuration reduces aminoacylation/decoding for several tRNAs and changes AAR geometry"),
            ("Discussion", "tRNA modifications can convert oxidative state into codon-biased translation control"),
        ]),
        ("Cas12a3 tRNA tail cleavage", [
            ("Hypothesis", "Some CRISPR effectors execute immunity by inactivating host tRNAs"),
            ("Methods", "Phylogeny, RNA cleavage assays, direct RNA sequencing, cryo-EM, reporter engineering"),
            ("Results", "Target RNA activates Cas12a3 to preferentially cleave conserved tRNA 3' CCA tails"),
            ("Discussion", "Conserved tRNA architecture makes translation shutdown fast, broad and programmable"),
        ]),
        ("PARIS antiviral defense", [
            ("Hypothesis", "PARIS senses viral antirestriction proteins and kills infection via tRNA cleavage"),
            ("Methods", "Cryo-EM, pull-down, ATPase assays, toxicity/translation assays, phage genetics"),
            ("Results", "AriB cleaves tRNALys; T5 encodes non-cleavable tRNALys to evade defense"),
            ("Discussion", "tRNA can be both immune effector target and viral counter-defense molecule"),
        ]),
        ("tRNA as vRNAP assembly chaperone", [
            ("Hypothesis", "Specific tRNA species can act as assembly chaperones outside translation"),
            ("Methods", "vRNAP reconstitution, cryo-EM intermediates, tRNA modification analysis, virion packaging"),
            ("Results", "Unmodified tRNAGln/Arg bridges factors and adopts a noncanonical conformation"),
            ("Discussion", "tRNA structural plasticity enables scaffold functions in large macromolecular machines"),
        ]),
        ("tRNA-Phe copy number variation", [
            ("Hypothesis", "Expanded tRNA isodecoder gene copy number has developmental necessity"),
            ("Methods", "CRISPR deletion of tRNA-Phe genes, development phenotyping, translation analysis"),
            ("Results", "tRNA gene dosage perturbation impairs balanced translation and mammalian development"),
            ("Discussion", "tRNA repertoire is a genome-encoded supply system with organismal consequences"),
        ]),
        ("Zebrafish embryonic tRNA repertoires", [
            ("Hypothesis", "tRNA availability changes during MZT and contributes to codon-dependent mRNA fate"),
            ("Methods", "Stage-resolved tRNA profiling, codon analysis, mRNA stability/translation integration"),
            ("Results", "tRNA repertoires are dynamic during early embryogenesis and align with codon programs"),
            ("Discussion", "Embryonic translation reprogramming includes a tRNA supply layer"),
        ]),
        ("Mouse ORACLE-tRNAseq", [
            ("Hypothesis", "Mouse embryos rebuild tRNA pools during ZGA to coordinate zygotic translation"),
            ("Methods", "Low-input ORACLE-tRNAseq from oocyte to blastocyst plus multi-omics/Ribo-seq"),
            ("Results", "Embryonic tRNA repertoire emerges; zygotic tRNA gene activation coincides with ZGA"),
            ("Discussion", "tRNA anticodon pools may help establish the zygotic translation machinery"),
        ]),
        ("Sperm tRNA fragments", [
            ("Hypothesis", "Sperm-borne small RNAs acquired during epididymal transit are required after fertilization"),
            ("Methods", "Small RNA profiling, epididymal sperm comparison, RNA manipulation, embryo assays"),
            ("Results", "tRNA fragments are gained during sperm maturation and loss disrupts embryo development"),
            ("Discussion", "tRNA-derived fragments can act as paternal inputs into early developmental regulation"),
        ]),
    ]
    card_sources = {
        "DM-DMS-MaPseq tRNA structurome": "Structurome",
        "OB-fold tRNA recognition": "OBfold",
        "METTL6-SerRS m3C32 writing": "METTL6",
        "Trl1 tRNA ligation": "Trl1",
        "PYROXD1-RTCB protection": "PYROXD1",
        "U34 oxidative desulfuration": "Desulfuration",
        "Cas12a3 tRNA tail cleavage": "Cas12a3",
        "PARIS antiviral defense": "PARIS",
        "tRNA as vRNAP assembly chaperone": "vRNAP",
        "tRNA-Phe copy number variation": "PheCNV",
        "Zebrafish embryonic tRNA repertoires": "Zebrafish",
        "Mouse ORACLE-tRNAseq": "MouseORACLE",
        "Sperm tRNA fragments": "SpermRNA",
    }
    for idx, (card_title, nodes) in enumerate(cards, start=1):
        slides.append((
            f"逐篇精读卡片 {idx}｜{card_title}",
            diag(f"card_{idx:02d}", card_title, nodes, footer="Close reading map: hypothesis - methods - results - discussion", cols=2),
            [
                "本页概述该文献在整份综述中的定位：其回答的是 tRNA 的哪一类结构、功能或发育问题。",
                "右侧四项分别对应：作者假说、方法步骤、关键结果和讨论意义。",
                "后续关键图页则展开该文献中最能支撑主线的实验图。",
            ],
            None,
            source_label(card_sources.get(card_title)),
        ))

    # Integration
    slides += [
        ("综合模型：tRNA 如何连接结构特征、生理功能和早期胚胎发育",
         diag("integrated_model", "Integrated model", [
             ("Structural identity", "Acceptor stem, anticodon arm, 3' CCA, variable loop"),
             ("Chemical identity", "m3C32, U34 sulfur, pseudouridine, aminoacylation"),
             ("Pool identity", "Isodecoder abundance and anticodon repertoire"),
             ("Fragment identity", "tsRNAs/tRFs as sperm or stress-derived signals"),
             ("Developmental output", "MZT, ZGA, translation efficiency, embryo competence"),
         ], cols=3),
         ["四类证据合并：结构生物学说明 tRNA 如何被识别；修饰/加工说明 tRNA 如何成熟；组学说明 tRNA pool 如何动态变化；发育文献说明这些变化有胚胎后果。",
          "早期胚胎的核心场景是：母源 RNA 清除、ZGA 启动和翻译系统重建。",
          "因此 tRNA 可能通过三个入口影响发育：codon-tRNA supply、modification-dependent decoding、sperm/embryo tsRNA signaling。"], None, None),
        ("后续研究假说：早期胚胎中的 tRNA 不是背景变量，而是翻译调控层",
         diag("future_hypotheses", "Testable hypotheses for early embryos", [
             ("H1", "ZGA requires matched embryonic tRNA anticodon pools"),
             ("H2", "U34/C32 modifications tune codon-biased translation during MZT"),
             ("H3", "tRNA processing stress alters cleavage timing and developmental competence"),
             ("H4", "Sperm tsRNAs prime early embryo chromatin or transcript turnover"),
         ], cols=2),
         ["可验证实验：单胚胎 tRNA-seq/DM-DMS-MaPseq、修饰质谱、Ribo-seq、codon reporter、tRF microinjection。",
          "重点不应只测总 tRNA abundance，而要同时看 isodecoder、charging、修饰、结构可及性和 fragment。",
          "最强逻辑链：tRNA repertoire/修饰变化 → codon-specific translation 或 mRNA stability → MZT/ZGA 表型。"], None, None),
    ]
    return slides


def build_ppt(slides):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    for title, image, bullets, subtitle, source in slides:
        add_slide(prs, title, image, bullets, subtitle=subtitle, source=source)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prs.save(PPTX_PATH)
    return len(prs.slides)


def validate(expected):
    prs = Presentation(PPTX_PATH)
    pictures = sum(1 for s in prs.slides for sh in s.shapes if sh.shape_type == 13)
    return {"slides": len(prs.slides), "expected": expected, "pictures": pictures}


def main():
    slides = build_slides()
    count = build_ppt(slides)
    qa = validate(count)
    manifest = [{"title": s[0], "image": str(s[1]), "source": s[4]} for s in slides]
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    QA_PATH.write_text(
        "\n".join([
            "# QA report",
            "",
            f"- PPTX: `{PPTX_PATH}`",
            f"- Slides: {qa['slides']} / expected {qa['expected']}",
            f"- Picture shapes: {qa['pictures']}",
            "- Style: white background, black text, minimal/no decoration.",
            "- Design: integrated review, not exhaustive figure dump.",
            "- Main deletions from prior source set: AAV suppressor tRNA therapy papers are not used as core physiology papers.",
            "- Added development sources: zebrafish early embryogenesis tRNA repertoires, mouse ORACLE-tRNAseq, tRNA-Phe copy number variation, sperm small RNAs during epididymal transit.",
            "",
        ]),
        encoding="utf-8",
    )
    print(json.dumps({"pptx": str(PPTX_PATH), "qa": qa, "manifest": str(MANIFEST_PATH)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
