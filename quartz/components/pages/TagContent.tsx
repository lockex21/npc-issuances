import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "../types"
import style from "../styles/listPage.scss"
import { PageList, SortFn } from "../PageList"
import {
  FullSlug,
  getAllSegmentPrefixes,
  resolveRelative,
  simplifySlug,
  slugOfficialOpinionTag,
} from "../../util/path"
import { QuartzPluginData } from "../../plugins/vfile"
import { Root } from "hast"
import { htmlToJsx } from "../../util/jsx"
import { i18n } from "../../i18n"
import { ComponentChildren } from "preact"
import { concatenateResources } from "../../util/resources"

interface TagContentOptions {
  sort?: SortFn
  numPages: number
}

const defaultOptions: TagContentOptions = {
  numPages: 10,
}

interface OfficialTagAccumulator {
  labels: Map<string, number>
  pages: Set<FullSlug>
}

interface OfficialTagDirectoryEntry {
  count: number
  label: string
  slug: string
}

function buildOfficialTagDirectory(allFiles: QuartzPluginData[]): {
  assignments: number
  entries: OfficialTagDirectoryEntry[]
  opinions: number
} {
  const tagMap = new Map<string, OfficialTagAccumulator>()
  let assignments = 0
  let opinions = 0

  for (const file of allFiles) {
    const officialTags = file.frontmatter?.officialTags ?? []
    if (officialTags.length === 0 || file.slug === undefined) continue
    opinions += 1

    for (const label of officialTags) {
      assignments += 1
      const tagSlug = slugOfficialOpinionTag(label)
      const entry = tagMap.get(tagSlug) ?? {
        labels: new Map<string, number>(),
        pages: new Set<FullSlug>(),
      }
      entry.labels.set(label, (entry.labels.get(label) ?? 0) + 1)
      entry.pages.add(file.slug)
      tagMap.set(tagSlug, entry)
    }
  }

  const entries = [...tagMap.entries()]
    .map(([tagSlug, entry]) => {
      const label = [...entry.labels.entries()].sort(
        ([labelA, countA], [labelB, countB]) => countB - countA || labelA.localeCompare(labelB),
      )[0][0]
      return { count: entry.pages.size, label, slug: tagSlug }
    })
    .sort((entryA, entryB) =>
      entryA.label.localeCompare(entryB.label, undefined, { sensitivity: "base" }),
    )

  return { assignments, entries, opinions }
}

function groupOfficialTags(entries: OfficialTagDirectoryEntry[]) {
  const groups = new Map<string, OfficialTagDirectoryEntry[]>()
  for (const entry of entries) {
    const firstCharacter = entry.label.trim().charAt(0).toUpperCase()
    const group = /^[A-Z]$/.test(firstCharacter) ? firstCharacter : "#"
    groups.set(group, [...(groups.get(group) ?? []), entry])
  }
  return [...groups.entries()].sort(([groupA], [groupB]) => {
    if (groupA === "#") return -1
    if (groupB === "#") return 1
    return groupA.localeCompare(groupB)
  })
}

export default ((opts?: Partial<TagContentOptions>) => {
  const options: TagContentOptions = { ...defaultOptions, ...opts }

  const TagContent: QuartzComponent = (props: QuartzComponentProps) => {
    const { tree, fileData, allFiles, cfg } = props
    const slug = fileData.slug

    if (!(slug?.startsWith("tags/") || slug === "tags")) {
      throw new Error(`Component "TagContent" tried to render a non-tag page: ${slug}`)
    }

    const tag = simplifySlug(slug.slice("tags/".length) as FullSlug)
    const allPagesWithTag = (tag: string) =>
      allFiles.filter((file) =>
        (file.frontmatter?.tags ?? []).flatMap(getAllSegmentPrefixes).includes(tag),
      )

    const content = (
      (tree as Root).children.length === 0
        ? fileData.description
        : htmlToJsx(fileData.filePath!, tree)
    ) as ComponentChildren
    const cssClasses: string[] = fileData.frontmatter?.cssclasses ?? []
    const classes = cssClasses.join(" ")
    if (tag === "opinion") {
      const directory = buildOfficialTagDirectory(allFiles)
      const groups = groupOfficialTags(directory.entries)

      return (
        <div class="popover-hint">
          <article class={classes}>{content}</article>
          <p class="official-tag-directory-summary">
            <strong>{directory.entries.length}</strong> distinct tags from {directory.assignments}{" "}
            PDF tag assignments across <strong>{directory.opinions}</strong> advisory opinions.
          </p>
          <nav class="official-tag-directory-jump" aria-label="Official tag initials">
            {groups.map(([group]) => {
              const anchor = group === "#" ? "numbers-and-symbols" : group.toLowerCase()
              return (
                <a class="official-tag-directory-jump-link" href={`#official-tags-${anchor}`}>
                  {group === "#" ? "0–9" : group}
                </a>
              )
            })}
          </nav>
          <div class="official-tag-directory">
            {groups.map(([group, entries]) => {
              const anchor = group === "#" ? "numbers-and-symbols" : group.toLowerCase()
              return (
                <section aria-labelledby={`official-tags-${anchor}`}>
                  <h2 id={`official-tags-${anchor}`}>{group === "#" ? "0–9" : group}</h2>
                  <ul>
                    {entries.map((entry) => (
                      <li>
                        <a
                          class="internal tag-link"
                          href={resolveRelative(
                            fileData.slug!,
                            `tags/opinion/${entry.slug}` as FullSlug,
                          )}
                        >
                          {entry.label}
                        </a>
                        <span class="official-tag-directory-count">
                          {entry.count} opinion{entry.count === 1 ? "" : "s"}
                        </span>
                      </li>
                    ))}
                  </ul>
                </section>
              )
            })}
          </div>
        </div>
      )
    }

    if (tag === "/") {
      const tags = [
        ...new Set(
          allFiles.flatMap((data) => data.frontmatter?.tags ?? []).flatMap(getAllSegmentPrefixes),
        ),
      ].sort((a, b) => a.localeCompare(b))
      const tagItemMap: Map<string, QuartzPluginData[]> = new Map()
      for (const tag of tags) {
        tagItemMap.set(tag, allPagesWithTag(tag))
      }
      return (
        <div class="popover-hint">
          <article class={classes}>
            <p>{content}</p>
          </article>
          <p>{i18n(cfg.locale).pages.tagContent.totalTags({ count: tags.length })}</p>
          <div>
            {tags.map((tag) => {
              const pages = tagItemMap.get(tag)!
              const listProps = {
                ...props,
                allFiles: pages,
              }

              const contentPage = allFiles.filter((file) => file.slug === `tags/${tag}`).at(0)

              const root = contentPage?.htmlAst
              const content =
                !root || root?.children.length === 0
                  ? contentPage?.description
                  : htmlToJsx(contentPage.filePath!, root)

              const tagListingPage = `/tags/${tag}` as FullSlug
              const href = resolveRelative(fileData.slug!, tagListingPage)

              return (
                <div>
                  <h2>
                    <a class="internal tag-link" href={href}>
                      {tag}
                    </a>
                  </h2>
                  {content && <p>{content}</p>}
                  <div class="page-listing">
                    <p>
                      {i18n(cfg.locale).pages.tagContent.itemsUnderTag({ count: pages.length })}
                      {pages.length > options.numPages && (
                        <>
                          {" "}
                          <span>
                            {i18n(cfg.locale).pages.tagContent.showingFirst({
                              count: options.numPages,
                            })}
                          </span>
                        </>
                      )}
                    </p>
                    <PageList limit={options.numPages} {...listProps} sort={options?.sort} />
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )
    } else {
      const pages = allPagesWithTag(tag)
      const listProps = {
        ...props,
        allFiles: pages,
      }

      return (
        <div class="popover-hint">
          <article class={classes}>{content}</article>
          <div class="page-listing">
            <p>{i18n(cfg.locale).pages.tagContent.itemsUnderTag({ count: pages.length })}</p>
            <div>
              <PageList {...listProps} sort={options?.sort} />
            </div>
          </div>
        </div>
      )
    }
  }

  TagContent.css = concatenateResources(
    style,
    PageList.css,
    `
.official-tag-directory-summary {
  color: var(--darkgray);
  margin: 1.5rem 0 0.75rem;
}

.official-tag-directory-jump {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin: 0 0 1.75rem;
}

.official-tag-directory-jump-link {
  align-items: center;
  background-color: var(--highlight);
  border-radius: 0.35rem;
  color: var(--secondary);
  display: inline-flex;
  font-weight: 600;
  justify-content: center;
  min-width: 1.8rem;
  padding: 0.2rem 0.35rem;
  text-decoration: none;
}

.official-tag-directory-jump-link:hover {
  color: var(--tertiary);
}

.official-tag-directory > section {
  scroll-margin-top: 5rem;
}

.official-tag-directory > section > h2 {
  border-bottom: 1px solid var(--lightgray);
  margin-top: 2rem;
  padding-bottom: 0.3rem;
}

.official-tag-directory > section > ul {
  column-gap: 2rem;
  columns: 2 18rem;
  list-style: none;
  padding-left: 0;
}

.official-tag-directory > section > ul > li {
  break-inside: avoid;
  display: flex;
  gap: 0.5rem;
  justify-content: space-between;
  margin: 0 0 0.55rem;
}

.official-tag-directory-count {
  color: var(--gray);
  flex: 0 0 auto;
  font-size: 0.85rem;
  white-space: nowrap;
}
`,
  )
  return TagContent
}) satisfies QuartzComponentConstructor
