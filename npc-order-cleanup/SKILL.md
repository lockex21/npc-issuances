---
name: npc-order-cleanup
description: "Fix OCR-corrupted or poorly-extracted markdown files for NPC Orders in content/orders/. Use whenever cleaning an order markdown file. Orders are directives (breach notification orders, CDOs, compliance orders, discovery orders) that use ## Order Text, have varied case number prefixes (NPC BN, NPC CC, NPC SS, CID BN, CID CDO, CID, bare NPC, date-based), and the year/ tag follows the folder year (order issue year), not the case number year. Common symptoms: title containing OCR table noise from margin columns, description with raw body text or scraped HTML, page-header injections (Order / Page N of M), footnotes as inline text, Facts/Issues/Discussion not promoted to ### headings, missing date and aliases, Source Tags with scraped gov.ph footer HTML. PDF cache: NPC_issuances/cache/orders/pdfs/. Use together with npc-markdown-cleanup for shared OCR, YAML, and state-file rules."
---

# NPC Order Cleanup

NPC orders are directives issued by the Commission during or after proceedings. They range from interlocutory orders (directing a party to submit documents or appear for discovery) to final enforcement orders (cease-and-desist orders, compliance orders closing out breach notifications). Unlike decisions — which adjudicate complaints between named parties — orders often arise from breach notifications (`NPC BN`, `CID BN`), sua sponte investigations (`NPC SS`, `NPC CC`), or cease-and-desist applications (`CID CDO`, `NPC CDO`). Some older orders use bare date-based references instead of case numbers.

**Use this skill together with `npc-markdown-cleanup`**, which covers the shared rules: reading the PDF, OCR artifact cleanup, formatting fidelity, footnote consolidation, YAML safety, and the state file/changelog. Read that skill first, then continue here for order-specific rules.

---

## Document structure

The correct Quartz layout for an order:

```markdown
---
[frontmatter]
---

## Source
- Reference: NPC BN YY-NNN (or whatever the case number is)
- Official PDF: [URL]
- Source page: http://privacy.gov.ph/orders-2/
- Issue date: [Month DD, YYYY]
- Published on NPC site: [date]
- Pages: [N]

## Source Tags
- [DPA provision tags from original extraction]

## Order Text

[Case title block — "IN RE: RESPONDENT NAME" or complainant-vs-respondent format]

[x----x separator]

[Optional sub-heading: ORDER or CEASE AND DESIST ORDER — keep as bold paragraph, not a heading]

[Optional commissioner attribution — e.g. "NAGA, D.P.C.:" or "AGUIRRE, D.P.C.:"]

[Opening paragraph — "Before the Commission is..." or "This Order refers to..." or "This resolves..."]

### Facts

[Narrative of events, submissions, procedural history]

### Issues

[Issue statement(s) — only if present in the PDF; many orders omit this section]

### Discussion

[Legal analysis]

#### [Sub-heading from PDF, if any]

[Analysis content]

[Dispositive portion — WHEREFORE paragraph + SO ORDERED.]

[Date line — "City of Pasay, Philippines. DD Month YYYY." or "Pasay City, Philippines. DD Month YYYY."]

[Signature block]

[Copy furnished block]

[^1]: Footnote text.
[^2]: Footnote text.
```

**Heading levels:**
- `## Source`, `## Source Tags`, `## Order Text` — second level (preserve as-is)
- `### Facts`, `### Issues`, `### Discussion` — third level, within Order Text
- `#### Sub-heading` — fourth level for sub-topics within Discussion
- `### Issues` is **optional** — include only if the PDF has a distinct Issues section; do not add one if absent
- Some older orders use variant labels like `The Facts`, `Arguments of the Parties`, or `Issues` — promote these to the appropriate `###` heading, normalizing the label to match the PDF

Footnotes go after the copy furnished block, as `[^N]:` entries in numeric order, no heading.

**No title heading in the body.** Quartz uses the `title` frontmatter field. Do not add a `# NPC BN 23-179: In re: Philippine National Police` heading inside the document.

---

## Case number formats and title formats

Orders use the widest variety of case number prefixes across all NPC document types. Each has its own title convention:

| Case number format | Example | Title format |
|---|---|---|
| `NPC BN YY-NNN` | NPC BN 18-095 | `"NPC BN 18-095: In re: DMCI Project Developers, Inc."` |
| `NPC CC YY-NNN` | NPC CC 20-001 | `"NPC CC 20-001: In re: Grab Philippines"` |
| `NPC SS YY-NNN` | NPC SS 21-006 | `"NPC SS 21-006: In re: WeFund Lending Corporation"` |
| `NPC YY-NNN` | NPC 19-438 | `"NPC 19-438: RPR v. Edukasyon.ph"` |
| `NPC YY-NNN` (compliance) | NPC 16-004 | `"NPC 16-004: CBP v. Orani Water District"` |
| `CID BN YY-NNN` | CID BN 17-043 | `"CID BN 17-043: In re: Jollibee Delivery (Vulnerability Assessment)"` |
| `CID CDO YY-NNN` | CID CDO 25-001 | `"CID CDO 25-001: In re: World App Processing of Personal Information"` |
| `CID YY-X-NNN` | CID 18-D-012 | `"CID 18-D-012: JBD v. JI and VVV"` |
| `NPC YY-NNN` (multiple) | NPC 21-010 to NPC 21-015 | `"NPC 21-010 to NPC 21-015: MVC et al. v. DSL"` |
| Date-based reference | 02-03-2020 | Derive a proper case number from the PDF body (often `NPC CC YY-NNN` or similar); use that as the title reference |

**Older "CID" case numbers** (pre-2021) use `CID BN`, `CID BN-`, `CID CDO`, or bare `CID` prefixes. Preserve the prefix exactly as it appears in the PDF.

**Date-based filenames** are a signal that the original extraction failed to identify a case number. Check the PDF for a case number in the margin, the case title block, or the opening paragraph. If found, use it. If genuinely absent, use the issue date in `YYYY-MM-DD` format as the reference.

---

## Frontmatter

Standard frontmatter for an order:

```yaml
---
title: "NPC BN 18-095: In re: DMCI Project Developers, Inc."
description: "One factual sentence: what the order directed, who it was directed at, and in what context."
aliases:
  - "NPC BN 18-095"
  - "npc bn 18-095"
  - "In re: DMCI Project Developers, Inc."
  - "in re: dmci project developers, inc."
tags:
  - "order"
  - "type/order"
  - "year/YYYY"
  - "npc-case"
date: "YYYY-MM-DD"
draft: false
---
```

**Tags — `year/YYYY`:**
For orders, `year/` follows the **subfolder year** (the year the order was issued), NOT the case number year. An order in `content/orders/2023/` concerning `NPC BN 18-071` is tagged `year/2023`. This matches the resolution convention and differs from the decision convention.

**Aliases block — all four forms required:**

For "In re" orders (`NPC BN`, `NPC CC`, `NPC SS`, `CID BN`, `CID CDO`, sua sponte):
1. Canonical reference: `"NPC BN 18-095"`
2. Lowercase: `"npc bn 18-095"`
3. Short respondent name: `"In re: DMCI Project Developers, Inc."`
4. Lowercase: `"in re: dmci project developers, inc."`

For complainant-vs-respondent orders (`NPC YY-NNN`, `CID YY-X-NNN`):
1. Canonical reference: `"NPC 19-438"`
2. Lowercase: `"npc 19-438"`
3. Short case name: `"RPR v. Edukasyon.ph"`
4. Lowercase: `"rpr v. edukasyon.ph"`

---

## Title format

**Where to find the title:**
1. The case title block in the PDF — the "IN RE:" header or complainant/respondent names
2. The case number in the margin or header
3. The opening paragraph: "Before the Commission is..." or "This Order refers to..."

**ALL CAPS entity names must be title-cased in the title field:**
```
# Bad:
title: "NPC BN 23-179: In Re: PHILIPPINE NATIONAL POLICE"

# Good:
title: "NPC BN 23-179: In re: Philippine National Police"
```

Note the casing of "In re:" — capitalize `In`, lowercase `re:`. This matches standard legal citation style.

**Abbreviations and initials stay as-is** — pseudonymized names and official acronyms:
```
# Good:
title: "CID 18-D-012: JBD v. JI and VVV"
title: "NPC 19-438: RPR v. Edukasyon.ph"
```

**Use `v.` for most orders; preserve `vs.` if the PDF uses that form.**

**OCR table noise in title blocks:** Some PDFs have the case number printed in a right-margin column next to the case name. OCR can interleave these, producing garbage like:
```
title: "CID CDO 25-001: In Re: The Matter of World App CID NPCCDO 25-00125- CID CDO Processing of Personal (Note: No Case No or 001..."
```
This must be reconstructed from the PDF. Read the case title block carefully; the actual title is the subject matter text, not the margin annotations.

**Description field must be a factual one-sentence summary — never raw body text, OCR garbage, or scraped HTML:**
```
# Bad — raw body sentence:
description: "Before the Commission is a Supplemental Post Breach Report dated 26 August 2022 submitted by DMCI Project Developers, Inc. (DMCI).1"

# Bad — OCR table noise:
description: "IN THE MATTER OF WORLD APP CID NPCCDO 25-00125- CID CDO PROCESSING OF PERSONAL (Note: No Case No..."

# Bad — scraped website footer:
description: "![Image 2](http://privacy.gov.ph/wp-content/uploads/2017/03/Coat_of_arms_of_the_Philippines.png)..."

# Good:
description: "Order directing the CID to conduct a sua sponte investigation into DMCI Project Developers, Inc. for concealment and belated notification of a personal data breach involving unauthorized disclosure of a unit owner's documents."
description: "Cease and desist order against Tools for Humanity (World App) for processing personal data in violation of the general data privacy principles and data subject rights under the DPA."
description: "Order directing Edukasyon.ph to submit its Security Incident Management Policy and notify affected data subjects after exposing participants' names and email addresses in a thank-you email."
```

---

## Order-specific OCR artifacts to fix

These are in addition to the generic OCR artifacts covered by `npc-markdown-cleanup`:

| Artifact | What it looks like | Fix |
|---|---|---|
| Page-header injection | `Order\nPage N of M` appearing mid-paragraph | Delete entirely |
| Page-header injection (indented) | Indented `Order\nPage 2 of 6` between body paragraphs | Delete entirely |
| Letterhead blockquote | `> 5th Floor, Philippine International Convention Center...` or `> 5th Floor West Banquet Hall (A. Imao Hall), Delegation Building, PICC Complex` | Delete entirely |
| Letterhead inline | `5th Floor West Banquet Hall...` or `URL: http://privacy.gov.ph Email Address: info@privacy.gov.ph` appearing as body text | Delete entirely |
| OCR table noise in title block | Case number, "For: Violation of the Data Privacy Act", "Note: No Case No", "type (BN/SS) Year- #." interleaved with the case name | Reconstruct clean title block from the PDF |
| Source Tags containing website footer | `![Image 2](http://privacy.gov.ph/...)`, `###### REPUBLIC OF THE PHILIPPINES`, `GOV.PH`, social media icons | Replace with actual DPA provision tags from the order content, or leave only the legitimate tags |
| Footnote text as inline text | `1 Supplemental Post Breach Report dated...` between body paragraphs, or footnotes separated by blank lines | Extract; consolidate as `[^N]:` entries at end |
| Detached footnote callout | Number glued to next word (`2EDF`) or orphaned (`15 Id.`) | Normalize to `[^N]` after punctuation |
| Facts/Issues/Discussion as plain text | `FACTS`, `The Facts`, `Arguments of the Parties`, `Issues`, `Discussion`, `DISCUSSION` as bare paragraph headings | Promote to `### Facts`, `### Issues`, `### Discussion` |
| `Sgd.`/`SGD`/`(sgd)`/`[SGD.]` lines | Lone signature marker before a commissioner's name | Delete — OCR artifact of a signature image |
| Missing `date` field | No `date:` in frontmatter | Find in the PDF closing line (`City of Pasay, Philippines. DD Month YYYY.` or `Pasay City, Philippines\nDD Month YYYY`); add `date: "YYYY-MM-DD"` |
| Missing `aliases` block | No `aliases:` in frontmatter | Derive from case number and party/respondent names; add all four forms |
| Wrong year/ tag | `year/2022` on a file in the `2023/` subfolder | Correct to match the subfolder year |
| Description from body | `description:` contains the opening sentence verbatim, a footnote reference, or website scraping artifacts | Replace with a factual one-sentence summary |

---

## The case title block

**"In re" format (BN, CC, SS, CDO, sua sponte):**

```markdown
IN RE: PHILIPPINE NATIONAL POLICE                                NPC BN 23-179

x----------------------------------------------------x
```

Or multi-line IN RE block (common in CDOs and long titles):

```markdown
IN RE: GRAB PHILIPPINES' [1] ROLL-OUT OF THE PASSENGER SELFIE VERIFICATION; [2] PILOT TEST OF THE IN-VEHICLE AUDIO RECORDING; AND [3] PILOT TEST OF THE IN-VEHICLE VIDEO RECORDING

x----------------------------------------------------x
```

**Complainant-vs-respondent format:**

```markdown
RPR,

Complainant,

-versus-

EDUKASYON.PH,

Respondent.

x----------------------------------------------------x
```

**With "CID Case No." and "For: Violation" margin text:**

The PDF may show a margin column with `CID Case No. 18-D-012 / For: Violation of the Data Privacy Act of 2012` alongside the party names. This margin text is not body content — if OCR injected it into the title block, remove it. The case number belongs in `## Source` and the frontmatter, not inline in the title block (unless the PDF truly places it there as part of the heading).

The `x------x` separator stays as plain text. Do not convert to `---`.

---

## The ORDER / CEASE AND DESIST ORDER sub-heading

Many orders have a centered heading after the case title block — either `ORDER` or `CEASE AND DESIST ORDER`. This is a label for the document type, not a structural heading within the analysis. Render it as a bold paragraph, not as `###`:

```markdown
x----------------------------------------------------x

**CEASE AND DESIST ORDER**

NAGA, D.P.C.:
```

or simply:

```markdown
x----------------------------------------------------x

**ORDER**

Before the Commission is...
```

---

## Commissioner attribution

Some orders begin with a commissioner attribution line (common in CDOs and compliance orders):

```markdown
NAGA, D.P.C.:

This resolves the Recommendation...
```

or:

```markdown
AGUIRRE, D.P.C.:

Before this Commission is a Complaint...
```

Preserve this line as-is from the PDF. It appears after the case title block (and after the ORDER sub-heading if present), before the opening paragraph.

Not every order has an attribution line. Simple breach notification orders often go straight from the title block to the opening paragraph.

---

## Section headings within the body

Promote section labels to `###` headings:

| PDF label | Markdown heading |
|---|---|
| `FACTS` or `The Facts` | `### Facts` |
| `Arguments of the Parties` | `### Arguments of the Parties` |
| `Issues` or `ISSUES` | `### Issues` |
| `Discussion` or `DISCUSSION` | `### Discussion` |

Some orders skip directly from the narrative to the Discussion — this is normal. Do not add a `### Facts` heading if the PDF doesn't have one. Just let the narrative flow after the opening paragraph.

For sub-topics within Discussion, promote to `####`:

```markdown
### Discussion

#### On the Delay in Notification

...analysis...

#### On the Concealment

...analysis...
```

---

## Dispositive portion

The WHEREFORE clause and SO ORDERED line close the order. Keep as plain paragraphs — no heading:

```markdown
WHEREFORE, premises considered, the Commission **DIRECTS** the Complaints and Investigation Division to conduct a sua sponte investigation on the circumstances surrounding the concealment of the personal data breach...

**SO ORDERED.**

City of Pasay, Philippines. 04 September 2024.
```

The operative words (`DIRECTS`, `ORDERS`, `CEASE AND DESIST`, `CLOSED`, `NOTED`) should be bold if they appear emphasized in the PDF.

---

## Signature block

Orders use several signature formats depending on the era and number of commissioners:

**Three-commissioner "WE CONCUR:" format (most common post-2022):**
```markdown
JOHN HENRY D. NAGA
Privacy Commissioner

WE CONCUR:

LEANDRO ANGELO Y. AGUIRRE
Deputy Privacy Commissioner

NERISSA N. DE JESUS
Deputy Privacy Commissioner
```

**Two-commissioner "I CONCUR:" format:**
```markdown
LEANDRO ANGELO Y. AGUIRRE
Deputy Privacy Commissioner

I CONCUR:

JOHN HENRY D. NAGA
Privacy Commissioner
```

**Older three-commissioner "Concurring:" format:**
```markdown
LEANDRO ANGELO Y. AGUIRRE
Deputy Privacy Commissioner

Concurring:

RAYMUND ENRIQUEZ LIBORO
Privacy Commissioner

JOHN HENRY DU NAGA
Deputy Privacy Commissioner
```

Match the PDF exactly. Strip lone `Sgd.`, `SGD`, `(sgd)`, or `[SGD.]` lines — these are OCR artifacts of signature images, not text to preserve.

---

## Copy furnished block

Preserve as plain text after the signature block:

```markdown
Copy furnished:

RPR
Complainant

EDUKASYON.PH
Respondent

COMPLAINTS AND INVESTIGATION DIVISION
ENFORCEMENT DIVISION
GENERAL RECORDS UNIT
```

Some orders use `COPY FURNISHED` (all caps) — normalize to `Copy furnished:` for consistency.

---

## `## Source` section

Orders use `## Source`. Standard fields:

```markdown
## Source
- Reference: NPC BN 18-095
- Official PDF: [full URL from privacy.gov.ph]
- Source page: http://privacy.gov.ph/orders-2/
- Issue date: [Month DD, YYYY]
- Published on NPC site: [date]
- Pages: [N]
```

Correct any fields that are missing or clearly wrong. If the Reference field uses a date-based identifier but the PDF reveals an actual case number, update it.

---

## `## Source Tags` section

Source Tags should contain DPA provision tags — short labels identifying the legal provisions discussed in the order. They should NOT contain:
- Scraped website HTML, footer links, or government portal boilerplate
- Image markdown (`![Image N](...)`)
- Social media icon links
- `REPUBLIC OF THE PHILIPPINES` headers
- `GOV.PH`, `Open Data Portal`, `Official Gazette` links

If the Source Tags section contains scraped website content, replace it entirely with legitimate provision tags derived from the order's legal discussion (e.g., `Sec 17. Notification of the Commission`, `Sec 20. Security of Personal Information`, `Cease and Desist Order`).

---

## PDF location for orders

```
NPC_issuances/cache/orders/pdfs/
```

All order types (NPC BN, NPC CC, NPC SS, CID BN, CID CDO, CID, bare NPC, date-based) use this folder.

---

## Critical rules (order-specific)

- **Delete all letterhead injections.** Whether as blockquotes (`>`) or inline text — anything containing `Philippine International Convention Center`, `Delegation Building`, `PICC Complex`, `privacy.gov.ph`, or `info@privacy.gov.ph` is a letterhead artifact. Delete it.
- **Delete all page-header injections.** Lines matching `Order\nPage N of M` (with or without indentation) are page headers from the PDF. Delete them.
- **`### Facts` and `### Discussion` are expected headings.** If they exist as plain text (`FACTS`, `The Facts`, `Discussion`, `DISCUSSION`), promote them. Not every order has both — some short orders flow directly into analysis without a labeled Facts section, which is fine.
- **`### Issues` is optional.** Add it only if the PDF has a distinct Issues section. Many orders skip straight from Facts to Discussion.
- **The ORDER / CEASE AND DESIST ORDER label is a bold paragraph**, not a `###` heading. It identifies the document type, not a structural section.
- **`year/` tag follows the subfolder year (order issue year), not the case number year.** An order in `content/orders/2023/` about `NPC BN 18-071` → `year/2023`.
- **`date` field is required.** Find it in the PDF's closing line. Date line formats vary: `City of Pasay, Philippines. DD Month YYYY.`, `Pasay City, Philippines.\nDD Month YYYY`, or `Pasay City, DD Month YYYY.` Format as `"YYYY-MM-DD"`.
- **Description must be a factual summary.** Never copy the opening sentence verbatim; never include footnote numbers; never include scraped HTML or OCR table noise. Write a fresh sentence describing what the order directed, who it was directed at, and the context.
- **`aliases` block is required.** Use the correct form set for the case type (In re or complainant-vs-respondent).
- **Clean up Source Tags.** Remove any scraped website footer HTML. Keep only DPA provision tags.
- **Do not convert the `x------x` separator to `---`.** It's a visual artifact, not a thematic break.
- **Strip all `Sgd.`/`SGD`/`(sgd)`/`[SGD.]` lines** — OCR artifacts of signature images.
- **Reconstruct garbled title blocks from the PDF.** If the OCR interleaved margin annotations (case number column, "For: Violation..." text) with the case name, reconstruct a clean title block that matches what the PDF actually shows.
