# NPC Issuance Wiki

This repository uses [Quartz](https://quartz.jzhao.xyz/) for publishing and treats Markdown in `content/` as the source of truth for the wiki.

## Build Model

The issuance pipeline is:

1. fetch the official NPC advisories/circulars index
2. cache PDFs under `cache/pdfs/` (local only)
3. extract text
   - direct PDF text extraction first
   - OCR fallback using `ocrmypdf` for image-only or low-text PDFs
4. clean recurring header/footer boilerplate (NPC address blocks, repeating footer metadata)
5. generate Markdown notes in `content/`

Decisions and resolutions are mirrored through `r.jina.ai` because the live NPC site sits behind a Cloudflare challenge for scripted fetches.

## Content Layout

- Primary issuance pages (text-first, manually annotatable): `content/issuances/<year>/...`
- Companion notes (summary, links, auto metadata/backlinks; internal only): `content/notes/<year>/...`
- Raw extraction notes (regenerated, internal only): `content/sources/<year>/...`
- Advisory opinions: `content/advisory-opinions/<year>/...`
- PDF-derived advisory-opinion tag manifest: `data/advisory_opinion_tags.json`
- Decisions: `content/decisions/<year>/...`
- Resolutions: `content/resolutions/<year>/...`
- Orders: `content/orders/<year>/...`
- Index pages: `content/types/`, `content/topics/`, `content/relationships/`

The primary issuance page is intentionally centered on the issuance text for precise search/citation workflows.

## Editing In Obsidian

Open this repository root as an Obsidian vault.

The primary issuance page preserves this editable block:

```md
<!-- BEGIN MANUAL ANNOTATED TEXT -->
...
<!-- END MANUAL ANNOTATED TEXT -->
```

Use that section for exact text cleanup, internal wikilinks, and external links.

Companion notes preserve:

```md
<!-- BEGIN MANUAL SUMMARY --> ... <!-- END MANUAL SUMMARY -->
<!-- BEGIN MANUAL LINKS --> ... <!-- END MANUAL LINKS -->
```

## Git And PDF Policy

- `content/pdfs/` is ignored and removed from tracking.
- `cache/` is ignored.
- PDFs stay local; the repo tracks Markdown, scripts, and config.

## Commands

Run the repo checks:

```bash
npm run check
```

This runs TypeScript and code formatting checks, validates the corpus with `scripts/validate_content.py`, and verifies that PDF-derived advisory-opinion tags are synchronized with the JSON data and Markdown frontmatter.

Run only the corpus validator:

```bash
npm run check:content
```

Refresh cache and metadata:

```bash
python3 scripts/build_npc_site.py sync --refresh
```

Generate Markdown corpus from local cache:

```bash
python3 scripts/build_npc_site.py build
```

Full refresh:

```bash
python3 scripts/build_npc_site.py all --refresh
```

Build decisions and resolutions:

```bash
python3 scripts/build_npc_decisions_resolutions.py all --refresh
```

Refresh only decision/resolution JSON and index pages from existing data:

```bash
python3 scripts/build_npc_decisions_resolutions.py all --indexes-only
```

Regenerate non-preserved decision/resolution pages:

```bash
python3 scripts/build_npc_decisions_resolutions.py all --rewrite-record-pages
```

Build advisory opinions:

```bash
python3 scripts/build_npc_advisory_opinions.py --refresh
```

Rebuild the advisory-opinion tag manifest from the local PDF text cache, then synchronize it into data and frontmatter:

```bash
python3 scripts/build_advisory_opinion_tag_manifest.py --write
python3 scripts/sync_advisory_opinion_tags.py
```

The tag manifest includes only terms printed in PDF footnotes. It does not infer topics from an opinion's text or use the NPC index page as a fallback. Image-only, unlabeled, and broken-font footnotes are kept as explicitly PDF-verified overrides in the manifest builder.

Build orders:

```bash
python3 scripts/build_npc_orders.py --refresh
```

Case-corpus builders preserve existing Markdown pages by default and write newly discovered pages when needed. Review diffs carefully after using `--rewrite-record-pages`; records pinned in `data/case_overrides.json` keep their corrected paths and preserve curated Markdown.

## Run Quartz Locally

Quartz 4 requires Node 22+ and npm 10.9.2+.

```bash
npm ci
npx quartz build --serve
```

Open `http://localhost:8080/`.

On advisory-opinion pages, the exact PDF terms appear under **Official opinion tags**. They are included in ordinary search results, and each chip opens the corresponding filtered tag page. The homepage also links to an alphabetical directory that consolidates capitalization variants while preserving each PDF's exact wording on its opinion page.

## Notes

- Automatic reference linking is strongest for numbered citations like `NPC Circular No. 2023-01`.
- Companion/source notes are regenerated around preserved manual blocks.
- `content/notes/` and `content/sources/` are internal maintenance folders and are excluded from the published Quartz site.
- Prettier is intentionally scoped to code and templates; do not bulk-format the legal Markdown corpus.
- If the source index drops a file, remove obsolete generated notes manually from `content/`.
