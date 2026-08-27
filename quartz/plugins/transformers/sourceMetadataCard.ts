import { Root, Heading, List, ListItem, Link, PhrasingContent, Paragraph, Parent } from "mdast"
import { Element, ElementContent, Properties, Text as HastText } from "hast"
import { visit } from "unist-util-visit"
import { toString } from "mdast-util-to-string"
import { QuartzTransformerPlugin } from "../types"

// This plugin looks for the specific "## Source" (and optional "## Source Tags")
// blocks emitted by the Python builders in scripts/ (build_npc_advisory_opinions.py,
// build_npc_decisions_resolutions.py, build_npc_orders.py, build_npc_site.py) and
// rewrites them from a plain bulleted list into a compact metadata card.
//
// The content pipeline regenerates these Markdown files, so this is implemented as a
// build-time transform rather than a one-off content migration: any change here applies
// uniformly the next time the corpus is rebuilt.

type FieldKind =
  | "reference"
  | "pdfLink"
  | "sourcePage"
  | "issueDate"
  | "publishedDate"
  | "pages"
  | "subject"
  | "tags"
  | "ocr"

// Exhaustive vocabulary of "- Label: value" fields actually emitted under a "## Source"
// heading across content/advisory-opinions, content/decisions, content/orders,
// content/resolutions, and content/issuances (verified against the live corpus).
// Anything outside this vocabulary is treated as an unrecognized shape and the block is
// left untouched rather than guessed at.
const LABEL_KIND: Record<string, FieldKind> = {
  reference: "reference",
  "official pdf": "pdfLink",
  "official source pdf": "pdfLink",
  "official source": "pdfLink",
  "source page": "sourcePage",
  "issue date": "issueDate",
  issued: "issueDate",
  "published on npc site": "publishedDate",
  pages: "pages",
  subject: "subject",
  tags: "tags",
  "ocr used during extraction": "ocr",
  "ocr used": "ocr",
}

// Friendly labels for the handful of general listing pages the corpus links back to.
const SOURCE_PAGE_LABELS: [string, string][] = [
  ["/advisory-opinions/", "NPC advisory opinions listing"],
  ["/decisions-2/", "NPC decisions listing"],
  ["/orders-2/", "NPC orders listing"],
  ["/resolutions/", "NPC resolutions listing"],
]

const MONTH_ABBR: Record<string, string> = {
  Jan: "January",
  Feb: "February",
  Mar: "March",
  Apr: "April",
  May: "May",
  Jun: "June",
  Jul: "July",
  Aug: "August",
  Sep: "September",
  Oct: "October",
  Nov: "November",
  Dec: "December",
}

interface ParsedField {
  kind: FieldKind
  label: string
  valueNodes: PhrasingContent[]
}

interface LinkValue {
  href: string
  text: string
}

function flatten(nodes: PhrasingContent[]): string {
  return nodes.map((n) => toString(n)).join("")
}

// Reformat an RFC 2822 date ("Fri, 24 May 2024 01:34:32 GMT") into "May 24, 2024"
// using string parsing (not Date), again to sidestep timezone-shift surprises.
function reformatRfc2822Date(raw: string): string | null {
  const m = raw.trim().match(/^\w+,\s*(\d{1,2})\s+([A-Za-z]{3})\w*\s+(\d{4})/)
  if (!m) return null
  const day = parseInt(m[1], 10)
  const month = MONTH_ABBR[m[2] as keyof typeof MONTH_ABBR]
  if (!month) return null
  return `${month} ${day}, ${m[3]}`
}

function friendlySourcePageLabel(href: string): string {
  for (const [needle, label] of SOURCE_PAGE_LABELS) {
    if (href.includes(needle)) return label
  }
  try {
    return new URL(href).hostname
  } catch {
    return href
  }
}

function el(tagName: string, properties: Properties, children: ElementContent[]): Element {
  return { type: "element", tagName, properties, children }
}

function text(value: string): HastText {
  return { type: "text", value }
}

// Quartz's own CrawlLinks transformer (quartz/plugins/transformers/links.ts) walks every
// <a> in the final HTML tree, tags external links with an "external" class, and appends
// its own external-link icon — so these anchors only need to supply href/text and let
// that pass handle the rest, rather than duplicating an icon here.
function externalLink(href: string, className: string, children: ElementContent[]): Element {
  return el(
    "a",
    { href, className: [className], target: "_blank", rel: "noopener noreferrer" },
    children,
  )
}

// Parses a single "- Label: value" list item into a label/value-node pair. Returns null
// if the item doesn't have the expected "text, then colon" shape at all (e.g. it isn't a
// simple paragraph, or has no leading text node) — the caller treats that as "this isn't
// the block we're looking for" and bails out without touching anything.
function parseListItem(item: ListItem): { label: string; valueNodes: PhrasingContent[] } | null {
  if (item.children.length !== 1 || item.children[0].type !== "paragraph") return null
  const para = item.children[0] as Paragraph
  const [firstChild, ...rest] = para.children
  if (!firstChild || firstChild.type !== "text") return null
  const match = firstChild.value.match(/^\s*([A-Za-z][A-Za-z0-9 ]*?)\s*:\s*(.*)$/s)
  if (!match) return null
  const [, label, restOfFirstText] = match
  const valueNodes: PhrasingContent[] = []
  if (restOfFirstText.length > 0) {
    valueNodes.push({ type: "text", value: restOfFirstText })
  }
  valueNodes.push(...rest)
  return { label: label.trim(), valueNodes }
}

function extractLinkValue(valueNodes: PhrasingContent[]): LinkValue | null {
  const linkNode = valueNodes.find((n): n is Link => n.type === "link")
  if (linkNode) {
    const linkText = toString(linkNode).trim()
    return { href: linkNode.url, text: linkText.length > 0 ? linkText : linkNode.url }
  }
  const plain = flatten(valueNodes).trim()
  if (/^https?:\/\//.test(plain)) {
    return { href: plain, text: plain }
  }
  return null
}

// Parses the list following "## Source" into recognized fields. Returns null if any
// item's label falls outside the known vocabulary, or any recognized link-shaped field
// doesn't actually resolve to a URL — in either case the caller leaves the page alone.
function parseSourceFields(list: List): Map<FieldKind, ParsedField> | null {
  const fields = new Map<FieldKind, ParsedField>()
  for (const item of list.children) {
    const parsed = parseListItem(item)
    if (!parsed) return null
    const kind = LABEL_KIND[parsed.label.toLowerCase()]
    if (!kind) return null
    if ((kind === "pdfLink" || kind === "sourcePage") && !extractLinkValue(parsed.valueNodes)) {
      return null
    }
    fields.set(kind, { kind, label: parsed.label, valueNodes: parsed.valueNodes })
  }
  return fields.size > 0 ? fields : null
}

function splitTagsField(raw: string): string[] {
  const delimiter = raw.includes(";") ? ";" : ","
  return raw
    .split(delimiter)
    .map((t) => t.trim())
    .filter((t) => t.length > 0)
}

// Parses the list following an optional "## Source Tags" heading. Decisions/orders/
// resolutions frequently bundle several concepts into a single comma-separated list
// item (that's how the source PDFs enumerate them), so each item is run through the
// same semicolon-or-comma splitter as the "Tags:" field to get individual chips.
function parseSourceTagsList(list: List): string[] {
  const tags: string[] = []
  for (const item of list.children) {
    if (item.children.length !== 1 || item.children[0].type !== "paragraph") return []
    const tagText = toString(item.children[0]).trim()
    if (tagText.length === 0) return []
    tags.push(...splitTagsField(tagText))
  }
  return tags
}

function buildCard(fields: Map<FieldKind, ParsedField>, extraTags: string[]): Element {
  const rows: Element[] = []
  const addRow = (label: string, valueChildren: ElementContent[]) => {
    rows.push(el("dt", {}, [text(label)]))
    rows.push(el("dd", {}, valueChildren))
  }

  const reference = fields.get("reference")
  if (reference) {
    addRow("Reference", [text(flatten(reference.valueNodes).trim())])
  }

  const subject = fields.get("subject")
  if (subject) {
    addRow("Subject", [text(flatten(subject.valueNodes).trim())])
  }

  // Deliberately no "Issue date" row: the date is already stated under the title by
  // ContentMeta, sourced from the `date:` frontmatter that scripts/backfill_dates.py
  // resolved from each document's own dateline. The raw "- Issue date:" field in the
  // Source block is not trustworthy enough to show — it is wrong outright in a number
  // of files and is DD/MM/YYYY rather than MM/DD/YYYY in others. The field is still
  // parsed above so that its presence does not make the card bail out.

  const publishedDate = fields.get("publishedDate")
  if (publishedDate) {
    const raw = flatten(publishedDate.valueNodes).trim()
    addRow("Published", [text(reformatRfc2822Date(raw) ?? raw)])
  }

  const pages = fields.get("pages")
  if (pages) {
    const raw = flatten(pages.valueNodes).trim()
    const n = parseInt(raw, 10)
    addRow("Length", [text(Number.isFinite(n) ? `${n} page${n === 1 ? "" : "s"}` : raw)])
  }

  const sourcePage = fields.get("sourcePage")
  if (sourcePage) {
    const link = extractLinkValue(sourcePage.valueNodes)!
    addRow("Source listing", [
      externalLink(link.href, "metadata-card-link", [text(friendlySourcePageLabel(link.href))]),
    ])
  }

  const children: ElementContent[] = []
  if (rows.length > 0) {
    children.push(el("dl", { className: ["metadata-card-fields"] }, rows))
  }

  const pdfLink = fields.get("pdfLink")
  if (pdfLink) {
    const link = extractLinkValue(pdfLink.valueNodes)!
    children.push(
      el("div", { className: ["metadata-card-actions"] }, [
        externalLink(link.href, "metadata-card-pdf-link", [text("Official PDF")]),
      ]),
    )
  }

  const tagsField = fields.get("tags")
  const allTags = [
    ...(tagsField ? splitTagsField(flatten(tagsField.valueNodes).trim()) : []),
    ...extraTags,
  ]
  if (allTags.length > 0) {
    children.push(
      el(
        "ul",
        { className: ["metadata-card-tags"] },
        allTags.map((tag) => el("li", { className: ["metadata-card-tag"] }, [text(tag)])),
      ),
    )
  }

  const ocr = fields.get("ocr")
  if (ocr) {
    const raw = flatten(ocr.valueNodes).trim()
    children.push(
      el("p", { className: ["metadata-card-note"] }, [text(`OCR used during extraction: ${raw}`)]),
    )
  }

  return el("aside", { className: ["metadata-card"] }, children)
}

export const SourceMetadataCard: QuartzTransformerPlugin = () => {
  return {
    name: "SourceMetadataCard",
    markdownPlugins() {
      return [
        () => {
          return (tree: Root) => {
            const matches: { parent: Parent; index: number }[] = []
            visit(tree, "heading", (node: Heading, index, parent) => {
              if (parent == null || index == null) return
              if (node.depth !== 2) return
              if (toString(node).trim() !== "Source") return
              matches.push({ parent: parent as Parent, index })
            })

            // Process in reverse document order so earlier indices in `matches` stay
            // valid as we splice nodes out of their parents.
            for (let i = matches.length - 1; i >= 0; i--) {
              const { parent, index } = matches[i]
              const list = parent.children[index + 1]
              if (!list || list.type !== "list" || (list as List).ordered) continue

              const fields = parseSourceFields(list as List)
              if (!fields) continue

              let consumeCount = 2
              let extraTags: string[] = []
              const maybeTagsHeading = parent.children[index + 2]
              const maybeTagsList = parent.children[index + 3]
              if (
                maybeTagsHeading &&
                maybeTagsHeading.type === "heading" &&
                (maybeTagsHeading as Heading).depth === 2 &&
                toString(maybeTagsHeading).trim() === "Source Tags" &&
                maybeTagsList &&
                maybeTagsList.type === "list" &&
                !(maybeTagsList as List).ordered
              ) {
                const tags = parseSourceTagsList(maybeTagsList as List)
                if (tags.length > 0) {
                  extraTags = tags
                  consumeCount = 4
                }
              }

              // Replace the heading with a plain paragraph node carrying hName/hChildren
              // overrides for the hast conversion. Using a non-heading mdast type (rather
              // than mutating the heading node's `data` in place) keeps it invisible to
              // other markdown-level plugins that key off `type === "heading"` — notably
              // TableOfContents, which would otherwise list an empty "Source" entry.
              const card = buildCard(fields, extraTags)
              const cardNode: Paragraph = {
                type: "paragraph",
                children: [],
                data: {
                  hName: card.tagName,
                  hProperties: card.properties,
                  hChildren: card.children,
                },
              }
              parent.children[index] = cardNode
              parent.children.splice(index + 1, consumeCount - 1)
            }
          }
        },
      ]
    },
  }
}
