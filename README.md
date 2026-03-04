# NPC Issuance Wiki

This repository now uses [Quartz](https://quartz.jzhao.xyz/) as the site layer and treats Markdown in `content/` as the published corpus.

## Model

The build pipeline is:

1. fetch the official NPC advisories/circulars index
2. cache each linked PDF under `cache/pdfs/`
3. extract text under `cache/text/`
4. generate Quartz-ready Markdown notes under `content/`
5. let Quartz build and serve the wiki

Main editable issuance notes live under:

- `content/issuances/<year>/...`
- `content/types/...`
- `content/topics/...`
- `content/relationships/index.md`

PDFs are copied to `content/pdfs/` so Quartz can publish them as static assets.
Generated source-text notes live under `content/sources/<year>/...`.

## Editing

Each generated issuance note is now a hand-editable working note. The generator preserves these manual sections:

```md
<!-- BEGIN MANUAL SUMMARY -->
...
<!-- END MANUAL SUMMARY -->

<!-- BEGIN MANUAL LINKS -->
...
<!-- END MANUAL LINKS -->

<!-- BEGIN MANUAL ANNOTATED TEXT -->
...
<!-- END MANUAL ANNOTATED TEXT -->
```

On first generation, the `MANUAL ANNOTATED TEXT` block is seeded from the extracted PDF text with automatic internal issuance links where references were detected. After that, rebuilds preserve your edits in that block so you can keep annotating the text manually in Obsidian.

The raw regenerated extract is written separately under `content/sources/` and embedded from the main note for reference.

Use `data/overrides.json` for metadata cleanup that should survive regeneration, such as:

- corrected excerpt
- corrected issue date
- extra tags

## Commands

Refresh the NPC cache and metadata:

```bash
python3 scripts/build_npc_site.py sync --refresh
```

Generate or refresh the Quartz Markdown corpus:

```bash
python3 scripts/build_npc_site.py build
```

Run the full refresh:

```bash
python3 scripts/build_npc_site.py all --refresh
```

## Run Quartz Locally

Quartz 4 currently requires Node 22+ and npm 10.9.2+.

Install dependencies:

```bash
npm ci
```

Serve locally:

```bash
npx quartz build --serve
```

Then open `http://localhost:8080/`.

## Docker Option

If you prefer not to install Node locally:

```bash
docker build -t npc-issuance-wiki .
docker run --rm -p 8080:8080 npc-issuance-wiki
```

## Notes

- The generated topic pages are heuristic starting points, not a finished taxonomy.
- Automatic cross-references are strongest for numbered citations such as `NPC Circular No. 2023-01`.
- Main notes are updated in place while preserving the manual blocks above.
- Generated source notes under `content/sources/` are overwritten on rebuild.
- If the source site ever removes a document, you may need to manually remove its stale note from `content/`.
