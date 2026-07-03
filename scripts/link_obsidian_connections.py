#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import build_npc_site as core


ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

DEFAULT_TARGET_DIRS = (
    "advisory-opinions",
    "decisions",
    "issuances",
    "orders",
    "resolutions",
)
SKIP_PARTS = {
    ".obsidian",
    ".quartz-cache",
    "node_modules",
    "sources",
}
SKIP_NAMES = {
    ".cleanup-log.md",
    "_cleanup-log.md",
}

FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)(?:\n---\n|\n---\Z)", re.DOTALL)
PROTECTED_RE = re.compile(
    r"\[\[[\s\S]*?\]\]"
    r"|\[[^\]\n]+\]\([^)]+\)"
    r"|`[^`\n]*`"
    r"|https?://[^\s<>)\]}]+",
    re.IGNORECASE,
)

DPA_SECTION_RE = re.compile(
    r"\bSection\s+(?P<section>\d+[A-Za-z]?)"
    r"(?P<subsection>\s*\([^)]+\))?"
    r"\s+of\s+the\s+"
    r"(?P<law>DPA|Data Privacy Act(?:\s+of\s+2012)?)\b",
    re.IGNORECASE,
)
IRR_SECTION_RE = re.compile(
    r"\bSection\s+(?P<section>\d+[A-Za-z]?)"
    r"(?P<subsection>\s*\([^)]+\))?"
    r"\s+of\s+the\s+"
    r"(?P<law>IRR|Implementing Rules and Regulations)\b",
    re.IGNORECASE,
)
DPA_RE = re.compile(
    r"\b(?:Republic\s+Act\s+No\.?\s+10173|R\.?\s*A\.?\s*(?:No\.?\s*)?10173|"
    r"Data\s+Privacy\s+Act(?:\s+of\s+2012)?|DPA)\b",
    re.IGNORECASE,
)
IRR_RE = re.compile(
    r"\b(?:Implementing\s+Rules\s+and\s+Regulations|DPA\s+IRR|IRR)\b",
    re.IGNORECASE,
)

CASE_REFERENCE_HINT_RE = re.compile(
    r"\b(?:NPC|CID|PS|PDD)"
    r"(?:\s+(?:BN|CN|SS|CC|SC|ON|OPC|N|D|K|G|J|C))?"
    r"(?:\s+No\.?)?\s+"
    r"(?:\d{2,4}[- ][A-Z]?\d{1,4}|\d{2}[- ][A-Z])\b",
    re.IGNORECASE,
)
EXTENDED_REFERENCE_RE = re.compile(
    r"\b(?:(?:National\s+Privacy\s+Commission|NPC)\s+)?"
    r"(?P<kind>Advisory|Circular|Memorandum Circular|Joint Circular|Joint Advisory|Advisory Opinion|Commission Resolution)"
    r"\s+No\.?\s*(?P<number>[A-Za-z0-9][A-Za-z0-9./-]*(?:\s*[-–—]\s*\d{1,4})?)",
    re.IGNORECASE,
)
NESTED_WIKILINK_RE = re.compile(r"\[\[\[(?P<target>[^\]|#]+(?:#[^\]|]+)?)\|(?P<label>[^\]]+)\]\]\]")
WIKILINK_TARGET_RE = re.compile(r"\[\[(?P<target>[^\]|#]+)(?P<anchor>#[^\]|]+)?(?:\|[^\]]*)?\]\]")
LAW_WIKILINK_RE = re.compile(
    r"\[\[(?P<target>laws/(?:data-privacy-act-of-2012|implementing-rules-and-regulations-of-the-data-privacy-act-of-2012))"
    r"#(?P<anchor>[^\]|]+)\|(?P<label>[^\]]+)\]\]"
)
SECTION_ANCHOR_RE = re.compile(r"\bsection[\s-]+(?P<section>\d+[A-Za-z]?)", re.IGNORECASE)
DATA_SUBJECT_RIGHTS_SPLIT_RE = re.compile(
    r"\[\[issuances/2021/(?:guidelines-on-the-processing-of-personal-data-for-election-campaign-or-partisan-political-activity|guidance-for-the-use-of-the-asean-model-contract-clauses-and-asean-data-management-framework)"
    r"\|NPC Advisory No\. 2021\]\]\s*[–—-]\s*01\]",
    re.IGNORECASE,
)
DATA_SUBJECT_RIGHTS_SPLIT_NO_BRACKET_RE = re.compile(
    r"\[\[issuances/2021/(?:guidelines-on-the-processing-of-personal-data-for-election-campaign-or-partisan-political-activity|guidance-for-the-use-of-the-asean-model-contract-clauses-and-asean-data-management-framework)"
    r"\|NPC Advisory No\. 2021\]\]\s*[–—-]\s*01",
    re.IGNORECASE,
)
DATA_SUBJECT_RIGHTS_SPACED_RE = re.compile(
    r"\[\[issuances/2021/(?:guidelines-on-the-processing-of-personal-data-for-election-campaign-or-partisan-political-activity|guidance-for-the-use-of-the-asean-model-contract-clauses-and-asean-data-management-framework)"
    r"\|NPC Advisory No\. 2021\s*[–—-]\s*01\]\]",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Target:
    path: str
    title: str
    labels: tuple[str, ...]


@dataclass
class Linker:
    reference_targets: dict[str, str]
    literal_targets: dict[str, str]
    literal_re: re.Pattern[str] | None

    def link_body(self, body: str, current_path: str) -> tuple[str, int]:
        changed = 0
        seen_targets: set[str] = set()
        seen_law_targets: set[str] = set()
        linked = collapse_nested_wikilinks(body)
        linked, normalized_count = normalize_existing_law_anchors(linked)
        changed += normalized_count
        linked, data_subject_count = normalize_data_subject_rights_links(linked)
        changed += data_subject_count
        seed_seen_targets(linked, seen_targets, seen_law_targets)

        def phase(text: str, func) -> str:
            pieces: list[str] = []
            last = 0
            for match in PROTECTED_RE.finditer(text):
                segment, count = func(text[last : match.start()])
                nonlocal changed
                changed += count
                pieces.append(segment)
                pieces.append(match.group(0))
                last = match.end()
            segment, count = func(text[last:])
            changed += count
            pieces.append(segment)
            return "".join(pieces)

        linked = phase(
            linked,
            lambda text: self._link_dpa_sections(text, current_path, seen_targets, seen_law_targets),
        )
        linked = phase(
            linked,
            lambda text: self._link_irr_sections(text, current_path, seen_targets, seen_law_targets),
        )
        linked = phase(linked, lambda text: self._link_numbered_references(text, current_path, seen_targets))
        linked = phase(linked, lambda text: self._link_literal_references(text, current_path, seen_targets))
        linked = phase(linked, lambda text: self._link_law_terms(text, current_path, seen_law_targets))
        collapsed = collapse_nested_wikilinks(linked)
        if collapsed != linked:
            changed += linked.count("[[[")
            linked = collapsed
        return linked, changed

    def _link_dpa_sections(
        self,
        text: str,
        current_path: str,
        seen_targets: set[str],
        seen_law_targets: set[str],
    ) -> tuple[str, int]:
        target_base = "laws/data-privacy-act-of-2012"
        if current_path == target_base:
            return text, 0

        count = 0

        def replace(match: re.Match[str]) -> str:
            nonlocal count
            label = core.normalize_space(match.group(0))
            section = match.group("section")
            target = law_section_anchor(target_base, section)
            if target in seen_targets:
                return label
            seen_targets.add(target)
            seen_law_targets.add(target_base)
            count += 1
            return f"[[{target}|{label}]]"

        return DPA_SECTION_RE.sub(replace, text), count

    def _link_irr_sections(
        self,
        text: str,
        current_path: str,
        seen_targets: set[str],
        seen_law_targets: set[str],
    ) -> tuple[str, int]:
        target_base = "laws/implementing-rules-and-regulations-of-the-data-privacy-act-of-2012"
        if current_path == target_base:
            return text, 0

        count = 0

        def replace(match: re.Match[str]) -> str:
            nonlocal count
            label = core.normalize_space(match.group(0))
            section = match.group("section")
            target = law_section_anchor(target_base, section)
            if target in seen_targets:
                return label
            seen_targets.add(target)
            seen_law_targets.add(target_base)
            count += 1
            return f"[[{target}|{label}]]"

        return IRR_SECTION_RE.sub(replace, text), count

    def _link_numbered_references(
        self,
        text: str,
        current_path: str,
        seen_targets: set[str],
    ) -> tuple[str, int]:
        count = 0

        def replace(match: re.Match[str]) -> str:
            nonlocal count
            normalized = normalize_reference_match(match)
            target = self.reference_targets.get(normalized)
            label = core.normalize_space(match.group(0))
            if not target or target == current_path or target in seen_targets:
                return label
            seen_targets.add(target)
            count += 1
            return f"[[{target}|{label}]]"

        linked = EXTENDED_REFERENCE_RE.sub(replace, text)
        linked = core.REFERENCE_PATTERN.sub(replace, linked)
        return linked, count

    def _link_literal_references(
        self,
        text: str,
        current_path: str,
        seen_targets: set[str],
    ) -> tuple[str, int]:
        if not self.literal_re:
            return text, 0

        count = 0

        def replace(match: re.Match[str]) -> str:
            nonlocal count
            label = core.normalize_space(match.group(0))
            key = label.casefold()
            target = self.literal_targets.get(key)
            if not target or target == current_path or target in seen_targets:
                return match.group(0)
            seen_targets.add(target)
            count += 1
            return f"[[{target}|{label}]]"

        return self.literal_re.sub(replace, text), count

    def _link_law_terms(
        self,
        text: str,
        current_path: str,
        seen_law_targets: set[str],
    ) -> tuple[str, int]:
        count = 0

        def dpa_replace(match: re.Match[str]) -> str:
            nonlocal count
            target = "laws/data-privacy-act-of-2012"
            if current_path == target or target in seen_law_targets:
                return match.group(0)
            seen_law_targets.add(target)
            count += 1
            return f"[[{target}|{core.normalize_space(match.group(0))}]]"

        def irr_replace(match: re.Match[str]) -> str:
            nonlocal count
            target = "laws/implementing-rules-and-regulations-of-the-data-privacy-act-of-2012"
            if current_path == target or target in seen_law_targets:
                return match.group(0)
            seen_law_targets.add(target)
            count += 1
            return f"[[{target}|{core.normalize_space(match.group(0))}]]"

        linked = DPA_RE.sub(dpa_replace, text)
        linked = IRR_RE.sub(irr_replace, linked)
        return linked, count


def markdown_target(path: Path) -> str:
    return str(path.relative_to(CONTENT_DIR)).removesuffix(".md")


def collapse_nested_wikilinks(text: str) -> str:
    return NESTED_WIKILINK_RE.sub(r"[[\g<target>|\g<label>]]", text)


def normalize_reference_match(match: re.Match[str]) -> str:
    number = re.sub(r"\s*[-–—]\s*", "-", match.group("number"))
    return core.normalize_reference(match.group("kind"), number)


LAW_SECTION_CACHE: dict[str, dict[str, str]] = {}


def law_section_map(target_base: str) -> dict[str, str]:
    if target_base in LAW_SECTION_CACHE:
        return LAW_SECTION_CACHE[target_base]

    path = CONTENT_DIR / f"{target_base}.md"
    sections: dict[str, str] = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            match = re.match(r"^###\s+(Section\s+(?P<section>\d+[A-Za-z]?)\.\s+.+)$", line)
            if match:
                sections[match.group("section").casefold()] = match.group(1).strip()
    LAW_SECTION_CACHE[target_base] = sections
    return sections


def law_section_anchor(target_base: str, section: str) -> str:
    section_key = section.casefold()
    sections = law_section_map(target_base)
    heading = sections.get(section_key)
    if not heading:
        digit_match = re.match(r"(\d+)", section_key)
        if digit_match:
            heading = sections.get(digit_match.group(1))
    if not heading:
        heading = f"Section {section}"
    return f"{target_base}#{quartz_heading_id(heading)}"


def quartz_heading_id(heading: str) -> str:
    slug = heading.strip().casefold()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def normalize_existing_law_anchors(text: str) -> tuple[str, int]:
    count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal count
        section_match = SECTION_ANCHOR_RE.search(match.group("anchor"))
        if not section_match:
            return match.group(0)
        target = law_section_anchor(match.group("target"), section_match.group("section"))
        replacement = f"[[{target}|{match.group('label')}]]"
        if replacement != match.group(0):
            count += 1
        return replacement

    return LAW_WIKILINK_RE.sub(replace, text), count


def normalize_data_subject_rights_links(text: str) -> tuple[str, int]:
    replacement = "[[issuances/2021/data-subject-rights|NPC Advisory No. 2021-01]]"
    text, split_count = DATA_SUBJECT_RIGHTS_SPLIT_RE.subn(replacement, text)
    text, split_no_bracket_count = DATA_SUBJECT_RIGHTS_SPLIT_NO_BRACKET_RE.subn(replacement, text)
    text, spaced_count = DATA_SUBJECT_RIGHTS_SPACED_RE.subn(replacement, text)
    return text, split_count + split_no_bracket_count + spaced_count


def seed_seen_targets(
    text: str,
    seen_targets: set[str],
    seen_law_targets: set[str],
) -> None:
    for match in WIKILINK_TARGET_RE.finditer(text):
        target = match.group("target").strip()
        anchor = match.group("anchor") or ""
        seen_targets.add(f"{target}{anchor}")
        if target in {
            "laws/data-privacy-act-of-2012",
            "laws/implementing-rules-and-regulations-of-the-data-privacy-act-of-2012",
        }:
            seen_law_targets.add(target)


def split_frontmatter(text: str) -> tuple[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return "", text
    return text[: match.end()], text[match.end() :]


def unquote_yaml_scalar(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if value[0] in {"'", '"'}:
        try:
            parsed = json.loads(value) if value[0] == '"' else value.strip("'")
            return str(parsed)
        except json.JSONDecodeError:
            return value.strip("\"'")
    return value


def parse_frontmatter(frontmatter: str) -> tuple[str, list[str]]:
    title = ""
    aliases: list[str] = []
    current_key = ""

    for raw_line in frontmatter.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped in {"---", ""}:
            continue
        if re.match(r"^[A-Za-z0-9_-]+:", stripped):
            key, value = stripped.split(":", 1)
            current_key = key.strip()
            if current_key == "title":
                title = unquote_yaml_scalar(value)
            elif current_key == "aliases" and value.strip().startswith("["):
                try:
                    aliases.extend(str(item) for item in json.loads(value.strip()))
                except json.JSONDecodeError:
                    pass
            continue
        if current_key == "aliases" and stripped.startswith("-"):
            aliases.append(unquote_yaml_scalar(stripped[1:]))

    return title, [alias for alias in aliases if alias]


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in CONTENT_DIR.rglob("*.md"):
        rel_parts = path.relative_to(CONTENT_DIR).parts
        if any(part in SKIP_PARTS or part.startswith(".") for part in rel_parts):
            continue
        if path.name in SKIP_NAMES:
            continue
        files.append(path)
    return sorted(files)


def build_targets(files: list[Path]) -> list[Target]:
    targets: list[Target] = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        frontmatter, _ = split_frontmatter(text)
        title, aliases = parse_frontmatter(frontmatter)
        labels = []
        if title:
            labels.append(title)
        labels.extend(aliases)
        if "advisory-opinions" in path.parts and title:
            match = re.search(r"Advisory Opinion No\.?\s+\d{4}-\d{1,4}", title, re.IGNORECASE)
            if match:
                labels.append(core.normalize_space(match.group(0)))
        targets.append(Target(markdown_target(path), title, tuple(dict.fromkeys(labels))))
    return targets


def add_reference_target(
    buckets: defaultdict[str, set[str]],
    label: str,
    target_path: str,
) -> None:
    for pattern in (core.REFERENCE_PATTERN, core.NUMBERED_TITLE_PATTERN, core.LOOSE_REFERENCE_PATTERN):
        match = pattern.search(label)
        if not match:
            continue
        kind = match.groupdict().get("kind") or match.groupdict().get("label")
        number = match.groupdict().get("number")
        if kind and number:
            buckets[core.normalize_reference(kind, number)].add(target_path)


def build_linker(targets: list[Target]) -> Linker:
    reference_buckets: defaultdict[str, set[str]] = defaultdict(set)
    literal_buckets: defaultdict[str, set[str]] = defaultdict(set)

    for target in targets:
        for label in target.labels:
            normalized = core.normalize_space(label)
            if not normalized:
                continue
            add_reference_target(reference_buckets, normalized, target.path)
            if CASE_REFERENCE_HINT_RE.fullmatch(normalized):
                literal_buckets[normalized.casefold()].add(target.path)

    reference_targets = {
        key: next(iter(paths))
        for key, paths in reference_buckets.items()
        if len(paths) == 1
    }
    literal_targets = {
        key: next(iter(paths))
        for key, paths in literal_buckets.items()
        if len(paths) == 1
    }

    literal_re = None
    if literal_targets:
        alternatives = sorted(
            (re.escape(label) for label in literal_targets),
            key=len,
            reverse=True,
        )
        literal_re = re.compile(
            r"(?<![\w/])(?:" + "|".join(alternatives) + r")(?![\w/])",
            re.IGNORECASE,
        )

    return Linker(reference_targets, literal_targets, literal_re)


def dirty_content_files() -> set[Path]:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", "content"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    dirty: set[Path] = set()
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        rel = line[3:].strip()
        if rel.startswith('"') and rel.endswith('"'):
            rel = rel[1:-1]
        path = (ROOT / rel).resolve()
        if path.suffix == ".md":
            dirty.add(path)
    return dirty


def target_files(files: list[Path], include_dirs: tuple[str, ...]) -> list[Path]:
    selected: list[Path] = []
    for path in files:
        rel_parts = path.relative_to(CONTENT_DIR).parts
        if include_dirs and rel_parts[0] not in include_dirs:
            continue
        if rel_parts[-1] == "index.md":
            continue
        selected.append(path)
    return selected


def link_file(path: Path, linker: Linker) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    frontmatter, body = split_frontmatter(text)
    current_path = markdown_target(path)
    linked_body, count = linker.link_body(body, current_path)
    if count:
        path.write_text(frontmatter + linked_body, encoding="utf-8")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add high-confidence Obsidian/Quartz links across content markdown."
    )
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing files.")
    parser.add_argument(
        "--include-dirty",
        action="store_true",
        help="Also edit files that already have uncommitted git changes.",
    )
    parser.add_argument(
        "--dirs",
        default=",".join(DEFAULT_TARGET_DIRS),
        help="Comma-separated content subdirectories to linkify.",
    )
    args = parser.parse_args()

    include_dirs = tuple(part.strip() for part in args.dirs.split(",") if part.strip())
    all_files = iter_markdown_files()
    linker = build_linker(build_targets(all_files))
    selected = target_files(all_files, include_dirs)
    dirty_files = set() if args.include_dirty else dirty_content_files()

    changed_files = 0
    total_links = 0
    skipped_dirty = 0
    results: list[tuple[str, int]] = []

    for path in selected:
        if path.resolve() in dirty_files:
            skipped_dirty += 1
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        frontmatter, body = split_frontmatter(text)
        current_path = markdown_target(path)
        linked_body, count = linker.link_body(body, current_path)
        if not count:
            continue
        changed_files += 1
        total_links += count
        results.append((str(path.relative_to(ROOT)), count))
        if not args.dry_run:
            path.write_text(frontmatter + linked_body, encoding="utf-8")

    action = "Would add" if args.dry_run else "Added"
    print(f"{action} {total_links} links across {changed_files} files.")
    print(f"Skipped {skipped_dirty} dirty files.")
    for rel, count in results[:80]:
        print(f"{count:4d}  {rel}")
    if len(results) > 80:
        print(f"... {len(results) - 80} more files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
