from __future__ import annotations

import csv
import json
import re
import tarfile
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "resource_collection"
OUT.mkdir(parents=True, exist_ok=True)

NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
GITHUB_API = "https://api.github.com/search/repositories"


HIGH_IMPACT_JOURNALS = {
    "Nature": 65,
    "Science": 63,
    "Cell": 62,
    "Nature Reviews Molecular Cell Biology": 55,
    "Nature Biotechnology": 46,
    "Nature Methods": 45,
    "Nature Genetics": 41,
    "Nature Structural & Molecular Biology": 18,
    "Nature Communications": 17,
    "Science Advances": 14,
    "Molecular Cell": 18,
    "Genome Biology": 13,
    "Genome Research": 12,
    "Nucleic Acids Research": 13,
    "Proceedings of the National Academy of Sciences of the United States of America": 11,
    "PNAS": 11,
    "EMBO Journal": 11,
    "Cell Reports": 9,
    "RNA": 5,
    "RNA Biology": 4,
    "Nature Protocols": 14,
    "Briefings in Bioinformatics": 10,
    "Bioinformatics": 6,
}


JOURNAL_FILTER = " OR ".join(f'"{j}"[jour]' for j in HIGH_IMPACT_JOURNALS)
DATE_FILTER = '("2020/01/01"[dp] : "3000"[dp])'


@dataclass(frozen=True)
class Topic:
    folder: str
    slug: str
    cn_title: str
    en_title: str
    pubmed_query: str
    github_queries: tuple[str, ...]
    cn_focus: str
    en_focus: str


TOPICS = [
    Topic(
        folder="biological functions and structural characteristics of tRNA",
        slug="biology_structure",
        cn_title="tRNA 的生物功能与结构特征",
        en_title="Biological functions and structural characteristics of tRNA",
        pubmed_query='(tRNA[Title] OR "transfer RNA"[Title]) AND (structure[Title/Abstract] OR "tertiary structure"[Title/Abstract] OR "tRNA fragment"[Title/Abstract] OR translation[Title/Abstract] OR aminoacylation[Title/Abstract] OR disease[Title/Abstract] OR codon[Title/Abstract] OR suppressor[Title/Abstract])',
        github_queries=(
            "tRNA structure",
            "transfer RNA structure",
            "tRNA biology",
            "tRNA fragments",
        ),
        cn_focus="关注 tRNA 的经典三叶草二级结构、L 型三级结构、氨酰化、密码子解码、质量控制、tRNA 衍生片段以及疾病/应激中的功能重编程。",
        en_focus="Focuses on tRNA secondary and tertiary structure, aminoacylation, codon decoding, quality control, tRNA-derived fragments, and disease/stress-associated functional rewiring.",
    ),
    Topic(
        folder="tRNA analysis tools and algorithms",
        slug="tools_algorithms",
        cn_title="tRNA 分析工具与算法",
        en_title="tRNA analysis tools and algorithms",
        pubmed_query='(tRNA[Title] OR "transfer RNA"[Title] OR "tRNA-seq"[Title/Abstract] OR tRNAscan[Title/Abstract] OR "mim-tRNAseq"[Title/Abstract]) AND (software[Title/Abstract] OR tool[Title/Abstract] OR algorithm[Title/Abstract] OR sequencing[Title/Abstract] OR profiling[Title/Abstract] OR prediction[Title/Abstract] OR annotation[Title/Abstract] OR mapping[Title/Abstract])',
        github_queries=(
            "tRNAscan",
            "tRNA-seq",
            "tRNA sequencing",
            "tRNA annotation",
            "tRNA analysis",
        ),
        cn_focus="关注 tRNA 基因识别、序列注释、测序读段比对、修饰导致的 RT-stop/mismatch 处理、表达定量与结构/修饰预测算法。",
        en_focus="Covers tRNA gene detection, annotation, read alignment, handling RT stops/mismatches caused by modifications, expression quantification, and structure/modification prediction.",
    ),
    Topic(
        folder="tRNA mod-fingerprint database",
        slug="mod_fingerprint_database",
        cn_title="tRNA 修饰指纹数据库",
        en_title="tRNA mod-fingerprint database",
        pubmed_query='(tRNA[Title] OR "transfer RNA"[Title] OR MODOMICS[Title/Abstract] OR tRNAdb[Title/Abstract]) AND (modification[Title/Abstract] OR modifications[Title/Abstract] OR epitranscriptomic[Title/Abstract] OR database[Title/Abstract] OR fingerprint[Title/Abstract] OR "mass spectrometry"[Title/Abstract])',
        github_queries=(
            "MODOMICS",
            "tRNA modification",
            "tRNA database",
            "epitranscriptomics tRNA",
            "tRNA fingerprint",
        ),
        cn_focus="关注 tRNA 修饰位点、修饰酶、LC-MS/MS 或测序产生的修饰指纹、跨物种数据库、标准化注释和可视化查询。",
        en_focus="Focuses on tRNA modification sites, modifying enzymes, LC-MS/MS or sequencing-derived modification fingerprints, cross-species databases, standardized annotation, and visualization/query tools.",
    ),
    Topic(
        folder="tRNA-related wet-lab experiments",
        slug="wet_lab_experiments",
        cn_title="tRNA 相关湿实验",
        en_title="tRNA-related wet-lab experiments",
        pubmed_query='(tRNA[Title] OR "transfer RNA"[Title] OR "tRNA-seq"[Title/Abstract]) AND (assay[Title/Abstract] OR protocol[Title/Abstract] OR experiment[Title/Abstract] OR "LC-MS"[Title/Abstract] OR "Northern blot"[Title/Abstract] OR aminoacylation[Title/Abstract] OR "in vitro transcription"[Title/Abstract] OR "modification detection"[Title/Abstract] OR sequencing[Title/Abstract])',
        github_queries=(
            "tRNA-seq protocol",
            "tRNA LC-MS",
            "tRNA modification detection",
            "aminoacylation assay tRNA",
            "tRNA wet lab",
        ),
        cn_focus="关注从样品制备、tRNA 富集/去修饰、氨酰化测定、Northern blot、LC-MS/MS 到高通量 tRNA-seq 的实验路线与关键质控。",
        en_focus="Covers experimental workflows from sample preparation, tRNA enrichment/demodification, aminoacylation assays, Northern blotting, LC-MS/MS, and high-throughput tRNA-seq to key QC controls.",
    ),
]

CURATED_REPOS = {
    "biology_structure": [
        "junchaoshi/sports1.1",
        "UCSC-LoweLab/tDRnamer",
    ],
    "tools_algorithms": [
        "UCSC-LoweLab/tRNAscan-SE",
        "nedialkova-lab/mim-tRNAseq",
        "merenlab/tRNA-seq-tools",
        "UCSC-LoweLab/tDRnamer",
        "rnabioco/tRNA004",
        "rnabioinfor/TRAC-Seq",
    ],
    "mod_fingerprint_database": [
        "nedialkova-lab/mim-tRNAseq",
        "rnabioco/tRNA004",
        "rnabioinfor/TRAC-Seq",
        "jfallmann/tRNA_ngs_mod_map_call_galaxy",
        "monimaanam/Modomics_Decoder",
    ],
    "wet_lab_experiments": [
        "rnabioco/aa-tRNA-seq",
        "rnabioco/tRNA004",
        "nedialkova-lab/mim-tRNAseq",
        "merenlab/tRNA-seq-tools",
        "rnabioinfor/TRAC-Seq",
    ],
}


def safe_name(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("_")[:120]


def ncbi_get(endpoint: str, params: dict[str, Any]) -> requests.Response:
    params = {
        **params,
        "tool": "codex_trna_resource_collector",
        "email": "anonymous@example.com",
    }
    for attempt in range(4):
        response = requests.get(f"{NCBI_BASE}/{endpoint}", params=params, timeout=40)
        if response.status_code == 429:
            time.sleep(2 + attempt)
            continue
        response.raise_for_status()
        time.sleep(0.35)
        return response
    response.raise_for_status()
    return response


def pubmed_search(query: str, retmax: int = 80) -> list[str]:
    response = ncbi_get(
        "esearch.fcgi",
        {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": retmax,
            "sort": "pub+date",
        },
    )
    return response.json().get("esearchresult", {}).get("idlist", [])


def text_of(node: ET.Element | None) -> str:
    if node is None:
        return ""
    return " ".join("".join(node.itertext()).split())


def parse_pubmed_xml(xml_text: str) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_text)
    records: list[dict[str, Any]] = []
    for article in root.findall(".//PubmedArticle"):
        medline = article.find("MedlineCitation")
        pubmed_data = article.find("PubmedData")
        if medline is None:
            continue
        pmid = text_of(medline.find("PMID"))
        art = medline.find("Article")
        if art is None:
            continue
        title = text_of(art.find("ArticleTitle"))
        journal = text_of(art.find("Journal/Title")) or text_of(art.find("Journal/ISOAbbreviation"))
        abstract = " ".join(text_of(a) for a in art.findall("Abstract/AbstractText")).strip()
        pub_date_node = art.find("Journal/JournalIssue/PubDate")
        year = text_of(pub_date_node.find("Year")) if pub_date_node is not None else ""
        if not year:
            medline_date = text_of(pub_date_node.find("MedlineDate")) if pub_date_node is not None else ""
            year_match = re.search(r"\d{4}", medline_date)
            year = year_match.group(0) if year_match else ""
        month = text_of(pub_date_node.find("Month")) if pub_date_node is not None else ""
        authors = []
        for author in art.findall("AuthorList/Author")[:8]:
            fore = text_of(author.find("ForeName"))
            last = text_of(author.find("LastName"))
            collab = text_of(author.find("CollectiveName"))
            name = " ".join(x for x in [fore, last] if x) or collab
            if name:
                authors.append(name)
        doi = ""
        pmcid = ""
        if pubmed_data is not None:
            for aid in pubmed_data.findall("ArticleIdList/ArticleId"):
                id_type = aid.attrib.get("IdType", "")
                if id_type == "doi":
                    doi = text_of(aid)
                if id_type == "pmc":
                    pmcid = text_of(aid)
        journal_score = HIGH_IMPACT_JOURNALS.get(journal, 0)
        for key, value in HIGH_IMPACT_JOURNALS.items():
            if journal_score == 0 and journal.lower() == key.lower():
                journal_score = value
        try:
            year_i = int(year)
        except ValueError:
            year_i = 0
        records.append(
            {
                "pmid": pmid,
                "pmcid": pmcid,
                "doi": doi,
                "title": title,
                "journal": journal,
                "year": year,
                "month": month,
                "authors": "; ".join(authors),
                "abstract": abstract,
                "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "doi_url": f"https://doi.org/{doi}" if doi else "",
                "journal_tier_score_proxy": journal_score,
                "recency_score": year_i,
            }
        )
    return records


def pubmed_fetch(pmids: list[str]) -> list[dict[str, Any]]:
    if not pmids:
        return []
    response = ncbi_get(
        "efetch.fcgi",
        {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
        },
    )
    return parse_pubmed_xml(response.text)


def select_literature(topic: Topic) -> list[dict[str, Any]]:
    high_query = f"({topic.pubmed_query}) AND {DATE_FILTER} AND ({JOURNAL_FILTER})"
    pmids = pubmed_search(high_query, retmax=120)
    records = pubmed_fetch(pmids)
    if len(records) < 15:
        fallback_query = f"({topic.pubmed_query}) AND {DATE_FILTER}"
        fallback_pmids = pubmed_search(fallback_query, retmax=120)
        seen = {r["pmid"] for r in records}
        records.extend(r for r in pubmed_fetch(fallback_pmids) if r["pmid"] not in seen)
    words = [w.lower() for w in re.findall(r"[A-Za-z0-9-]+", topic.pubmed_query) if len(w) > 2]
    def relevance(record: dict[str, Any]) -> int:
        hay = (record["title"] + " " + record["abstract"] + " " + record["journal"]).lower()
        return sum(1 for w in set(words) if w.lower() in hay)

    for record in records:
        record["topic_relevance_score"] = relevance(record)
        record["selection_score"] = (
            record["journal_tier_score_proxy"] * 10
            + record["recency_score"]
            + record["topic_relevance_score"] * 5
        )
    records.sort(
        key=lambda r: (
            r["selection_score"],
            r["recency_score"],
            r["journal_tier_score_proxy"],
            r["topic_relevance_score"],
        ),
        reverse=True,
    )
    return records[:15]


def github_search(queries: tuple[str, ...], per_page: int = 12) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for query in queries:
        response = requests.get(
            GITHUB_API,
            params={
                "q": f"{query} in:name,description,readme",
                "sort": "stars",
                "order": "desc",
                "per_page": per_page,
            },
            headers={"Accept": "application/vnd.github+json"},
            timeout=40,
        )
        if response.status_code == 403:
            break
        response.raise_for_status()
        for item in response.json().get("items", []):
            merged.setdefault(item.get("full_name", ""), item)
        time.sleep(0.3)
    def repo_relevant(item: dict[str, Any]) -> bool:
        hay = f"{item.get('full_name', '')} {item.get('description') or ''}".lower()
        return bool(
            re.search(r"(^|[^a-z])trna([^a-z]|$)", hay)
            or "transfer rna" in hay
            or "trnascan" in hay
            or "modomics" in hay
            or "mim-trnaseq" in hay
            or "tdrnamer" in hay
            or "aa-trna" in hay
        )

    relevant_items = [item for item in merged.values() if repo_relevant(item)]
    data = sorted(
        relevant_items,
        key=lambda item: (item.get("stargazers_count", 0), item.get("updated_at", "")),
        reverse=True,
    )[:per_page]
    repos = []
    for item in data:
        repos.append(
            {
                "name": item.get("full_name", ""),
                "description": item.get("description") or "",
                "url": item.get("html_url", ""),
                "stars": item.get("stargazers_count", 0),
                "forks": item.get("forks_count", 0),
                "language": item.get("language") or "",
                "updated_at": item.get("updated_at", ""),
                "pushed_at": item.get("pushed_at", ""),
                "license": (item.get("license") or {}).get("spdx_id", ""),
                "topics": ", ".join(item.get("topics") or []),
            }
        )
    return repos


def github_repo_metadata(full_name: str) -> dict[str, Any] | None:
    try:
        response = requests.get(
            f"https://api.github.com/repos/{full_name}",
            headers={"Accept": "application/vnd.github+json"},
            timeout=30,
        )
        if response.status_code != 200:
            return None
        item = response.json()
        return {
            "name": item.get("full_name", full_name),
            "description": item.get("description") or "",
            "url": item.get("html_url", f"https://github.com/{full_name}"),
            "stars": item.get("stargazers_count", 0),
            "forks": item.get("forks_count", 0),
            "language": item.get("language") or "",
            "updated_at": item.get("updated_at", ""),
            "pushed_at": item.get("pushed_at", ""),
            "license": (item.get("license") or {}).get("spdx_id", ""),
            "topics": ", ".join(item.get("topics") or []),
        }
    except Exception:
        return None


def augment_curated_repos(slug: str, repos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = {repo["name"]: repo for repo in repos}
    for full_name in CURATED_REPOS.get(slug, []):
        if full_name not in merged:
            metadata = github_repo_metadata(full_name)
            if metadata:
                merged[full_name] = metadata
            else:
                merged[full_name] = {
                    "name": full_name,
                    "description": "Curated tRNA-related repository; metadata unavailable due to API limits.",
                    "url": f"https://github.com/{full_name}",
                    "stars": 0,
                    "forks": 0,
                    "language": "",
                    "updated_at": "",
                    "pushed_at": "",
                    "license": "",
                    "topics": "",
                }
            time.sleep(0.15)
    return sorted(merged.values(), key=lambda r: (int(r.get("stars") or 0), r.get("updated_at", "")), reverse=True)[:12]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_topic_report(topic: Topic, papers: list[dict[str, Any]], repos: list[dict[str, Any]]) -> str:
    lines = [
        f"# {topic.cn_title}",
        "",
        f"**English title:** {topic.en_title}",
        "",
        "## 中文阐述",
        topic.cn_focus,
        "",
        "## English explanation",
        topic.en_focus,
        "",
        "## PubMed 文献筛选策略 / PubMed selection strategy",
        "- 时间范围：2020-2026；优先高影响力期刊池，若不足 15 篇则以主题相关性补齐。",
        "- 排序代理：期刊分层代理分 + 年份新近度 + 标题/摘要主题相关性；不是 Clarivate JIF 官方数值。",
        "- Date range: 2020-2026; high-impact journal pool first, then relevance fallback if fewer than 15 records.",
        "- Ranking proxy: journal-tier proxy + recency + title/abstract relevance; not official Clarivate JIF values.",
        "",
        "## 最新高影响力文献 / Recent high-impact literature",
    ]
    for i, p in enumerate(papers, 1):
        lines.extend(
            [
                f"{i}. **{p['title']}**",
                f"   - Journal/Year: {p['journal']} ({p['year']})",
                f"   - Authors: {p['authors']}",
                f"   - PMID/PMCID/DOI: {p['pmid']} / {p['pmcid'] or 'NA'} / {p['doi'] or 'NA'}",
                f"   - Link: {p['pubmed_url']}",
                f"   - Why included: high-impact proxy={p['journal_tier_score_proxy']}, relevance={p['topic_relevance_score']}",
            ]
        )
    lines.extend(["", "## GitHub 资料 / GitHub resources"])
    for i, repo in enumerate(repos, 1):
        lines.extend(
            [
                f"{i}. **{repo['name']}** ({repo['stars']} stars, {repo['language']})",
                f"   - {repo['description']}",
                f"   - Updated: {repo['updated_at']}; License: {repo['license'] or 'NA'}",
                f"   - Link: {repo['url']}",
            ]
        )
    return "\n".join(lines) + "\n"


def fetch_oa_package_for_figures(pmcid: str, target: Path, max_members: int = 4) -> list[dict[str, str]]:
    """Download a few image files from the NCBI OA package when available."""
    target.mkdir(parents=True, exist_ok=True)
    extracted: list[dict[str, str]] = []

    # PMC article HTML exposes figure renditions through stable NCBI CDN URLs.
    # This is more reliable in restricted environments than FTP OA packages.
    try:
        article_url = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"
        html = requests.get(article_url, timeout=40).text
        urls = []
        for match in re.finditer(
            r"https://cdn\.ncbi\.nlm\.nih\.gov/pmc/blobs/[^\"'\s<>]+?(?:Fig|fig)[^\"'\s<>]+?\.(?:jpg|jpeg|png|gif)",
            html,
        ):
            url = match.group(0).replace("&amp;", "&")
            if url not in urls:
                urls.append(url)
        for url in urls[:max_members]:
            suffix = Path(url.split("?")[0]).suffix or ".jpg"
            out_file = target / f"{pmcid}_{safe_name(Path(url.split('?')[0]).name)}{suffix if not str(url).lower().endswith(suffix.lower()) else ''}"
            image_response = requests.get(url, timeout=50)
            image_response.raise_for_status()
            out_file.write_bytes(image_response.content)
            extracted.append({"pmcid": pmcid, "source_member": article_url, "source_url": url, "path": str(out_file)})
        if extracted:
            return extracted
    except Exception as exc:
        (target / f"{pmcid}_html_error.txt").write_text(str(exc), encoding="utf-8")

    return extracted

    meta_url = "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi"
    try:
        meta = requests.get(meta_url, params={"id": pmcid}, timeout=30)
        if meta.status_code != 200 or "<error" in meta.text.lower():
            return []
        root = ET.fromstring(meta.text)
        link = None
        for node in root.findall(".//link"):
            if node.attrib.get("format") == "tgz" and node.attrib.get("href"):
                link = node.attrib["href"]
                break
        if not link:
            return []
        if link.startswith("ftp://ftp.ncbi.nlm.nih.gov/"):
            link = link.replace("ftp://ftp.ncbi.nlm.nih.gov/", "https://ftp.ncbi.nlm.nih.gov/", 1)
        tgz_path = target / f"{pmcid}.tgz"
        with requests.get(link, stream=True, timeout=80) as r:
            r.raise_for_status()
            with tgz_path.open("wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 256):
                    if chunk:
                        f.write(chunk)
        with tarfile.open(tgz_path, "r:gz") as tar:
            image_members = [
                m
                for m in tar.getmembers()
                if m.isfile()
                and re.search(r"\.(png|jpg|jpeg|tif|tiff)$", m.name, re.I)
                and "fig" in Path(m.name).name.lower()
            ][:max_members]
            for member in image_members:
                src = tar.extractfile(member)
                if src is None:
                    continue
                out_file = target / f"{pmcid}_{safe_name(Path(member.name).name)}"
                out_file.write_bytes(src.read())
                extracted.append({"pmcid": pmcid, "source_member": member.name, "source_url": link, "path": str(out_file)})
        try:
            tgz_path.unlink()
        except OSError:
            pass
        return extracted
    except Exception as exc:  # best-effort asset harvesting
        (target / f"{pmcid}_error.txt").write_text(str(exc), encoding="utf-8")
        return []


def main() -> None:
    all_manifest: dict[str, Any] = {"topics": []}
    for topic in TOPICS:
        topic_dir = ROOT / topic.folder
        topic_dir.mkdir(exist_ok=True)
        data_dir = topic_dir / "downloaded_resources"
        data_dir.mkdir(exist_ok=True)

        papers = select_literature(topic)
        repos = augment_curated_repos(topic.slug, github_search(topic.github_queries, per_page=12))

        write_csv(data_dir / "pubmed_literature_selected.csv", papers)
        write_csv(data_dir / "github_repositories_selected.csv", repos)
        (data_dir / "pubmed_literature_selected.json").write_text(
            json.dumps(papers, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (data_dir / "github_repositories_selected.json").write_text(
            json.dumps(repos, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        report = write_topic_report(topic, papers, repos)
        (topic_dir / "bilingual_topic_report.md").write_text(report, encoding="utf-8")

        figures = []
        for paper in papers:
            if len(figures) >= 8:
                break
            pmcid = paper.get("pmcid")
            if pmcid:
                figures.extend(fetch_oa_package_for_figures(pmcid, data_dir / "figures", max_members=2))
        (data_dir / "figure_asset_manifest.json").write_text(
            json.dumps(figures, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        all_manifest["topics"].append(
            {
                "slug": topic.slug,
                "folder": topic.folder,
                "cn_title": topic.cn_title,
                "en_title": topic.en_title,
                "paper_count": len(papers),
                "github_repo_count": len(repos),
                "figure_count": len(figures),
            }
        )
        print(f"{topic.slug}: {len(papers)} papers, {len(repos)} repos, {len(figures)} figures")

    (OUT / "collection_manifest.json").write_text(
        json.dumps(all_manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
