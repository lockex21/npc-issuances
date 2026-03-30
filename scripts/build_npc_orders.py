#!/usr/bin/env python3
"""Download NPC Orders PDFs and build Quartz markdown.

Index source: https://privacy.gov.ph/orders-2/
Fetched via the r.jina.ai mirror to bypass Cloudflare.

Each order is:
  - Downloaded as a PDF to cache/orders/pdfs/
  - Text-extracted with pdftotext (OCR fallback via ocrmypdf)
  - Written as a markdown note to content/orders/YYYY/<slug>.md
  - Recorded in data/orders.json

CLI usage:
    python3 scripts/build_npc_orders.py                # full run (skip already-cached)
    python3 scripts/build_npc_orders.py --refresh      # re-download everything
    python3 scripts/build_npc_orders.py --download-only  # PDFs only, no markdown
    python3 scripts/build_npc_orders.py --text-only    # rebuild markdown from cached PDFs
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import build_npc_site as core


# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CACHE_DIR = ROOT / "cache" / "orders"
CONTENT_DIR = ROOT / "content" / "orders"

ORDERS_URL = "http://privacy.gov.ph/orders-2/"
MIRROR_PREFIX = "https://r.jina.ai/http://"
MIRROR_URL = f"{MIRROR_PREFIX}{ORDERS_URL.removeprefix('http://')}"
INDEX_CACHE = CACHE_DIR / "index.md"
DATA_PATH = DATA_DIR / "orders.json"
USER_AGENT = "Mozilla/5.0 (compatible; NPC-Issuance-Wiki/1.0)"

# Section heading as it appears in the Jina markdown mirror.
# The orders page renders "# ORDERS" as an H1 before the entry list.
HEADING = "# ORDERS"

MARKDOWN_MARKER = "Markdown Content:\n"
MONTH_NAME_RE = (
    "January|February|March|April|May|June|July|August|September|"
    "October|November|December"
)

# Matches lines like:
#   NPC BN 18-095[In Re: DMCI Project Developers, Inc.](http://...pdf)
# where the reference code (anything before the bracket) can be empty.
ENTRY_RE = re.compile(
    r"^(?P<reference>.*?)\[(?P<title>[^\]]+)\]\((?P<url>https?://[^)]+\.pdf)\)\s*$",
    re.IGNORECASE,
)

DATE_YMD_RE = re.compile(
    r"\b(?P<year>20\d{2}|19\d{2})[._-](?P<month>\d{1,2})[._-](?P<day>\d{1,2})\b"
)
DATE_MDY_RE = re.compile(
    r"\b(?P<month>\d{1,2})[._-](?P<day>\d{1,2})[._-](?P<year>20\d{2}|19\d{2})\b"
)
DATE_DMY_WORD_RE = re.compile(
    rf"\b(?P<day>\d{{1,2}})\s+(?P<month>{MONTH_NAME_RE})\s+(?P<year>20\d{{2}}|19\d{{2}})\b",
    re.IGNORECASE,
)
DATE_MONTH_WORD_RE = re.compile(
    rf"\b(?P<month>{MONTH_NAME_RE})\s+(?P<day>\d{{1,2}}),\s+(?P<year>20\d{{2}}|19\d{{2}})\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class IndexEntry:
    reference_label: str | None
    short_title: str
    source_url: str
    source_tags_raw: str
    source_tags: list[str]


@dataclass
class OrderRecord:
    title: str
    reference_label: str | None
    source_url: str
    source_tags: list[str]
    issue_date: str | None
    issue_date_iso: str | None
    year: str
    slug: str
    pdf_path: str
    raw_text_path: str
    text_path: str
    markdown_path: str
    excerpt: str
    ocr_used: bool

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


# ---------------------------------------------------------------------------
# Network helpers
# ---------------------------------------------------------------------------

def fetch_text_with_retries(url: str, attempts: int = 5) -> str:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return core.fetch_text(url)
        except urllib.error.HTTPError as exc:
            last_error = exc
            if attempt == attempts:
                break
            wait = 10 * attempt if exc.code == 429 else attempt
            time.sleep(wait)
        except Exception as exc:
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(attempt)
    assert last_error is not None
    raise last_error


def load_or_fetch(path: Path, url: str, refresh: bool) -> str:
    if refresh or not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        text = fetch_text_with_retries(url)
        path.write_text(text, encoding="utf-8")
        return text
    return path.read_text(encoding="utf-8")


def download_pdf(source_url: str, pdf_path: Path, refresh: bool) -> bool:
    """Download a PDF to pdf_path. Returns True on success."""
    if not refresh and pdf_path.exists() and pdf_path.stat().st_size > 0:
        return True
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(
            source_url,
            headers={"User-Agent": USER_AGENT},
        )
        with urllib.request.urlopen(req, timeout=120) as resp, pdf_path.open("wb") as fh:
            shutil.copyfileobj(resp, fh)
        return True
    except Exception as exc:
        print(f"    [download error] {source_url}: {exc}")
        if pdf_path.exists():
            pdf_path.unlink(missing_ok=True)
        return False


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def split_mirror_response(raw_text: str) -> str:
    """Extract the Markdown Content section from a Jina mirror response."""
    _, _, markdown = raw_text.partition(MARKDOWN_MARKER)
    return markdown.strip()


def normalize_reference_label(value: str) -> str | None:
    cleaned = core.normalize_space(value).strip("[]").strip()
    return cleaned or None


def parse_source_tags(raw: str) -> list[str]:
    text = core.normalize_space(raw)
    if not text:
        return []
    # Strip leading "Tags:" or "Tag:"
    text = re.sub(r"^tags?:\s*", "", text, flags=re.IGNORECASE)
    # Tags are separated by semicolons or commas
    parts = [core.normalize_space(p).strip(" .") for p in re.split(r"\s*[;,]\s*", text)]
    deduped: list[str] = []
    seen: set[str] = set()
    for part in parts:
        if not part:
            continue
        key = part.casefold()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(part)
    return deduped


def parse_index_entries(markdown: str) -> list[IndexEntry]:
    """Parse order entries from the Jina-mirrored index page markdown."""
    # Locate the ORDERS section heading — try both with and without # prefix
    idx = -1
    for candidate in (f"\n{HEADING}\n", f"\nORDERS\n"):
        idx = markdown.find(candidate)
        if idx != -1:
            break
    if idx == -1 and markdown.startswith(f"{HEADING}\n"):
        idx = 0
    if idx == -1:
        raise ValueError(
            f"Unable to locate ORDERS section in the mirrored index page. "
            f"Check {INDEX_CACHE} and ensure the page rendered correctly."
        )

    body = markdown[idx:].lstrip("\n")
    entries: list[IndexEntry] = []
    seen_urls: set[str] = set()
    current: dict | None = None

    def flush() -> None:
        nonlocal current
        if not current:
            return
        url = current["source_url"]
        if url in seen_urls:
            current = None
            return
        seen_urls.add(url)
        raw_tags = "\n".join(current["tag_lines"]).strip()
        entries.append(
            IndexEntry(
                reference_label=current["reference_label"],
                short_title=current["short_title"],
                source_url=url,
                source_tags_raw=raw_tags,
                source_tags=parse_source_tags(raw_tags),
            )
        )
        current = None

    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        # Skip the heading itself and any underline markers
        if line in (HEADING, "ORDERS") or re.fullmatch(r"=+|-+", line):
            continue
        match = ENTRY_RE.match(line)
        if not match:
            if current is not None:
                current["tag_lines"].append(line)
            continue
        flush()
        current = {
            "reference_label": normalize_reference_label(match.group("reference")),
            "short_title": core.normalize_space(match.group("title")),
            "source_url": match.group("url"),
            "tag_lines": [],
        }

    flush()
    return entries


# ---------------------------------------------------------------------------
# PDF caching helpers
# ---------------------------------------------------------------------------

def pdf_stem(source_url: str) -> str:
    """Deterministic filename stem for a PDF URL: slugified basename + SHA-1 prefix."""
    basename = urllib.parse.unquote(
        Path(urllib.parse.urlparse(source_url).path).stem
    )
    digest = hashlib.sha1(source_url.encode("utf-8")).hexdigest()[:10]
    return f"{core.slugify(basename)}-{digest}"


# ---------------------------------------------------------------------------
# Date parsing
# ---------------------------------------------------------------------------

def parse_issue_date(entry: IndexEntry, text: str) -> tuple[str | None, str | None]:
    """Infer the issue date from the PDF filename, then from the document text."""
    basename = urllib.parse.unquote(
        Path(urllib.parse.urlparse(entry.source_url).path).name
    )
    sources = [basename, entry.reference_label or "", entry.short_title, text[:4000]]

    # Filename carries YYYY.MM.DD dates most reliably (e.g. 2024.04.18 or 09.04.2024)
    for src in (basename,):
        m = DATE_YMD_RE.search(src)
        if m:
            try:
                dt = datetime(int(m.group("year")), int(m.group("month")), int(m.group("day")))
                return f"{dt.strftime('%B')} {dt.day}, {dt.year}", dt.strftime("%Y-%m-%d")
            except ValueError:
                pass

    for src in (basename,):
        m = DATE_MDY_RE.search(src)
        if m:
            try:
                dt = datetime(int(m.group("year")), int(m.group("month")), int(m.group("day")))
                return f"{dt.strftime('%B')} {dt.day}, {dt.year}", dt.strftime("%Y-%m-%d")
            except ValueError:
                pass

    # Fall back to natural-language dates in the document text
    for src in sources:
        for pattern, fmt_args in [
            (DATE_DMY_WORD_RE, ("day", "month", "year")),
            (DATE_MONTH_WORD_RE, ("month", "day", "year")),
        ]:
            m = pattern.search(src)
            if not m:
                continue
            try:
                day = m.group("day")
                month = m.group("month").title()
                year = m.group("year")
                if fmt_args[0] == "day":
                    dt = datetime.strptime(f"{day} {month} {year}", "%d %B %Y")
                else:
                    dt = datetime.strptime(f"{month} {day} {year}", "%B %d %Y")
                return f"{dt.strftime('%B')} {dt.day}, {dt.year}", dt.strftime("%Y-%m-%d")
            except ValueError:
                pass

    return None, None


# ---------------------------------------------------------------------------
# Markdown building
# ---------------------------------------------------------------------------

def build_display_title(reference_label: str | None, short_title: str) -> str:
    if reference_label and short_title:
        if short_title.casefold().startswith(reference_label.casefold()):
            return short_title
        return f"{reference_label}: {short_title}"
    return short_title or reference_label or "NPC Order"


def build_excerpt(text: str, fallback: str) -> str:
    for para in re.split(r"\n\s*\n", text):
        para = core.normalize_space(para)
        if (
            len(para) >= 80
            and not para.startswith(">")
            and not para.lower().startswith("page ")
            and not para.lower().startswith("npc_")
        ):
            return textwrap.shorten(para, width=280, placeholder="...")
    return textwrap.shorten(core.normalize_space(fallback), width=280, placeholder="...")


def build_markdown(record: OrderRecord, cleaned_text: str) -> str:
    lines = [
        "---",
        f"title: {json.dumps(record.title, ensure_ascii=False)}",
        f"description: {json.dumps(record.excerpt, ensure_ascii=False)}",
        "tags:",
        '  - "order"',
        '  - "type/order"',
        f'  - "year/{record.year}"',
        '  - "npc-case"',
        "draft: false",
        "---",
        "",
        "## Source",
        f"- Reference: {record.reference_label or 'None listed on source page'}",
        f"- Official PDF: {record.source_url}",
        f"- Source page: {ORDERS_URL}",
        f"- Issue date: {record.issue_date or 'Unknown'}",
        f"- OCR used during extraction: {'yes' if record.ocr_used else 'no'}",
    ]
    if record.source_tags:
        lines.extend(
            [
                "",
                "## Source Tags",
                *[f"- {tag}" for tag in record.source_tags],
            ]
        )
    lines.extend(
        [
            "",
            "## Order Text",
            cleaned_text.strip(),
            "",
        ]
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def build_records(refresh: bool) -> list[OrderRecord]:
    """Full pipeline: fetch index → download PDFs → extract text → write markdown."""
    raw_index = load_or_fetch(INDEX_CACHE, MIRROR_URL, refresh=refresh)
    index_markdown = split_mirror_response(raw_index)
    entries = parse_index_entries(index_markdown)
    print(f"Parsed {len(entries)} order entries from the index page")

    pdf_dir = CACHE_DIR / "pdfs"
    raw_dir = CACHE_DIR / "text_raw"
    text_dir = CACHE_DIR / "text"
    for d in (pdf_dir, raw_dir, text_dir):
        d.mkdir(parents=True, exist_ok=True)

    records: list[OrderRecord] = []
    seen_slugs: set[str] = set()

    for i, entry in enumerate(entries, 1):
        stem = pdf_stem(entry.source_url)
        pdf_path = pdf_dir / f"{stem}.pdf"
        raw_txt_path = raw_dir / f"{stem}.txt"
        clean_txt_path = text_dir / f"{stem}.txt"

        label = entry.reference_label or entry.short_title[:60]
        print(f"  [{i}/{len(entries)}] {label}")

        # --- Download PDF ---
        ok = download_pdf(entry.source_url, pdf_path, refresh=refresh)
        if not ok or not pdf_path.exists():
            print(f"    [skip] could not download PDF")
            continue

        # --- Extract / cache text ---
        if refresh or not clean_txt_path.exists():
            _, cleaned_text, ocr_used = core.extract_text(pdf_path, raw_txt_path, clean_txt_path)
        else:
            cleaned_text = clean_txt_path.read_text(encoding="utf-8")
            # Check if OCR sidecar exists as a proxy for whether OCR was used
            ocr_dir = CACHE_DIR / "ocr"
            ocr_used = any(ocr_dir.glob(f"{stem}*")) if ocr_dir.exists() else False

        # --- Infer metadata ---
        issue_date, issue_date_iso = parse_issue_date(entry, cleaned_text)
        year = issue_date_iso[:4] if issue_date_iso else "undated"

        display_title = build_display_title(entry.reference_label, entry.short_title)
        base_slug = core.slugify(display_title)
        slug = base_slug
        n = 2
        while slug in seen_slugs:
            slug = f"{base_slug}-{n}"
            n += 1
        seen_slugs.add(slug)

        markdown_path = CONTENT_DIR / year / f"{slug}.md"
        excerpt = build_excerpt(cleaned_text, display_title)

        record = OrderRecord(
            title=display_title,
            reference_label=entry.reference_label,
            source_url=entry.source_url,
            source_tags=entry.source_tags,
            issue_date=issue_date,
            issue_date_iso=issue_date_iso,
            year=year,
            slug=slug,
            pdf_path=str(pdf_path.relative_to(ROOT)),
            raw_text_path=str(raw_txt_path.relative_to(ROOT)),
            text_path=str(clean_txt_path.relative_to(ROOT)),
            markdown_path=str(markdown_path.relative_to(ROOT)),
            excerpt=excerpt,
            ocr_used=ocr_used,
        )
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(build_markdown(record, cleaned_text), encoding="utf-8")
        records.append(record)

    return sorted(
        records,
        key=lambda r: (r.issue_date_iso or "", r.reference_label or "", r.title),
        reverse=True,
    )


def download_only(refresh: bool) -> None:
    """Fetch index and download PDFs; skip text extraction and markdown."""
    raw_index = load_or_fetch(INDEX_CACHE, MIRROR_URL, refresh=refresh)
    index_markdown = split_mirror_response(raw_index)
    entries = parse_index_entries(index_markdown)
    print(f"Parsed {len(entries)} order entries")

    pdf_dir = CACHE_DIR / "pdfs"
    pdf_dir.mkdir(parents=True, exist_ok=True)

    for i, entry in enumerate(entries, 1):
        stem = pdf_stem(entry.source_url)
        pdf_path = pdf_dir / f"{stem}.pdf"
        label = entry.reference_label or entry.short_title[:60]
        if not refresh and pdf_path.exists() and pdf_path.stat().st_size > 0:
            print(f"  [{i}/{len(entries)}] [skip] {label}")
            continue
        print(f"  [{i}/{len(entries)}] [download] {label}")
        download_pdf(entry.source_url, pdf_path, refresh=refresh)

    pdfs_found = sum(1 for p in pdf_dir.glob("*.pdf") if p.stat().st_size > 0)
    print(f"PDFs cached: {pdfs_found} in {pdf_dir}")


def text_only() -> None:
    """Rebuild text extraction and markdown from already-cached PDFs."""
    pdf_dir = CACHE_DIR / "pdfs"
    raw_dir = CACHE_DIR / "text_raw"
    text_dir = CACHE_DIR / "text"
    for d in (raw_dir, text_dir):
        d.mkdir(parents=True, exist_ok=True)

    raw_index = load_or_fetch(INDEX_CACHE, MIRROR_URL, refresh=False)
    index_markdown = split_mirror_response(raw_index)
    entries = parse_index_entries(index_markdown)

    seen_slugs: set[str] = set()
    records: list[OrderRecord] = []

    for i, entry in enumerate(entries, 1):
        stem = pdf_stem(entry.source_url)
        pdf_path = pdf_dir / f"{stem}.pdf"
        if not pdf_path.exists():
            print(f"  [{i}/{len(entries)}] [missing pdf] {entry.reference_label or entry.short_title[:40]}")
            continue

        raw_txt_path = raw_dir / f"{stem}.txt"
        clean_txt_path = text_dir / f"{stem}.txt"
        label = entry.reference_label or entry.short_title[:60]
        print(f"  [{i}/{len(entries)}] {label}")

        _, cleaned_text, ocr_used = core.extract_text(pdf_path, raw_txt_path, clean_txt_path)

        issue_date, issue_date_iso = parse_issue_date(entry, cleaned_text)
        year = issue_date_iso[:4] if issue_date_iso else "undated"
        display_title = build_display_title(entry.reference_label, entry.short_title)
        base_slug = core.slugify(display_title)
        slug = base_slug
        n = 2
        while slug in seen_slugs:
            slug = f"{base_slug}-{n}"
            n += 1
        seen_slugs.add(slug)

        markdown_path = CONTENT_DIR / year / f"{slug}.md"
        excerpt = build_excerpt(cleaned_text, display_title)
        record = OrderRecord(
            title=display_title,
            reference_label=entry.reference_label,
            source_url=entry.source_url,
            source_tags=entry.source_tags,
            issue_date=issue_date,
            issue_date_iso=issue_date_iso,
            year=year,
            slug=slug,
            pdf_path=str(pdf_path.relative_to(ROOT)),
            raw_text_path=str(raw_txt_path.relative_to(ROOT)),
            text_path=str(clean_txt_path.relative_to(ROOT)),
            markdown_path=str(markdown_path.relative_to(ROOT)),
            excerpt=excerpt,
            ocr_used=ocr_used,
        )
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(build_markdown(record, cleaned_text), encoding="utf-8")
        records.append(record)

    records = sorted(
        records,
        key=lambda r: (r.issue_date_iso or "", r.reference_label or "", r.title),
        reverse=True,
    )
    write_json(records)
    build_index_pages(records)
    print(f"Generated {len(records)} orders under {CONTENT_DIR}")


def write_json(records: list[OrderRecord]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "source_page": ORDERS_URL,
        "count": len(records),
        "records": [r.as_dict() for r in records],
    }
    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {DATA_PATH} ({len(records)} records)")


def build_index_pages(records: list[OrderRecord]) -> None:
    year_groups: dict[str, list[OrderRecord]] = defaultdict(list)
    for record in records:
        year_groups[record.year].append(record)

    index_lines = [
        "Generated notes for the NPC orders corpus from the official website.",
        "",
        f"- Corpus size: **{len(records)}** orders",
        f"- Source page: {ORDERS_URL}",
        "",
        "## Years",
        *[
            f"- [[orders/{year}/index|{year}]] ({len(items)} orders)"
            for year, items in sorted(year_groups.items(), reverse=True)
        ],
    ]
    core.render_index_page(
        CONTENT_DIR / "index.md",
        "Orders",
        "Browse NPC orders by year.",
        index_lines,
        default_manual="Add your own reading guide for NPC orders here.",
    )

    for year, items in sorted(year_groups.items(), reverse=True):
        lines = [
            f"Generated notes for **{year}** NPC orders.",
            "",
            "## Notes",
            *[
                f"- {core.note_link(record.markdown_path, record.title)}"
                for record in sorted(
                    items,
                    key=lambda r: (r.issue_date_iso or "", r.title),
                    reverse=True,
                )
            ],
        ]
        core.render_index_page(
            CONTENT_DIR / year / "index.md",
            f"{year} Orders",
            f"NPC orders for {year}.",
            lines,
            default_manual=f"Add {year}-specific notes for NPC orders here.",
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download NPC Orders PDFs and build Quartz markdown notes."
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Re-download PDFs and re-extract text even if cached.",
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Download PDFs only; skip text extraction and markdown generation.",
    )
    parser.add_argument(
        "--text-only",
        action="store_true",
        help="Rebuild text extraction and markdown from already-cached PDFs.",
    )
    args = parser.parse_args()

    if args.download_only:
        download_only(refresh=args.refresh)
        return 0

    if args.text_only:
        text_only()
        return 0

    records = build_records(refresh=args.refresh)
    write_json(records)
    build_index_pages(records)
    print(f"Generated {len(records)} orders under {CONTENT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
