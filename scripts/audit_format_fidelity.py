#!/usr/bin/env python3
"""Conservatively audit PDF-to-Markdown formatting fidelity for NPC records.

The audit reads the existing registry files, resolves every primary record's
cached PDF and Markdown page, and compares only high-confidence PDF evidence
with Markdown.  By default it is read-only; ``--apply-safe-reflow`` can join
only conservative three-line-or-longer OCR wrap runs in corpus Markdown.  It
never modifies cleanup state or PDF caches.

Examples:
  python3 scripts/audit_format_fidelity.py --category issuances --year 2024
  python3 scripts/audit_format_fidelity.py --limit 10 --json-output /tmp/audit.json
  python3 scripts/audit_format_fidelity.py --category decisions --markdown-output /tmp/audit.md

MuPDF structured-text JSON is deliberately kept in memory.  The optional
reports contain compact snippets and coordinates, not the raw PDF extraction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import urllib.parse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

# CLI category -> data file / cache folder / display name.
CATEGORIES: dict[str, tuple[str, str, str]] = {
    "issuances": ("issuances", "", "Issuances"),
    "advisory-opinions": ("advisory_opinions", "advisory_opinions", "Advisory opinions"),
    "decisions": ("decisions", "decisions", "Decisions"),
    "resolutions": ("resolutions", "resolutions", "Resolutions"),
    "orders": ("orders", "orders", "Orders"),
}
CATEGORY_ALIASES = {"advisory_opinions": "advisory-opinions", "advisory": "advisory-opinions"}
RECORD_LIST_KEYS = ("records", "issuances", "orders", "decisions", "resolutions")

FRONTMATTER_OPEN = "---"
FOOTNOTE_RE = re.compile(r"(?<!\\)\[\^([^\]\n]+)\]")
FOOTNOTE_DEF_RE = re.compile(r"^ {0,3}\[\^([^\]\n]+)\]:")
HEADING_PREFIX_RE = re.compile(r"^#{1,6}\s+")
LIST_PREFIX_RE = re.compile(r"^(?:[-+*]\s+|\d+[.)]\s+|[a-zA-Z][.)]\s+)")
PDF_NUMBERED_HEADING_RE = re.compile(
    r"^(?:section|rule|article|chapter|part|annex|appendix)\s+"
    r"(?:[a-z0-9ivxlcdm]+|\d+\s*\([a-z0-9]+\))(?=\s*(?:[.:\-–—]|$))",
    re.IGNORECASE,
)
PDF_LABEL_HEADING_RE = re.compile(
    r"^(?:facts?|issue|discussion|disposition|resolution|background|scope|definitions?|general\s+provisions?)\s*[:.]?$",
    re.IGNORECASE,
)
OPERATIVE_ALL_CAPS_RE = re.compile(
    r"\b(?:WHEREFORE|SO\s+ORDERED|ORDERED|RESOLVED|CLOSED|TERMINATED|SECTION|RULE|ARTICLE)\b"
)
SEMANTIC_EMPHASIS_RE = re.compile(
    r"\b(?:section|rule|article|chapter|part|annex|appendix|wherefore|so\s+ordered|"
    r"whereas|case\s+no|republic\s+act|data\s+privacy\s+act|\bdpa\b|\birr\b|"
    r"v\.?|vs\.?)\b",
    re.IGNORECASE,
)
HEADER_NOISE_RE = re.compile(
    r"^(?:republic of the philippines|national privacy commission|"
    r"commission on human rights|privacy\.gov\.ph|page\s*\d+)$",
    re.IGNORECASE,
)
TERMINAL_PUNCTUATION = ".?!:;"


@dataclass(frozen=True)
class Record:
    category: str
    title: str
    year: str
    markdown_path: Path
    pdf_path: Path
    ocr_used: bool


@dataclass(frozen=True)
class Finding:
    category: str
    year: str
    markdown_path: str
    pdf_path: str
    code: str
    severity: str
    message: str
    line: int | None = None
    source_page: int | None = None
    source_text: str | None = None
    target_text: str | None = None
    confidence: str = "high"

    def as_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "year": self.year,
            "markdown_path": self.markdown_path,
            "pdf_path": self.pdf_path,
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "line": self.line,
            "source_page": self.source_page,
            "source_text": self.source_text,
            "target_text": self.target_text,
            "confidence": self.confidence,
        }


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def normalize_text(value: str) -> str:
    """Normalize for exact word-sequence comparison, retaining word boundaries."""
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def compact(value: str, limit: int = 180) -> str:
    value = " ".join(value.split())
    return value if len(value) <= limit else value[: limit - 3].rstrip() + "..."


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return value.strip("-") or "issuance"


def cache_stem(source_url: str) -> str:
    """Mirror the existing decisions/resolutions cache-name algorithm."""
    basename = urllib.parse.unquote(Path(urllib.parse.urlparse(source_url).path).stem)
    digest = hashlib.sha1(source_url.encode("utf-8")).hexdigest()[:10]
    return f"{slugify(basename)}-{digest}"


def record_list(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in RECORD_LIST_KEYS:
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def normalize_category(value: str) -> str:
    value = CATEGORY_ALIASES.get(value, value)
    if value not in CATEGORIES:
        choices = ", ".join(CATEGORIES)
        raise ValueError(f"unknown category {value!r}; choose from: {choices}")
    return value


def resolve_pdf_path(category: str, item: dict[str, Any]) -> Path:
    explicit = item.get("pdf_path")
    if isinstance(explicit, str) and explicit:
        return ROOT / explicit
    source_url = item.get("source_url")
    cache_folder = CATEGORIES[category][1]
    if isinstance(source_url, str) and source_url and cache_folder:
        return ROOT / "cache" / cache_folder / "pdfs" / f"{cache_stem(source_url)}.pdf"
    return ROOT / "__missing_pdf_path__"


def load_records(categories: Iterable[str], years: set[str]) -> list[Record]:
    records: list[Record] = []
    for category in categories:
        data_name = CATEGORIES[category][0]
        data_path = DATA_DIR / f"{data_name}.json"
        try:
            payload = json.loads(data_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            # The caller emits a per-record-style mapping issue below only when
            # it has a record.  A registry-level finding is added in main.
            continue
        for item in record_list(payload):
            markdown = item.get("content_path") or item.get("markdown_path")
            if not isinstance(markdown, str) or not markdown:
                continue
            year = str(item.get("year") or Path(markdown).parent.name or "unknown")
            if years and year not in years:
                continue
            records.append(
                Record(
                    category=category,
                    title=str(item.get("title") or item.get("reference_label") or Path(markdown).stem),
                    year=year,
                    markdown_path=ROOT / markdown,
                    pdf_path=resolve_pdf_path(category, item),
                    ocr_used=bool(item.get("ocr_used")),
                )
            )
    return sorted(records, key=lambda item: (item.category, item.year, item.markdown_path.as_posix()))


def finding(record: Record, code: str, severity: str, message: str, **kwargs: Any) -> Finding:
    return Finding(
        category=record.category,
        year=record.year,
        markdown_path=rel(record.markdown_path),
        pdf_path=rel(record.pdf_path),
        code=code,
        severity=severity,
        message=message,
        **kwargs,
    )


def frontmatter_end(lines: list[str]) -> tuple[int, list[Finding]]:
    """Return content start and conservative structural frontmatter findings."""
    issues: list[Finding] = []
    if not lines or lines[0].strip() != FRONTMATTER_OPEN:
        return 0, issues
    for index in range(1, len(lines)):
        if lines[index].strip() == FRONTMATTER_OPEN:
            return index + 1, issues
    return 0, issues


def is_fence(line: str) -> bool:
    return bool(re.match(r"^\s*(```|~~~)", line))


def markdown_style_matches(line: str, phrase: str, want_bold: bool, want_italic: bool) -> bool:
    """Check whether a uniquely matching phrase is inside matching Markdown emphasis."""
    needle = normalize_text(phrase)
    if not needle:
        return True
    if want_bold and HEADING_PREFIX_RE.match(line):
        # Quartz headings are visually bold; a PDF bold heading need not carry **.
        want_bold = False
    patterns: list[tuple[re.Pattern[str], bool, bool]] = [
        (re.compile(r"\*\*\*([^*\n]+)\*\*\*"), True, True),
        (re.compile(r"\*\*([^*\n]+)\*\*"), True, False),
        (re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)"), False, True),
        (re.compile(r"__([^_\n]+)__"), True, False),
        (re.compile(r"(?<!_)_([^_\n]+)_(?!_)"), False, True),
    ]
    for pattern, bold, italic in patterns:
        if want_bold and not bold:
            continue
        if want_italic and not italic:
            continue
        for match in pattern.finditer(line):
            styled = normalize_text(match.group(1))
            if f" {needle} " in f" {styled} ":
                return True
    return not want_bold and not want_italic


def markdown_heading_like(line: str, phrase: str) -> bool:
    if HEADING_PREFIX_RE.match(line):
        return True
    # Existing legal pages sometimes encode a section head as an emphasized
    # line rather than an ATX heading, e.g. **SECTION 1.** ***Title.***.
    if "**" in line and (PDF_NUMBERED_HEADING_RE.match(phrase.strip()) or PDF_LABEL_HEADING_RE.match(phrase.strip())):
        return True
    return False


def prose_line(line: str) -> bool:
    stripped = line.strip()
    if len(stripped) < 35 or stripped.startswith(("#", ">", "<", "<!--", "[^") ):
        return False
    if LIST_PREFIX_RE.match(stripped) or stripped in {"---", "***", "___"}:
        return False
    if "|" in stripped and stripped.count("|") >= 2:
        return False
    return bool(re.search(r"[A-Za-z]{4}", stripped))


def is_wrap_transition(current: str, following: str) -> bool:
    raw_current = current
    current = current.strip()
    following = following.strip()
    if not prose_line(current) or not prose_line(following):
        return False
    if current[-1:] in TERMINAL_PUNCTUATION or raw_current.endswith("  "):
        return False
    # Parenthesized legal-list markers are structural even when their text is
    # long enough to resemble prose.  Joining before one collapses distinct
    # source items such as ``(a)``/``(b)`` or ``(5)``/``(6)``.
    if re.match(r"^\((?:[a-z]|\d+|[ivxlcdm]+)\)\s", following, re.IGNORECASE):
        return False
    return bool(re.match(r"^[a-z(\[\"']", following))


def wrap_join_separator(current: str, following: str) -> str:
    """Return the safe separator for one conservative PDF-line-wrap join."""
    current = current.rstrip()
    following = following.lstrip()
    if current.endswith(("-", "/")) and following[:1].islower():
        return ""
    # A wrapped wikilink target must not acquire whitespace.  Display text,
    # which follows the pipe, remains ordinary prose and keeps one space.
    opening = current.rfind("[[")
    closing = current.rfind("]]" )
    if opening > closing and "|" not in current[opening:]:
        return ""
    return " "


def safe_reflow_markdown(text: str) -> tuple[str, int]:
    """Join only flush-left runs already reported as likely OCR hard wraps."""
    lines = text.splitlines()
    trailing_newline = text.endswith("\n")
    content_start, _ = frontmatter_end(lines)
    output = lines[:content_start]
    index = content_start
    joins = 0
    in_fence = False
    while index < len(lines):
        line = lines[index]
        if is_fence(line):
            in_fence = not in_fence
            output.append(line)
            index += 1
            continue
        if in_fence or index + 2 >= len(lines) or line != line.lstrip():
            output.append(line)
            index += 1
            continue
        if not is_wrap_transition(line, lines[index + 1]):
            output.append(line)
            index += 1
            continue
        end = index + 1
        while (
            end + 1 < len(lines)
            and lines[end] == lines[end].lstrip()
            and lines[end + 1] == lines[end + 1].lstrip()
            and is_wrap_transition(lines[end], lines[end + 1])
        ):
            end += 1
        if end - index < 2:
            output.append(line)
            index += 1
            continue
        merged = lines[index].rstrip()
        for continuation in lines[index + 1 : end + 1]:
            merged += wrap_join_separator(merged, continuation) + continuation.strip()
            joins += 1
        output.append(merged)
        index = end + 1
    result = "\n".join(output)
    if trailing_newline:
        result += "\n"
    return result, joins


def audit_markdown(record: Record, text: str) -> tuple[list[Finding], list[tuple[int, str]]]:
    findings: list[Finding] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_OPEN:
        findings.append(finding(record, "markdown.frontmatter-missing", "high", "missing YAML frontmatter"))
        content_start = 0
    else:
        content_start = 0
        for index in range(1, len(lines)):
            if lines[index].strip() == FRONTMATTER_OPEN:
                content_start = index + 1
                break
        else:
            findings.append(
                finding(record, "markdown.frontmatter-unclosed", "high", "opening YAML frontmatter has no closing delimiter")
            )
        if content_start and not any(re.match(r"^title\s*:\s*\S", line) for line in lines[1 : content_start - 1]):
            findings.append(finding(record, "markdown.frontmatter-title-missing", "high", "YAML frontmatter has no title field"))
    if content_start and any("\t" in line for line in lines[:content_start]):
        findings.append(finding(record, "markdown.frontmatter-tab", "medium", "tab found in YAML frontmatter"))

    content = list(enumerate(lines[content_start:], start=content_start + 1))
    visible_lines: list[tuple[int, str]] = []
    in_fence = False
    in_indented_code = False
    for position, (line_number, line) in enumerate(content):
        if is_fence(line):
            in_fence = not in_fence
            in_indented_code = False
            continue
        if in_fence:
            continue
        visible_lines.append((line_number, line))
        stripped = line.strip()
        if not stripped:
            continue
        previous_line = content[position - 1][1] if position else ""
        previous = previous_line.strip()
        previous_blank = not previous
        previous_nonblank = ""
        if previous_blank:
            for prior_position in range(position - 2, -1, -1):
                candidate = content[prior_position][1].strip()
                if candidate:
                    previous_nonblank = candidate
                    break
        if line.startswith("\t") or re.match(r"^ {4,}\S", line):
            # CommonMark indented code cannot interrupt a paragraph.  Raw PDF
            # extraction frequently emits a flush-left first line followed by
            # indented visual continuations; those continuations remain part of
            # the paragraph and must not be reported as code.  Flag only a run
            # that starts after a blank line (or continues a run already known
            # to be code), while conservatively excluding nested list bodies.
            nested_list_body = previous_blank and bool(LIST_PREFIX_RE.match(previous_nonblank))
            starts_code = previous_blank and not nested_list_body
            if in_indented_code or starts_code:
                findings.append(
                    finding(
                        record,
                        "markdown.indented-code-risk",
                        "high",
                        "four-space or tab indentation will render as a code block",
                        line=line_number,
                        target_text=compact(line),
                    )
                )
                in_indented_code = True
            else:
                in_indented_code = False
        elif re.match(r"^ {2,3}\S", line) and not re.match(r"^ {2,3}(?:[-+*]|\d+[.)]|\[\^)", line):
            in_indented_code = False
            if not previous.startswith(("-", "*", "+", ">")):
                findings.append(
                    finding(
                        record,
                        "markdown.suspicious-indent",
                        "medium",
                        "orphan two/three-space indentation may be OCR residue",
                        line=line_number,
                        target_text=compact(line),
                        confidence="medium",
                    )
                )
        else:
            in_indented_code = False
    if in_fence:
        findings.append(finding(record, "markdown.fence-unclosed", "high", "unclosed fenced code block"))

    definitions: dict[str, list[int]] = {}
    references: dict[str, list[int]] = {}
    for line_number, line in visible_lines:
        definition = FOOTNOTE_DEF_RE.match(line)
        if definition:
            definitions.setdefault(definition.group(1), []).append(line_number)
        for match in FOOTNOTE_RE.finditer(line):
            label = match.group(1)
            if definition and match.start() == definition.start():
                continue
            references.setdefault(label, []).append(line_number)
    for label, locations in sorted(references.items()):
        if label not in definitions:
            findings.append(
                finding(
                    record,
                    "markdown.footnote-undefined",
                    "high",
                    f"footnote reference [^{label}] has no definition",
                    line=locations[0],
                )
            )
    for label, locations in sorted(definitions.items()):
        if len(locations) > 1:
            findings.append(
                finding(
                    record,
                    "markdown.footnote-duplicate-definition",
                    "high",
                    f"footnote [^{label}] is defined {len(locations)} times",
                    line=locations[1],
                )
            )
        if label not in references:
            findings.append(
                finding(
                    record,
                    "markdown.footnote-orphan-definition",
                    "medium",
                    f"footnote [^{label}] is defined but never referenced",
                    line=locations[0],
                    confidence="medium",
                )
            )

    # Report runs only when three prose lines form two likely hard-wrap joins.
    just_lines = [line for _, line in visible_lines]
    just_numbers = [number for number, _ in visible_lines]
    index = 0
    while index + 2 < len(just_lines):
        if not is_wrap_transition(just_lines[index], just_lines[index + 1]):
            index += 1
            continue
        end = index + 1
        while end + 1 < len(just_lines) and is_wrap_transition(just_lines[end], just_lines[end + 1]):
            end += 1
        if end - index >= 2:
            findings.append(
                finding(
                    record,
                    "markdown.ocr-wrap-run",
                    "medium",
                    f"{end - index + 1} consecutive prose lines look like hard-wrapped OCR text",
                    line=just_numbers[index],
                    target_text=compact(" ".join(just_lines[index : end + 1])),
                    confidence="medium",
                )
            )
        index = end + 1
    return findings, visible_lines


def run_mutool(pdf_path: Path) -> dict[str, Any]:
    process = subprocess.run(
        ["mutool", "draw", "-q", "-F", "stext.json", "-o", "-", str(pdf_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode:
        detail = process.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(detail or f"mutool exited {process.returncode}")
    try:
        return json.loads(process.stdout.decode("utf-8", errors="replace"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"mutool returned invalid structured text: {exc.msg}") from exc


def pdf_segments(payload: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return visual lines and styled text runs from MuPDF's structured text."""
    visual_lines: list[dict[str, Any]] = []
    styled_runs: list[dict[str, Any]] = []
    for page_index, page in enumerate(payload.get("pages", []), start=1):
        for block in page.get("blocks", []):
            if block.get("type") != "text":
                continue
            grouped: dict[int, list[dict[str, Any]]] = {}
            for segment in block.get("lines", []):
                text = str(segment.get("text") or "")
                font = segment.get("font") or {}
                y = float(segment.get("y") or (segment.get("bbox") or {}).get("y") or 0)
                key = round(y * 2)  # 0.5-point buckets preserve baselines but group font runs.
                item = {
                    "text": text,
                    "x": float(segment.get("x") or (segment.get("bbox") or {}).get("x") or 0),
                    "y": y,
                    "size": float(font.get("size") or 0),
                    "bold": str(font.get("weight") or "").lower() in {"bold", "semibold", "black"},
                    "italic": str(font.get("style") or "").lower() in {"italic", "oblique"},
                    "page": page_index,
                }
                grouped.setdefault(key, []).append(item)
                normalized = normalize_text(text)
                if normalized and (item["bold"] or item["italic"]):
                    styled_runs.append(item)
            for segments in grouped.values():
                segments.sort(key=lambda item: item["x"])
                text = "".join(item["text"] for item in segments)
                if not normalize_text(text):
                    continue
                visual_lines.append(
                    {
                        "text": text,
                        "x": min(item["x"] for item in segments),
                        "y": median(item["y"] for item in segments),
                        "size": max(item["size"] for item in segments),
                        "bold": any(item["bold"] for item in segments),
                        "italic": any(item["italic"] for item in segments),
                        "page": page_index,
                    }
                )
    return visual_lines, styled_runs


def occurrence_lines(visible_lines: list[tuple[int, str]], phrase: str) -> list[tuple[int, str]]:
    needle = normalize_text(phrase)
    if not needle:
        return []
    return [
        (line_number, line)
        for line_number, line in visible_lines
        if f" {needle} " in f" {normalize_text(line)} "
    ]


def meaningful_style_run(item: dict[str, Any]) -> bool:
    text = compact(str(item["text"]), 140)
    normalized = normalize_text(text)
    words = normalized.split()
    if not normalized or sum(char.isalpha() for char in text) < 4 or len(normalized) < 4 or len(words) > 14:
        return False
    if HEADER_NOISE_RE.match(text.strip()):
        return False
    if text.strip().isupper() and len(words) > 1 and not OPERATIVE_ALL_CAPS_RE.search(text):
        # Signatures, offices, and copy-furnished recipients often use bold
        # capitals in a PDF but do not need Markdown emphasis.
        return False
    if not OPERATIVE_ALL_CAPS_RE.search(text) and not SEMANTIC_EMPHASIS_RE.search(text):
        # PDF fonts are often switched to italic for whole witness quotations
        # and quotations.  Fragment-level comparison cannot reliably say those
        # Markdown lines need emphasis, so reserve findings for legal/operative
        # anchors whose formatting is meaningful to the reader.
        return False
    # A single lowercase word is normally typographic noise.  Preserve all
    # multiword and prominent operative single-word candidates.
    return len(words) > 1 or text.strip().isupper() or len(normalized) >= 9


def audit_pdf_comparison(record: Record, visible_lines: list[tuple[int, str]]) -> list[Finding]:
    findings: list[Finding] = []
    try:
        payload = run_mutool(record.pdf_path)
    except (OSError, RuntimeError) as exc:
        return [finding(record, "pdf.unreadable", "high", f"cannot extract structured PDF text: {compact(str(exc))}")]
    visual_lines, styled_runs = pdf_segments(payload)
    alpha = sum(sum(char.isalpha() for char in str(item["text"])) for item in visual_lines)
    if alpha < 180:
        findings.append(
            finding(
                record,
                "pdf.unusable-text",
                "high",
                "PDF has too little structured text for a reliable formatting comparison",
            )
        )
        return findings
    if record.ocr_used:
        findings.append(
            finding(
                record,
                "pdf.ocr-source",
                "medium",
                "registry marks this PDF as OCR-derived; style/layout comparisons are lower confidence",
                confidence="medium",
            )
        )

    body_sizes = [item["size"] for item in visual_lines if 7 <= item["size"] <= 16]
    body_size = median(body_sizes) if body_sizes else median([item["size"] for item in visual_lines])
    heading_seen: set[str] = set()
    for item in visual_lines:
        text = compact(str(item["text"]), 160)
        normalized = normalize_text(text)
        if not normalized or normalized in heading_seen or HEADER_NOISE_RE.match(text.strip()):
            continue
        heading_signal = PDF_NUMBERED_HEADING_RE.match(text.strip()) is not None or PDF_LABEL_HEADING_RE.match(text.strip()) is not None
        typography_signal = bool(item["bold"]) or item["size"] >= body_size * 1.12
        if not heading_signal or not typography_signal:
            continue
        matches = occurrence_lines(visible_lines, text)
        if len(matches) != 1:
            continue
        line_number, markdown_line = matches[0]
        if not markdown_heading_like(markdown_line, text):
            findings.append(
                finding(
                    record,
                    "pdf.heading-not-structured",
                    "medium",
                    "PDF heading candidate appears once in Markdown but is not a heading/emphasized legal section",
                    line=line_number,
                    source_page=int(item["page"]),
                    source_text=text,
                    target_text=compact(markdown_line),
                    confidence="medium",
                )
            )
        heading_seen.add(normalized)

    # Only unique PDF style runs which also occur exactly once in Markdown can
    # yield a finding.  That conservatively avoids broad body-font and repeated
    # header/footer false positives.
    style_counts = Counter(normalize_text(str(item["text"])) for item in styled_runs if meaningful_style_run(item))
    compared = 0
    for item in sorted(styled_runs, key=lambda value: (value["page"], value["y"], value["x"], str(value["text"]))):
        if not meaningful_style_run(item):
            continue
        text = compact(str(item["text"]), 140)
        normalized = normalize_text(text)
        if style_counts[normalized] != 1:
            continue
        matches = occurrence_lines(visible_lines, text)
        if len(matches) != 1:
            continue
        compared += 1
        if compared > 300:
            break
        line_number, markdown_line = matches[0]
        if not markdown_style_matches(markdown_line, text, bool(item["bold"]), bool(item["italic"])):
            style_name = "bold italic" if item["bold"] and item["italic"] else "bold" if item["bold"] else "italic"
            findings.append(
                finding(
                    record,
                    "pdf.emphasis-missing",
                    "medium",
                    f"PDF {style_name} phrase appears exactly once in Markdown without matching emphasis",
                    line=line_number,
                    source_page=int(item["page"]),
                    source_text=text,
                    target_text=compact(markdown_line),
                    confidence="medium",
                )
            )
    return findings


def audit_record(record: Record) -> list[Finding]:
    findings: list[Finding] = []
    if not record.markdown_path.exists():
        return [finding(record, "mapping.markdown-missing", "high", "registry Markdown path does not exist")]
    if not record.pdf_path.exists():
        return [finding(record, "mapping.pdf-missing", "high", "cached PDF path does not exist")]
    text = record.markdown_path.read_text(encoding="utf-8", errors="replace")
    markdown_findings, visible_lines = audit_markdown(record, text)
    findings.extend(markdown_findings)
    findings.extend(audit_pdf_comparison(record, visible_lines))
    return findings


def sort_findings(items: Iterable[Finding]) -> list[Finding]:
    severity_order = {"high": 0, "medium": 1, "low": 2, "info": 3}
    return sorted(
        items,
        key=lambda item: (
            item.category,
            item.year,
            item.markdown_path,
            item.line or 0,
            severity_order.get(item.severity, 9),
            item.code,
            item.source_page or 0,
            item.source_text or "",
        ),
    )


def build_report(records: list[Record], findings: list[Finding], categories: list[str], years: set[str]) -> dict[str, Any]:
    ordered = sort_findings(findings)
    severity_counts = Counter(item.severity for item in ordered)
    code_counts = Counter(item.code for item in ordered)
    return {
        "scope": {
            "categories": categories,
            "years": sorted(years),
            "records_scanned": len(records),
            "raw_mutool_json_retained": False,
        },
        "summary": {
            "findings": len(ordered),
            "by_severity": dict(sorted(severity_counts.items())),
            "by_code": dict(sorted(code_counts.items())),
        },
        "findings": [item.as_dict() for item in ordered],
    }


def markdown_report(report: dict[str, Any]) -> str:
    scope = report["scope"]
    summary = report["summary"]
    lines = [
        "# PDF-to-Markdown Formatting Fidelity Audit",
        "",
        f"- Categories: {', '.join(scope['categories'])}",
        f"- Years: {', '.join(scope['years']) if scope['years'] else 'all'}",
        f"- Records scanned: {scope['records_scanned']}",
        f"- Findings: {summary['findings']}",
        "- Raw MuPDF JSON retained: no",
        "",
        "## Findings",
        "",
        "| Severity | Code | Markdown | Location | Evidence |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in report["findings"]:
        location = f"p.{item['source_page']}" if item["source_page"] else ""
        if item["line"]:
            location = f"{location} / L{item['line']}".strip(" /")
        evidence = item["source_text"] or item["target_text"] or item["message"]
        evidence = str(evidence).replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {item['severity']} | `{item['code']}` | `{item['markdown_path']}` | {location} | {evidence} |"
        )
    return "\n".join(lines) + "\n"


def write_output(path_arg: str, content: str) -> None:
    if path_arg == "-":
        sys.stdout.write(content)
        return
    path = Path(path_arg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Conservative PDF-to-Markdown formatting fidelity audit.")
    parser.add_argument("--category", action="append", default=[], help="Corpus category; repeatable (default: all).")
    parser.add_argument("--year", action="append", default=[], help="Record year; repeatable (default: all).")
    parser.add_argument("--limit", type=int, help="Scan at most N deterministically sorted records.")
    parser.add_argument(
        "--apply-safe-reflow",
        action="store_true",
        help="Join only conservative flush-left runs of three or more PDF-wrapped prose lines before auditing.",
    )
    parser.add_argument("--json-output", help="Write deterministic JSON report to this path, or - for stdout.")
    parser.add_argument("--markdown-output", help="Write deterministic Markdown report to this path, or - for stdout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.limit is not None and args.limit < 1:
        print("--limit must be positive", file=sys.stderr)
        return 2
    if args.json_output == "-" and args.markdown_output == "-":
        print("only one report format may use stdout", file=sys.stderr)
        return 2
    try:
        selected_categories = [normalize_category(value) for raw in args.category for value in raw.split(",")]
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    categories = list(dict.fromkeys(selected_categories or list(CATEGORIES)))
    years = {value for raw in args.year for value in raw.split(",") if value}
    records = load_records(categories, years)
    if args.limit is not None:
        records = records[: args.limit]
    if args.apply_safe_reflow:
        changed_files = 0
        joined_lines = 0
        for record in records:
            if not record.markdown_path.exists():
                continue
            original = record.markdown_path.read_text(encoding="utf-8", errors="replace")
            updated, joins = safe_reflow_markdown(original)
            if not joins or updated == original:
                continue
            record.markdown_path.write_text(updated, encoding="utf-8")
            changed_files += 1
            joined_lines += joins
        print(f"Safe reflow changed {changed_files} file(s); joined {joined_lines} wrapped line(s).", file=sys.stderr)
    findings: list[Finding] = []
    for record in records:
        findings.extend(audit_record(record))
    report = build_report(records, findings, categories, years)
    if args.json_output:
        write_output(args.json_output, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    if args.markdown_output:
        write_output(args.markdown_output, markdown_report(report))
    if not args.json_output and not args.markdown_output:
        summary = report["summary"]
        print(f"Scanned {report['scope']['records_scanned']} record(s); {summary['findings']} finding(s).")
        for key, value in summary["by_severity"].items():
            print(f"  {key}: {value}")
        for item in report["findings"][:50]:
            line = f":{item['line']}" if item["line"] else ""
            page = f" PDF p.{item['source_page']}" if item["source_page"] else ""
            print(f"- [{item['severity']}] {item['code']} {item['markdown_path']}{line}{page} — {item['message']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
