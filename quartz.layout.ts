import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"
import { FileTrieNode } from "./quartz/util/fileTrie"

const explorerFilter = (node: FileTrieNode) =>
  node.slugSegment !== "tags" && node.slugSegment !== "sources" && node.slugSegment !== "notes"

function explorerSortFn(a: FileTrieNode, b: FileTrieNode): number {
  if (a.isFolder !== b.isFolder) {
    return a.isFolder ? -1 : 1
  }

  const aSegment = a.slugSegment.toLowerCase()
  const aLabel = a.displayName.toLowerCase()
  let yearA: number | null = null
  if (aSegment === "undated" || aLabel === "undated") {
    yearA = -1
  } else if (/^\d{4}$/.test(aSegment)) {
    yearA = Number(aSegment)
  } else if (/^\d{4}$/.test(aLabel)) {
    yearA = Number(aLabel)
  } else {
    const aSegmentMatch = aSegment.match(/(19|20)\d{2}/)
    if (aSegmentMatch) {
      yearA = Number(aSegmentMatch[0])
    } else {
      const aLabelMatch = aLabel.match(/(19|20)\d{2}/)
      if (aLabelMatch) yearA = Number(aLabelMatch[0])
    }
  }

  const bSegment = b.slugSegment.toLowerCase()
  const bLabel = b.displayName.toLowerCase()
  let yearB: number | null = null
  if (bSegment === "undated" || bLabel === "undated") {
    yearB = -1
  } else if (/^\d{4}$/.test(bSegment)) {
    yearB = Number(bSegment)
  } else if (/^\d{4}$/.test(bLabel)) {
    yearB = Number(bLabel)
  } else {
    const bSegmentMatch = bSegment.match(/(19|20)\d{2}/)
    if (bSegmentMatch) {
      yearB = Number(bSegmentMatch[0])
    } else {
      const bLabelMatch = bLabel.match(/(19|20)\d{2}/)
      if (bLabelMatch) yearB = Number(bLabelMatch[0])
    }
  }

  if (yearA !== null && yearB !== null && yearA !== yearB) {
    return yearB - yearA
  }

  if (yearA !== null && yearB === null) return -1
  if (yearA === null && yearB !== null) return 1

  return a.displayName.localeCompare(b.displayName, undefined, {
    numeric: true,
    sensitivity: "base",
  })
}

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      "NPC Source Index": "https://privacy.gov.ph/pips-and-pics/advisories-circulars/",
      Quartz: "https://quartz.jzhao.xyz/",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
      ],
    }),
    Component.Explorer({
      title: "Corpus",
      folderDefaultState: "open",
      folderClickBehavior: "link",
      filterFn: explorerFilter,
      sortFn: explorerSortFn,
    }),
  ],
  right: [
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks(),
    Component.Graph(),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
      ],
    }),
    Component.Explorer({
      title: "Corpus",
      folderDefaultState: "open",
      folderClickBehavior: "link",
      filterFn: explorerFilter,
      sortFn: explorerSortFn,
    }),
  ],
  right: [],
}
