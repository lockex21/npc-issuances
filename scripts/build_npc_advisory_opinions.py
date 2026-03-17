#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import textwrap
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import build_npc_site as core


ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / "cache" / "advisory_opinions"
PDF_DIR = CACHE_DIR / "pdfs"
RAW_TEXT_DIR = CACHE_DIR / "text_raw"
TEXT_DIR = CACHE_DIR / "text"
OCR_DIR = CACHE_DIR / "ocr"
INDEX_DIR = CACHE_DIR / "index_pages"
CONTENT_DIR = ROOT / "content" / "advisory-opinions"
DATA_PATH = ROOT / "data" / "advisory_opinions.json"
SEARCH_URL = "https://r.jina.ai/http://privacy.gov.ph/wp-json/wp/v2/media"
SEARCH_TERM = "Opinion No."
PAGE_SIZE = 100

REF_RE = re.compile(
    r"(?:adv(?:i|si)ory|advisory)[-_ ]*opinion[-_ ]*no\.?[-_ ]*(?P<year>(?:19|20)\d{2})[-_ ]*(?P<num>\d{1,4})",
    re.IGNORECASE,
)


@dataclass
class AdvisoryOpinion:
    title: str
    reference_label: str
    year: str
    slug: str
    source_url: str
    pdf_path: str
    raw_text_path: str
    text_path: str
    markdown_path: str
    ocr_used: bool
    excerpt: str

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


def parse_mirror_json(raw_text: str) -> Any:
    marker = "Markdown Content:\n"
    if marker in raw_text:
        payload = raw_text.split(marker, 1)[1].strip()
    else:
        payload = raw_text.strip()
    return json.loads(payload)


def fetch_media_page(page: int) -> list[dict[str, Any]]:
    query = urllib.parse.urlencode(
        {
            "search": SEARCH_TERM,
            "per_page": str(PAGE_SIZE),
            "page": str(page),
            "_fields": "id,date,title,mime_type,source_url",
        }
    )
    url = f"{SEARCH_URL}?{query}"
    raw = core.fetch_text(url)
    payload = parse_mirror_json(raw)
    if isinstance(payload, dict):
        # WordPress returns an object for out-of-range pages.
        return []
    if not isinstance(payload, list):
        return []
    return [item for item in payload if isinstance(item, dict)]


def extract_reference(url: str, title: str) -> tuple[str | None, str | None]:
    for source in (urllib.parse.unquote(url), title):
        match = REF_RE.search(source)
        if not match:
            continue
        year = match.group("year")
        num = match.group("num").zfill(3)
        return f"Advisory Opinion No. {year}-{num}", year
    return None, None


def is_advisory_opinion(entry: dict[str, Any]) -> bool:
    source_url = str(entry.get("source_url", ""))
    title = str(entry.get("title", {}).get("rendered", ""))
    if str(entry.get("mime_type", "")).lower() != "application/pdf":
        return False
    if not source_url.lower().endswith(".pdf"):
        return False
    return bool(REF_RE.search(source_url) or REF_RE.search(title))


def clean_title(raw_title: str, reference_label: str | None) -> str:
    title = core.normalize_space(html.unescape(raw_title))
    if title:
        return title
    return reference_label or "Advisory Opinion"


def excerpt_from_text(text: str, fallback: str) -> str:
    paragraphs = [core.normalize_space(p) for p in re.split(r"\n\s*\n", text) if core.normalize_space(p)]
    for paragraph in paragraphs:
        if len(paragraph) >= 80:
            return textwrap.shorten(paragraph, width=260, placeholder="...")
    return textwrap.shorten(core.normalize_space(fallback), width=260, placeholder="...")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def build_markdown(record: AdvisoryOpinion, cleaned_text: str) -> str:
    lines = [
        "---",
        f"title: {json.dumps(record.title, ensure_ascii=False)}",
        f"description: {json.dumps(record.excerpt, ensure_ascii=False)}",
        "tags:",
        '  - "issuance"',
        '  - "type/advisory-opinion"',
        f'  - "year/{record.year}"',
        "draft: false",
        "---",
        "",
        "## Source",
        f"- Reference: {record.reference_label}",
        f"- Official PDF: {record.source_url}",
        f"- OCR used during extraction: {'yes' if record.ocr_used else 'no'}",
        "",
        "## Text",
        cleaned_text.strip(),
        "",
    ]
    return "\n".join(lines)


def collect_entries() -> list[dict[str, Any]]:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, Any]] = []
    for page in range(1, 30):
        page_entries = fetch_media_page(page)
        (INDEX_DIR / f"page-{page}.json").write_text(json.dumps(page_entries, ensure_ascii=False, indent=2), encoding="utf-8")
        if not page_entries:
            break
        entries.extend(page_entries)
        if len(page_entries) < PAGE_SIZE:
            break

    filtered = [entry for entry in entries if is_advisory_opinion(entry)]
    deduped: dict[str, dict[str, Any]] = {}
    for entry in filtered:
        source_url = entry["source_url"]
        existing = deduped.get(source_url)
        if not existing or int(entry.get("id", 0)) > int(existing.get("id", 0)):
            deduped[source_url] = entry
    return list(deduped.values())


def run(refresh: bool) -> list[AdvisoryOpinion]:
    # Reuse the existing extraction pipeline with advisory-opinion-specific cache directories.
    core.PDF_DIR = PDF_DIR
    core.RAW_TEXT_DIR = RAW_TEXT_DIR
    core.TEXT_DIR = TEXT_DIR
    core.OCR_DIR = OCR_DIR

    entries = collect_entries()
    seen_slugs: set[str] = set()
    records: list[AdvisoryOpinion] = []

    for entry in sorted(entries, key=lambda item: str(item.get("source_url", ""))):
        source_url = str(entry["source_url"])
        title_raw = str(entry.get("title", {}).get("rendered", "")).strip()
        reference_label, ref_year = extract_reference(source_url, title_raw)
        if not reference_label:
            continue
        year = ref_year or "undated"

        basename = urllib.parse.unquote(Path(urllib.parse.urlparse(source_url).path).name)
        digest = hashlib.sha1(source_url.encode("utf-8")).hexdigest()[:10]
        filename = f"{Path(basename).stem}-{digest}.pdf"

        pdf_path = PDF_DIR / filename
        raw_text_path = RAW_TEXT_DIR / f"{Path(filename).stem}.txt"
        cleaned_text_path = TEXT_DIR / f"{Path(filename).stem}.txt"
        if refresh or not pdf_path.exists():
            core.download_file(source_url, pdf_path)

        _, cleaned_text, ocr_used = core.extract_text(pdf_path, raw_text_path, cleaned_text_path)
        title = clean_title(title_raw, reference_label)
        base_slug = core.slugify(f"{reference_label} {title}")
        slug = base_slug
        n = 2
        while slug in seen_slugs:
            slug = f"{base_slug}-{n}"
            n += 1
        seen_slugs.add(slug)

        md_path = CONTENT_DIR / year / f"{slug}.md"
        excerpt = excerpt_from_text(cleaned_text, title)
        record = AdvisoryOpinion(
            title=title,
            reference_label=reference_label,
            year=year,
            slug=slug,
            source_url=source_url,
            pdf_path=rel(pdf_path),
            raw_text_path=rel(raw_text_path),
            text_path=rel(cleaned_text_path),
            markdown_path=rel(md_path),
            ocr_used=ocr_used,
            excerpt=excerpt,
        )
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(build_markdown(record, cleaned_text), encoding="utf-8")
        records.append(record)

    payload = {
        "source": SEARCH_URL,
        "query": SEARCH_TERM,
        "count": len(records),
        "records": [record.as_dict() for record in records],
    }
    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Build markdown corpus for NPC Advisory Opinions.")
    parser.add_argument("--refresh", action="store_true", help="Re-download PDFs even when already cached.")
    args = parser.parse_args()
    records = run(refresh=args.refresh)
    print(f"Generated {len(records)} advisory opinion markdown files under {CONTENT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
