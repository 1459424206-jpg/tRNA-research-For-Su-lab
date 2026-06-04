from pathlib import Path
import json
import re
import textwrap

import fitz
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


ROOT = Path(r"D:\Project\tRNA research\biological functions and structural characteristics of tRNA\downloaded_resources")
PDF_DIR = ROOT / "pdfs"
FIG_JSON = ROOT / "reading_extraction" / "clean_figures.json"
OUT_DIR = ROOT / "paper2ppt_per_figure_white"
ASSET_DIR = OUT_DIR / "figure_pages"
PPTX_PATH = OUT_DIR / "tRNA_literature_per_figure_white_black.pptx"
MANIFEST_PATH = OUT_DIR / "asset_manifest.json"
QA_PATH = OUT_DIR / "QA_report.md"


WHITE = RGBColor(255, 255, 255)
BLACK = RGBColor(0, 0, 0)
GREY = RGBColor(85, 85, 85)
LIGHT_GREY = RGBColor(235, 235, 235)


PAPER_SHORT_TITLES = {
    "38918637": "METTL6-SerRS 识别 tRNASer 并催化 m3C32",
    "39075051": "OB-fold 通过 tRNA 3' 端识别成熟 tRNA",
    "39111359": "病毒 tRNA 中和 PARIS 抗病毒系统",
    "40069351": "PYROXD1 保护人 tRNA ligase complex",
    "40447571": "DM-DMS-MaPseq 解析体内 tRNA 结构组",
    "40563009": "真菌 tRNA ligase Trl1 的 RNA 结合机制",
    "40908366": "tRNA 作为 vRNAP 装配伴侣",
    "41407712": "AAV 递送 sup-tRNAArg 恢复视网膜功能",
    "41501459": "Cas12a3 切割 tRNA tail 执行免疫",
    "41555020": "UGA sup-tRNA 的 disease-agnostic AAV 递送",
    "41807381": "氧化脱硫 tRNA 修饰调控翻译",
}


MAIN_FIG_NOTES = {
    "38918637": {
        "Fig. 1": "整体结构图：SerRS 二聚体、tRNASer 和 METTL6 形成复合物，说明 SerRS 参与 METTL6 的底物选择。",
        "Fig. 2": "聚焦 METTL6 的 m3C-specific RNA-binding domain，显示它如何接触和固定 tRNA 反密码子臂。",
        "Fig. 3": "显示 tRNA 反密码子臂被重塑，使 C32/A37 区域进入适合识别和催化的位置。",
        "Fig. 4": "展示 METTL6 活性中心，解释 C32 与 SAM/SAH 结合口袋之间的催化几何关系。",
        "Fig. 5": "展示 METTL6、SerRS 与 tRNA 可变臂界面，说明 tRNASer 特异选择的结构基础。",
    },
    "39075051": {
        "Fig. 1": "建立 Trbp111/Arc1p 等 OB-fold 蛋白的结构域背景和 tRNA 结合能力。",
        "Fig. 2": "共晶结构核心证据：Trbp111 主要捕获成熟 tRNA 的 3' CA 末端。",
        "Fig. 3": "突变和生化验证 3' 端接触界面，证明该识别模式具有功能意义。",
        "Fig. 4": "Arc1p 截短和点突变说明 OB-fold 与额外区域协同增强 tRNA 结合。",
        "Fig. 5": "改变全长 tRNA 的 3' 端会削弱 Arc1p 结合，支持 3' 末端是关键识别标志。",
        "Fig. 6": "minihelix/microhelix/ssRNA 实验分解出局部末端结构对结合的贡献。",
        "Fig. 7": "比较不同 OB-fold 核酸识别模式，把 Trbp/Arc1p 放入更广泛结构框架。",
    },
    "39111359": {
        "Fig. 1": "显示 PARIS 由 AriA/AriB 组装为大型螺旋桨状免疫复合物。",
        "Fig. 2": "解析 AriA-AriB 接触界面，说明该界面是防御功能的结构前提。",
        "Fig. 3": "证明病毒 Ocr 蛋白可通过 AriA 触发 AriB 释放。",
        "Fig. 4": "展示 PARIS 激活后的细胞死亡和翻译抑制，是抗病毒防御的效应输出。",
        "Fig. 5": "关键 tRNA 证据：PARIS 切宿主 tRNALys，而 T5 编码抗切割 tRNALys 逃逸。",
        "Fig. 6": "系统发育图说明 PARIS/ABC ATPase-TOPRIM 防御架构广泛存在。",
    },
    "40069351": {
        "Fig. 1": "RTCB-PYROXD1 复合物整体结构，显示 PYROXD1 贴近 RTCB 催化中心。",
        "Fig. 2": "PYROXD1 C 端尾部遮挡 RTCB 活性中心，解释抗氧化保护的直接机制。",
        "Fig. 3": "FAD/NADH 状态改变 PYROXD1 构象，调控 RTCB 招募和复合物形成。",
        "Fig. 4": "PYROXD1 与 RTCB 定时解离，使 Archease 可以接管并激活 RTCB。",
    },
    "40447571": {
        "Fig. 1": "方法学验证：DM-DMS-MaPseq 能在体内捕捉 RNA 可及性和结构信息。",
        "Fig. 2": "核编码 tRNA 的体内/体外 DMS 图谱不同，说明细胞环境强烈影响 tRNA 可及性。",
        "Fig. 3": "体内 DMS 保护信号与 tRNA-蛋白/核糖体互作对应。",
        "Fig. 4": "砷酸盐氧化应激改变细胞质 tRNA 结构和互作。",
        "Fig. 5": "线粒体 tRNA 也可被系统绘制体内结构图谱。",
        "Fig. 6": "应激下线粒体 tRNA 互作改变，提示线粒体翻译参与应激响应。",
    },
    "40563009": {
        "Fig. 1": "概述 Trl1 连接 tRNA exon halves 的化学步骤和底物结构。",
        "Fig. 2": "CtTrl1-LIG 与活化 RNA 中间体结构快照，展示反应中心如何定位。",
        "Fig. 3": "RNA 结合界面和突变验证，定义 Trl1-LIG 抓住 RNA 的关键残基。",
        "Fig. 4": "把短 RNA 结构建模到真实 tRNA 剪接 exon halves 场景。",
        "Fig. 5": "与 T4 Rnl2-AppDNA 比较，说明连接酶共享核酸末端定位逻辑。",
        "Fig. 6": "分析 Trl1-LIG C 端结构域在底物结合和连接效率中的作用。",
        "Fig. 7": "保守 Arg 残基识别 2'-phosphate，解释真菌 tRNA 剪接底物特异性。",
    },
    "40908366": {
        "Fig. 1": "vRNAP 装配中间体重构策略，展示如何检测 tRNA 参与装配。",
        "Fig. 2": "早期 PIC 结构中间体显示 tRNA 如何桥接多个转录/加工因子。",
        "Fig. 3": "提出 tRNA-chaperoned assembly cycle，把结构中间体串成装配路径。",
        "Fig. 4": "完整 vRNAP 高分辨率结构，显示 tRNA 与所有关键因子的空间关系。",
        "Fig. 5": "展示 tRNAGln(UUG) 的非经典构象和与蛋白的多点接触。",
        "Fig. 6": "鉴定 tRNAGln/Arg 修饰状态并测试其对复合物形成的影响。",
        "Fig. 7": "在 cryo-EM 密度中识别 tRNA 修饰，把化学状态与结构联系起来。",
        "Fig. 8": "完整 vRNAP 被整体包装入病毒颗粒，说明该装配机制有生命周期意义。",
    },
    "41407712": {
        "Fig. 1": "细胞中筛选工程化 sup-tRNAArg，提高 RPE65-R44X readthrough。",
        "Fig. 2": "scAAV8.A4T1 治疗恢复 rd12 小鼠 RPE65 蛋白表达。",
        "Fig. 3": "ERG 和锥细胞保护证明视网膜功能和结构得到改善。",
        "Fig. 4": "视觉 cliff 行为实验显示视觉引导行为恢复。",
        "Fig. 5": "H&E、转录组和 ribosome profiling 支持治疗安全性。",
    },
    "41501459": {
        "Fig. 1": "定义 Cas12a3/Cas12a4 作为 RNA 激活的 type V nuclease 新分支。",
        "Fig. 2": "关键证据：Cas12a3 被 target RNA 激活后优先切 tRNA 3' CCA tail。",
        "Fig. 3": "四元结构显示 tRNA 如何被 activated Cas12a3 捕获和装载。",
        "Fig. 4": "比较二元/三元/四元结构，解析 tRNA 结合和切割步骤。",
        "Fig. 5": "利用 tRNA-like reporter 扩展 CRISPR RNA 检测多重化能力。",
    },
    "41555020": {
        "Fig. 1": "NFS context 增强 UGA-sup-tRNAArg 的 readthrough potency。",
        "Fig. 2": "CuO-CymR 在生产阶段抑制 sup-tRNA 功能，改善 AAV 包装。",
        "Fig. 3": "优化 rAAV 产量、纯度和 vector genome homogeneity。",
        "Fig. 4": "AAV-NoSTOP(UGA) 在 IduaKI/KI 小鼠中恢复 IDUA 活性。",
        "Fig. 5": "不同组织中的 sup-tRNA 表达和 charging efficiency 解释疗效差异。",
    },
    "41807381": {
        "Fig. 1": "展示 tRNA U34 处 2-thiouridine 修饰及其氧化脱硫产物。",
        "Fig. 2": "spike-in tracer tRNA 实验证明脱硫产物可在细胞环境中形成。",
        "Fig. 3": "质谱检测细胞质和线粒体 tRNA 中的 h2U 衍生物。",
        "Fig. 4": "体外翻译系统显示脱硫修饰降低特定翻译输出。",
        "Fig. 5": "脱硫 tRNA 在 Lys/Gln/Glu 等氨酰化效率下降。",
        "Fig. 6": "A-site binding 实验证明 tRNALys 的 AAA/AAG 识别受影响。",
        "Fig. 7": "cryo-EM 解释 mcm5s2U34 与 mcm5h2U34 对 AAR 解码的结构差异。",
        "Fig. 8": "模型图总结氧化压力通过 U34 脱硫调控翻译。",
    },
}


def paper_id(file_name: str) -> str:
    return file_name.split("_", 1)[0]


def figure_rank(label: str) -> tuple:
    if label.startswith("Fig.") or label.startswith("Figure"):
        rank = 0
    elif label.startswith("Extended Data Fig."):
        rank = 1
    elif label.startswith("Supplementary Fig."):
        rank = 2
    else:
        rank = 3
    m = re.search(r"(\d+)", label)
    return (rank, int(m.group(1)) if m else 999, label)


def clean_caption(caption: str) -> str:
    caption = re.sub(r"\s+", " ", caption).strip()
    caption = re.sub(r"---PAGE\s+\d+---.*?$", "", caption).strip()
    return caption


def caption_title(label: str, caption: str) -> str:
    cap = clean_caption(caption)
    if "|" in cap:
        title = cap.split("|", 1)[1].strip()
    else:
        title = cap
    title = re.split(r"\s+[a-z]\,\s+", title, maxsplit=1)[0]
    title = re.split(r"\.\s+[a-z]\,\s+", title, maxsplit=1)[0]
    title = title.strip(" .")
    return title[:190] if title else label


def chinese_note(pid: str, label: str, title: str) -> str:
    main = MAIN_FIG_NOTES.get(pid, {}).get(label)
    if main:
        return main
    if label.startswith("Extended Data Fig."):
        return f"补充证据图：围绕“{title}”提供样品质量、结构解析流程、突变/功能验证或额外对照，用来支撑主文结论的可靠性。"
    if label.startswith("Supplementary Fig."):
        return f"补充图：围绕“{title}”给出额外实验或分析细节，主要用于解释主文图背后的方法、对照或数据稳健性。"
    return f"该图主要展示“{title}”，用于支撑本资料中关于 tRNA 结构、功能或工程应用的核心论点。"


def find_label_page(doc: fitz.Document, label: str) -> tuple[int, str]:
    escaped = re.escape(label).replace(r"\ ", r"\s+")
    strict = re.compile(rf"(?m)^{escaped}\s*\|")
    strict_see = re.compile(rf"(?m)^{escaped}\s*\|\s*See next page for caption", re.I)
    loose = re.compile(escaped)
    first_loose = None
    for i, page in enumerate(doc):
        text = page.get_text("text") or ""
        if strict_see.search(text):
            return i, "label-see-next-page"
        if strict.search(text):
            return i, "label-caption"
        if first_loose is None and loose.search(text):
            first_loose = i
    if first_loose is not None:
        return first_loose, "loose-match"
    return 0, "fallback-first-page"


def render_page_asset(pdf_path: Path, label: str, out_path: Path) -> dict:
    doc = fitz.open(pdf_path)
    page_index, match_type = find_label_page(doc, label)
    page = doc[page_index]
    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    # Trim white-ish margin lightly.
    bg = Image.new("RGB", img.size, (255, 255, 255))
    diff = Image.eval(ImageChops.difference(img, bg), lambda p: 255 if p > 12 else 0) if False else None
    max_w = 1500
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, int(img.height * ratio)), Image.Resampling.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, quality=92)
    return {"page": page_index + 1, "match_type": match_type, "asset": str(out_path)}


def set_white_bg(slide):
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


def add_bullets(slide, x, y, w, h, items, size=15):
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
        p.space_after = Pt(5)
    return box


def add_rule(slide, y):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45), Inches(y), Inches(12.45), Inches(0.015))
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


def load_figures():
    data = json.loads(FIG_JSON.read_text(encoding="utf-8"))
    papers = []
    for paper in data:
        figs = [f for f in paper["figures"] if not f["label"].startswith("Table")]
        figs.sort(key=lambda x: figure_rank(x["label"]))
        papers.append({**paper, "figures": figs})
    return papers


def generate_assets(papers):
    manifest = {}
    for paper_idx, paper in enumerate(papers, start=1):
        pid = paper_id(paper["file"])
        pdf_path = PDF_DIR / paper["file"]
        manifest[paper["file"]] = []
        for fig_idx, fig in enumerate(paper["figures"], start=1):
            safe_label = re.sub(r"[^A-Za-z0-9]+", "_", fig["label"]).strip("_")
            asset = ASSET_DIR / f"{paper_idx:02d}_{pid}_{fig_idx:02d}_{safe_label}.jpg"
            meta = render_page_asset(pdf_path, fig["label"], asset)
            manifest[paper["file"]].append({"label": fig["label"], **meta})
    return manifest


def build_ppt(papers, manifest):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # Cover
    slide = prs.slides.add_slide(blank)
    set_white_bg(slide)
    add_text(slide, 0.65, 0.9, 12.1, 0.8, "tRNA 文献逐图阅读汇报", size=38, bold=True)
    add_text(slide, 0.68, 1.85, 11.8, 0.45, "每份资料每一张图一页 | 图文对应 | 白底黑字", size=22)
    add_text(slide, 0.68, 5.9, 11.8, 0.5, f"资料数：{len(papers)} | 图页数：{sum(len(p['figures']) for p in papers)}", size=18, color=GREY)

    # Index
    slide = prs.slides.add_slide(blank)
    set_white_bg(slide)
    add_text(slide, 0.55, 0.45, 12.0, 0.5, "目录", size=30, bold=True)
    add_rule(slide, 1.08)
    lines = []
    for i, paper in enumerate(papers, start=1):
        pid = paper_id(paper["file"])
        lines.append(f"{i}. {PAPER_SHORT_TITLES.get(pid, paper['title'])}  ({len(paper['figures'])} 张图)")
    add_bullets(slide, 0.75, 1.35, 12.0, 5.6, lines, size=15)

    global_fig_no = 0
    for paper_idx, paper in enumerate(papers, start=1):
        pid = paper_id(paper["file"])
        short_title = PAPER_SHORT_TITLES.get(pid, paper["title"])

        # Section slide
        slide = prs.slides.add_slide(blank)
        set_white_bg(slide)
        add_text(slide, 0.65, 0.9, 12.0, 0.7, f"{paper_idx}. {short_title}", size=30, bold=True)
        add_text(slide, 0.68, 1.82, 11.9, 0.5, paper["file"], size=13, color=GREY)
        add_rule(slide, 2.45)
        fig_labels = ", ".join(f["label"] for f in paper["figures"])
        add_text(slide, 0.72, 2.85, 11.8, 2.2, f"本节逐图覆盖：{fig_labels}", size=18)
        add_text(slide, 0.72, 5.75, 11.8, 0.45, f"共 {len(paper['figures'])} 张图", size=20, bold=True)

        for fig_idx, fig in enumerate(paper["figures"], start=1):
            global_fig_no += 1
            label = fig["label"]
            title = caption_title(label, fig["caption"])
            note = chinese_note(pid, label, title)
            caption = clean_caption(fig["caption"])
            caption_excerpt = caption[:700] + ("..." if len(caption) > 700 else "")
            meta = manifest[paper["file"]][fig_idx - 1]
            asset = Path(meta["asset"])

            slide = prs.slides.add_slide(blank)
            set_white_bg(slide)
            add_text(slide, 0.35, 0.25, 12.6, 0.42, f"{paper_idx}.{fig_idx} {label}: {title}", size=18, bold=True)
            add_rule(slide, 0.78)
            add_picture_fit(slide, asset, 0.35, 0.95, 7.25, 6.05)

            add_text(slide, 7.85, 0.98, 5.05, 0.35, "图文对应解读", size=18, bold=True)
            add_bullets(slide, 7.85, 1.42, 5.05, 1.7, [
                f"这张图说什么：{note}",
                f"所在资料：{short_title}",
                f"源页码：PDF p.{meta['page']}；匹配方式：{meta['match_type']}",
            ], size=13)

            add_text(slide, 7.85, 3.38, 5.05, 0.32, "原始图注摘录", size=16, bold=True)
            add_text(slide, 7.85, 3.78, 5.05, 2.9, caption_excerpt, size=10)
            add_text(slide, 0.35, 7.05, 12.0, 0.25, f"Figure slide {global_fig_no} / {sum(len(p['figures']) for p in papers)}", size=9, color=GREY)

    # Summary
    slide = prs.slides.add_slide(blank)
    set_white_bg(slide)
    add_text(slide, 0.65, 0.65, 12.0, 0.65, "总结合并：这些图共同证明什么", size=30, bold=True)
    add_rule(slide, 1.5)
    add_bullets(slide, 0.85, 1.9, 11.7, 4.6, [
        "tRNA 的功能识别依赖局部结构：3' CA、3' CCA tail、反密码子臂、D/T loop、可变臂和剪接末端都可成为识别标志。",
        "tRNA 修饰是动态调控层：m3C32、U34 硫修饰/脱硫、缺失 mcm5s2U34 等会改变翻译、结构识别或复合物装配。",
        "免疫系统反复利用 tRNA 作为翻译关闭节点：PARIS 和 Cas12a3 都通过切 tRNA 抑制感染传播。",
        "工程化 suppressor tRNA 的转化关键已经从能否 readthrough，推进到递送、包装、组织表达、charging efficiency 和安全性。",
    ], size=22)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prs.save(PPTX_PATH)
    return len(prs.slides)


def validate(slide_count_expected: int):
    prs = Presentation(PPTX_PATH)
    picture_count = sum(1 for slide in prs.slides for shape in slide.shapes if shape.shape_type == 13)
    return {"slides": len(prs.slides), "expected_slides": slide_count_expected, "pictures": picture_count}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    papers = load_figures()
    manifest = generate_assets(papers)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    slide_count = build_ppt(papers, manifest)
    qa = validate(slide_count)
    total_figs = sum(len(p["figures"]) for p in papers)
    QA_PATH.write_text(
        "\n".join([
            "# QA report",
            "",
            f"- PPTX: `{PPTX_PATH}`",
            f"- Papers: {len(papers)}",
            f"- Figure slides: {total_figs}",
            f"- Total slides: {qa['slides']}",
            f"- Expected slides: {qa['expected_slides']}",
            f"- Embedded pictures: {qa['pictures']}",
            "- Style: white background, black text, no decoration.",
            "- Scope: Fig., Extended Data Fig., and Supplementary Fig. entries from `clean_figures.json`; tables excluded.",
            "- Visual asset policy: each slide uses the rendered PDF page where the figure label/caption was detected, plus the figure-specific interpretation text.",
            "",
        ]),
        encoding="utf-8",
    )
    print(json.dumps({"pptx": str(PPTX_PATH), "qa": qa, "figure_slides": total_figs, "manifest": str(MANIFEST_PATH)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
