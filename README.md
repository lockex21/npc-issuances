# NPC Issuance Wiki

This repository uses [Quartz](https://quartz.jzhao.xyz/) for publishing and treats Markdown in `content/` as the source of truth for the wiki.

## Build Model

The pipeline is:

1. fetch the official NPC advisories/circulars index
2. cache PDFs under `cache/pdfs/` (local only)
3. extract text
   - direct PDF text extraction first
   - OCR fallback using `ocrmypdf` for image-only or low-text PDFs
4. clean recurring header/footer boilerplate (NPC address blocks, repeating footer metadata)
5. generate Markdown notes in `content/`

## Content Layout

- Primary issuance pages (text-first, manually annotatable): `content/issuances/<year>/...`
- Companion notes (summary, links, auto metadata/backlinks): `content/notes/<year>/...`
- Raw extraction notes (regenerated): `content/sources/<year>/...`
- Index pages: `content/types/`, `content/topics/`, `content/relationships/`

The primary issuance page is intentionally centered on the issuance text for precise search/citation workflows.

## Editing In Obsidian

Open `/Users/reinier/NPC_issuances` as an Obsidian vault.

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

## Run Quartz Locally

Quartz 4 requires Node 22+ and npm 10.9.2+.

```bash
npm ci
npx quartz build --serve
```

Open `http://localhost:8080/`.

## Notes

- Automatic reference linking is strongest for numbered citations like `NPC Circular No. 2023-01`.
- Companion/source notes are regenerated around preserved manual blocks.
- If the source index drops a file, remove obsolete generated notes manually from `content/`.
