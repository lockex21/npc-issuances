---
name: npc-markdown-cleanup
description: "Shared base skill for cleaning any NPC markdown issuance destined for a Quartz knowledge base. Always use this skill when working on any NPC markdown file — decisions, resolutions, circulars, advisory opinions, or other issuances. It covers the rules that apply to every document type: reading the cached PDF, fixing OCR artifacts (broken paragraphs, fragmented footnotes, page headers injected mid-body, broken words), restoring formatting fidelity (bold, italic, block quotes, lists), consolidating footnotes, YAML safety rules for frontmatter, and maintaining the per-folder state file and changelog. Use this skill together with a document-type-specific skill (e.g. npc-advisory-opinion-cleanup) — the generic skill handles the shared layer; the specific skill handles document structure and title format."
---

# NPC Markdown Cleanup — Shared Base

This skill covers rules that apply to every NPC issuance regardless of type. Use it together with whichever document-type-specific skill is appropriate:

- Advisory opinions (`content/advisory-opinions/`) → also use `npc-advisory-opinion-cleanup`
- Circulars, advisories, memorandum circulars, FAQs, rules (`content/issuances/`) → also use `npc-circular-cleanup`
- Decisions, special proceedings (`content/decisions/`) → also use `npc-decision-cleanup`
- Resolutions (`content/resolutions/`) → also use `npc-resolution-cleanup`

Read this skill first, then read the type-specific skill. Between the two you'll have everything needed for a clean, Quartz-compatible file.

---

## Step 1: Locate and read both files

**File structure:**
```
NPC_issuances/
  content/<type>/<year>/
    .cleanup-state.json         ← per-subfolder state (hidden from Quartz)
    *.md
  cache/
    advisory_opinions/pdfs/     ← advisory opinions
    decisions/pdfs/             ← decisions
    resolutions/pdfs/           ← resolutions
    pdfs/                       ← circulars and other issuances
  .cleanup-log.md               ← flat changelog (hidden from Quartz)
```

**Read the markdown file** from the path passed in.

**Find and read the PDF** by extracting its filename from the `Official PDF` link in `## Source` (or `## Source And Notes`), then locate it in the correct cache subfolder:

| Content path contains | PDF cache location |
|---|---|
| `advisory-opinions/` | `cache/advisory_opinions/pdfs/` |
| `decisions/` | `cache/decisions/pdfs/` |
| `resolutions/` | `cache/resolutions/pdfs/` |
| anything else | `cache/pdfs/` |

Do not download from `privacy.gov.ph` (returns 403). The filename in the URL may be URL-encoded — decode if needed:
```python
from urllib.parse import unquote
pdf_name = unquote(url.split('/')[-1])
```

**PDFs over 10 pages:** The `Read` tool fails silently without a `pages` parameter (max 20 pages per request). Check the page count first:
```bash
python3 -c "import PyPDF2; r=PyPDF2.PdfReader(open('PATH','rb')); print(len(r.pages))"
```
Then read in chunks: `pages: "1-10"`, `pages: "11-20"`, etc.

The PDF is authoritative for text, formatting, and structure. Read both files before changing anything.

---

## Step 2: Fix OCR artifacts

| Artifact | What it looks like | Fix |
|---|---|---|
| OCR line breaks | Blank line after every sentence | Join into continuous paragraphs |
| Inline footnote callouts | `... Act .1` or `... evidence ,  4` | Normalize to `[^1]`, `[^4]` after punctuation |
| Scattered footnote text | `> 4Id., at p. 3.` or bare `12 Id.` in body | Extract; place as `[^N]:` entries at end of file |
| Split URLs | URL fragment dangling on next line | Reconstruct full URL from PDF |
| Page header injections | `Decision\nNPC Case No.\nPage 3 of 17` mid-paragraph | Delete entirely |
| Broken words | `containin g`, `non -disclosure` | Reunite |
| Orphaned section headings | ALL CAPS grouping label as plain paragraph | Promote to heading — level determined by document type |
| Broken list items | Numbered/bulleted item split across paragraphs | Rejoin |
| Duplicate paragraphs | Same text appears twice (truncated then complete) | Delete truncated copy |

---

## Step 3: Restore formatting fidelity

The PDF is the authority — visually inspect it for every item below:

- **Bold/italic**: `**bold**`, `*italic*`, `***bold-italic***`. Typical locations: legal maxims (*Ubi lex non distinguit...*), defined terms when introduced, case names (`*Ople v. Torres*`), operative phrases in dispositive portions (`**FINDS**`, `**SO ORDERED.**`), section title lines in circulars
- **Underlined text** in quoted statutes → render as `**bold**` (markdown has no underline)
- **Block quotations** (statutes, IRR, jurisprudence) → `> blockquote`; `>>` for quoted text nested inside another quotation; rejoin across deleted page headers
- **Lists**: restore numbered (`1.`) and bulleted (`-`) structure exactly as in the PDF; sub-items indented under their parent; do not collapse into prose
- **Inline citation placement**: after closing punctuation — `evidence,[^4]` not `evidence ,  4`
- **Lettered sub-items**: `- **A.** Text`; numbered sub-items: `  1. Text`

---

## Step 4: Consolidate footnotes

Pull all footnote fragments from the body; place as `[^N]:` entries in numeric order at the end of the file. No `### Footnotes` heading needed. Placement within the file depends on document type — see the type-specific skill. Every callout in the body must have a matching entry.

Standard shorthands: `*Id.*`, `*Ibid.*`, `*Supra* note N`, `*See*`

---

## Step 5: YAML frontmatter safety

The title and description fields are double-quoted YAML strings. Four patterns crash Quartz's parser:

**1. Unclosed quote** — must start *and* end with straight ASCII `"`
```
# Bad:
title: "NPC Circular No. 2019-001
# Good:
title: "NPC Circular No. 2019-001"
```

**2. Curly/smart quotes** — always `"` (U+0022), never `"` (U+201C) or `"` (U+201D)
```
# Bad — looks the same in some fonts, breaks YAML:
title: "NPC Circular No. 2017-001"
# Good:
title: "NPC Circular No. 2017-001"
```

**3. Unescaped inner double-quotes** — a `"` inside a double-quoted value ends the string early; rephrase to remove inner quotes
```
# Bad:
title: "Definition of "Data" Under the DPA"
# Good:
title: "Definition of Data Under the DPA"
```

**4. Doubled closing quote**
```
# Bad:
title: "NPC Circular No. 2017-001 — Some Title""
# Good:
title: "NPC Circular No. 2017-001 — Some Title"
```

**Validate before writing** — if this raises an error, fix it first:
```bash
python3 -c "
import yaml, sys
fm = open('PATH_TO_FILE').read().split('---')[1]
try:
    yaml.safe_load(fm)
    print('Frontmatter OK')
except yaml.YAMLError as e:
    print('INVALID YAML:', e)
    sys.exit(1)
"
```

Other frontmatter rules:
- `tags` — unquoted bare strings: `- issuance`, never `- "issuance"`
- `draft` — `false` exactly once, no duplicates
- `description` — one factual sentence from the PDF; never a placeholder like `[to be filled from PDF content]`

---

## Step 6: State file

Each subfolder has a `.cleanup-state.json`. Read it at the start; create if missing.

```json
{
  "some-opinion.md": { "status": "done", "timestamp": "2025-08-13T10:00:00Z" },
  "another-opinion.md": { "status": "error", "note": "PDF not found" }
}
```

Filenames are top-level keys. Statuses: `pending` (default), `done` (skip on all future runs — no exceptions), `skipped`, `error`. Write after every file — do not batch.

---

## Step 7: Changelog

Append to `NPC_issuances/.cleanup-log.md` after each file. The agent never reads this file.

```markdown
## 2025-08-13T10:00:00 | advisory-opinions/2022/advisory-opinion-no-2022-001.md | done
- Rejoined 11 OCR-fragmented paragraphs
- Consolidated 6 footnotes to end of file
- Fixed 2 broken words; restored bold on 3 phrases
- Corrected ## Discussion → ### Discussion
```

One line per category of change, not per instance.

---

## Critical rules

- **PDF is authoritative.** Every word, every heading, every list item must match the source. No paraphrasing.
- **PDFs over 10 pages must be read in chunks.** Check page count, then read in ranges. Do not proceed without the full PDF.
- **Validate YAML before writing.** Run the yaml.safe_load check and fix any errors first.
- **Long files.** For files over ~600 lines, verify footnotes in the second half were cleaned throughout.
