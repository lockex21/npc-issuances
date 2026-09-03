#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
DATA_DIR = ROOT / "data"

CONTENT_PATH_KEYS = ("content_path", "markdown_path", "notes_path", "source_note_path")
RECORD_LIST_KEYS = ("records", "issuances", "orders", "decisions", "resolutions")
SKIP_MARKDOWN_NAMES = {".cleanup-log.md", "_cleanup-log.md"}
UNPUBLISHED_CONTENT_PREFIXES = ("notes/", "sources/")
CORPUS_FOLDERS = ("advisory-opinions", "decisions", "resolutions", "orders", "issuances")
UNDATED_FOLDER_NAME = "undated"
INDEX_MARKDOWN_NAME = "index.md"
OBSIDIAN_FOLDER_NAME = ".obsidian"
CLEANUP_STATE_NAME = ".cleanup-state.json"
CLEANUP_STATE_WRAPPER_KEY = "files"

FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)(?:\n---\n|\n---\Z)", re.DOTALL)
WIKILINK_RE = re.compile(r"(?<!!)\[\[(?P<body>[^\]\n]+)\]\]")
BEGIN_MARKER_RE = re.compile(r"<!--\s*BEGIN\s+(?P<label>[^>]+?)\s*-->")
END_MARKER_RE = re.compile(r"<!--\s*END\s+(?P<label>[^>]+?)\s*-->")
FINDER_DUPLICATE_RE = re.compile(r" \d+(?:\.[^/]*)?$")


@dataclass(frozen=True)
class Issue:
    code: str
    path: Path
    message: str
    line: int | None = None

    def display(self) -> str:
        path = self.path.relative_to(ROOT) if self.path.is_absolute() else self.path
        suffix = f":{self.line}" if self.line else ""
        return f"[{self.code}] {path}{suffix} - {self.message}"


@dataclass
class Stats:
    markdown_files: int = 0
    data_records: int = 0
    wikilinks: int = 0
    state_entries: int = 0


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def is_hidden_or_internal(path: Path) -> bool:
    rel_parts = path.relative_to(CONTENT_DIR).parts
    return (
        path.name in SKIP_MARKDOWN_NAMES
        or any(FINDER_DUPLICATE_RE.search(part) for part in rel_parts)
        or any(part.startswith(".") for part in rel_parts)
    )


def iter_markdown_files() -> list[Path]:
    try:
        result = subprocess.run(
            [
                "git",
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "-z",
                "--",
                "content",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        candidates = [
            ROOT / value
            for value in result.stdout.decode("utf-8", errors="surrogateescape").split("\0")
            if value.endswith(".md")
        ]
    except (OSError, subprocess.CalledProcessError):
        candidates = list(CONTENT_DIR.rglob("*.md"))
    return sorted(
        path for path in candidates if path.is_file() and not is_hidden_or_internal(path)
    )


def slug_for(path: Path) -> str:
    return path.relative_to(CONTENT_DIR).with_suffix("").as_posix()


def is_unpublished_content(path: Path) -> bool:
    slug = slug_for(path)
    return slug.startswith(UNPUBLISHED_CONTENT_PREFIXES)


# Documents with no determinable issue date: none in the PDF (footer stamps are
# template-revision artifacts) and issue_date is null in the synced index data.
DATE_EXEMPT_SLUGS = {
    "advisory-opinions/2025/advisory-opinion-no-2025-007-npc-advisory-opinion-no-2025-007-redacted",
    "issuances/2020/faqs",
    "issuances/2023/faq-prerequisites-for-the-philippine-privacy-mark-certification-program",
    "issuances/2023/faq-security-of-personal-data-in-the-government-and-the-private-sector",
}


def requires_frontmatter_date(path: Path) -> bool:
    rel_parts = path.relative_to(CONTENT_DIR).parts
    return (
        len(rel_parts) > 1
        and rel_parts[0] in CORPUS_FOLDERS
        and path.name != INDEX_MARKDOWN_NAME
        and UNDATED_FOLDER_NAME not in rel_parts[:-1]
        and slug_for(path) not in DATE_EXEMPT_SLUGS
    )


def iter_finder_duplicates() -> list[Path]:
    matches: list[Path] = []
    for path in CONTENT_DIR.rglob("*"):
        rel_parts = path.relative_to(CONTENT_DIR).parts
        if OBSIDIAN_FOLDER_NAME in rel_parts:
            continue
        if FINDER_DUPLICATE_RE.search(path.name):
            matches.append(path)
    return sorted(matches)


def iter_cleanup_state_files() -> list[Path]:
    return sorted(CONTENT_DIR.rglob(CLEANUP_STATE_NAME))


def load_state_entries(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    wrapped = payload.get(CLEANUP_STATE_WRAPPER_KEY)
    if isinstance(wrapped, dict):
        return wrapped
    return payload


def build_slug_index(markdown_files: list[Path]) -> tuple[set[str], set[str]]:
    slugs: set[str] = set()
    basenames: set[str] = set()
    for path in markdown_files:
        slug = slug_for(path)
        slugs.add(slug)
        basenames.add(Path(slug).name)
        if slug.endswith("/index"):
            slugs.add(slug[: -len("/index")])
    return slugs, basenames


def normalize_link_target(target: str) -> str:
    target = target.strip()
    target = target.removeprefix("content/")
    target = target.removesuffix(".md")
    target = target.strip("/")
    return target


def load_record_list(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in RECORD_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def load_case_override_records(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    records: list[dict[str, Any]] = []
    for overrides in payload.values():
        if not isinstance(overrides, dict):
            continue
        records.extend(value for value in overrides.values() if isinstance(value, dict))
    return records


def validate_data_files(
    issues: list[Issue], stats: Stats, committable_markdown: set[Path]
) -> None:
    for path in sorted(DATA_DIR.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(Issue("json.invalid", path, exc.msg, exc.lineno))
            continue

        records = load_record_list(payload)
        if path.name == "overrides.json" and isinstance(payload, dict):
            records = [value for value in payload.values() if isinstance(value, dict)]
        if path.name == "case_overrides.json":
            records = load_case_override_records(payload)

        stats.data_records += len(records)

        if isinstance(payload, dict):
            declared_count = payload.get("count", payload.get("issuance_count"))
            if isinstance(declared_count, int) and declared_count != len(records):
                issues.append(
                    Issue(
                        "json.count",
                        path,
                        f"declares {declared_count} records but contains {len(records)}",
                    )
                )

        for index, record in enumerate(records):
            title = record.get("title") or record.get("reference_label") or f"record {index}"
            for key in CONTENT_PATH_KEYS:
                value = record.get(key)
                if not isinstance(value, str) or not value:
                    continue
                target = ROOT / value
                if target not in committable_markdown:
                    issues.append(
                        Issue(
                            "data.missing-path",
                            path,
                            f"{key} for {title!r} does not exist: {value}",
                        )
                    )


def validate_frontmatter(path: Path, text: str, issues: list[Issue]) -> None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        issues.append(Issue("markdown.frontmatter", path, "missing YAML frontmatter"))
        return
    body = match.group("body")
    if not re.search(r"(?m)^title:\s*.+", body):
        issues.append(Issue("markdown.title", path, "frontmatter is missing title"))


def validate_frontmatter_date(path: Path, text: str, issues: list[Issue]) -> None:
    if not requires_frontmatter_date(path):
        return
    match = FRONTMATTER_RE.match(text)
    if not match:
        return
    if not re.search(r"(?m)^date:\s*.+", match.group("body")):
        issues.append(Issue("markdown.date", path, "frontmatter is missing date"))


def validate_manual_markers(path: Path, text: str, issues: list[Issue]) -> None:
    stack: list[tuple[str, int]] = []
    events: list[tuple[int, str, str]] = []
    for match in BEGIN_MARKER_RE.finditer(text):
        events.append((match.start(), "begin", " ".join(match.group("label").split())))
    for match in END_MARKER_RE.finditer(text):
        events.append((match.start(), "end", " ".join(match.group("label").split())))

    for offset, event_type, label in sorted(events):
        line = line_for_offset(text, offset)
        if event_type == "begin":
            stack.append((label, line))
            continue

        if not stack:
            issues.append(Issue("markers.unmatched-end", path, f"END {label} has no BEGIN", line))
            continue

        active_label, active_line = stack.pop()
        if active_label != label:
            issues.append(
                Issue(
                    "markers.mismatch",
                    path,
                    f"END {label} closes BEGIN {active_label} from line {active_line}",
                    line,
                )
            )

    for label, line in stack:
        issues.append(Issue("markers.unmatched-begin", path, f"BEGIN {label} has no END", line))


def validate_wikilinks(
    path: Path,
    text: str,
    slugs: set[str],
    basenames: set[str],
    issues: list[Issue],
    stats: Stats,
) -> None:
    if "[[[" in text or "]]]" in text:
        for line_no, line in enumerate(text.splitlines(), start=1):
            if "[[[" in line or "]]]" in line:
                issues.append(
                    Issue("wikilink.nested", path, "malformed nested wikilink marker", line_no)
                )

    for match in WIKILINK_RE.finditer(text):
        raw_target = match.group("body").split("|", 1)[0].split("#", 1)[0]
        target = normalize_link_target(raw_target)
        if not target or target.startswith(("http://", "https://")):
            continue
        if target.startswith("["):
            continue

        stats.wikilinks += 1
        if not is_unpublished_content(path) and target.startswith(UNPUBLISHED_CONTENT_PREFIXES):
            issues.append(
                Issue(
                    "wikilink.unpublished-target",
                    path,
                    f"published page links to unpublished target: {target}",
                    line_for_offset(text, match.start()),
                )
            )
            continue

        if target in slugs or f"{target}/index" in slugs:
            continue
        if "/" not in target and target in basenames:
            continue

        issues.append(
            Issue(
                "wikilink.broken",
                path,
                f"target does not exist: {target}",
                line_for_offset(text, match.start()),
            )
        )


def validate_markdown_files(
    issues: list[Issue], stats: Stats, markdown_files: list[Path]
) -> None:
    slugs, basenames = build_slug_index(markdown_files)
    stats.markdown_files = len(markdown_files)

    for path in markdown_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        validate_frontmatter(path, text, issues)
        validate_frontmatter_date(path, text, issues)
        validate_manual_markers(path, text, issues)
        validate_wikilinks(path, text, slugs, basenames, issues, stats)


def validate_finder_duplicates(issues: list[Issue]) -> None:
    for path in iter_finder_duplicates():
        kind = "directory" if path.is_dir() else "file"
        issues.append(
            Issue(
                "content.finder-duplicate",
                path,
                f"Finder/iCloud sync duplicate {kind}; delete it from the working copy",
            )
        )


def validate_cleanup_state(issues: list[Issue], stats: Stats) -> None:
    for path in iter_cleanup_state_files():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            message = exc.msg if isinstance(exc, json.JSONDecodeError) else str(exc)
            line = exc.lineno if isinstance(exc, json.JSONDecodeError) else None
            issues.append(Issue("state.invalid-json", path, message, line))
            continue

        entries = load_state_entries(payload)
        stats.state_entries += len(entries)
        for name in sorted(entries):
            if not (path.parent / name).is_file():
                issues.append(
                    Issue(
                        "state.ghost-entry",
                        path,
                        f"entry has no matching file in this folder: {name}",
                    )
                )


def main() -> int:
    issues: list[Issue] = []
    stats = Stats()
    markdown_files = iter_markdown_files()

    validate_data_files(issues, stats, set(markdown_files))
    validate_markdown_files(issues, stats, markdown_files)
    validate_finder_duplicates(issues)
    validate_cleanup_state(issues, stats)

    if issues:
        counts = Counter(issue.code for issue in issues)
        print(f"Content validation failed with {len(issues)} issue(s).")
        print("Issue counts:")
        for code, count in sorted(counts.items()):
            print(f"  {code}: {count}")
        print()
        for issue in issues[:200]:
            print(f"- {issue.display()}")
        if len(issues) > 200:
            print(f"- ... {len(issues) - 200} more issue(s) omitted")
        return 1

    print(
        "Content validation passed: "
        f"{stats.markdown_files} markdown files, "
        f"{stats.wikilinks} wikilinks, "
        f"{stats.data_records} data records, "
        f"{stats.state_entries} cleanup-state entries."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
