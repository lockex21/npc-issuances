#!/usr/bin/env python3
"""Tag the full NPC corpus with topic/<key> tags and regenerate topic pages.

Offline and rerunnable: scans the markdown files already in content/
(issuances, advisory opinions, decisions, resolutions, orders, laws), infers
topics from the shared TOPIC_RULES in build_npc_site.py, writes the inferred
topics into each file's frontmatter tags idempotently, and regenerates
content/topics/. Preserves the MANUAL INDEX NOTES block of existing topic
pages, matching the behaviour of build_npc_site.py.

Matching policy (deliberately conservative to avoid over-tagging):
- a pattern match in the title or description assigns the topic outright;
- body text alone assigns a topic only when it matches strongly (a per-topic
  occurrence threshold, higher for terms like "consent" or "security" that
  nearly every quasi-judicial document mentions in passing);
- topic/ tags already present in a file's frontmatter are authoritative and
  always preserved.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_npc_site import (  # noqa: E402
    CONTENT_DIR,
    TOPIC_RULES,
    display_topic_name,
    render_index_page,
)

# (folder name, topic page section heading) in display order.
CORPUS_SECTIONS: tuple[tuple[str, str], ...] = (
    ("laws", "Laws"),
    ("issuances", "Issuances"),
    ("advisory-opinions", "Advisory Opinions"),
    ("decisions", "Decisions"),
    ("resolutions", "Resolutions"),
    ("orders", "Orders"),
)

# Corpus-wide pattern overrides for TOPIC_RULES entries that are too generic
# once decisions/resolutions/orders enter the mix ("surveillance" matches
# disease surveillance, "certification" matches the certification against
# forum shopping in every pleading, "charges" matches criminal charges, etc.).
PATTERN_OVERRIDES: dict[str, tuple[str, ...]] = {
    "ai": ("artificial intelligence", "machine learning", "automated decision-making", "generative ai"),
    "cctv-surveillance": (
        "cctv",
        "closed-circuit television",
        "closed circuit television",
        "body-worn camera",
        "video surveillance",
        "surveillance camera",
        "surveillance footage",
    ),
    "children": (r"\bchild\b", r"\bchildren\b", r"\bminors?\b", "child-oriented"),
    "cross-border-transfers": (
        "cross-border",
        "cross border",
        "transborder",
        "outside the philippines",
        "contractual clauses",
    ),
    "elections": (r"\belections?\b", "electoral", "partisan political", "comelec"),
    "fees-and-payments": (r"\bfees?\b", "filing fee", "processing fee", "payment of fees"),
    "registration": (
        "data protection officer",
        "seal of registration",
        "registration of data processing",
        "npc registration",
        "registration with the commission",
        "register with the commission",
    ),
    "security": (r"\bsecurity\b", r"\bcyber\b", "cybersecurity", "cybercrime"),
    "training-certification": (
        "privacy mark",
        "competency program",
        "data privacy competency",
        "privacy training",
        "certification body",
        "certified data protection",
        "training on data privacy",
    ),
}

# Body-only matches need this many total pattern hits before a topic sticks.
DEFAULT_BODY_THRESHOLD = 3
BODY_THRESHOLDS: dict[str, int] = {
    "breach-notification": 5,
    "children": 6,
    "consent": 10,
    "data-sharing": 4,
    "elections": 5,
    "employment": 8,
    "fees-and-payments": 8,
    "government": 12,
    "registration": 4,
    "security": 10,
}

FRONTMATTER_RE = re.compile(r"\A---\n(?P<fm>.*?\n)---\n", re.DOTALL)
TAGS_BLOCK_RE = re.compile(r"(?m)^tags:[ \t]*\n(?P<items>(?:[ \t]*-[ \t][^\n]*\n)+)")
TAGS_INLINE_RE = re.compile(r"(?m)^tags:[ \t]*\[(?P<items>[^\]\n]*)\][ \t]*$")
DATE_ISO_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


@dataclass
class CorpusDoc:
    section: str
    path: Path
    slug: str
    title: str
    sort_key: str
    topics: set[str] = field(default_factory=set)


def compiled_topic_patterns() -> dict[str, tuple[re.Pattern[str], ...]]:
    rules: dict[str, tuple[re.Pattern[str], ...]] = {}
    for topic, patterns in TOPIC_RULES.items():
        patterns = PATTERN_OVERRIDES.get(topic, patterns)
        rules[topic] = tuple(re.compile(pattern) for pattern in patterns)
    return rules


def unquote_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        if value[0] == '"':
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        return value[1:-1]
    return value


def frontmatter_scalar(frontmatter: str, key: str) -> str:
    match = re.search(rf"(?m)^{key}:[ \t]*(?P<value>[^\n]+)$", frontmatter)
    return unquote_scalar(match.group("value")) if match else ""


def parse_existing_tags(frontmatter: str) -> list[str]:
    block = TAGS_BLOCK_RE.search(frontmatter)
    if block:
        return [
            unquote_scalar(re.sub(r"^[ \t]*-[ \t]*", "", line))
            for line in block.group("items").splitlines()
        ]
    inline = TAGS_INLINE_RE.search(frontmatter)
    if inline:
        return [unquote_scalar(item) for item in inline.group("items").split(",") if item.strip()]
    return []


def infer_topics(
    head: str,
    body: str,
    patterns: dict[str, tuple[re.Pattern[str], ...]],
) -> set[str]:
    head = head.lower()
    body = body.lower()
    topics: set[str] = set()
    for topic, topic_patterns in patterns.items():
        if any(pattern.search(head) for pattern in topic_patterns):
            topics.add(topic)
            continue
        threshold = BODY_THRESHOLDS.get(topic, DEFAULT_BODY_THRESHOLD)
        hits = 0
        for pattern in topic_patterns:
            hits += len(pattern.findall(body))
            if hits >= threshold:
                topics.add(topic)
                break
    return topics


def iter_corpus_files() -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    for section, _heading in CORPUS_SECTIONS:
        base = CONTENT_DIR / section
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.name == "index.md" or path.name.startswith((".", "_")):
                continue
            if any(part.startswith((".", "_")) for part in path.relative_to(CONTENT_DIR).parts):
                continue
            files.append((section, path))
    return files


def doc_sort_key(frontmatter: str, tags: list[str], path: Path) -> str:
    date_value = frontmatter_scalar(frontmatter, "date")
    match = DATE_ISO_RE.search(date_value)
    if match:
        return match.group(0)
    for tag in tags:
        year_match = re.fullmatch(r"year/(\d{4})", tag)
        if year_match:
            return f"{year_match.group(1)}-00-00"
    folder = path.parent.name
    if re.fullmatch(r"\d{4}", folder):
        return f"{folder}-00-00"
    return "0000-00-00"


def add_topic_tags_to_file(path: Path, topics: set[str]) -> bool:
    """Insert missing topic/<key> tags into the file's frontmatter tags list.

    Pure string surgery: everything outside the inserted tag lines is
    preserved byte-for-byte, existing tags are never reordered or rewritten.
    """
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        print(f"  ! skipping (no frontmatter): {path}")
        return False
    frontmatter = match.group("fm")
    existing = set(parse_existing_tags(frontmatter))
    new_tags = [f"topic/{topic}" for topic in sorted(topics) if f"topic/{topic}" not in existing]
    if not new_tags:
        return False

    block = TAGS_BLOCK_RE.search(frontmatter)
    if block:
        first_item = block.group("items").splitlines()[0]
        indent = re.match(r"[ \t]*", first_item).group(0)
        quoted = bool(re.match(r"[ \t]*-[ \t]+\"", first_item))
        addition = "".join(
            f'{indent}- "{tag}"\n' if quoted else f"{indent}- {tag}\n" for tag in new_tags
        )
        insert_at = match.start("fm") + block.end("items")
    else:
        inline = TAGS_INLINE_RE.search(frontmatter)
        if inline:
            inner = inline.group("items")
            quoted = '"' in inner
            rendered = ", ".join(f'"{tag}"' if quoted else tag for tag in new_tags)
            addition = (", " if inner.strip() else "") + rendered
            insert_at = match.start("fm") + inline.end("items")
        else:
            addition = "tags:\n" + "".join(f"  - {tag}\n" for tag in new_tags)
            insert_at = match.end("fm")

    path.write_text(text[:insert_at] + addition + text[insert_at:], encoding="utf-8")
    return True


def collect_documents() -> list[CorpusDoc]:
    patterns = compiled_topic_patterns()
    docs: list[CorpusDoc] = []
    for section, path in iter_corpus_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        match = FRONTMATTER_RE.match(text)
        frontmatter = match.group("fm") if match else ""
        body = text[match.end():] if match else text
        title = frontmatter_scalar(frontmatter, "title") or path.stem.replace("-", " ").title()
        description = frontmatter_scalar(frontmatter, "description")
        tags = parse_existing_tags(frontmatter)
        existing_topics = {tag.removeprefix("topic/") for tag in tags if tag.startswith("topic/")}
        inferred = infer_topics(f"{title}\n{description}", body, patterns)
        docs.append(
            CorpusDoc(
                section=section,
                path=path,
                slug=path.relative_to(CONTENT_DIR).with_suffix("").as_posix(),
                title=title,
                sort_key=doc_sort_key(frontmatter, tags, path),
                topics=existing_topics | inferred,
            )
        )
    return docs


def apply_topic_tags(docs: list[CorpusDoc]) -> int:
    changed = 0
    for doc in docs:
        if doc.topics and add_topic_tags_to_file(doc.path, doc.topics):
            changed += 1
    return changed


def generate_topic_pages(docs: list[CorpusDoc]) -> None:
    grouped: dict[str, dict[str, list[CorpusDoc]]] = defaultdict(lambda: defaultdict(list))
    for doc in docs:
        for topic in doc.topics:
            grouped[topic][doc.section].append(doc)

    section_headings = dict(CORPUS_SECTIONS)
    topics = sorted(set(TOPIC_RULES) | set(grouped))

    def topic_counts(topic: str) -> str:
        parts = [
            f"{len(grouped[topic][section])} {heading.lower()}"
            for section, heading in CORPUS_SECTIONS
            if grouped[topic].get(section)
        ]
        total = sum(len(items) for items in grouped[topic].values())
        return f"{total} documents: {', '.join(parts)}" if parts else "0 documents"

    topic_index_lines = [
        "Topic pages are generated from lightweight keyword tagging across the full corpus"
        " (laws, issuances, advisory opinions, decisions, resolutions, and orders)."
        " Treat them as starting points and extend them manually.",
        "",
        "## Topics",
        *[
            f"- [[topics/{topic}|{display_topic_name(topic)}]] ({topic_counts(topic)})"
            for topic in topics
        ],
    ]
    render_index_page(
        CONTENT_DIR / "topics" / "index.md",
        "Topics",
        "Auto-generated topic landing pages for the NPC corpus.",
        topic_index_lines,
        default_manual="Add new handcrafted topic notes in this folder whenever the generated set is not enough.",
    )

    for topic in topics:
        lines = [
            f"Auto-generated topic cluster for **{display_topic_name(topic)}**,"
            " covering the full corpus of laws, issuances, advisory opinions,"
            " decisions, resolutions, and orders.",
        ]
        for section, heading in CORPUS_SECTIONS:
            items = grouped[topic].get(section)
            if not items:
                continue
            lines.append("")
            lines.append(f"## {heading}")
            for doc in sorted(items, key=lambda item: (item.sort_key, item.title), reverse=True):
                lines.append(f"- [[{doc.slug}|{doc.title}]]")
        if len(lines) == 1:
            lines.extend(["", "No documents are currently tagged with this topic."])
        render_index_page(
            CONTENT_DIR / "topics" / f"{topic}.md",
            display_topic_name(topic),
            f"NPC documents related to {display_topic_name(topic)}.",
            lines,
            default_manual="Add your own synthesis, definitions, and extra wikilinks here.",
        )


def print_summary(docs: list[CorpusDoc]) -> None:
    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for doc in docs:
        for topic in doc.topics:
            counts[topic][doc.section] += 1

    sections = [section for section, _heading in CORPUS_SECTIONS]
    header = f"{'topic':<24} {'total':>5} " + " ".join(f"{section[:10]:>10}" for section in sections)
    print(header)
    print("-" * len(header))
    for topic in sorted(set(TOPIC_RULES) | set(counts)):
        total = sum(counts[topic].values())
        row = f"{topic:<24} {total:>5} " + " ".join(
            f"{counts[topic].get(section, 0):>10}" for section in sections
        )
        print(row)
    tagged = sum(1 for doc in docs if doc.topics)
    print(f"\n{tagged} of {len(docs)} corpus documents carry at least one topic tag.")


def run(*, write_tags: bool = True, write_pages: bool = True) -> list[CorpusDoc]:
    docs = collect_documents()
    if write_tags:
        changed = apply_topic_tags(docs)
        print(f"Updated frontmatter tags in {changed} file(s).")
    if write_pages:
        generate_topic_pages(docs)
        print(f"Regenerated topic pages at {CONTENT_DIR / 'topics'}")
    print_summary(docs)
    return docs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Tag the NPC corpus with topic/ tags and regenerate content/topics/."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report inferred topics without writing tags or topic pages.",
    )
    args = parser.parse_args()
    run(write_tags=not args.dry_run, write_pages=not args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
