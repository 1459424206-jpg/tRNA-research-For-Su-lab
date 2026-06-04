from __future__ import annotations

import json
import re
import time
from pathlib import Path

from deep_translator import GoogleTranslator
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Pt


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "output" / "final_presentation_cn_deep_literature.pptx"
DST = ROOT / "output" / "final_presentation_cn_deep_literature_zh_only.pptx"
CACHE = ROOT / "output" / "translation_cache_zh.json"
REPORT = ROOT / "output" / "translation_zh_report.json"


PROTECTED_SHORT = {
    "tRNA", "mRNA", "RNA", "DNA", "AAV", "UGA", "Cas12a3", "PARIS", "METTL1",
    "METTL6", "SerRS", "AARS1", "NAT10", "ALKB-1", "PYROXD1", "Trl1", "OB",
    "LC-MS", "LC-MS/MS", "RT", "PMID", "PMCID", "DOI", "PMC", "PDF",
    "Nature", "Cell", "Molecular Cell", "Nature Communications",
    "Nature Biotechnology", "Nature Genetics", "Nature Structural & Molecular Biology",
}


def normalize_abbreviations(text: str) -> str:
    replacements = {
        "t RNA": "tRNA",
        "m RNA": "mRNA",
        "r RNA": "rRNA",
        "nc RNA": "ncRNA",
        "small RNAs": "small RNA",
        "t RNAs": "tRNAs",
        "m6 A": "m6A",
        "m1 A": "m1A",
        "m3 C": "m3C",
        "m7 G": "m7G",
        "N7- methylguanosine": "N7-甲基鸟苷",
        "N7-甲基鸟嘌呤": "N7-甲基鸟苷",
        "PDF/PMC figure": "PDF/PMC 图像",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"\bexperimental\b", "实验研究", text, flags=re.I)
    text = re.sub(r"\breview\b", "综述", text, flags=re.I)
    text = re.sub(r"\bSource:\s*", "来源：", text)
    text = re.sub(r"\bDeck logic\b", "PPT 制作逻辑", text)
    text = re.sub(r"\bArticles covered\b", "覆盖文献", text)
    text = re.sub(r"\bPart\s+(\d+)\.", r"第 \1 部分：", text)
    text = text.replace("tRNA research", "tRNA 研究")
    return text


def should_translate(text: str) -> bool:
    t = normalize_abbreviations(text).strip()
    if not t:
        return False
    letters = len(re.findall(r"[A-Za-z]", t))
    cjk = len(re.findall(r"[\u4e00-\u9fff]", t))
    if letters < 8:
        return False
    # Keep pure source metadata mostly local-translated by normalize_source().
    if letters > cjk:
        return True
    return bool(re.search(r"[A-Za-z]{4,} [A-Za-z]{4,}", t))


def normalize_source(text: str) -> str:
    text = normalize_abbreviations(text)
    if "来源：" in text:
        text = text.replace("PMCID NA", "PMCID 无")
        text = text.replace("DOI NA", "DOI 无")
    return text


def postprocess_translation(original: str, translated: str) -> str:
    out = normalize_abbreviations(translated)
    # Fix common scientific term choices from generic machine translation.
    fixes = {
        "疾病不可知": "不限定疾病类型",
        "疾病不可知的": "不限定疾病类型的",
        "执行细菌免疫": "介导细菌免疫",
        "抑制 tRNA": "抑制子 tRNA",
        "抑制器 tRNA": "抑制子 tRNA",
        "氨基酰化": "氨酰化",
        "肿瘤发生": "肿瘤发生发展",
        "体内": "体内",
        "PDF/PMC 数字": "PDF/PMC 图像",
        "数字": "图",
        "逐篇深入阅读": "逐篇精读",
    }
    for old, new in fixes.items():
        out = out.replace(old, new)
    out = normalize_source(out)
    # Keep DOI and PMID/PMCID exactly if machine translation drops punctuation.
    for token in re.findall(r"10\.\d{4,9}/[A-Za-z0-9._;()/:+-]+", original):
        if token not in out:
            out += f"；DOI {token}"
    for label in ["PMID", "PMCID"]:
        m = re.search(label + r"\s+[A-Z0-9]+", original)
        if m and m.group(0) not in out:
            out += f"；{m.group(0)}"
    out = out.replace("： ", "：").replace(" ;", "；")
    return out.strip()


def iter_text_shapes(shapes):
    for shape in shapes:
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from iter_text_shapes(shape.shapes)
        elif hasattr(shape, "text_frame"):
            yield shape


def set_para_text(para, text: str) -> None:
    # Preserve paragraph-level style as far as python-pptx allows.
    if para.runs:
        ref = para.runs[0]
        size = ref.font.size
        bold = ref.font.bold
        italic = ref.font.italic
        color = None
        try:
            color = ref.font.color.rgb
        except Exception:
            color = None
    else:
        size = None
        bold = None
        italic = None
        color = None
    para.text = text
    if para.runs:
        run = para.runs[0]
        run.font.name = "Microsoft YaHei"
        if size:
            run.font.size = size
        elif len(text) > 120:
            run.font.size = Pt(9)
        if bold is not None:
            run.font.bold = bold
        if italic is not None:
            run.font.italic = italic
        if color is not None:
            run.font.color.rgb = color


def main() -> None:
    if not SRC.exists():
        raise FileNotFoundError(SRC)

    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    prs = Presentation(SRC)
    translator = GoogleTranslator(source="auto", target="zh-CN")

    unique_texts: list[str] = []
    seen = set()
    for slide in prs.slides:
        for shape in iter_text_shapes(slide.shapes):
            for para in shape.text_frame.paragraphs:
                text = "".join(run.text for run in para.runs).strip()
                text = normalize_abbreviations(text)
                if should_translate(text) and text not in cache and text not in seen:
                    unique_texts.append(text)
                    seen.add(text)

    failures = []
    for idx, text in enumerate(unique_texts, 1):
        try:
            translated = translator.translate(text)
            cache[text] = postprocess_translation(text, translated)
        except Exception as exc:
            failures.append({"text": text, "error": str(exc)})
            cache[text] = normalize_source(text)
        if idx % 25 == 0:
            CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
            time.sleep(0.5)
        else:
            time.sleep(0.08)

    replaced = 0
    normalized_only = 0
    for slide in prs.slides:
        for shape in iter_text_shapes(slide.shapes):
            for para in shape.text_frame.paragraphs:
                text = "".join(run.text for run in para.runs).strip()
                if not text:
                    continue
                norm = normalize_abbreviations(text)
                new_text = cache.get(norm)
                if new_text:
                    set_para_text(para, new_text)
                    replaced += 1
                elif norm != text:
                    set_para_text(para, normalize_source(norm))
                    normalized_only += 1

    prs.save(DST)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

    # Reopen and count remaining English-like text. Proper nouns and DOI strings
    # are expected to remain, but this helps QA.
    check = Presentation(DST)
    remaining = []
    for si, slide in enumerate(check.slides, 1):
        for shape in iter_text_shapes(slide.shapes):
            for para in shape.text_frame.paragraphs:
                text = "".join(run.text for run in para.runs).strip()
                if should_translate(text):
                    remaining.append({"slide": si, "text": text})
    REPORT.write_text(
        json.dumps(
            {
                "source": str(SRC),
                "output": str(DST),
                "unique_translated": len(unique_texts),
                "paragraphs_replaced": replaced,
                "paragraphs_normalized_only": normalized_only,
                "failures": failures[:50],
                "remaining_english_like_count": len(remaining),
                "remaining_english_like_sample": remaining[:100],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {DST}")
    print(f"Translated unique texts: {len(unique_texts)}")
    print(f"Remaining english-like: {len(remaining)}")


if __name__ == "__main__":
    main()
