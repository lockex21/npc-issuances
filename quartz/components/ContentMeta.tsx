import { Date, getDate } from "./Date"
import { QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
import { JSX } from "preact"
import style from "./styles/contentMeta.scss"

interface ContentMetaOptions {
  /**
   * Whether to display a document-type badge (derived from the `type/...` tag)
   */
  showDocType: boolean
  showComma: boolean
}

const defaultOptions: ContentMetaOptions = {
  showDocType: true,
  showComma: true,
}

// Maps the segment after `type/` in a frontmatter tag to a human-readable label.
// This corpus is a fixed, known set of NPC issuance types (see quartz.layout.ts /
// content/*/index.md for the full taxonomy), so an explicit map is more legible
// than a generic slug-humanizer and lets us special-case abbreviations like "FAQ".
const DOC_TYPE_LABELS: Record<string, string> = {
  "advisory-opinion": "Advisory Opinion",
  decision: "Decision",
  resolution: "Resolution",
  order: "Order",
  circular: "Circular",
  advisory: "Advisory",
  faq: "FAQ",
  annex: "Annex",
  "joint-advisory": "Joint Advisory",
  "joint-memorandum-circular": "Joint Memorandum Circular",
  "rules-of-procedure": "Rules of Procedure",
}

function humanize(slug: string): string {
  return slug
    .split("-")
    .map((word) => (word.length > 0 ? word[0].toUpperCase() + word.slice(1) : word))
    .join(" ")
}

// Derive a document-type badge from the page's frontmatter tags. Legal issuances in
// this corpus are tagged `type/<kind>` (e.g. `type/advisory-opinion`); the two core
// law texts instead carry a bare `law` tag. Returns undefined (no badge) for pages
// that carry neither, e.g. folder index pages.
function getDocType(fileData: QuartzComponentProps["fileData"]): string | undefined {
  const tags = fileData.frontmatter?.tags ?? []
  for (const tag of tags) {
    if (tag.startsWith("type/")) {
      const key = tag.slice("type/".length)
      return DOC_TYPE_LABELS[key] ?? humanize(key)
    }
  }
  if (tags.includes("law")) {
    return "Law"
  }
  return undefined
}

export default ((opts?: Partial<ContentMetaOptions>) => {
  // Merge options with defaults
  const options: ContentMetaOptions = { ...defaultOptions, ...opts }

  function ContentMetadata({ cfg, fileData, displayClass }: QuartzComponentProps) {
    const text = fileData.text

    if (text) {
      const segments: (string | JSX.Element)[] = []

      // Only render a date when the source frontmatter actually supplied one for the
      // site's configured date type (e.g. `date:`/`published:`). Absent that, the
      // CreatedModifiedDate transformer silently coerces to the current build time,
      // which would misrepresent an unknown issuance date as today's date on a legal
      // document. Checking the frontmatter directly (rather than `fileData.dates`,
      // which is always populated) lets us tell "no date given" apart from "today".
      const dateType = cfg.defaultDateType
      const hasExplicitDate = dateType != null && fileData.frontmatter?.[dateType] != null
      if (hasExplicitDate && fileData.dates) {
        segments.push(
          <span class="content-meta-date">
            Issued <Date date={getDate(cfg, fileData)!} locale={cfg.locale} />
          </span>,
        )
      }

      // Display a document-type badge instead of a "N min read" estimate, which is
      // blog furniture that doesn't help a lawyer or privacy officer citing a document.
      if (options.showDocType) {
        const docType = getDocType(fileData)
        if (docType) {
          segments.push(<span class="content-meta-doctype">{docType}</span>)
        }
      }

      if (segments.length === 0) {
        return null
      }

      return (
        <p show-comma={options.showComma} class={classNames(displayClass, "content-meta")}>
          {segments}
        </p>
      )
    } else {
      return null
    }
  }

  ContentMetadata.css = style

  return ContentMetadata
}) satisfies QuartzComponentConstructor
