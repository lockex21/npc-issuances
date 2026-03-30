---
name: npc-resolution-cleanup
description: "Fix OCR-corrupted or poorly-extracted markdown files for NPC Resolutions in content/resolutions/. Use whenever cleaning a resolution markdown file. Resolutions follow a quasi-judicial format similar to decisions (case title block, Facts / Discussion sections, signature block) but use ## Resolution Text, have varied case number prefixes (NPC, NPC BN, NPC SS, NPC CDO, CID BN, CID), and the year/ tag follows the folder year (resolution issue year), not the case number year. Common symptoms: letterhead blockquotes injected throughout the body, page-header injections mid-paragraph, footnotes scattered as inline blockquotes, Facts/Discussion not marked as ### headings, description containing raw body text or footnote references, missing date and aliases, wrong year/ tag. PDF cache: NPC_issuances/cache/resolutions/pdfs/. Use together with npc-markdown-cleanup for shared OCR, YAML, and state-file rules."
---

# NPC Resolution Cleanup

NPC resolutions are post-adjudication orders issued after a decision or investigation has been concluded. They cover a range of actions: compliance orders, closure orders, breach notification rulings, cease-and-desist orders (CDOs), and sua sponte investigation closures. Like decisions they are quasi-judicial in tone, but resolutions are shorter and often lack an `### Issue` section.

**Use this skill together with `npc-markdown-cleanup`**, which covers the shared rules: reading the PDF, OCR artifact cleanup, formatting fidelity, footnote consolidation, YAML safety, and the state file/changelog. Read that skill first, then continue here for resolution-specific rules.

---

## Document structure

The correct Quartz layout for a resolution:

```markdown
---
[frontmatter]
---

## Source
- Reference: NPC YY-NNN
- Official PDF: [URL]
- Source page: http://privacy.gov.ph/resolutions/
- Issue date: [Month DD, YYYY]
- Published on NPC site: [date]
- Pages: [N]

## Source Tags
- [DPA provision tags from original extraction]

## Resolution Text

[Case title block — complainant, "-versus-", respondent, "x----x" separator]
[OR: "IN RE: RESPONDENT NAME" block for BN/SS/CDO types]

[Commissioner attribution — e.g. "NAGA, P.C.;" or "AGUIRRE, D.P.C.:"]

[Opening paragraph — "Before the Commission is..." or "This Resolution refers to..."]

### Facts

[Narrative of events and procedural history]

### Issue

[Issue statement — only if present in the PDF; many resolutions omit this section]

### Discussion

[Legal analysis and findings]

[Dispositive portion — WHEREFORE paragraph + SO ORDERED.]

[Date line — "City of Pasay, Philippines. DD Month YYYY."]

[Signature block]

[Copy furnished block]

[^1]: Footnote text.
[^2]: Footnote text.
```

**Heading levels:**
- `## Source`, `## Source Tags`, `## Resolution Text` — second level (preserve as-is)
- `### Facts`, `### Issue`, `### Discussion` — third level, within Resolution Text
- `#### Sub-heading` — fourth level for sub-topics within Discussion
- `### Issue` is **optional** — include only if the PDF has a distinct Issue section; do not add one if absent

Footnotes go after the copy furnished block, as `[^N]:` entries in numeric order, no heading.

**No title heading in the body.** Quartz uses the `title` frontmatter field. Do not add a `# NPC 21-086: RTB v. East West Banking Corporation` heading inside the document.

---

## Case number formats and title formats

Resolutions use several case number prefixes. Each has its own title convention:

| Case number format | Example | Title format |
|---|---|---|
| `NPC YY-NNN` | NPC 21-086 | `"NPC 21-086: Complainant v. Respondent"` |
| `NPC BN YY-NNN` | NPC BN 22-107 | `"NPC BN 22-107: In re: Respondent Name"` |
| `NPC SS YY-NNN` | NPC SS 19-001 | `"NPC SS 19-001: In re: Respondent Name"` |
| `NPC CDO YY-NNN` | NPC CDO 22-001 | `"NPC CDO 22-001: Complainant v. Respondent"` or `"NPC CDO 22-001: In re: Respondent"` |
| `CID BN YY-NNN` | CID BN 17-019 | `"CID BN 17-019: In re: Respondent Name"` |
| `CID YY-NNN` | CID 18-D-012 | `"CID 18-D-012: Complainant v. Respondent"` |
| `NPC YY-NNN and NPC YY-NNN` | NPC 20-317 and NPC 20-318 | `"NPC 20-317 and NPC 20-318: Complainant v. Respondent"` |

**Older "CID" case numbers** (pre-2021 breach notifications and complaints filed before the current numbering system) use `CID BN`, `CID BN-`, or bare `CID` prefixes. Preserve the prefix exactly as it appears in the PDF.

---

## Frontmatter

Standard frontmatter for a resolution:

```yaml
---
title: "NPC YY-NNN: Complainant v. Respondent"
description: "One factual sentence: who the respondent is, what the resolution concerned, and the outcome."
aliases:
  - "NPC YY-NNN"
  - "npc yy-nnn"
  - "Complainant v. Respondent"
  - "complainant v. respondent"
tags:
  - "resolution"
  - "type/resolution"
  - "year/YYYY"
  - "npc-case"
date: "YYYY-MM-DD"
draft: false
---
```

**Tags — `year/YYYY`:**
For resolutions, `year/` follows the **resolution issue date year** (which equals the subfolder year), NOT the case number year. A resolution closing NPC 16-004 issued in 2022 is tagged `year/2022`. This differs from decisions, where the tag follows the case number year.

**Aliases block:**

For complainant-vs-respondent resolutions (`NPC YY-NNN`, `CID YY-NNN`, `NPC CDO YY-NNN` adversarial format):
1. Canonical reference: `"NPC YY-NNN"` (e.g. `"NPC 21-086"`)
2. Lowercase: `"npc yy-nnn"` (e.g. `"npc 21-086"`)
3. Short case name: `"Complainant v. Respondent"` (e.g. `"RTB v. East West Banking Corporation"`)
4. Lowercase case name: `"complainant v. respondent"` (e.g. `"rtb v. east west banking corporation"`)

For "In re" resolutions (`NPC BN YY-NNN`, `NPC SS YY-NNN`, `CID BN YY-NNN`):
1. Canonical reference: `"NPC BN YY-NNN"` (e.g. `"NPC BN 22-107"`)
2. Lowercase: `"npc bn yy-nnn"` (e.g. `"npc bn 22-107"`)
3. Short respondent name: `"In re: Asia United Bank Corporation"`
4. Lowercase: `"in re: asia united bank corporation"`

---

## Title format

**Where to find the title:**
1. The case title block in the PDF — complainant and respondent names, or "IN RE:" header
2. The opening paragraph: "Before the Commission is..." or "This Resolution refers to..."

**ALL CAPS entity names must be title-cased in the title field:**
```
# Bad:
title: "NPC CDO 22-001: CID VS. PH-CHECK.COM"

# Good:
title: "NPC CDO 22-001: CID vs. PH-Check.com"
```

**Abbreviations and initials stay as-is** — they are pseudonymized names or official acronyms:
```
# Good — preserve the initials:
title: "NPC 21-086: RTB v. East West Banking Corporation"
title: "NPC BN 22-107: In re: Asia United Bank Corporation"
```

**Use `v.` for most resolutions; preserve `vs.` if the PDF uses that form.**

**Description field must be a factual one-sentence summary — never raw body text or a footnote reference:**
```
# Bad — raw footnote text:
description: "Helen Flores, DFA Passport Maker Runs Off with All Data, THE PHILIPPINE STAR, 12 January 2019"

# Bad — mirrors the title:
description: "NPC 21-086: RTB v. East West Banking Corporation"

# Bad — raw WHEREAS clause or procedural boilerplate:
description: "In re: Asia United Bank Corporation, NPC BN 22-107, Preliminary Breach Notification Form, Data"

# Good:
description: "Resolution closing NPC 21-086 after East West Banking Corporation paid nominal damages of P15,000.00 to RTB in compliance with the February 2022 decision."
description: "Breach notification resolution finding that Asia United Bank Corporation need not notify affected data subjects due to the low risk of harm from delayed handover of delivery receipts."
description: "Cease and desist order against PH-Check.com for unauthorized processing of personal data scraped from the DTI Business Name Registration System."
```

---

## Resolution-specific OCR artifacts to fix

These are in addition to the generic OCR artifacts covered by `npc-markdown-cleanup`:

| Artifact | What it looks like | Fix |
|---|---|---|
| Letterhead blockquote | `> 5th Floor, Philippine International Convention Center, Vicente Sotto Avenue, Pasay City, Metro Manila 1307` | Delete entirely |
| Letterhead blockquote (long form) | `> NPC_OPC_ADJU_DCSN-V1.0,R0.0, 05 May 2021 5th Floor, Philippine International Convention Center...` | Delete entirely |
| Page-header injection | `NPC 21-086` appearing as a standalone line mid-paragraph | Delete |
| Page-header injection (with case name) | `NPC 21-086\nRTB v. East West Banking Corporation` as standalone lines | Delete |
| "For: Violation" orphan | `For: Violation of the Data Privacy Act of 2012 NPC 21-086` mid-body | Delete (repeated page header) |
| Footnote text as inline blockquote | `> 1Id.`, `> 3Id. at 5.` between body paragraphs | Extract; consolidate as `[^N]:` entries at end |
| Detached footnote callout | `.1` or `,  4` glued to/near words | Normalize to `[^1]`, `[^4]` after punctuation |
| Facts/Discussion as plain text | `Facts`, `Discussion` as bare paragraph headings | Promote to `### Facts`, `### Discussion` |
| Issue as plain text | `Issue` as a bare paragraph heading | Promote to `### Issue` |
| Extra spaces in party names | `RTB ,` or `-versus -` | Tighten: `RTB,`, `-versus-` |
| Broken case title block | Party name split across lines with OCR breaks | Preserve the split-line format (it matches the PDF layout) |
| Wrong year/ tag | `year/2022` on a file whose resolution was actually issued in 2021 | Correct to match the subfolder year and issue date |
| Description from body | `description:` contains the opening sentence or a footnote citation | Replace with a factual one-sentence summary |
| Missing `date` field | No `date:` in frontmatter | Find in PDF closing line (`City of Pasay, Philippines. DD Month YYYY.`); add `date: "YYYY-MM-DD"` |
| Missing `aliases` block | No `aliases:` in frontmatter | Derive from case number and party names; add all required forms |
| `Sgd.` lines | Lone `Sgd.` before a commissioner's name | Delete — OCR artifact of a signature image |
| ORDER heading at top (CDO) | `ORDER` appearing as a bare paragraph after the case title block | This is body text in CDO resolutions — leave as a plain paragraph or bold it; do not promote to heading |

---

## The case title block

**Complainant-vs-respondent format:**

```markdown
RTB,

Complainant,

-versus-

EAST WEST BANKING CORPORATION,

Respondent.

x----------------------------------------------------x
```

**"In re" format (BN, SS, and suo sponte cases):**

```markdown
IN RE: ASIA UNITED BANK CORPORATION

x----------------------------------------------------x
```

Or multi-line IN RE block:

```markdown
IN RE: DEPARTMENT OF FOREIGN AFFAIRS (DFA) PASSPORT BREACH INITIATED AS A SUA SPONTE NPC INVESTIGATION INTO THE POSSIBLE DATA PRIVACY VIOLATIONS COMMITTED BY THE DEPARTMENT OF FOREIGN AFFAIRS

x----------------------------------------------------x
```

The `x------x` separator stays as plain text. Do not convert to `---`.

**CID-as-complainant format (CDO):**

```markdown
COMPLAINTS AND INVESTIGATION DIVISION – NATIONAL PRIVACY COMMISSION,

Complainant,

-versus-

PH-CHECK.COM,

Respondent.

x----------------------------------------------------x
```

---

## Section headings within Discussion

Promote Discussion sub-topics to `####`:

```markdown
### Discussion

#### On the Respondent's Compliance

...analysis...

#### On the Motion for Reconsideration

...analysis...
```

Not every resolution has sub-headings. If the PDF has a single continuous Discussion, leave it as `### Discussion` followed by prose.

---

## Dispositive portion

The WHEREFORE clause and SO ORDERED close the resolution. Keep them as plain paragraphs — no heading:

```markdown
WHEREFORE, premises considered, the Commission resolves that NPC 21-086 – RTB v. East West Banking Corporation is hereby **CLOSED**.

Further, East West Banking Corporation's Compliance and Manifestation dated 02 May 2022 is hereby **NOTED**.

**SO ORDERED.**

City of Pasay, Philippines. 28 July 2022.
```

The operative words (`CLOSED`, `NOTED`, `GRANTED`, `DISMISSED`, `ISSUED`) should be bold if they appear in bold or small caps in the PDF.

---

## Signature block

Resolutions use "WE CONCUR:" (multiple commissioners) more frequently than decisions, but the format otherwise matches decisions:

**Standard (presiding commissioner + concurring commissioners):**
```markdown
LEANDRO ANGELO Y. AGUIRRE
Deputy Privacy Commissioner

WE CONCUR:

JOHN HENRY D. NAGA
Privacy Commissioner

DUG CHRISTOPHER B. MAH
Deputy Privacy Commissioner
```

**Two-commissioner format (one presides, one concurs with "I CONCUR:"):**
```markdown
JOHN HENRY D. NAGA
Privacy Commissioner

I CONCUR:

LEANDRO ANGELO Y. AGUIRRE
Deputy Privacy Commissioner
```

Match the PDF exactly. Strip lone `Sgd.` lines — OCR artifacts of signature images.

---

## Copy furnished block

Preserve as plain text after the signature block:

```markdown
Copy furnished:

RTB
Complainant

ONA PAMFILO & BUBAN LAW OFFICES
Counsel for East West Banking Corporation

COMPLAINTS AND INVESTIGATION DIVISION
ENFORCEMENT DIVISION
GENERAL RECORDS UNIT
```

---

## `## Source` section

Resolutions use `## Source` (not `## Source And Notes`). Standard fields:

```markdown
## Source
- Reference: NPC YY-NNN
- Official PDF: [full URL from privacy.gov.ph]
- Source page: http://privacy.gov.ph/resolutions/
- Issue date: [Month DD, YYYY]
- Published on NPC site: [RFC date]
- Pages: [N]
```

Correct any fields that differ from the PDF (e.g., wrong issue date).

---

## PDF location for resolutions

```
NPC_issuances/cache/resolutions/pdfs/
```

All resolution types (NPC, NPC BN, NPC SS, NPC CDO, CID BN, CID) use this folder.

---

## Critical rules (resolution-specific)

- **Delete all letterhead blockquotes.** Any `>` blockquote containing `Philippine International Convention Center`, `NPC_OPC_ADJU`, `privacy.gov.ph`, or `info@privacy.gov.ph` is a letterhead injection — delete, do not keep.
- **`### Facts` and `### Discussion` are required headings.** If they exist as plain text, promote them. If the PDF has them and the markdown doesn't, add the headings.
- **`### Issue` is optional.** Add it only if the PDF has a distinct Issue section. Many resolutions move directly from Facts to Discussion.
- **`year/` tag follows the subfolder year (resolution issue year), not the case number year.** NPC 16-004 resolved in 2022 → `year/2022`. This differs from decisions.
- **`date` field is required.** Find it in the PDF's closing line (`City of Pasay, Philippines. DD Month YYYY.`). Format: `"YYYY-MM-DD"`.
- **Description must be a factual summary.** Never copy a footnote citation, never copy the opening sentence verbatim, never mirror the title.
- **`aliases` block is required.** Use the correct form set for the case number type (complainant-vs-respondent or "In re").
- **Do not convert the `x------x` separator to `---`.** It's a visual artifact of the original document, not a thematic break.
- **Strip lone `Sgd.` lines** — OCR artifacts of signature images.
- **The CDO `ORDER` heading is body text**, not a section heading. Leave it as a plain paragraph; do not promote it to `###`.
