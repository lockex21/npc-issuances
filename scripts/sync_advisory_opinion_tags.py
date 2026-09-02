#!/usr/bin/env python3
"""Synchronize PDF-derived advisory-opinion tags into corpus metadata.

The tracked manifest is deliberately separate from the NPC website's index
tags.  The latter contain omissions, shifted rows, and extraction artifacts;
the manifest contains only terms printed in the source PDF footnotes.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "advisory_opinions.json"
MANIFEST_PATH = ROOT / "data" / "advisory_opinion_tags.json"

FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)(?P<close>\n---(?:\n|\Z))", re.DOTALL)
OFFICIAL_TAGS_RE = re.compile(
    r"(?m)^official_tags:[ \t]*\n(?:[ \t]+-[ \t]+[^\n]*\n?)+"
)
TAGS_BLOCK_RE = re.compile(r"(?m)^tags:[ \t]*\n(?:[ \t]+-[ \t]+[^\n]*\n?)+")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_manifest() -> dict[str, list[str]]:
    payload = load_json(MANIFEST_PATH)
    records = payload.get("records") if isinstance(payload, dict) else None
    if not isinstance(records, list):
        raise ValueError(f"{MANIFEST_PATH} must contain a records list")

    result: dict[str, list[str]] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"manifest record {index} is not an object")
        reference = record.get("reference_label")
        tags = record.get("tags")
        if not isinstance(reference, str) or not reference:
            raise ValueError(f"manifest record {index} has no reference_label")
        if reference in result:
            raise ValueError(f"duplicate manifest record: {reference}")
        if not isinstance(tags, list) or not tags:
            raise ValueError(f"manifest record {reference} has no tags")
        if not all(isinstance(tag, str) and tag.strip() == tag and tag for tag in tags):
            raise ValueError(f"manifest record {reference} has an invalid tag")
        if len(tags) != len(set(tags)):
            raise ValueError(f"manifest record {reference} has duplicate tags")
        result[reference] = tags

    declared_count = payload.get("record_count")
    if declared_count != len(result):
        raise ValueError(
            f"manifest declares {declared_count!r} records but contains {len(result)}"
        )
    return result


def render_official_tags(tags: list[str]) -> str:
    lines = ["official_tags:"]
    lines.extend(f"  - {json.dumps(tag, ensure_ascii=False)}" for tag in tags)
    return "\n".join(lines) + "\n"


def sync_frontmatter(text: str, tags: list[str]) -> str:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")

    body = match.group("body") + "\n"
    body = OFFICIAL_TAGS_RE.sub("", body)
    block = render_official_tags(tags)

    tag_block = TAGS_BLOCK_RE.search(body)
    if tag_block:
        body = body[: tag_block.end()] + block + body[tag_block.end() :]
    else:
        insertion = re.search(r"(?m)^(?:date|draft|aliases):", body)
        offset = insertion.start() if insertion else len(body)
        body = body[:offset] + block + body[offset:]

    body = body.rstrip("\n")
    return "---\n" + body + match.group("close") + text[match.end() :]


def with_official_tags(record: dict[str, Any], tags: list[str] | None) -> dict[str, Any]:
    updated: dict[str, Any] = {}
    inserted = False
    for key, value in record.items():
        if key == "official_tags":
            continue
        updated[key] = value
        if key == "tags" and tags:
            updated["official_tags"] = tags
            inserted = True
    if tags and not inserted:
        updated["official_tags"] = tags
    return updated


def expected_outputs() -> tuple[str, dict[Path, str]]:
    manifest = load_manifest()
    payload = load_json(DATA_PATH)
    records = payload.get("records") if isinstance(payload, dict) else None
    if not isinstance(records, list):
        raise ValueError(f"{DATA_PATH} must contain a records list")

    seen: set[str] = set()
    markdown_outputs: dict[Path, str] = {}
    updated_records: list[dict[str, Any]] = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError(f"{DATA_PATH} contains a non-object record")
        reference = record.get("reference_label")
        markdown_path = record.get("markdown_path")
        if not isinstance(reference, str) or not isinstance(markdown_path, str):
            raise ValueError("advisory-opinion record lacks reference_label or markdown_path")
        seen.add(reference)
        official_tags = manifest.get(reference)
        updated_records.append(with_official_tags(record, official_tags))

        path = ROOT / markdown_path
        if not path.is_file():
            raise ValueError(f"missing advisory-opinion Markdown: {markdown_path}")
        current = path.read_text(encoding="utf-8")
        if official_tags:
            markdown_outputs[path] = sync_frontmatter(current, official_tags)
        elif OFFICIAL_TAGS_RE.search(current):
            markdown_outputs[path] = OFFICIAL_TAGS_RE.sub("", current)

    missing_records = sorted(set(manifest) - seen)
    if missing_records:
        raise ValueError(f"manifest references unknown opinions: {missing_records}")

    updated_payload = dict(payload)
    updated_payload["records"] = updated_records
    data_text = json.dumps(updated_payload, ensure_ascii=False, indent=2) + "\n"
    return data_text, markdown_outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if data or Markdown is not synchronized; do not write files",
    )
    args = parser.parse_args()

    expected_data, expected_markdown = expected_outputs()
    stale: list[Path] = []

    if DATA_PATH.read_text(encoding="utf-8") != expected_data:
        stale.append(DATA_PATH)
        if not args.check:
            DATA_PATH.write_text(expected_data, encoding="utf-8")

    for path, expected in expected_markdown.items():
        if path.read_text(encoding="utf-8") == expected:
            continue
        stale.append(path)
        if not args.check:
            path.write_text(expected, encoding="utf-8")

    if args.check and stale:
        print(f"Advisory-opinion tags are out of sync in {len(stale)} file(s):")
        for path in stale[:50]:
            print(f"- {path.relative_to(ROOT)}")
        if len(stale) > 50:
            print(f"- ... {len(stale) - 50} more")
        return 1

    action = "Verified" if args.check else "Synchronized"
    print(f"{action} PDF-derived tags for {len(load_manifest())} advisory opinions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
