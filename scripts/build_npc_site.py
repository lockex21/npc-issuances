#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import textwrap
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / "cache"
PDF_DIR = CACHE_DIR / "pdfs"
TEXT_DIR = CACHE_DIR / "text"
DATA_DIR = ROOT / "data"
CONTENT_DIR = ROOT / "content"
CONTENT_PDF_DIR = CONTENT_DIR / "pdfs"
SOURCE_NOTES_DIR = CONTENT_DIR / "sources"
INDEX_CACHE = CACHE_DIR / "advisories-circulars.html"
ISSUANCES_JSON = DATA_DIR / "issuances.json"
OVERRIDES_JSON = DATA_DIR / "overrides.json"
SOURCE_URL = "https://privacy.gov.ph/pips-and-pics/advisories-circulars/"
USER_AGENT = "Mozilla/5.0 (compatible; NPC-Issuance-Wiki/1.0)"
MANUAL_START = "<!-- BEGIN MANUAL CONTENT -->"
MANUAL_END = "<!-- END MANUAL CONTENT -->"
SUMMARY_START = "<!-- BEGIN MANUAL SUMMARY -->"
SUMMARY_END = "<!-- END MANUAL SUMMARY -->"
LINKS_START = "<!-- BEGIN MANUAL LINKS -->"
LINKS_END = "<!-- END MANUAL LINKS -->"
ANNOTATED_START = "<!-- BEGIN MANUAL ANNOTATED TEXT -->"
ANNOTATED_END = "<!-- END MANUAL ANNOTATED TEXT -->"
RECORD_START = "<!-- BEGIN GENERATED RECORD -->"
RECORD_END = "<!-- END GENERATED RECORD -->"
SOURCE_EMBED_START = "<!-- BEGIN GENERATED SOURCE EMBED -->"
SOURCE_EMBED_END = "<!-- END GENERATED SOURCE EMBED -->"

REFERENCE_PATTERN = re.compile(
    r"\b(?:(?:National\s+Privacy\s+Commission|NPC)\s+)?"
    r"(?P<kind>Advisory|Circular|Memorandum Circular|Joint Circular|Joint Advisory|Advisory Opinion|Commission Resolution)"
    r"\s+No\.?\s*(?P<number>[A-Za-z0-9][A-Za-z0-9./-]*)",
    re.IGNORECASE,
)
NUMBERED_TITLE_PATTERN = re.compile(
    r"\b(?P<label>Advisory|Circular|Memorandum Circular|Joint Circular|Joint Advisory|Advisory Opinion|Commission Resolution)"
    r"(?:\s+No\.?\s*|\s+Number\s+)(?P<number>[A-Za-z0-9][A-Za-z0-9./-]*)",
    re.IGNORECASE,
)
FILENAME_REFERENCE_PATTERN = re.compile(
    r"(?P<label>Advisory|Circular|Memorandum[-_ ]Circular|Joint[-_ ]Circular|Joint[-_ ]Advisory|Advisory[-_ ]Opinion|Commission[-_ ]Resolution)"
    r"(?:[-_ ]*No\.?[-_ ]*|[-_ ]*)(?P<number>(?:19|20)\d{2}(?:[-_.]\d{1,2})?|\d{2}[-_.]\d{2})(?![._-]\d{2}\b)(?=$|[^A-Za-z0-9])",
    re.IGNORECASE,
)
DATE_PATTERN = re.compile(
    r"\b(?P<month>January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+(?P<day>\d{1,2}),\s+(?P<year>20\d{2}|19\d{2})\b"
)
WS_RE = re.compile(r"\s+")

TOPIC_RULES: dict[str, tuple[str, ...]] = {
    "ai": ("artificial intelligence", r"\bai\b"),
    "children": ("child-oriented", "children", "minor"),
    "consent": (r"\bconsent\b",),
    "cross-border-transfers": ("cross-border", "cross border", "transfer"),
    "cctv-surveillance": ("cctv", "closed-circuit television", "body-worn camera", "surveillance"),
    "data-sharing": ("data sharing", "sharing agreement"),
    "elections": ("election", "political"),
    "fees-and-payments": ("fees", "charges", "payment"),
    "government": ("government", "public sector"),
    "legitimate-interest": ("legitimate interest",),
    "privacy-engineering": ("privacy engineering", "systems life cycle"),
    "registration": ("registration", "seal of registration", "data protection officer"),
    "security": ("security", "breach", "cyber"),
    "training-certification": ("competency", "privacy mark", "certification", "training"),
}
TOPIC_DISPLAY_NAMES = {
    "ai": "AI",
    "cctv-surveillance": "CCTV Surveillance",
}


def normalize_space(value: str) -> str:
    return WS_RE.sub(" ", value).strip()


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "issuance"


def normalize_reference(kind: str, number: str) -> str:
    kind = normalize_space(kind).lower()
    number = normalize_space(number).replace(" ", "")
    return f"{kind} no. {number.lower()}"


def prettify_reference(reference: str | None) -> str | None:
    if not reference:
        return None
    match = re.match(r"([a-z ]+)\s+no\.\s+(.+)", reference)
    if not match:
        return reference.title()
    kind, number = match.groups()
    return f"{kind.title()} No. {number.upper()}"


def normalize_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    path = urllib.parse.quote(parsed.path, safe="/%")
    query = urllib.parse.quote_plus(parsed.query, safe="=&")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, query, parsed.fragment))


def url_basename(url: str) -> str:
    return urllib.parse.unquote(Path(urllib.parse.urlparse(url).path).name)


def filename_search_text(url: str) -> str:
    return normalize_space(re.sub(r"[_-]+", " ", url_basename(url)))


def run_command(args: list[str], cwd: Path | None = None) -> str:
    proc = subprocess.run(
        args,
        cwd=cwd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc.stdout


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(normalize_url(url), headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def fetch_text(url: str) -> str:
    return fetch_bytes(url).decode("utf-8", errors="replace")


def download_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(normalize_url(url), headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp, dest.open("wb") as fh:
        shutil.copyfileobj(resp, fh)


def markdown_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def extract_reference(source: str, *, filename_mode: bool = False) -> str | None:
    pattern = FILENAME_REFERENCE_PATTERN if filename_mode else NUMBERED_TITLE_PATTERN
    matches = list(pattern.finditer(source))
    if not matches:
        return None
    match = max(matches, key=lambda item: len(item.group("number")))
    label = normalize_space(match.group("label").replace("-", " ").replace("_", " "))
    number = match.group("number").replace("_", "-").replace(".", "-")
    return normalize_reference(label, number)


class PDFLinkParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.entries: list[dict[str, str]] = []
        self._current_href: str | None = None
        self._current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attrs_dict = dict(attrs)
        href = attrs_dict.get("href")
        if not href:
            return
        full_url = urllib.parse.urljoin(self.base_url, href)
        if full_url.lower().endswith(".pdf"):
            self._current_href = full_url
            self._current_text = []

    def handle_data(self, data: str) -> None:
        if self._current_href:
            self._current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "a" or not self._current_href:
            return
        title = normalize_space("".join(self._current_text))
        if title:
            self.entries.append({"title": title, "url": self._current_href})
        self._current_href = None
        self._current_text = []


@dataclass
class Issuance:
    title: str
    reference_label: str | None
    source_url: str
    pdf_path: str
    text_path: str
    slug: str
    year: str
    kind: str
    canonical_reference: str | None
    aliases: list[str]
    tags: list[str]
    excerpt: str
    issue_date: str | None
    issue_date_iso: str | None
    page_count: int | None
    citations: list[str]
    outgoing_refs: list[str]
    incoming_refs: list[str]
    content_path: str
    source_note_path: str

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


def load_overrides() -> dict[str, Any]:
    if not OVERRIDES_JSON.exists():
        return {}
    return json.loads(OVERRIDES_JSON.read_text(encoding="utf-8"))


def parse_pdf_index(html_text: str) -> list[dict[str, str]]:
    parser = PDFLinkParser(SOURCE_URL)
    parser.feed(html_text)
    deduped: list[dict[str, str]] = []
    seen: set[str] = set()
    for entry in parser.entries:
        if entry["url"] in seen:
            continue
        seen.add(entry["url"])
        deduped.append(entry)
    return deduped


def save_index_cache() -> list[dict[str, str]]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    html_text = fetch_text(SOURCE_URL)
    INDEX_CACHE.write_text(html_text, encoding="utf-8")
    return parse_pdf_index(html_text)


def load_cached_index() -> list[dict[str, str]]:
    if not INDEX_CACHE.exists():
        return save_index_cache()
    return parse_pdf_index(INDEX_CACHE.read_text(encoding="utf-8"))


def extract_text(pdf_path: Path, text_path: Path) -> str:
    text_path.parent.mkdir(parents=True, exist_ok=True)
    if not text_path.exists() or text_path.stat().st_mtime < pdf_path.stat().st_mtime:
        run_command(["pdftotext", "-layout", str(pdf_path), str(text_path)])
    return text_path.read_text(encoding="utf-8", errors="replace")


def extract_pdf_metadata(pdf_path: Path) -> dict[str, str]:
    raw = run_command(["pdfinfo", str(pdf_path)])
    metadata: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def infer_canonical_reference(title: str, text: str, url: str) -> str | None:
    return extract_reference(url_basename(url), filename_mode=True) or extract_reference(text[:1200])


def infer_kind(title: str, text: str, url: str, canonical_reference: str | None) -> str:
    title_head = title.split(" (", 1)[0]
    source = f"{filename_search_text(url)}\n{title_head}\n{text[:600]}".lower()
    if title_head.lower().startswith("faq") or source.startswith("faq"):
        return "FAQ"
    if canonical_reference:
        return prettify_reference(canonical_reference).split(" No.", 1)[0]
    if "joint advisory" in source:
        return "Joint Advisory"
    if "joint circular" in source:
        return "Joint Circular"
    if "memorandum circular" in source:
        return "Memorandum Circular"
    if "advisory" in source:
        return "Advisory"
    if "circular" in source:
        return "Circular"
    return "Issuance"


def infer_issue_date(title: str, url: str) -> tuple[str | None, str | None]:
    month_names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    month_abbr = {
        "jan": "January",
        "feb": "February",
        "mar": "March",
        "apr": "April",
        "may": "May",
        "jun": "June",
        "jul": "July",
        "aug": "August",
        "sep": "September",
        "sept": "September",
        "oct": "October",
        "nov": "November",
        "dec": "December",
    }
    for source in (title, url_basename(url)):
        match = DATE_PATTERN.search(source)
        if match:
            dt = datetime.strptime(
                f"{match.group('month')} {match.group('day')} {match.group('year')}",
                "%B %d %Y",
            )
            return f"{match.group('month')} {int(match.group('day'))}, {match.group('year')}", dt.strftime("%Y-%m-%d")
        numeric = re.search(r"\b(20\d{2})[._-](\d{2})[._-](\d{2})\b", source)
        if numeric:
            year, month, day = numeric.groups()
            if 1 <= int(month) <= 12:
                return f"{month_names[int(month) - 1]} {int(day)}, {year}", f"{year}-{month}-{day}"
        compact = re.search(
            r"\b(\d{1,2})[-_. ]?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*[-_. ]?(20\d{2})\b",
            source,
            re.IGNORECASE,
        )
        if compact:
            day, month, year = compact.groups()
            month_name = month_abbr[month.lower()]
            dt = datetime.strptime(f"{month_name} {day} {year}", "%B %d %Y")
            return f"{month_name} {int(day)}, {year}", dt.strftime("%Y-%m-%d")
    return None, None


def infer_year(title: str, text: str, canonical_reference: str | None, url: str, issue_date_iso: str | None) -> str:
    for source in (url_basename(url),):
        match = re.search(r"\b(19|20)\d{2}\b", source)
        if match:
            return match.group(0)
    if canonical_reference:
        year_match = re.search(r"\b(19|20)\d{2}\b", canonical_reference)
        if year_match:
            return year_match.group(0)
    if issue_date_iso:
        return issue_date_iso[:4]
    match = re.search(r"\b(19|20)\d{2}\b", title)
    if match:
        return match.group(0)
    date_match = DATE_PATTERN.search(text[:4000]) or DATE_PATTERN.search(title)
    if date_match:
        return date_match.group("year")
    return "undated"


def build_excerpt(text: str, fallback: str) -> str:
    paragraphs = [normalize_space(p) for p in re.split(r"\n\s*\n", text) if normalize_space(p)]
    for paragraph in paragraphs:
        if len(paragraph) < 80:
            continue
        lowered = paragraph.lower()
        if any(
            token in lowered
            for token in (
                "republic of the philippines",
                "national privacy commission",
                "quezon city",
                "pasay city",
                "philippine international convention center",
            )
        ):
            continue
        return textwrap.shorten(paragraph, width=280, placeholder="...")
    return textwrap.shorten(normalize_space(fallback), width=280, placeholder="...")


def collect_aliases(title: str, canonical_reference: str | None) -> list[str]:
    aliases = {normalize_space(title).lower()}
    if canonical_reference:
        aliases.add(canonical_reference)
        match = re.match(r"([a-z ]+)\s+no\.\s+(.+)", canonical_reference)
        if match:
            kind, number = match.groups()
            aliases.add(f"npc {kind} no. {number}")
    return sorted(aliases)


def infer_topic_tags(title: str, excerpt: str, kind: str) -> list[str]:
    source = f"{title}\n{excerpt}".lower()
    tags = []
    for topic, patterns in TOPIC_RULES.items():
        if any(re.search(pattern, source) for pattern in patterns):
            tags.append(f"topic/{topic}")
    if kind:
        tags.append(f"type/{slugify(kind)}")
    return sorted(set(tags))


def display_topic_name(topic: str) -> str:
    return TOPIC_DISPLAY_NAMES.get(topic, topic.replace("-", " ").title())


def detect_citations(text: str) -> list[str]:
    citations: set[str] = set()
    for match in REFERENCE_PATTERN.finditer(text):
        citations.add(normalize_reference(match.group("kind"), match.group("number")))
    return sorted(citations)


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def markdown_link_path(path: str) -> str:
    return path.removeprefix("content/").removesuffix(".md")


def wiki_link(record: Issuance, label: str | None = None) -> str:
    target = markdown_link_path(record.content_path)
    return f"[[{target}|{label or record.title}]]"


def note_link(path: str, label: str | None = None) -> str:
    target = markdown_link_path(path)
    return f"[[{target}{'|' + label if label else ''}]]"


def build_records(index_entries: list[dict[str, str]], refresh: bool) -> list[Issuance]:
    overrides = load_overrides()
    records: list[Issuance] = []
    seen_slugs: set[str] = set()

    for entry in index_entries:
        url = entry["url"]
        title = normalize_space(entry["title"]).strip(" -")
        basename = Path(urllib.parse.urlparse(url).path).name
        pdf_path = PDF_DIR / basename
        text_path = TEXT_DIR / f"{pdf_path.stem}.txt"

        if refresh or not pdf_path.exists():
            download_file(url, pdf_path)

        text = extract_text(pdf_path, text_path)
        meta = extract_pdf_metadata(pdf_path)
        canonical_reference = infer_canonical_reference(title, text, url)
        issue_date, issue_date_iso = infer_issue_date(title, url)
        year = infer_year(title, text, canonical_reference, url, issue_date_iso)
        base_slug = slugify(title)
        slug = base_slug
        suffix = 2
        while slug in seen_slugs:
            slug = f"{base_slug}-{suffix}"
            suffix += 1
        seen_slugs.add(slug)

        excerpt = build_excerpt(text, title)
        kind = infer_kind(title, text, url, canonical_reference)
        tags = sorted({"issuance", f"year/{year}", *infer_topic_tags(title, excerpt, kind)})
        content_path = f"content/issuances/{year}/{slug}.md"
        source_note_path = f"content/sources/{year}/{slug}.md"

        record = Issuance(
            title=title,
            reference_label=prettify_reference(canonical_reference),
            source_url=url,
            pdf_path=relative_path(pdf_path),
            text_path=relative_path(text_path),
            slug=slug,
            year=year,
            kind=kind,
            canonical_reference=canonical_reference,
            aliases=collect_aliases(title, canonical_reference),
            tags=tags,
            excerpt=excerpt,
            issue_date=issue_date,
            issue_date_iso=issue_date_iso,
            page_count=int(meta["Pages"]) if meta.get("Pages", "").isdigit() else None,
            citations=detect_citations(text),
            outgoing_refs=[],
            incoming_refs=[],
            content_path=content_path,
            source_note_path=source_note_path,
        )

        override = overrides.get(record.slug) or overrides.get(record.title)
        if isinstance(override, dict):
            for key, value in override.items():
                if hasattr(record, key):
                    setattr(record, key, value)
        records.append(record)

    alias_map: dict[str, Issuance] = {}
    for record in records:
        for alias in record.aliases:
            alias_map.setdefault(alias, record)

    incoming: dict[str, set[str]] = defaultdict(set)
    for record in records:
        targets: set[str] = set()
        for citation in record.citations:
            target = alias_map.get(citation)
            if not target or target.slug == record.slug:
                continue
            targets.add(target.slug)
            incoming[target.slug].add(record.slug)
        record.outgoing_refs = sorted(targets)

    by_slug = {record.slug: record for record in records}
    for record in records:
        record.incoming_refs = sorted(incoming.get(record.slug, set()))
        record.outgoing_refs = [slug for slug in record.outgoing_refs if slug in by_slug]

    return sorted(records, key=lambda item: (item.year, item.kind, item.title), reverse=True)


def write_json(records: list[Issuance]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "source_url": SOURCE_URL,
        "issuance_count": len(records),
        "issuances": [record.as_dict() for record in records],
    }
    ISSUANCES_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def ensure_seed_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not OVERRIDES_JSON.exists():
        OVERRIDES_JSON.write_text("{}\n", encoding="utf-8")


def load_manual_block(path: Path, default_body: str) -> str:
    if path.exists():
        content = path.read_text(encoding="utf-8")
        match = re.search(
            rf"{re.escape(MANUAL_START)}\n?(?P<body>.*?){re.escape(MANUAL_END)}",
            content,
            re.DOTALL,
        )
        if match:
            return match.group("body").strip("\n")
    return default_body


def extract_block(path: Path, start_marker: str, end_marker: str, default_body: str) -> str:
    if path.exists():
        content = path.read_text(encoding="utf-8")
        match = re.search(
            rf"{re.escape(start_marker)}\n?(?P<body>.*?){re.escape(end_marker)}",
            content,
            re.DOTALL,
        )
        if match:
            return match.group("body").strip("\n")
    return default_body


def render_block(start_marker: str, body: str, end_marker: str) -> str:
    return f"{start_marker}\n{body.rstrip()}\n{end_marker}"


def frontmatter_lines(record: Issuance) -> list[str]:
    lines = [
        "---",
        f"title: {markdown_quote(record.title)}",
        f"description: {markdown_quote(record.excerpt)}",
        "aliases:",
    ]
    for alias in sorted({*record.aliases, *( [record.reference_label] if record.reference_label else [] )}):
        lines.append(f"  - {markdown_quote(alias)}")
    lines.append("tags:")
    for tag in sorted(set(record.tags)):
        lines.append(f"  - {markdown_quote(tag)}")
    if record.issue_date_iso:
        lines.append(f"date: {markdown_quote(record.issue_date_iso)}")
    lines.append("draft: false")
    lines.append("---")
    return lines


def is_placeholder_text(value: str) -> bool:
    stripped = value.strip()
    return stripped in {
        "",
        "Add your own analysis here.\n\n- Use wikilinks to connect this issuance to topic notes.\n- Example: [[topics/cctv-surveillance]]",
        "Add your own analysis here.\n\n- Use wikilinks to connect this issuance to topic notes.\n- Example: [[topics/cctv-surveillance]]\n",
    }


def render_manual_section(body: str) -> str:
    return render_block(MANUAL_START, body, MANUAL_END)


def compute_relative(from_path: Path, to_path: Path) -> str:
    from_parts = from_path.resolve().parts
    to_parts = to_path.resolve().parts
    common = 0
    for a, b in zip(from_parts, to_parts):
        if a != b:
            break
        common += 1
    up = [".."] * (len(from_parts) - common)
    down = list(to_parts[common:])
    if not up and not down:
        return "."
    return str(Path(*up, *down))


def linkify_text(text: str, current_slug: str, alias_map: dict[str, Issuance]) -> str:
    def replace(match: re.Match[str]) -> str:
        normalized = normalize_reference(match.group("kind"), match.group("number"))
        target = alias_map.get(normalized)
        original = normalize_space(match.group(0))
        if not target or target.slug == current_slug:
            return original
        return wiki_link(target, original)

    linked = REFERENCE_PATTERN.sub(replace, text)
    paragraphs: list[str] = []
    for raw_paragraph in re.split(r"\n\s*\n", linked):
        paragraph = raw_paragraph.rstrip()
        if not normalize_space(paragraph):
            continue
        lines = [line.rstrip() for line in paragraph.splitlines()]
        lines = [line for line in lines if line.strip()]
        paragraphs.append("  \n".join(lines))
    return "\n\n".join(paragraphs)


def render_source_note(record: Issuance, alias_map: dict[str, Issuance]) -> str:
    text = (ROOT / record.text_path).read_text(encoding="utf-8", errors="replace")
    linked_text = linkify_text(text, record.slug, alias_map)
    note_path = ROOT / record.source_note_path
    pdf_target = CONTENT_PDF_DIR / Path(record.pdf_path).name
    pdf_relative = compute_relative(note_path.parent, pdf_target)
    lines = [
        "---",
        f"title: {markdown_quote(f'{record.title} Source Text')}",
        f"description: {markdown_quote(f'Generated extracted text for {record.title}.')}",
        "aliases:",
        f"  - {markdown_quote(f'{record.title} Source Text')}",
        "tags:",
        '  - "source-text"',
        f'  - "year/{record.year}"',
        "draft: false",
        "---",
        "",
        "> This note is generated from the cached PDF and is safe to regenerate.",
        "",
        "## Source",
        f"- Main note: {wiki_link(record)}",
        f"- PDF: [Open PDF]({pdf_relative})",
        f"- Official source: {record.source_url}",
        "",
        "## Extracted Text",
        linked_text,
        "",
    ]
    return "\n".join(lines)


def render_issuance_page(record: Issuance, by_slug: dict[str, Issuance], alias_map: dict[str, Issuance]) -> str:
    existing_path = ROOT / record.content_path
    text = (ROOT / record.text_path).read_text(encoding="utf-8", errors="replace")
    linked_text = linkify_text(text, record.slug, alias_map)
    legacy_manual = load_manual_block(existing_path, "")
    summary_default = (
        legacy_manual
        if not is_placeholder_text(legacy_manual)
        else "Write a concise summary of the issuance here."
    )
    links_default = "\n".join(
        [
            "- Add links to topic notes, related issuances, or outside references here.",
            "- Example internal link: [[topics/cctv-surveillance]]",
            "- Example external link: [Official Gazette](https://www.officialgazette.gov.ph/)",
        ]
    )
    summary_block = extract_block(existing_path, SUMMARY_START, SUMMARY_END, summary_default)
    links_block = extract_block(existing_path, LINKS_START, LINKS_END, links_default)
    annotated_default = linked_text
    annotated_block = extract_block(existing_path, ANNOTATED_START, ANNOTATED_END, annotated_default)

    outgoing_lines = (
        "\n".join(f"- {wiki_link(by_slug[slug])}" for slug in record.outgoing_refs)
        if record.outgoing_refs
        else "- None detected automatically."
    )
    incoming_lines = (
        "\n".join(f"- {wiki_link(by_slug[slug])}" for slug in record.incoming_refs)
        if record.incoming_refs
        else "- No backlinks detected yet."
    )

    note_path = ROOT / record.content_path
    pdf_target = CONTENT_PDF_DIR / Path(record.pdf_path).name
    pdf_relative = compute_relative(note_path.parent, pdf_target)
    topic_links = sorted(
        note_link(f"content/topics/{tag.removeprefix('topic/')}.md", display_topic_name(tag.removeprefix("topic/")))
        for tag in record.tags
        if tag.startswith("topic/")
    )
    source_note_link = note_link(record.source_note_path, "Generated source text")
    record_block = "\n".join(
        [
            f"- Reference: {record.reference_label or 'None detected'}",
            f"- Type: {record.kind}",
            f"- Year: {record.year}",
            f"- Issued: {record.issue_date or 'Unknown'}",
            f"- Pages: {record.page_count if record.page_count is not None else 'Unknown'}",
            f"- Source PDF: [Open PDF]({pdf_relative})",
            f"- Official source: {record.source_url}",
            f"- Topic pages: {', '.join(topic_links) if topic_links else 'None yet'}",
            f"- Generated source note: {source_note_link}",
            "",
            "### Automatic References Out",
            outgoing_lines,
            "",
            "### Automatic Backlinks",
            incoming_lines,
        ]
    )
    source_embed = f"![[{markdown_link_path(record.source_note_path)}]]"

    body = [
        "\n".join(frontmatter_lines(record)),
        "",
        f"> {record.excerpt}",
        "",
        "## Summary",
        render_block(SUMMARY_START, summary_block, SUMMARY_END),
        "",
        "## Links",
        render_block(LINKS_START, links_block, LINKS_END),
        "",
        "## Annotated Text",
        render_block(ANNOTATED_START, annotated_block, ANNOTATED_END),
        "",
        "## Generated Record",
        render_block(RECORD_START, record_block, RECORD_END),
        "",
        "## Raw Source Text",
        render_block(SOURCE_EMBED_START, source_embed, SOURCE_EMBED_END),
        "",
    ]
    return "\n".join(body)


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def render_index_page(
    path: Path,
    title: str,
    description: str,
    body_lines: list[str],
    default_manual: str = "Add curated notes or a reading path here.",
) -> None:
    manual_block = load_manual_block(path, default_manual)
    frontmatter = [
        "---",
        f"title: {markdown_quote(title)}",
        f"description: {markdown_quote(description)}",
        "draft: false",
        "---",
        "",
    ]
    content = "\n".join(
        frontmatter
        + body_lines
        + [
            "",
            "## Manual Notes",
            render_manual_section(manual_block),
            "",
        ]
    )
    write_markdown(path, content)


def build_content_tree(records: list[Issuance]) -> None:
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    CONTENT_PDF_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_NOTES_DIR.mkdir(parents=True, exist_ok=True)

    by_slug = {record.slug: record for record in records}
    alias_map = {alias: record for record in records for alias in record.aliases}

    for record in records:
        shutil.copy2(ROOT / record.pdf_path, CONTENT_PDF_DIR / Path(record.pdf_path).name)
        write_markdown(ROOT / record.source_note_path, render_source_note(record, alias_map))

    for record in records:
        write_markdown(ROOT / record.content_path, render_issuance_page(record, by_slug, alias_map))

    year_groups: dict[str, list[Issuance]] = defaultdict(list)
    type_groups: dict[str, list[Issuance]] = defaultdict(list)
    topic_groups: dict[str, list[Issuance]] = defaultdict(list)

    for record in records:
        year_groups[record.year].append(record)
        type_groups[record.kind].append(record)
        for tag in record.tags:
            if tag.startswith("topic/"):
                topic_groups[tag.removeprefix("topic/")].append(record)

    issuance_count = len(records)
    reference_rich = sorted(records, key=lambda item: (len(item.incoming_refs), item.title), reverse=True)[:10]
    home_lines = [
        "This Quartz workspace is generated from the National Privacy Commission advisories and circulars corpus.",
        "",
        f"- Corpus size: **{issuance_count}** issuances",
        f"- Source index: {SOURCE_URL}",
        "- Local workflow: run `python3 scripts/build_npc_site.py all --refresh` to refresh the corpus, then `npx quartz build --serve` to preview the wiki.",
        "",
        "## Browse",
        "- [[issuances/index|Issuances by year]]",
        "- [[types/index|Issuances by type]]",
        "- [[topics/index|Topics]]",
        "- [[relationships/index|Reference map]]",
        "",
        "## Most Referenced Issuances",
        *[
            f"- {wiki_link(record)} ({len(record.incoming_refs)} backlinks)"
            for record in reference_rich
        ],
    ]
    render_index_page(
        CONTENT_DIR / "index.md",
        "NPC Issuance Wiki",
        "Quartz workspace for NPC advisories, circulars, and cross-references.",
        home_lines,
        default_manual="Use this space for a curated homepage blurb or reading guide.",
    )

    issuance_index_lines = [
        "Year folders contain the generated issuance notes. Quartz Explorer will show the same tree in the sidebar.",
        "",
        "## Years",
        *[
            f"- [[issuances/{year}/index|{year}]] ({len(items)} issuances)"
            for year, items in sorted(year_groups.items(), reverse=True)
        ],
    ]
    render_index_page(
        CONTENT_DIR / "issuances" / "index.md",
        "Issuances",
        "Browse NPC issuances by year.",
        issuance_index_lines,
        default_manual="Add your own high-level reading order or category notes here.",
    )

    for year, items in sorted(year_groups.items(), reverse=True):
        lines = [
            f"Generated notes for **{year}**.",
            "",
            "## Notes",
            *[
                f"- {wiki_link(record)}"
                + (f" ({record.reference_label})" if record.reference_label else "")
                for record in sorted(items, key=lambda item: (item.issue_date_iso or "", item.title), reverse=True)
            ],
        ]
        render_index_page(
            CONTENT_DIR / "issuances" / year / "index.md",
            f"{year} Issuances",
            f"NPC issuances for {year}.",
            lines,
            default_manual="Add year-specific context, milestones, or legislative notes here.",
        )

    type_index_lines = [
        "Each page below groups issuances by issuance type.",
        "",
        "## Types",
        *[
            f"- [[types/{slugify(kind)}|{kind}]] ({len(items)} issuances)"
            for kind, items in sorted(type_groups.items())
        ],
    ]
    render_index_page(
        CONTENT_DIR / "types" / "index.md",
        "Issuance Types",
        "Browse NPC issuances by document type.",
        type_index_lines,
    )

    for kind, items in sorted(type_groups.items()):
        lines = [
            f"All generated notes tagged as **{kind}**.",
            "",
            "## Notes",
            *[f"- {wiki_link(record)}" for record in sorted(items, key=lambda item: (item.year, item.title), reverse=True)],
        ]
        render_index_page(
            CONTENT_DIR / "types" / f"{slugify(kind)}.md",
            kind,
            f"NPC issuances of type {kind}.",
            lines,
            default_manual=f"Add your own criteria for reading {kind.lower()} issuances here.",
        )

    topic_index_lines = [
        "Topic pages are generated from lightweight keyword tagging. Treat them as starting points and extend them manually.",
        "",
        "## Topics",
        *[
            f"- [[topics/{topic}|{display_topic_name(topic)}]] ({len(items)} issuances)"
            for topic, items in sorted(topic_groups.items())
        ],
    ]
    render_index_page(
        CONTENT_DIR / "topics" / "index.md",
        "Topics",
        "Auto-generated topic landing pages for the NPC corpus.",
        topic_index_lines,
        default_manual="Add new handcrafted topic notes in this folder whenever the generated set is not enough.",
    )

    for topic, items in sorted(topic_groups.items()):
        lines = [
            f"Auto-generated topic cluster for **{display_topic_name(topic)}**.",
            "",
            "## Related Issuances",
            *[f"- {wiki_link(record)}" for record in sorted(items, key=lambda item: (item.year, item.title), reverse=True)],
        ]
        render_index_page(
            CONTENT_DIR / "topics" / f"{topic}.md",
            display_topic_name(topic),
            f"NPC issuances related to {display_topic_name(topic)}.",
            lines,
            default_manual="Add your own synthesis, definitions, and extra wikilinks here.",
        )

    citation_counts = Counter()
    for record in records:
        for slug in record.outgoing_refs:
            citation_counts[slug] += 1
    relationship_lines = [
        "This page summarizes the automatic cross-reference graph derived from numbered citations in the extracted PDF text.",
        "",
        f"- Pages with outgoing references: **{sum(1 for record in records if record.outgoing_refs)}**",
        f"- Pages with backlinks: **{sum(1 for record in records if record.incoming_refs)}**",
        "",
        "## Most Referenced",
        *[
            f"- {wiki_link(by_slug[slug])} ({count} references)"
            for slug, count in citation_counts.most_common(15)
        ],
        "",
        "## Most Outgoing Links",
        *[
            f"- {wiki_link(record)} ({len(record.outgoing_refs)} outgoing references)"
            for record in sorted(records, key=lambda item: (len(item.outgoing_refs), item.title), reverse=True)[:15]
        ],
    ]
    render_index_page(
        CONTENT_DIR / "relationships" / "index.md",
        "Reference Map",
        "Overview of automatically detected cross-references between NPC issuances.",
        relationship_lines,
        default_manual="Add your own interpretive map of how major issuances relate to one another.",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Quartz content from NPC issuances.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync", help="Download source files and refresh JSON metadata.")
    sync_parser.add_argument("--refresh", action="store_true", help="Re-download PDFs even when cached.")

    build_parser = subparsers.add_parser("build", help="Generate Quartz Markdown content from the local cache.")
    build_parser.add_argument("--refresh", action="store_true", help="Refresh the source page before generating content.")

    all_parser = subparsers.add_parser("all", help="Sync source files, then generate Quartz content.")
    all_parser.add_argument("--refresh", action="store_true", help="Refresh the source page and all PDFs.")

    args = parser.parse_args()
    ensure_seed_files()

    if args.command in {"sync", "all"}:
        index_entries = save_index_cache()
        records = build_records(index_entries, refresh=args.refresh)
        write_json(records)
        if args.command == "sync":
            print(f"Synced {len(records)} issuances into {ISSUANCES_JSON}")
            return 0

    if args.command == "build":
        index_entries = save_index_cache() if args.refresh else load_cached_index()
        records = build_records(index_entries, refresh=False)
        write_json(records)
        build_content_tree(records)
        print(f"Generated Quartz content with {len(records)} issuances at {CONTENT_DIR}")
        return 0

    if args.command == "all":
        index_entries = load_cached_index()
        records = build_records(index_entries, refresh=False)
        write_json(records)
        build_content_tree(records)
        print(f"Generated Quartz content with {len(records)} issuances at {CONTENT_DIR}")
        return 0

    parser.error("Unsupported command")
    return 1


if __name__ == "__main__":
    sys.exit(main())
