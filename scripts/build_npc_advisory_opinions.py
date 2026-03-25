#!/usr/bin/env python3
"""Build markdown corpus for NPC Advisory Opinions.

Primary data source: the advisory-opinions index page on the NPC website,
which renders a paginated HTML table containing every published advisory
opinion with its PDF link, issue date, subject, and tags.

The previous approach queried the WordPress media-library API, which
returned an incomplete set (only ~361 of ~385 opinions, badly
under-representing 2018 and 2019).
"""
from __future__ import annotations

import argparse
import hashlib
import html as html_mod
import json
import re
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import build_npc_site as core


ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / "cache" / "advisory_opinions"
PDF_DIR = CACHE_DIR / "pdfs"
RAW_TEXT_DIR = CACHE_DIR / "text_raw"
TEXT_DIR = CACHE_DIR / "text"
OCR_DIR = CACHE_DIR / "ocr"
INDEX_CACHE = CACHE_DIR / "index.html"
CONTENT_DIR = ROOT / "content" / "advisory-opinions"
DATA_PATH = ROOT / "data" / "advisory_opinions.json"
INDEX_URL = "https://privacy.gov.ph/advisory-opinions/"
USER_AGENT = "Mozilla/5.0 (compatible; NPC-Issuance-Wiki/1.0)"

REF_RE = re.compile(
    r"(?:adv(?:i|si)ory|advisory)[-_ ]*opinion[-_ ]*no\.?[-_ ]*"
    r"(?P<year>(?:19|20)\d{2})[-_ ]*(?P<num>\d{1,4})",
    re.IGNORECASE,
)


@dataclass
class IndexEntry:
    """An entry parsed from the NPC advisory-opinions HTML table."""
    reference_label: str
    year: str
    number: str
    source_url: str
    link_text: str
    subject: str
    issue_date: str
    tags: str


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
    subject: str = ""
    issue_date: str = ""
    tags: str = ""

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


# ---------------------------------------------------------------------------
# Index page fetching and parsing
# ---------------------------------------------------------------------------

def fetch_index_html(refresh: bool = False) -> str:
    """Fetch the advisory-opinions HTML page from the NPC website.

    The full table (all ~385 rows) is rendered server-side; the client-side
    pagination is purely cosmetic JavaScript.  A single fetch gives us every
    entry.
    """
    if not refresh and INDEX_CACHE.exists():
        return INDEX_CACHE.read_text(encoding="utf-8")

    INDEX_CACHE.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(INDEX_URL, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                html_text = resp.read().decode("utf-8")
            INDEX_CACHE.write_text(html_text, encoding="utf-8")
            return html_text
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < 3:
                time.sleep(2 * attempt)
    assert last_error is not None
    raise last_error


def parse_index_html(html_text: str) -> list[IndexEntry]:
    """Extract advisory opinion entries from the HTML table."""
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html_text, re.DOTALL)
    entries: list[IndexEntry] = []
    seen_refs: dict[str, IndexEntry] = {}

    for row in rows:
        link_match = re.search(
            r'<a[^>]+href="([^"]*\.pdf)"[^>]*>([^<]*)</a>', row, re.IGNORECASE
        )
        if not link_match:
            continue
        pdf_url = link_match.group(1)
        link_text = core.normalize_space(html_mod.unescape(link_match.group(2)))

        # Make URL absolute.
        if pdf_url.startswith("/"):
            pdf_url = "https://privacy.gov.ph" + pdf_url

        # Extract reference number from link text or URL.
        ref_match = REF_RE.search(link_text) or REF_RE.search(
            urllib.parse.unquote(pdf_url)
        )
        if not ref_match:
            continue

        year = ref_match.group("year")
        num = ref_match.group("num").zfill(3)
        ref_label = f"Advisory Opinion No. {year}-{num}"

        # Extract "Re:" subject.
        re_match = re.search(r"Re:\s*(.*?)(?:<|Tags:|$)", row, re.DOTALL)
        subject = ""
        if re_match:
            subject = re.sub(r"<[^>]+>", "", re_match.group(1)).strip()
            subject = core.normalize_space(subject)

        # Extract issue date from the second <td>.
        tds = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
        issue_date = ""
        if len(tds) >= 2:
            date_text = re.sub(r"<[^>]+>", "", tds[1]).strip()
            if re.match(r"\d{2}/\d{2}/\d{4}", date_text):
                issue_date = date_text

        # Extract tags.
        tags = ""
        tags_match = re.search(r"Tags:\s*(.*?)(?:</|$)", row, re.DOTALL)
        if tags_match:
            tags = re.sub(r"<[^>]+>", "", tags_match.group(1)).strip().rstrip(".")
            tags = core.normalize_space(tags)

        entry = IndexEntry(
            reference_label=ref_label,
            year=year,
            number=num,
            source_url=pdf_url,
            link_text=link_text,
            subject=subject,
            issue_date=issue_date,
            tags=tags,
        )

        # Deduplicate by reference label (keep first occurrence — the NPC
        # page lists most-recently-uploaded first, which is preferred).
        if ref_label not in seen_refs:
            seen_refs[ref_label] = entry
            entries.append(entry)

    return entries


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clean_title(link_text: str, subject: str, reference_label: str) -> str:
    """Build a readable title from available metadata."""
    if subject:
        return f"{reference_label} — {subject}"
    title = core.normalize_space(link_text)
    if title:
        return title
    return reference_label


def excerpt_from_text(text: str, fallback: str) -> str:
    paragraphs = [
        core.normalize_space(p)
        for p in re.split(r"\n\s*\n", text)
        if core.normalize_space(p)
    ]
    for paragraph in paragraphs:
        if len(paragraph) >= 80:
            return textwrap.shorten(paragraph, width=260, placeholder="...")
    return textwrap.shorten(
        core.normalize_space(fallback), width=260, placeholder="..."
    )


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
    ]
    if record.issue_date:
        lines.append(f"- Issue date: {record.issue_date}")
    if record.subject:
        lines.append(f"- Subject: {record.subject}")
    if record.tags:
        lines.append(f"- Tags: {record.tags}")
    lines.append(
        f"- OCR used during extraction: {'yes' if record.ocr_used else 'no'}"
    )
    lines += [
        "",
        "## Text",
        cleaned_text.strip(),
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main build pipeline
# ---------------------------------------------------------------------------

def run(
    refresh: bool = False,
    download_only: bool = False,
    text_only: bool = False,
) -> list[AdvisoryOpinion]:
    """Build the advisory-opinions corpus.

    Parameters
    ----------
    refresh : bool
        Re-download PDFs even when already cached.
    download_only : bool
        Only fetch the index and download PDFs; skip text extraction and
        markdown generation.
    text_only : bool
        Skip PDF downloads; only (re-)extract text and rebuild markdown for
        PDFs already on disk.
    """
    # Point core helpers at advisory-opinion-specific cache directories.
    core.PDF_DIR = PDF_DIR
    core.RAW_TEXT_DIR = RAW_TEXT_DIR
    core.TEXT_DIR = TEXT_DIR
    core.OCR_DIR = OCR_DIR

    # --- Phase 0: fetch and parse the index page --------------------------
    print("Fetching advisory-opinions index page …")
    html_text = fetch_index_html(refresh=refresh)
    entries = parse_index_html(html_text)
    print(f"  {len(entries)} unique advisory opinions found in index.")

    # --- Phase 1: download PDFs -------------------------------------------
    if not text_only:
        print("Downloading PDFs …")
        downloaded = 0
        skipped = 0
        failed: list[str] = []
        for entry in entries:
            pdf_path = _pdf_path_for(entry)
            if not refresh and pdf_path.exists():
                skipped += 1
                continue
            try:
                core.download_file(entry.source_url, pdf_path)
                downloaded += 1
            except Exception as exc:
                print(f"  WARN: failed to download {entry.reference_label}: {exc}")
                failed.append(entry.reference_label)
        print(
            f"  {downloaded} downloaded, {skipped} already cached"
            + (f", {len(failed)} failed" if failed else "")
        )
        if download_only:
            return []

    # --- Phase 2: extract text and generate markdown ----------------------
    print("Extracting text and building markdown …")
    seen_slugs: set[str] = set()
    records: list[AdvisoryOpinion] = []

    for entry in sorted(entries, key=lambda e: (e.year, e.number)):
        pdf_path = _pdf_path_for(entry)
        if not pdf_path.exists():
            print(f"  SKIP (no PDF): {entry.reference_label}")
            continue

        stem = pdf_path.stem
        raw_text_path = RAW_TEXT_DIR / f"{stem}.txt"
        cleaned_text_path = TEXT_DIR / f"{stem}.txt"

        _, cleaned_text, ocr_used = core.extract_text(
            pdf_path, raw_text_path, cleaned_text_path
        )

        title = clean_title(entry.link_text, entry.subject, entry.reference_label)
        base_slug = core.slugify(f"{entry.reference_label} {entry.subject or title}")
        slug = base_slug
        n = 2
        while slug in seen_slugs:
            slug = f"{base_slug}-{n}"
            n += 1
        seen_slugs.add(slug)

        md_path = CONTENT_DIR / entry.year / f"{slug}.md"
        excerpt = excerpt_from_text(cleaned_text, title)
        record = AdvisoryOpinion(
            title=title,
            reference_label=entry.reference_label,
            year=entry.year,
            slug=slug,
            source_url=entry.source_url,
            pdf_path=rel(pdf_path),
            raw_text_path=rel(raw_text_path),
            text_path=rel(cleaned_text_path),
            markdown_path=rel(md_path),
            ocr_used=ocr_used,
            excerpt=excerpt,
            subject=entry.subject,
            issue_date=entry.issue_date,
            tags=entry.tags,
        )
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(build_markdown(record, cleaned_text), encoding="utf-8")
        records.append(record)

    # --- Phase 3: write data JSON -----------------------------------------
    payload = {
        "source": INDEX_URL,
        "count": len(records),
        "records": [record.as_dict() for record in records],
    }
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return records


def _pdf_path_for(entry: IndexEntry) -> Path:
    """Deterministic local PDF path for an index entry."""
    basename = urllib.parse.unquote(
        Path(urllib.parse.urlparse(entry.source_url).path).name
    )
    digest = hashlib.sha1(entry.source_url.encode("utf-8")).hexdigest()[:10]
    filename = f"{Path(basename).stem}-{digest}.pdf"
    return PDF_DIR / filename


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build markdown corpus for NPC Advisory Opinions."
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Re-download PDFs and re-fetch the index even when already cached.",
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Only fetch the index and download PDFs; skip text extraction.",
    )
    parser.add_argument(
        "--text-only",
        action="store_true",
        help="Skip PDF downloads; only rebuild text and markdown from cached PDFs.",
    )
    args = parser.parse_args()

    if args.download_only and args.text_only:
        parser.error("--download-only and --text-only are mutually exclusive.")

    records = run(
        refresh=args.refresh,
        download_only=args.download_only,
        text_only=args.text_only,
    )
    if records:
        print(f"Generated {len(records)} advisory opinion markdown files under {CONTENT_DIR}")
    elif args.download_only:
        print("PDF download phase complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
