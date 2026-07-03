#!/usr/bin/env python3
from __future__ import annotations

import argparse
import email.utils
import hashlib
import json
import re
import textwrap
import time
import urllib.error
import urllib.parse
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import build_npc_site as core


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CACHE_DIR = ROOT / "cache"
CONTENT_DIR = ROOT / "content"
CASE_OVERRIDES_JSON = DATA_DIR / "case_overrides.json"
MIRROR_PREFIX = "https://r.jina.ai/http://"
MARKDOWN_MARKER = "Markdown Content:\n"
MONTH_NAME_RE = (
    "January|February|March|April|May|June|July|August|September|October|November|December"
)
ENTRY_RE = re.compile(r"^(?P<reference>.*?)\[(?P<title>[^\]]+)\]\((?P<url>https?://[^)]+\.pdf)\)\s*$", re.IGNORECASE)
PDF_LINK_RE = re.compile(r"\[[^\]]+\]\((https?://[^)]+\.pdf)\)", re.IGNORECASE)
NOISE_LINE_RE = re.compile(
    r"^(?:"
    r"republic of the philippines|"
    r"national privacy commission|"
    r"page \d+ ?of \d+|"
    r"npc_\S.*|"                                    # NPC document codes (NPC_OPC_ADJU_DCSN-V1.0 …)
    r"url:\s*https?//www\.privacy\.gov\.ph.*|"
    r"\d+(?:st|nd|rd|th) floor,.*|"                # any NPC floor/address line
    r"delegation building,.*|"
    r"picc complex,.*|"
    r"vicente sotto avenue,.*|"
    r"info@privacy\.gov\.ph|"
    r"tel no\..*|"
    r"email add:.*"
    r")$",
    re.IGNORECASE,
)
DATE_MDY_RE = re.compile(r"\b(?P<month>\d{1,2})[._-](?P<day>\d{1,2})[._-](?P<year>20\d{2}|19\d{2})\b")
DATE_YMD_RE = re.compile(r"\b(?P<year>20\d{2}|19\d{2})[._-](?P<month>\d{1,2})[._-](?P<day>\d{1,2})\b")
DATE_DMY_WORD_RE = re.compile(
    rf"\b(?P<day>\d{{1,2}})\s+(?P<month>{MONTH_NAME_RE})\s+(?P<year>20\d{{2}}|19\d{{2}})\b",
    re.IGNORECASE,
)
DATE_MONTH_WORD_RE = re.compile(
    rf"\b(?P<month>{MONTH_NAME_RE})\s+(?P<day>\d{{1,2}}),\s+(?P<year>20\d{{2}}|19\d{{2}})\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class CorpusConfig:
    key: str
    heading: str
    title: str
    description: str
    official_url: str
    folder: str
    body_heading: str
    singular: str
    tag: str

    @property
    def mirror_url(self) -> str:
        return mirror_url(self.official_url)

    @property
    def cache_dir(self) -> Path:
        return CACHE_DIR / self.folder

    @property
    def raw_dir(self) -> Path:
        return self.cache_dir / "text_raw"

    @property
    def text_dir(self) -> Path:
        return self.cache_dir / "text"

    @property
    def index_cache_path(self) -> Path:
        return self.cache_dir / "index.md"

    @property
    def data_path(self) -> Path:
        return DATA_DIR / f"{self.folder}.json"

    @property
    def content_dir(self) -> Path:
        return CONTENT_DIR / self.folder


@dataclass
class SourceEntry:
    reference_label: str | None
    short_title: str
    source_url: str
    source_tags_raw: str
    source_tags: list[str]


@dataclass
class CaseRecord:
    title: str
    short_title: str
    reference_label: str | None
    source_url: str
    source_tags_raw: str
    source_tags: list[str]
    issue_date: str | None
    issue_date_iso: str | None
    published_time: str | None
    published_time_iso: str | None
    page_count: int | None
    year: str
    slug: str
    raw_text_path: str
    text_path: str
    markdown_path: str
    excerpt: str

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


CORPORA: dict[str, CorpusConfig] = {
    "decisions": CorpusConfig(
        key="decisions",
        heading="DECISIONS",
        title="Decisions",
        description="Browse NPC decisions by year.",
        official_url="http://privacy.gov.ph/decisions-2/",
        folder="decisions",
        body_heading="Decision Text",
        singular="decision",
        tag="decision",
    ),
    "resolutions": CorpusConfig(
        key="resolutions",
        heading="RESOLUTIONS",
        title="Resolutions",
        description="Browse NPC resolutions by year.",
        official_url="http://privacy.gov.ph/resolutions/",
        folder="resolutions",
        body_heading="Resolution Text",
        singular="resolution",
        tag="resolution",
    ),
}

CASE_OVERRIDE_META_KEYS = {"preserve_existing_markdown"}


def mirror_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    rebuilt = urllib.parse.urlunsplit(("http", parsed.netloc, parsed.path, parsed.query, parsed.fragment))
    return f"{MIRROR_PREFIX}{rebuilt.removeprefix('http://')}"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_case_overrides() -> dict[str, dict[str, dict[str, Any]]]:
    if not CASE_OVERRIDES_JSON.exists():
        return {}

    payload = json.loads(CASE_OVERRIDES_JSON.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{CASE_OVERRIDES_JSON} must contain a JSON object")

    record_fields = set(CaseRecord.__dataclass_fields__)
    allowed_keys = record_fields | CASE_OVERRIDE_META_KEYS
    normalized: dict[str, dict[str, dict[str, Any]]] = {}

    for corpus_key, overrides in payload.items():
        if corpus_key not in CORPORA:
            raise ValueError(f"Unknown case override corpus: {corpus_key}")
        if not isinstance(overrides, dict):
            raise ValueError(f"Overrides for {corpus_key} must be a JSON object")

        normalized[corpus_key] = {}
        for slug, override in overrides.items():
            if not isinstance(override, dict):
                raise ValueError(f"Override for {corpus_key}/{slug} must be a JSON object")
            unknown_keys = sorted(set(override) - allowed_keys)
            if unknown_keys:
                raise ValueError(
                    f"Unknown override key(s) for {corpus_key}/{slug}: {', '.join(unknown_keys)}"
                )
            normalized[corpus_key][str(slug)] = override

    return normalized


def apply_case_override(record: CaseRecord, override: dict[str, Any]) -> bool:
    for key, value in override.items():
        if key in CASE_OVERRIDE_META_KEYS:
            continue
        setattr(record, key, value)
    return bool(override.get("preserve_existing_markdown"))


def sort_case_records(records: list[CaseRecord]) -> list[CaseRecord]:
    return sorted(
        records,
        key=lambda item: (
            item.issue_date_iso or "",
            item.published_time_iso or "",
            item.reference_label or "",
            item.title,
        ),
        reverse=True,
    )


def load_records_from_json(
    config: CorpusConfig,
    *,
    case_overrides: dict[str, dict[str, Any]] | None = None,
) -> list[CaseRecord]:
    if not config.data_path.exists():
        raise FileNotFoundError(f"Missing existing data file for --indexes-only: {config.data_path}")

    payload = json.loads(config.data_path.read_text(encoding="utf-8"))
    raw_records = payload.get("records") if isinstance(payload, dict) else None
    if not isinstance(raw_records, list):
        raise ValueError(f"{config.data_path} must contain a records list")

    record_fields = set(CaseRecord.__dataclass_fields__)
    records: list[CaseRecord] = []
    case_overrides = case_overrides or {}
    for index, raw_record in enumerate(raw_records):
        if not isinstance(raw_record, dict):
            raise ValueError(f"{config.data_path} record {index} must be a JSON object")
        missing_keys = sorted(record_fields - set(raw_record))
        if missing_keys:
            raise ValueError(
                f"{config.data_path} record {index} is missing key(s): {', '.join(missing_keys)}"
            )
        record = CaseRecord(**{key: raw_record[key] for key in record_fields})
        override = case_overrides.get(record.slug)
        if override:
            apply_case_override(record, override)
        records.append(record)

    return sort_case_records(records)


def fetch_text_with_retries(url: str, attempts: int = 5) -> str:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return core.fetch_text(url)
        except urllib.error.HTTPError as exc:  # pragma: no cover - network error handling
            last_error = exc
            if attempt == attempts:
                break
            if exc.code == 429:
                time.sleep(10 * attempt)
                continue
            time.sleep(attempt)
        except Exception as exc:  # pragma: no cover - network error handling
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(attempt)
    assert last_error is not None
    raise last_error


def split_mirror_response(raw_text: str) -> tuple[dict[str, str], str]:
    head, _, markdown = raw_text.partition(MARKDOWN_MARKER)
    metadata: dict[str, str] = {}
    for line in head.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata, markdown.strip()


def parse_published_time(value: str | None) -> tuple[str | None, str | None]:
    if not value:
        return None, None
    try:
        dt = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return value, None
    return value, dt.isoformat()


def normalize_reference_label(value: str) -> str | None:
    cleaned = core.normalize_space(value).strip("[]")
    return cleaned or None


def parse_source_tags(raw_tags: str) -> list[str]:
    text = core.normalize_space(raw_tags)
    if not text:
        return []
    text = re.sub(r"^tags?:\s*", "", text, flags=re.IGNORECASE)
    parts = [core.normalize_space(part).strip(" .") for part in re.split(r"\s*;\s*", text) if core.normalize_space(part)]
    deduped: list[str] = []
    seen: set[str] = set()
    for part in parts:
        key = part.casefold()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(part)
    return deduped


def extract_relevant_body(markdown: str, heading: str) -> str:
    heading_pattern = re.compile(
        rf"(?m)^(?:#+\s*)?{re.escape(heading)}\s*$",
        re.IGNORECASE,
    )
    match = heading_pattern.search(markdown)
    idx = match.start() if match else -1
    if idx == -1:
        raise ValueError(f"Unable to locate section heading {heading!r}")
    body = markdown[idx:]
    if body.startswith("\n"):
        body = body[1:]
    parts = re.split(r"\n!\[Image \d+\]|\n###### REPUBLIC OF THE PHILIPPINES", body, maxsplit=1)
    return parts[0].strip()


def parse_index_entries(markdown: str, heading: str) -> list[SourceEntry]:
    body = extract_relevant_body(markdown, heading)
    entries: list[SourceEntry] = []
    seen_urls: set[str] = set()
    current: dict[str, Any] | None = None

    def flush_current() -> None:
        nonlocal current
        if not current:
            return
        source_url = current["source_url"]
        if source_url in seen_urls:
            current = None
            return
        seen_urls.add(source_url)
        raw_tags = "\n".join(current["tag_lines"]).strip()
        entries.append(
            SourceEntry(
                reference_label=current["reference_label"],
                short_title=current["short_title"],
                source_url=source_url,
                source_tags_raw=raw_tags,
                source_tags=parse_source_tags(raw_tags),
            )
        )
        current = None

    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line == heading or re.fullmatch(r"=+", line):
            continue

        match = ENTRY_RE.match(line)
        if not match:
            if current is not None:
                current["tag_lines"].append(line)
            continue

        flush_current()
        current = {
            "reference_label": normalize_reference_label(match.group("reference")),
            "short_title": core.normalize_space(match.group("title")),
            "source_url": match.group("url"),
            "tag_lines": [],
        }

    flush_current()
    return entries


def cache_stem(source_url: str) -> str:
    basename = urllib.parse.unquote(Path(urllib.parse.urlparse(source_url).path).stem)
    digest = hashlib.sha1(source_url.encode("utf-8")).hexdigest()[:10]
    return f"{core.slugify(basename)}-{digest}"


def build_display_title(reference_label: str | None, short_title: str) -> str:
    if reference_label and short_title:
        if short_title.casefold().startswith(reference_label.casefold()):
            return short_title
        return f"{reference_label}: {short_title}"
    return short_title or reference_label or "NPC Case Document"


def build_case_excerpt(text: str, fallback: str) -> str:
    paragraphs = [core.normalize_space(p) for p in re.split(r"\n\s*\n", text) if core.normalize_space(p)]
    for paragraph in paragraphs:
        lowered = paragraph.casefold()
        if len(paragraph) < 80:
            continue
        if paragraph.startswith(">"):
            continue
        if lowered.startswith("npc_opc_"):
            continue
        if lowered.startswith("page "):
            continue
        return textwrap.shorten(paragraph, width=280, placeholder="...")
    return textwrap.shorten(core.normalize_space(fallback), width=280, placeholder="...")


def clean_pdf_markdown(markdown: str, reference_label: str | None, short_title: str, singular: str) -> str:
    lines = [line.rstrip() for line in markdown.replace("\r\n", "\n").splitlines()]
    normalized_counts = Counter(
        core.normalize_space(line.lstrip("> ").strip()).casefold()
        for line in lines
        if core.normalize_space(line)
    )
    removable: set[str] = set()
    for candidate in (reference_label, short_title, singular.title(), singular):
        if not candidate:
            continue
        normalized = core.normalize_space(candidate).casefold()
        if normalized_counts.get(normalized, 0) > 1:
            removable.add(normalized)

    # Any short line that repeats suspiciously often is a page header or
    # footer injected by Jina on every page of the source PDF.  Five or more
    # occurrences of the same text in a single document is a reliable signal.
    HIGH_FREQ_THRESHOLD = 5
    for candidate, count in normalized_counts.items():
        if count >= HIGH_FREQ_THRESHOLD and len(candidate) < 300:
            removable.add(candidate)

    cleaned_lines: list[str] = []
    for line in lines:
        normalized = core.normalize_space(line.lstrip("> ").strip())
        lowered = normalized.casefold()
        if not normalized:
            cleaned_lines.append("")
            continue
        if NOISE_LINE_RE.match(normalized):
            continue
        if lowered in removable:
            continue
        cleaned_lines.append(line)

    cleaned = "\n".join(cleaned_lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def parse_issue_date(entry: SourceEntry, cleaned_text: str) -> tuple[str | None, str | None]:
    basename = urllib.parse.unquote(Path(urllib.parse.urlparse(entry.source_url).path).name)
    sources = [
        basename,
        entry.reference_label or "",
        entry.short_title,
        cleaned_text[:4000],
    ]

    for source in (basename,):
        match = DATE_YMD_RE.search(source)
        if not match:
            continue
        year = int(match.group("year"))
        month = int(match.group("month"))
        day = int(match.group("day"))
        try:
            dt = datetime(year, month, day)
        except ValueError:
            continue
        return f"{dt.strftime('%B')} {dt.day}, {dt.year}", dt.strftime("%Y-%m-%d")

    for source in sources:
        match = DATE_MDY_RE.search(source)
        if not match:
            continue
        month = int(match.group("month"))
        day = int(match.group("day"))
        year = int(match.group("year"))
        try:
            dt = datetime(year, month, day)
        except ValueError:
            continue
        return f"{dt.strftime('%B')} {dt.day}, {dt.year}", dt.strftime("%Y-%m-%d")

    ordered_segment = cleaned_text.rsplit("SO ORDERED", 1)[-1]
    for source in (ordered_segment,):
        match = DATE_DMY_WORD_RE.search(source)
        if not match:
            continue
        dt = datetime.strptime(
            f"{match.group('day')} {match.group('month').title()} {match.group('year')}",
            "%d %B %Y",
        )
        return f"{dt.strftime('%B')} {dt.day}, {dt.year}", dt.strftime("%Y-%m-%d")

    for source in (ordered_segment,):
        match = DATE_MONTH_WORD_RE.search(source)
        if not match:
            continue
        dt = datetime.strptime(
            f"{match.group('month').title()} {match.group('day')} {match.group('year')}",
            "%B %d %Y",
        )
        return f"{dt.strftime('%B')} {dt.day}, {dt.year}", dt.strftime("%Y-%m-%d")

    for source in sources:
        match = DATE_DMY_WORD_RE.search(source)
        if not match:
            continue
        dt = datetime.strptime(
            f"{match.group('day')} {match.group('month').title()} {match.group('year')}",
            "%d %B %Y",
        )
        return f"{dt.strftime('%B')} {dt.day}, {dt.year}", dt.strftime("%Y-%m-%d")

    for source in sources:
        match = DATE_MONTH_WORD_RE.search(source)
        if not match:
            continue
        dt = datetime.strptime(
            f"{match.group('month').title()} {match.group('day')} {match.group('year')}",
            "%B %d %Y",
        )
        return f"{dt.strftime('%B')} {dt.day}, {dt.year}", dt.strftime("%Y-%m-%d")

    return None, None


def build_markdown(config: CorpusConfig, record: CaseRecord, cleaned_text: str) -> str:
    lines = [
        "---",
        f"title: {json.dumps(record.title, ensure_ascii=False)}",
        f"description: {json.dumps(record.excerpt, ensure_ascii=False)}",
        "tags:",
        f'  - "{config.tag}"',
        f'  - "type/{config.tag}"',
        f'  - "year/{record.year}"',
        '  - "npc-case"',
        "draft: false",
        "---",
        "",
        "## Source",
        f"- Reference: {record.reference_label or 'None listed on source page'}",
        f"- Official PDF: {record.source_url}",
        f"- Source page: {config.official_url}",
        f"- Issue date: {record.issue_date or 'Unknown'}",
        f"- Published on NPC site: {record.published_time or 'Unknown'}",
        f"- Pages: {record.page_count if record.page_count is not None else 'Unknown'}",
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
            f"## {config.body_heading}",
            cleaned_text.strip(),
            "",
        ]
    )
    return "\n".join(lines)


def load_or_fetch(path: Path, url: str, refresh: bool) -> str:
    if refresh or not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        text = fetch_text_with_retries(url)
        path.write_text(text, encoding="utf-8")
        return text
    return path.read_text(encoding="utf-8")


def build_records(
    config: CorpusConfig,
    refresh: bool,
    *,
    case_overrides: dict[str, dict[str, Any]] | None = None,
    write_record_pages: bool = True,
    rewrite_record_pages: bool = False,
) -> list[CaseRecord]:
    raw_index = load_or_fetch(config.index_cache_path, config.mirror_url, refresh=refresh)
    _, index_markdown = split_mirror_response(raw_index)
    entries = parse_index_entries(index_markdown, config.heading)
    case_overrides = case_overrides or {}

    records: list[CaseRecord] = []
    seen_slugs: set[str] = set()

    for entry in entries:
        stem = cache_stem(entry.source_url)
        raw_path = config.raw_dir / f"{stem}.md"
        clean_path = config.text_dir / f"{stem}.txt"
        raw_pdf_text = load_or_fetch(raw_path, mirror_url(entry.source_url), refresh=refresh)
        pdf_meta, pdf_markdown = split_mirror_response(raw_pdf_text)
        published_time, published_time_iso = parse_published_time(pdf_meta.get("Published Time"))
        page_count = None
        pages_value = pdf_meta.get("Number of Pages")
        if pages_value and pages_value.isdigit():
            page_count = int(pages_value)

        cleaned_text = clean_pdf_markdown(
            pdf_markdown,
            reference_label=entry.reference_label,
            short_title=entry.short_title,
            singular=config.singular,
        )
        clean_path.parent.mkdir(parents=True, exist_ok=True)
        clean_path.write_text(cleaned_text, encoding="utf-8")

        issue_date, issue_date_iso = parse_issue_date(entry, cleaned_text)
        year = (
            issue_date_iso[:4]
            if issue_date_iso
            else (published_time_iso[:4] if published_time_iso else "undated")
        )
        display_title = build_display_title(entry.reference_label, entry.short_title)
        base_slug = core.slugify(display_title)
        slug = base_slug
        suffix = 2
        while slug in seen_slugs:
            slug = f"{base_slug}-{suffix}"
            suffix += 1
        seen_slugs.add(slug)

        markdown_path = config.content_dir / year / f"{slug}.md"
        excerpt = build_case_excerpt(cleaned_text, display_title)
        record = CaseRecord(
            title=display_title,
            short_title=entry.short_title,
            reference_label=entry.reference_label,
            source_url=entry.source_url,
            source_tags_raw=entry.source_tags_raw,
            source_tags=entry.source_tags,
            issue_date=issue_date,
            issue_date_iso=issue_date_iso,
            published_time=published_time,
            published_time_iso=published_time_iso,
            page_count=page_count,
            year=year,
            slug=slug,
            raw_text_path=rel(raw_path),
            text_path=rel(clean_path),
            markdown_path=rel(markdown_path),
            excerpt=excerpt,
        )
        preserve_existing_markdown = False
        override = case_overrides.get(record.slug)
        if override:
            preserve_existing_markdown = apply_case_override(record, override)

        markdown_path = ROOT / record.markdown_path
        if write_record_pages:
            skip_existing = markdown_path.exists() and (
                preserve_existing_markdown or not rewrite_record_pages
            )
            if not skip_existing:
                markdown_path.parent.mkdir(parents=True, exist_ok=True)
                markdown_path.write_text(build_markdown(config, record, cleaned_text), encoding="utf-8")
        records.append(record)

    return sort_case_records(records)


def write_json(config: CorpusConfig, records: list[CaseRecord]) -> None:
    payload = {
        "source_page": config.official_url,
        "count": len(records),
        "records": [record.as_dict() for record in records],
    }
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    config.data_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def build_index_pages(config: CorpusConfig, records: list[CaseRecord]) -> None:
    year_groups: dict[str, list[CaseRecord]] = defaultdict(list)
    for record in records:
        year_groups[record.year].append(record)

    index_lines = [
        f"Generated notes for the NPC {config.title.lower()} corpus mirrored from the official website.",
        "",
        f"- Corpus size: **{len(records)}** {config.title.lower()}",
        f"- Source page: {config.official_url}",
        "",
        "## Years",
        *[
            f"- [[{config.folder}/{year}/index|{year}]] ({len(items)} {config.title.lower()})"
            for year, items in sorted(year_groups.items(), reverse=True)
        ],
    ]
    core.render_index_page(
        CONTENT_DIR / config.folder / "index.md",
        config.title,
        config.description,
        index_lines,
        default_manual=f"Add your own reading guide for NPC {config.title.lower()} here.",
    )

    for year, items in sorted(year_groups.items(), reverse=True):
        lines = [
            f"Generated notes for **{year}** NPC {config.title.lower()}.",
            "",
            "## Notes",
            *[
                f"- {core.note_link(record.markdown_path, record.title)}"
                for record in sorted(
                    items,
                    key=lambda item: (
                        item.issue_date_iso or "",
                        item.published_time_iso or "",
                        item.title,
                    ),
                    reverse=True,
                )
            ],
        ]
        core.render_index_page(
            CONTENT_DIR / config.folder / year / "index.md",
            f"{year} {config.title}",
            f"NPC {config.title.lower()} for {year}.",
            lines,
            default_manual=f"Add {year}-specific notes for these NPC {config.title.lower()} here.",
        )


def download_pdfs(config: CorpusConfig, refresh: bool) -> None:
    """Download the original source PDFs for a corpus to cache/<folder>/pdfs/."""
    pdf_dir = config.cache_dir / "pdfs"
    pdf_dir.mkdir(parents=True, exist_ok=True)

    raw_index = load_or_fetch(config.index_cache_path, config.mirror_url, refresh=False)
    _, index_markdown = split_mirror_response(raw_index)
    entries = parse_index_entries(index_markdown, config.heading)

    for entry in entries:
        stem = cache_stem(entry.source_url)
        pdf_path = pdf_dir / f"{stem}.pdf"
        if not refresh and pdf_path.exists():
            print(f"  [skip] {pdf_path.name}")
            continue
        try:
            print(f"  [download] {entry.source_url}")
            req = __import__("urllib.request", fromlist=["Request", "urlopen"]).Request(
                entry.source_url, headers={"User-Agent": "Mozilla/5.0 (compatible; NPC-Issuance-Wiki/1.0)"}
            )
            import shutil, urllib.request as _ur
            with _ur.urlopen(req, timeout=120) as resp, pdf_path.open("wb") as fh:
                shutil.copyfileobj(resp, fh)
        except Exception as exc:
            print(f"  [error] {entry.source_url}: {exc}")

    print(f"PDFs saved to {pdf_dir} ({len(entries)} entries)")


def run(
    configs: list[CorpusConfig],
    refresh: bool,
    *,
    use_existing_records: bool = False,
    write_record_pages: bool = True,
    rewrite_record_pages: bool = False,
) -> dict[str, list[CaseRecord]]:
    case_overrides = load_case_overrides()
    results: dict[str, list[CaseRecord]] = {}
    for config in configs:
        overrides = case_overrides.get(config.key, {})
        if use_existing_records:
            records = load_records_from_json(config, case_overrides=overrides)
        else:
            records = build_records(
                config,
                refresh=refresh,
                case_overrides=overrides,
                write_record_pages=write_record_pages,
                rewrite_record_pages=rewrite_record_pages,
            )
        write_json(config, records)
        build_index_pages(config, records)
        results[config.key] = records
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Build markdown corpora for NPC decisions and resolutions.")
    parser.add_argument("corpus", choices=["decisions", "resolutions", "all"])
    parser.add_argument("--refresh", action="store_true", help="Refresh the mirrored source pages and documents.")
    parser.add_argument(
        "--indexes-only",
        action="store_true",
        help="Regenerate JSON and index pages from existing data without reading or writing case Markdown pages.",
    )
    parser.add_argument(
        "--rewrite-record-pages",
        action="store_true",
        help=(
            "Rewrite existing case Markdown pages. Records marked preserve_existing_markdown "
            "in data/case_overrides.json are still skipped."
        ),
    )
    parser.add_argument(
        "--download-pdfs",
        action="store_true",
        help="Download the original source PDFs to cache/<corpus>/pdfs/ and exit (no markdown rebuild).",
    )
    args = parser.parse_args()

    if args.corpus == "all":
        selected = [CORPORA["decisions"], CORPORA["resolutions"]]
    else:
        selected = [CORPORA[args.corpus]]

    if args.indexes_only and args.rewrite_record_pages:
        parser.error("--indexes-only cannot be combined with --rewrite-record-pages")
    if args.indexes_only and args.refresh:
        parser.error("--indexes-only reads existing JSON and cannot be combined with --refresh")

    if args.download_pdfs:
        for config in selected:
            print(f"Downloading PDFs for {config.title}…")
            download_pdfs(config, refresh=args.refresh)
        return 0

    results = run(
        selected,
        refresh=args.refresh,
        use_existing_records=args.indexes_only,
        write_record_pages=not args.indexes_only,
        rewrite_record_pages=args.rewrite_record_pages,
    )
    summary = ", ".join(f"{len(records)} {key}" for key, records in results.items())
    print(f"Generated {summary} under {CONTENT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
