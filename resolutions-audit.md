# NPC Resolutions Cleanup — Final Audit Report

**Date:** 2026-04-10  
**Scope:** All `.md` files in `content/resolutions/*/` (excluding `index.md`)  
**Total files scanned:** 140  

---

## Results

| Status | Count |
|--------|-------|
| ✅ Pass (no symptoms) | 140 |
| ❌ Fail (symptoms remain) | 0 |
| ⚠️ YAML error | 0 |

**All 140 resolution files pass the audit.**

---

## Batch Summary (98 files re-cleaned)

The batch targeted 98 resolution files that had been falsely marked "done" by a prior run. Each file was cleaned sequentially using one subagent per file, reading both `npc-markdown-cleanup/SKILL.md` and `npc-resolution-cleanup/SKILL.md`.

**Common fixes applied across the batch:**
- OCR paragraph fragmentation rejoined (hundreds of line breaks per file)
- Footnote blockquotes (`> N`) consolidated to end-of-file `[^N]:` entries
- Page-header injections removed (mid-body `NPC BN XX-XXX` lines)
- Letterhead blockquotes deleted (`Philippine International Convention Center` address blocks)
- `Sgd.` OCR artifacts removed from signature blocks
- Broken words repaired (`"dat a"` → `"data"`, `"re sult ed"` → `"resulted"`, etc.)
- YAML frontmatter rebuilt: factual descriptions, four-alias blocks, `year/` tag matching folder year
- Section headings promoted to `### Facts`, `### Issue`, `### Discussion`
- Operative words bolded (**WHEREFORE**, **SO ORDERED**, etc.)
- `x------x` case-title separators preserved as plain text

**Average line reduction:** ~55% (OCR files often 400–1000 lines; cleaned files 150–300 lines)

---

## Post-Batch Corrections

Two YAML issues were found after the main batch and fixed immediately:

| File | Issue | Fix |
|------|-------|-----|
| `2023/npc-bn-20-167-in-re-travelservices-inc-2.md` | Smart quotes (U+201C/D, U+2019) throughout frontmatter | Replaced with straight quotes |
| `2024/npc-19-002-in-re-pj-lhuillier-incorporated.md` | Smart apostrophe (U+2019) in description | Replaced with straight apostrophe |

Three files outside the batch had lingering artifacts fixed during the audit:

| File | Issue | Fix |
|------|-------|-----|
| `2018/npc-bn-18-029-in-re-hc-consumer-finance-philippines-inc.md` | `NPC BN 18 -029` mid-body page header | Removed |
| `2018/npc-bn-18-035-in-re-active-network-llc.md` | 3 `Sgd.` artifacts in signature block | Removed |
| `2023/npc-bn-18-200-in-re-cardinal-health-international-philippines-inc.md` | 3 `Sgd.` artifacts in signature block | Removed |

---

## Known Out-of-Scope Issues

One file (`2018/npc-bn-18-033-and-npc-bn-18-076-...md`, 1,975 lines) has significant OCR corruption but was not part of the original 98-file batch. It is flagged here for a future dedicated cleanup run.

---

## Audit Method

Symptoms scanned per file:
1. Footnote blockquotes (`^> \d+` patterns) in body
2. Letterhead injections (`Philippine International Convention Center`)
3. Mid-body OCR page headers (case-number lines with OCR spacing artifacts, excluding case title block)
4. `Sgd.` artifact lines
5. Excessive blank-line ratio (> 90%)
6. YAML parse errors
7. Smart quotes (U+2018/2019/201C/201D) in frontmatter
