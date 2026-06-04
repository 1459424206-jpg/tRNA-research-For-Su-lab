from __future__ import annotations

import csv
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REFS = ROOT / "references.tsv"
OUT = ROOT / "literature_pdfs"
MANIFEST = OUT / "download_manifest.tsv"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Codex literature downloader"
SSL_CONTEXT = ssl._create_unverified_context()


def request(url: str, timeout: int = 30) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as resp:
        return resp.read(), resp.headers.get("content-type", "")


def is_pdf(content: bytes, content_type: str) -> bool:
    return content[:5] == b"%PDF-" or "pdf" in content_type.lower()


def safe_name(text: str, year: str) -> str:
    base = re.sub(r"[^A-Za-z0-9._-]+", "_", text.strip())[:95].strip("_")
    return f"{year}_{base}.pdf" if year else f"{base}.pdf"


def nature_pdf(url: str) -> str | None:
    if "nature.com/articles/" in url:
        return url.rstrip("/") + ".pdf"
    return None


def frontiers_pdf(url: str) -> str | None:
    if "frontiersin.org/articles/" in url and not url.rstrip("/").endswith("/pdf"):
        return url.rstrip("/") + "/pdf"
    return None


def bmc_pdf(url: str) -> str | None:
    if "biomedcentral.com/articles/" in url and not url.endswith(".pdf"):
        doi = url.rstrip("/").split("/articles/")[-1]
        return f"https://bmcgenomics.biomedcentral.com/counter/pdf/{doi}.pdf"
    return None


def pmc_pdf_candidates(url: str) -> list[str]:
    try:
        html, _ = request(url)
    except Exception:
        return []
    text = html.decode("utf-8", errors="ignore")
    candidates: list[str] = []
    for meta_url in re.findall(r'name=["\']citation_pdf_url["\']\s+content=["\']([^"\']+)["\']', text, flags=re.I):
        candidates.append(urllib.parse.urljoin(url, meta_url))
    for href in re.findall(r'href=["\']([^"\']+)["\']', text, flags=re.I):
        lower = href.lower()
        if ".pdf" in lower or "/pdf/" in lower or lower.endswith("/pdf"):
            candidates.append(urllib.parse.urljoin(url, href))
    # Newer PMC article pages sometimes expose the PDF through a /pdf/ route.
    m = re.search(r"/articles/(PMC\d+)/?", url)
    if m:
        candidates.append(f"https://pmc.ncbi.nlm.nih.gov/articles/{m.group(1)}/pdf/")
    return list(dict.fromkeys(candidates))


def generic_candidates(url: str) -> list[str]:
    candidates: list[str] = []
    for fn in (nature_pdf, frontiers_pdf, bmc_pdf):
        value = fn(url)
        if value:
            candidates.append(value)
    if "pmc.ncbi.nlm.nih.gov/articles/PMC" in url:
        candidates.extend(pmc_pdf_candidates(url))
    return list(dict.fromkeys(candidates))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(REFS.open("r", encoding="utf-8"), delimiter="\t"))
    manifest_rows: list[dict[str, str]] = []

    for i, row in enumerate(rows, start=1):
        title = row["Topic"]
        year = row["Year"]
        link = row["Link"]
        filename = safe_name(title, year)
        dest = OUT / filename
        status = "not_downloaded"
        pdf_url = ""
        note = "No open PDF candidate found automatically"

        for candidate in generic_candidates(link):
            try:
                content, ctype = request(candidate)
                if not is_pdf(content, ctype):
                    note = f"Candidate was not a PDF: {candidate}"
                    continue
                dest.write_bytes(content)
                status = "downloaded"
                pdf_url = candidate
                note = f"{len(content)} bytes"
                break
            except Exception as exc:
                note = f"{type(exc).__name__}: {exc}"
            time.sleep(0.5)

        manifest_rows.append(
            {
                "index": str(i),
                "topic": title,
                "year": year,
                "status": status,
                "pdf_file": str(dest.name) if status == "downloaded" else "",
                "source_link": link,
                "pdf_url": pdf_url,
                "note": note,
            }
        )

    with MANIFEST.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            delimiter="\t",
            fieldnames=["index", "topic", "year", "status", "pdf_file", "source_link", "pdf_url", "note"],
        )
        writer.writeheader()
        writer.writerows(manifest_rows)

    downloaded = sum(1 for row in manifest_rows if row["status"] == "downloaded")
    print(f"Downloaded {downloaded}/{len(manifest_rows)} PDFs")
    print(MANIFEST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
