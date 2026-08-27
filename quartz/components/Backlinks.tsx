import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { QuartzPluginData } from "../plugins/vfile"
import style from "./styles/backlinks.scss"
import { resolveRelative, simplifySlug } from "../util/path"
import { i18n } from "../i18n"
import { classNames } from "../util/lang"
import OverflowListFactory from "./OverflowList"

interface BacklinksOptions {
  hideWhenEmpty: boolean
}

const defaultOptions: BacklinksOptions = {
  hideWhenEmpty: true,
}

// Slug prefixes that identify auto-generated hub/listing pages rather than real
// documents. These pages exist to enumerate many documents (a tag cluster, a
// topic cluster, a document-type cluster) and so link to nearly everything in
// their category — counting them as a "backlink" is noise, not a genuine
// cross-reference between two documents.
const HUB_SLUG_PREFIXES = ["tags/", "topics/", "types/"]

// A source file is a genuine cross-reference only if it's an actual document,
// not a folder index page (e.g. "advisory-opinions/2021/index", which links to
// every opinion filed that year) or one of the auto-generated hub pages above.
function isGenuineReference(file: QuartzPluginData): boolean {
  const slug = file.slug ?? ""
  if (slug === "index" || slug.endsWith("/index")) {
    return false
  }
  return !HUB_SLUG_PREFIXES.some((prefix) => slug.startsWith(prefix))
}

export default ((opts?: Partial<BacklinksOptions>) => {
  const options: BacklinksOptions = { ...defaultOptions, ...opts }
  const { OverflowList, overflowListAfterDOMLoaded } = OverflowListFactory()

  const Backlinks: QuartzComponent = ({
    fileData,
    allFiles,
    displayClass,
    cfg,
  }: QuartzComponentProps) => {
    const slug = simplifySlug(fileData.slug!)
    const backlinkFiles = allFiles.filter(
      (file) => file.links?.includes(slug) && isGenuineReference(file),
    )
    if (options.hideWhenEmpty && backlinkFiles.length == 0) {
      return null
    }
    return (
      <div class={classNames(displayClass, "backlinks")}>
        <h3>{i18n(cfg.locale).components.backlinks.title}</h3>
        <OverflowList>
          {backlinkFiles.length > 0 ? (
            backlinkFiles.map((f) => (
              <li>
                <a href={resolveRelative(fileData.slug!, f.slug!)} class="internal">
                  {f.frontmatter?.title}
                </a>
              </li>
            ))
          ) : (
            <li>{i18n(cfg.locale).components.backlinks.noBacklinksFound}</li>
          )}
        </OverflowList>
      </div>
    )
  }

  Backlinks.css = style
  Backlinks.afterDOMLoaded = overflowListAfterDOMLoaded

  return Backlinks
}) satisfies QuartzComponentConstructor
