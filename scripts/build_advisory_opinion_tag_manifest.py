#!/usr/bin/env python3
"""Build the curated advisory-opinion tag manifest from PDF text caches.

Only terms printed in PDF footnotes are included.  The small override table is
for footnotes that are image-only, unlabeled, or affected by broken font text;
each override was checked against a rendered first page of the source PDF.
Website-index tags are never used as a fallback.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "advisory_opinions.json"
OUTPUT_PATH = ROOT / "data" / "advisory_opinion_tags.json"

TAG_LABEL_RE = re.compile(r"(?im)^\s*\d*\s*tags?\s*[:;,]\s*")
NEXT_FOOTNOTE_RE = re.compile(
    r"(?i)^\s*(?:"
    r"\d{1,2}\s+|"
    r"\d{1,2}\s*(?=[A-Z§])|"
    r"\d{1,2}\s*$|"
    r"Ref\.?\s*No\.?|"
    r"\d+(?:st|nd|rd|th)\s+Floor|"
    r"URL\s*:|"
    r"Page\s+\d+"
    r")"
)
PLACEHOLDER_RE = re.compile(r"topics related.*separated by commas", re.IGNORECASE)


# These values are transcriptions, not inferred topics.  Several PDFs omit the
# word "Tags" before footnote 1; others have an image-only first page that the
# corpus-wide pdftotext pass could not read.
PDF_VERIFIED_OVERRIDES: dict[str, list[str]] = {
    # Commas are part of the middle tag; semicolons separate the printed tags.
    "Advisory Opinion No. 2021-033": [
        "sensitive personal information",
        "anti-fraud campaign, training, and awareness",
        "internal disclosure of sensitive personal information",
        "proportionality",
    ],
    # Commas are part of one legal-claims tag; semicolons separate the printed tags.
    "Advisory Opinion No. 2021-040": [
        "Condominium Certificate of Title",
        "lawful processing",
        "consent",
        "establishment, exercise, or defense of legal claims",
        "general data privacy principles",
        "proportionality",
        "privacy impact assessment",
    ],
    "Advisory Opinion No. 2021-043": [
        "data sharing",
        "data sharing agreement",
        "general data privacy principles",
        "law and regulation",
        "consent",
        "statistics",
    ],
    # The comma joins a single legal-claims tag in the printed footnote.
    "Advisory Opinion No. 2022-003": [
        "sensitive personal information",
        "lawful processing",
        "protection of lawful rights and interest of natural or legal persons in court proceedings",
        "establishment, exercise or defense of legal claims",
    ],
    # The comma joins a single legal-claims tag in the printed footnote.
    "Advisory Opinion No. 2022-005": [
        "lawful processing",
        "consent",
        "legitimate interest",
        "protection of lawful rights and interest of natural or legal persons in court proceedings",
        "establishment, exercise or defense of legal claims",
    ],
    "Advisory Opinion No. 2022-010": ["Consent"],
    "Advisory Opinion No. 2022-015": [
        "lawful processing",
        "statutory mandate",
        "photographs",
        "taking of videos",
    ],
    # The comma is internal to one statutory-citation tag.
    "Advisory Opinion No. 2022-017": [
        "personal data",
        "lawful processing",
        "consent of data subjects",
        "legal claims",
        "Sec. 13 (f), DPA",
    ],
    # The citation wraps onto a second PDF line and is one complete tag.
    "Advisory Opinion No. 2022-028": [
        "cancellation of title",
        "lis pendens",
        "tax declaration",
        "certificate of title",
        "tax clearance",
        "establishment of legal claims",
        "Section 13 (f)",
    ],
    "Advisory Opinion No. 2023-004": [
        "subscriber records",
        "subscriber data",
        "Bureau of Internal Revenue",
        "internal revenue tax purposes",
        "special cases",
        "public authority",
    ],
    "Advisory Opinion No. 2023-006": [
        "lawful processing",
        "legitimate interest",
        "proportionality",
        "security measures",
    ],
    "Advisory Opinion No. 2023-008": [
        "Scope",
        "general data privacy principles",
        "law and regulation",
        "lawful processing",
    ],
    "Advisory Opinion No. 2023-009": [
        "data sharing",
        "international body",
        "immunity from suit",
    ],
    "Advisory Opinion No. 2023-010": [
        "lawful processing",
        "legitimate interest",
        "proportionality",
        "security measures",
    ],
    "Advisory Opinion No. 2023-014": [
        "Lawful Processing",
        "Contractual Obligation",
        "Legitimate Interest",
        "Accountability",
    ],
    "Advisory Opinion No. 2023-017": [
        "Lawful Processing",
        "Contractual Obligation",
        "Legitimate Interest",
        "Accountability",
    ],
    "Advisory Opinion No. 2023-027": [
        "Personal information controller",
        "obligations",
        "data sharing",
    ],
    "Advisory Opinion No. 2024-007": [
        "Incident reports",
        "court order",
        "proportionality",
        "law enforcement",
    ],
    "Advisory Opinion No. 2024-009": [
        "Sec. 12 DPA",
        "Personal Information",
        "Fulfillment of Mandate",
        "Publication",
    ],
    "Advisory Opinion No. 2024-019": [
        "Foreign jurisdiction",
        "special cases",
        "legitimate purpose",
        "lawful processing",
    ],
    "Advisory Opinion No. 2025-002": [
        "Scope of DPA",
        "Lawful processing",
        "legitimate interest",
        "legal claims",
    ],
    "Advisory Opinion No. 2025-003": [
        "lawful processing of personal data",
        "access to government records",
        "data privacy principles",
        "consent",
        "legitimate interest",
        "legal obligations",
        "data subject rights",
        "public authority",
    ],
    "Advisory Opinion No. 2025-009": [
        "Transcript of Records",
        "sensitive personal information",
        "security measures",
        "administrative fines",
    ],
    "Advisory Opinion No. 2025-010": [
        "peer-to-peer disclosure",
        "online conversations and group chats",
        "educational institutions",
        "Section 13(f) DP",
        "disciplinary proceedings",
        "reasonable expectation of privacy",
    ],
    # The statutory citations and statute abbreviation form one printed tag.
    "Advisory Opinion No. 2025-012": [
        "Registry of Deeds",
        "Sec. 12(f), 13(f), DPA",
        "Legal claims",
        "Right to access",
    ],
    "Advisory Opinion No. 2025-017": [
        "academic records",
        "student grades",
        "sensitive personal information",
        "data subject rights",
        "right to access",
    ],
    "Advisory Opinion No. 2026-001": [
        "Lawful Processing",
        "Disclosure",
        "Constitutional and Statutory Mandate",
        "Data Privacy Principles",
        "Data Sharing",
        "Authorized Access",
    ],
    # The PDF text layer renders "disclosure" incorrectly; the rendered page
    # was used for this transcription.
    "Advisory Opinion No. 2026-003": [
        "lawful processing",
        "disclosure",
        "legal obligation",
        "government records",
        "local government unit",
        "landowner names",
        "property identification maps",
    ],
}


def first_nonempty_page(text: str) -> str:
    return next((page for page in text.split("\f") if page.strip()), "")


def extract_labeled_tag_text(text: str) -> str:
    page = first_nonempty_page(text)
    match = TAG_LABEL_RE.search(page)
    if not match:
        return ""

    parts: list[str] = []
    for line in page[match.end() :].splitlines():
        if NEXT_FOOTNOTE_RE.match(line):
            break
        stripped = line.strip()
        if not stripped:
            continue
        if parts and parts[-1].endswith("-") and stripped[:1].islower():
            parts[-1] = parts[-1][:-1] + stripped
        else:
            parts.append(stripped)
    return re.sub(r"\s+", " ", " ".join(parts)).strip().strip(";:").rstrip(".")


def split_tags(raw: str) -> list[str]:
    # The PDFs use commas and semicolons interchangeably as keyword
    # separators, including within the same footnote.
    parts = re.split(r"\s*[;,]\s*", raw)
    tags = [part.strip().strip(";:").rstrip(".") for part in parts]
    return [tag for tag in tags if tag]


def build_manifest(source_root: Path) -> dict[str, Any]:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError(f"{DATA_PATH} must contain a records list")

    tagged_records: list[dict[str, Any]] = []
    placeholder_records: list[str] = []
    year_counts: Counter[str] = Counter()
    for record in records:
        reference = record.get("reference_label")
        raw_text_path = record.get("raw_text_path")
        year = record.get("year")
        if not all(isinstance(value, str) for value in (reference, raw_text_path, year)):
            raise ValueError("advisory-opinion record lacks reference, year, or raw text path")

        raw_text_file = source_root / raw_text_path
        if not raw_text_file.is_file():
            raise FileNotFoundError(raw_text_file)
        raw_tags = extract_labeled_tag_text(raw_text_file.read_text(errors="replace"))
        if raw_tags and PLACEHOLDER_RE.search(raw_tags):
            placeholder_records.append(reference)
            tags: list[str] = []
        else:
            tags = split_tags(raw_tags) if raw_tags else []

        if reference in PDF_VERIFIED_OVERRIDES:
            tags = PDF_VERIFIED_OVERRIDES[reference]
        if not tags:
            continue
        if len(tags) != len(set(tags)):
            raise ValueError(f"duplicate PDF tags for {reference}")

        tagged_records.append({"reference_label": reference, "tags": tags})
        year_counts[year] += 1

    return {
        "source_basis": "Tags printed in the source advisory-opinion PDF footnotes; no inferred topics.",
        "coverage_note": (
            "The earliest located PDF tags are in Advisory Opinion No. 2018-073. "
            "Late-2018 use is intermittent; only opinions with real printed tag terms are listed."
        ),
        "record_count": len(tagged_records),
        "records_by_year": dict(sorted(year_counts.items())),
        "excluded_placeholders": placeholder_records,
        "records": tagged_records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=Path,
        default=ROOT,
        help="repository root containing the ignored cache/ directory",
    )
    parser.add_argument("--write", action="store_true", help=f"write {OUTPUT_PATH}")
    args = parser.parse_args()

    manifest = build_manifest(args.source_root.resolve())
    rendered = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        OUTPUT_PATH.write_text(rendered, encoding="utf-8")
        print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")
    print(
        f"Found {manifest['record_count']} opinions with PDF tags: "
        f"{manifest['records_by_year']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
