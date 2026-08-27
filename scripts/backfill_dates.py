#!/usr/bin/env python3
"""Backfill missing `date:` YAML frontmatter across the NPC issuances corpus.

quartz.config.ts sets `defaultDateType: "published"`, and the FrontMatter
transformer aliases a `date:` frontmatter key onto both `created` and
`published`. Writing `date: "YYYY-MM-DD"` into a file's existing frontmatter
block is therefore the correct and sufficient fix for pages that currently
fall back to the git/build date.

This script only ever *adds* a `date:` line to files that lack one. It never
rewrites, reorders, or reflows anything else - these are legal texts under
manual curation, and a stray reflow is a defect.

Derivation strategy, most authoritative source first:

  advisory-opinions/
    1. The spelled-out dateline at the top of the "## Text" section of the
       letter itself (e.g. "2 July 2021" or "**26 November 2020**"), read
       from the text between "## Text" and the first "Re:"/"Dear" line.
       This is the actual date written on the letter and is preferred over
       extracted metadata whenever both exist and disagree.
    2. Falls back to the "- Issue date: MM/DD/YYYY" line in the "## Source"
       section (interpreted as MM/DD/YYYY, per the corpus's dominant
       convention - validated against (1) below).

  laws/
    A "Approved: <spelled date>" line in the body (only the Data Privacy Act
    of 2012 carries one; the IRR has no single enactment date and is left
    unresolved on purpose).

  issuances/, orders/, decisions/, resolutions/
    These are >90% already backfilled. Anything still missing a date in
    these trees is checked for a spelled-out "- Issue date: <Month D, YYYY>"
    line in the "## Source" section; if absent (typically index pages,
    undated FAQs, and public advisories with no single issuance date) the
    file is left alone.

Usage:
    python3 scripts/backfill_dates.py             # dry run (default)
    python3 scripts/backfill_dates.py --dry-run    # explicit dry run
    python3 scripts/backfill_dates.py --apply      # write changes
    python3 scripts/backfill_dates.py --apply -v   # verbose per-file log
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

# --- shared file-selection rules (mirrors scripts/validate_content.py) -----

SKIP_MARKDOWN_NAMES = {".cleanup-log.md", "_cleanup-log.md"}
UNPUBLISHED_CONTENT_PREFIXES = ("notes/", "sources/")
FINDER_DUPLICATE_RE = re.compile(r" \d+(?:\.[^/]*)?$")

FRONTMATTER_RE = re.compile(r"\A(---\n)(.*?)(\n---\n)", re.DOTALL)
DATE_KEY_RE = re.compile(r"^date:\s*\S", re.MULTILINE)
DRAFT_TRUE_RE = re.compile(r"^draft:\s*true\s*$", re.MULTILINE)
DRAFT_LINE_RE = re.compile(r"^draft:.*$", re.MULTILINE)

# --- date parsing helpers ---------------------------------------------------

MONTHS_FULL = [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
]
MONTHS_ABBR = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
    "Aug", "Sep", "Sept", "Oct", "Nov", "Dec",
]
MONTH_MAP: dict[str, int] = {}
for _i, _m in enumerate(MONTHS_FULL, start=1):
    MONTH_MAP[_m.lower()] = _i
for _i, _m in enumerate(MONTHS_ABBR, start=1):
    MONTH_MAP["sept" if _m == "Sept" else _m.lower()] = 9 if _m == "Sept" else _i

_MONTH_ALT = "|".join(MONTHS_FULL + MONTHS_ABBR)

# "2 July 2021" / "26th November 2020" / "2 Jul. 2021"
# or "July 2, 2021" / "Jul 2 2021"
SPELLED_DATE_RE = re.compile(
    rf"(?P<d1>\d{{1,2}})(?:st|nd|rd|th)?\.?\s+(?P<month1>{_MONTH_ALT})\.?,?\s+(?P<y1>\d{{4}})"
    rf"|(?P<month2>{_MONTH_ALT})\.?\s+(?P<d2>\d{{1,2}})(?:st|nd|rd|th)?,?\s+(?P<y2>\d{{4}})"
)

ISSUE_DATE_NUMERIC_RE = re.compile(
    r"^- Issue date:\s*(\d{1,2})/(\d{1,2})/(\d{4})\s*$", re.MULTILINE
)
ISSUE_DATE_LINE_RE = re.compile(r"^- Issue date:\s*(.+?)\s*$", re.MULTILINE)

DOC_NUMBER_YEAR_RE = re.compile(r"(?<!\d)(19|20)\d{2}(?=-\d{3}\b)")


def parse_spelled_date(text_window: str) -> date | None:
    m = SPELLED_DATE_RE.search(text_window)
    if not m:
        return None
    if m.group("month1"):
        month = MONTH_MAP[m.group("month1").lower()]
        day = int(m.group("d1"))
        year = int(m.group("y1"))
    else:
        month = MONTH_MAP[m.group("month2").lower()]
        day = int(m.group("d2"))
        year = int(m.group("y2"))
    try:
        return date(year, month, day)
    except ValueError:
        return None


# --- result bookkeeping -----------------------------------------------------


@dataclass
class FileResult:
    path: Path
    status: str  # already_has_date | skipped_unpublished | skipped_draft | resolved | unresolved
    value: date | None = None
    source: str | None = None
    reason: str | None = None
    disagreement: tuple | None = None  # (numeric_field, ground_truth, note)
    year_mismatch: tuple | None = None  # (kind, expected, got)


def iter_candidate_files() -> list[Path]:
    try:
        result = subprocess.run(
            [
                "git", "ls-files", "--cached", "--others", "--exclude-standard",
                "-z", "--", "content",
            ],
            cwd=ROOT, check=True, capture_output=True,
        )
        candidates = [
            ROOT / value
            for value in result.stdout.decode("utf-8", errors="surrogateescape").split("\0")
            if value.endswith(".md")
        ]
    except (OSError, subprocess.CalledProcessError):
        candidates = list(CONTENT_DIR.rglob("*.md"))

    out = []
    for p in candidates:
        if not p.is_file():
            continue
        try:
            rel_parts = p.relative_to(CONTENT_DIR).parts
        except ValueError:
            continue
        if p.name in SKIP_MARKDOWN_NAMES:
            continue
        if any(FINDER_DUPLICATE_RE.search(part) for part in rel_parts):
            continue
        if any(part.startswith(".") for part in rel_parts):
            continue
        out.append(p)
    return sorted(out)


def slug_for(path: Path) -> str:
    return path.relative_to(CONTENT_DIR).with_suffix("").as_posix()


# --- type-specific derivation ------------------------------------------------


def extract_advisory_opinion_date(
    text: str, frontmatter_end: int
) -> tuple[date | None, str | None, tuple | None]:
    """Returns (date, source, disagreement) for an advisory-opinion file."""
    body_after = text[frontmatter_end:]

    numeric_match = ISSUE_DATE_NUMERIC_RE.search(text)

    dateline_date: date | None = None
    text_heading = re.search(r"^## Text\s*\n+", body_after, re.MULTILINE)
    if text_heading:
        after = body_after[text_heading.end():]
        stop = re.search(r"\bRe:|\bDear\b", after)
        window = after[: stop.start()] if stop else after[:300]
        dateline_date = parse_spelled_date(window)

    disagreement = None

    if dateline_date is not None:
        if numeric_match:
            mm, dd, yyyy = (
                int(numeric_match.group(1)),
                int(numeric_match.group(2)),
                int(numeric_match.group(3)),
            )
            try:
                mmdd_as_date = date(yyyy, mm, dd)
            except ValueError:
                mmdd_as_date = None
            if mmdd_as_date != dateline_date:
                note = "issue_date field disagrees with body dateline; using dateline"
                disagreement = (f"{mm:02d}/{dd:02d}/{yyyy}", str(dateline_date), note)
        return dateline_date, "body dateline (## Text)", disagreement

    if numeric_match:
        mm, dd, yyyy = (
            int(numeric_match.group(1)),
            int(numeric_match.group(2)),
            int(numeric_match.group(3)),
        )
        try:
            return date(yyyy, mm, dd), "Issue date field (MM/DD/YYYY)", None
        except ValueError:
            return None, None, None

    return None, None, None


def extract_law_date(text: str) -> tuple[date | None, str | None]:
    # Require the colon (e.g. "**Approved: August 15, 2012**") so a bare
    # "Approved," valediction in a signature block isn't mistaken for it.
    for m in re.finditer(r"\*{0,2}Approved:\*{0,2}\s*", text):
        window = text[m.end(): m.end() + 60]
        d = parse_spelled_date(window)
        if d is not None:
            return d, "'Approved:' line in body"
    return None, None


def extract_generic_spelled_issue_date(text: str) -> tuple[date | None, str | None]:
    """For issuances/orders/decisions/resolutions: their '- Issue date:' lines
    use a spelled month, e.g. '- Issue date: November 12, 2020' (unambiguous,
    unlike the numeric MM/DD/YYYY convention used only in advisory-opinions).
    """
    m = ISSUE_DATE_LINE_RE.search(text)
    if not m:
        return None, None
    d = parse_spelled_date(m.group(1))
    if d is not None:
        return d, "Issue date field (spelled)"
    # ISO-looking fallback, e.g. "2020-11-12"
    iso = re.match(r"(\d{4})-(\d{2})-(\d{2})$", m.group(1).strip())
    if iso:
        try:
            return date(int(iso.group(1)), int(iso.group(2)), int(iso.group(3))), "Issue date field (ISO)"
        except ValueError:
            return None, None
    return None, None


def check_year_mismatch(path: Path, derived: date) -> tuple | None:
    rel_parts = path.relative_to(CONTENT_DIR).parts
    if len(rel_parts) >= 2 and rel_parts[1].isdigit() and len(rel_parts[1]) == 4:
        folder_year = int(rel_parts[1])
        if folder_year != derived.year:
            docnum = DOC_NUMBER_YEAR_RE.search(path.name)
            docnum_year = int(docnum.group(0)) if docnum else None
            return ("folder", folder_year, derived.year, docnum_year)
    return None


def process_file(path: Path) -> FileResult:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return FileResult(path, "unresolved", reason="no YAML frontmatter block")

    body = m.group(2)
    if DATE_KEY_RE.search(body):
        return FileResult(path, "already_has_date")

    slug = slug_for(path)
    if slug.startswith(UNPUBLISHED_CONTENT_PREFIXES):
        return FileResult(path, "skipped_unpublished")

    if DRAFT_TRUE_RE.search(body):
        return FileResult(path, "skipped_draft")

    if not DRAFT_LINE_RE.search(body):
        return FileResult(path, "unresolved", reason="no draft: key to anchor insertion before")

    rel_parts = path.relative_to(CONTENT_DIR).parts
    doc_type = rel_parts[0]

    derived: date | None = None
    src: str | None = None
    disagreement = None

    frontmatter_end = m.end()

    if doc_type == "advisory-opinions":
        derived, src, disagreement = extract_advisory_opinion_date(text, frontmatter_end)
    elif doc_type == "laws":
        derived, src = extract_law_date(text)
    elif doc_type in ("issuances", "orders", "decisions", "resolutions"):
        derived, src = extract_generic_spelled_issue_date(text)
    else:
        return FileResult(
            path, "not_applicable",
            reason=f"'{doc_type}' is a navigation/taxonomy tree, not a dated issuance type",
        )

    if derived is None:
        return FileResult(
            path, "unresolved",
            reason="no spelled-out dateline and no usable Issue date field found",
        )

    year_mismatch = check_year_mismatch(path, derived)

    return FileResult(
        path, "resolved", value=derived, source=src,
        disagreement=disagreement, year_mismatch=year_mismatch,
    )


def apply_date(path: Path, value: date) -> None:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    body = m.group(2)
    draft_match = DRAFT_LINE_RE.search(body)
    insert_at = m.start(2) + draft_match.start()
    new_line = f'date: "{value.isoformat()}"\n'
    new_text = text[:insert_at] + new_line + text[insert_at:]
    path.write_text(new_text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Report what would change (default).")
    mode.add_argument("--apply", action="store_true", help="Write the resolved dates to disk.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print every resolved file, not just a summary.")
    parser.add_argument(
        "--max-disagreement-rate", type=float, default=0.20,
        help="Abort --apply if more than this fraction of cross-checked advisory-opinion "
             "files disagree between the body dateline and the Issue date field (default 0.20).",
    )
    args = parser.parse_args()
    apply_changes = args.apply and not args.dry_run

    files = iter_candidate_files()

    by_status: dict[str, list[FileResult]] = {}
    by_type_resolved: dict[str, int] = {}
    disagreements: list[FileResult] = []
    year_mismatches: list[FileResult] = []
    cross_checked_ao = 0

    results: list[FileResult] = []
    for path in files:
        r = process_file(path)
        results.append(r)
        by_status.setdefault(r.status, []).append(r)
        if r.status == "resolved":
            doc_type = path.relative_to(CONTENT_DIR).parts[0]
            by_type_resolved[doc_type] = by_type_resolved.get(doc_type, 0) + 1
            if r.disagreement:
                disagreements.append(r)
            if r.year_mismatch:
                year_mismatches.append(r)

    # Count how many advisory-opinion files had BOTH signals available, for the
    # disagreement-rate gate (recomputed cheaply from already-loaded results).
    ao_both_signals = 0
    for path, r in zip(files, results):
        if r.status != "resolved":
            continue
        if path.relative_to(CONTENT_DIR).parts[0] != "advisory-opinions":
            continue
        if r.source == "body dateline (## Text)":
            # only counts as "cross-checked" if an Issue date field also exists
            text = path.read_text(encoding="utf-8")
            if ISSUE_DATE_NUMERIC_RE.search(text):
                ao_both_signals += 1

    disagreement_rate = (len(disagreements) / ao_both_signals) if ao_both_signals else 0.0

    print("=" * 72)
    print("Backfill dates - summary")
    print("=" * 72)
    print(f"Candidate files scanned: {len(files)}")
    for status in ("already_has_date", "skipped_unpublished", "skipped_draft", "resolved", "unresolved", "not_applicable"):
        print(f"  {status}: {len(by_status.get(status, []))}")
    print()
    print("Resolved, by content type:")
    for t, n in sorted(by_type_resolved.items()):
        print(f"  {t}: {n}")
    print()
    print(f"Advisory-opinion cross-check: {ao_both_signals} files had both a body dateline "
          f"and an Issue date field; {ao_both_signals - len(disagreements)} agreed, "
          f"{len(disagreements)} disagreed ({disagreement_rate:.1%}).")
    if disagreements:
        print("  Disagreements (resolved using the body dateline, the more authoritative source):")
        for r in disagreements:
            print(f"    {r.path.relative_to(ROOT)}: {r.disagreement[0]} (field) vs {r.disagreement[1]} (dateline) - {r.disagreement[2]}")
    print()
    if year_mismatches:
        print(f"Year sanity-check mismatches ({len(year_mismatches)}) - derived date's year does not "
              f"match its folder year (applied anyway; evidence for the date itself was solid):")
        for r in year_mismatches:
            kind, folder_year, got_year, docnum_year = r.year_mismatch
            print(f"    {r.path.relative_to(ROOT)}: folder={folder_year} docnum={docnum_year} derived_year={got_year} -> {r.value}")
    else:
        print("Year sanity-check: no mismatches.")
    print()

    unresolved = by_status.get("unresolved", [])
    print(f"Unresolved ({len(unresolved)}) - left untouched:")
    for r in unresolved:
        print(f"    {r.path.relative_to(ROOT)}: {r.reason}")
    print()

    if args.verbose:
        print("All resolved files:")
        for r in by_status.get("resolved", []):
            print(f"    {r.path.relative_to(ROOT)}: {r.value} (source: {r.source})")
        print()

    if not apply_changes:
        print("Dry run only - no files were modified. Re-run with --apply to write changes.")
        return 0

    if ao_both_signals and disagreement_rate > args.max_disagreement_rate:
        print(
            f"ABORTING: disagreement rate {disagreement_rate:.1%} exceeds threshold "
            f"{args.max_disagreement_rate:.1%}. Not applying any changes.",
            file=sys.stderr,
        )
        return 1

    applied = 0
    for r in by_status.get("resolved", []):
        apply_date(r.path, r.value)
        applied += 1
    print(f"Applied date: to {applied} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
