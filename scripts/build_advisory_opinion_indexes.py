#!/usr/bin/env python3
"""Generate index.md pages for content/advisory-opinions/ and its year folders.

Offline and rerunnable: scans the markdown files already in the corpus, so it
can run after any cleanup pass without touching the network. Preserves the
MANUAL INDEX NOTES block of existing index pages, matching the behaviour of
build_npc_site.py.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AO_DIR = ROOT / "content" / "advisory-opinions"
SOURCE_URL = "https://privacy.gov.ph/advisory-opinions/"
MANUAL_BEGIN = "<!-- BEGIN MANUAL INDEX NOTES -->"
MANUAL_END = "<!-- END MANUAL INDEX NOTES -->"


def read_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if match:
        title_match = re.search(r"^title:\s*(.+)$", match.group(1), re.M)
        if title_match:
            return title_match.group(1).strip().strip("\"'")
    return path.stem.replace("-", " ").title()


def existing_manual_block(path: Path, default: str) -> str:
    if path.exists():
        match = re.search(
            re.escape(MANUAL_BEGIN) + r"\n(.*?)\n" + re.escape(MANUAL_END),
            path.read_text(encoding="utf-8"),
            re.S,
        )
        if match:
            return match.group(1)
    return default


def write_index(path: Path, title: str, description: str, body_lines: list[str], default_manual: str) -> None:
    manual = existing_manual_block(path, default_manual)
    lines = [
        "---",
        f'title: "{title}"',
        f'description: "{description}"',
        "draft: false",
        "---",
        "",
        *body_lines,
        "",
        "## Manual Notes",
        MANUAL_BEGIN,
        manual,
        MANUAL_END,
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    year_groups: dict[str, list[Path]] = {}
    for year_dir in sorted(AO_DIR.iterdir()):
        if not year_dir.is_dir():
            continue
        files = sorted(
            p
            for p in year_dir.glob("*.md")
            if p.name != "index.md" and not p.name.startswith((".", "_"))
        )
        if files:
            year_groups[year_dir.name] = files

    total = sum(len(files) for files in year_groups.values())

    for year, files in year_groups.items():
        body = [
            f"Advisory opinions issued by the NPC in {year}.",
            "",
            "## Opinions",
            *[
                f"- [[advisory-opinions/{year}/{p.stem}|{read_title(p)}]]"
                for p in files
            ],
        ]
        write_index(
            AO_DIR / year / "index.md",
            f"Advisory Opinions {year}",
            f"NPC advisory opinions issued in {year}.",
            body,
            default_manual=f"Add your own reading guide for {year} advisory opinions here.",
        )

    top_body = [
        "Letters of the NPC responding to requests for advisory opinions on the Data Privacy Act and related issuances.",
        "",
        f"- Corpus size: **{total}** advisory opinions",
        f"- Source page: {SOURCE_URL}",
        "",
        "## Years",
        *[
            f"- [[advisory-opinions/{year}/index|{year}]] ({len(files)} opinions)"
            for year, files in sorted(year_groups.items(), reverse=True)
        ],
    ]
    write_index(
        AO_DIR / "index.md",
        "Advisory Opinions",
        "Browse NPC advisory opinions by year.",
        top_body,
        default_manual="Add your own reading guide for NPC advisory opinions here.",
    )
    print(f"Generated advisory opinion indexes: {len(year_groups)} years, {total} opinions.")


if __name__ == "__main__":
    main()
