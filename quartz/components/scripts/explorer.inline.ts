import { FileTrieNode } from "../../util/fileTrie"
import { FullSlug, resolveRelative, simplifySlug } from "../../util/path"
import { ContentDetails } from "../../plugins/emitters/contentIndex"

type MaybeHTMLElement = HTMLElement | undefined

interface ParsedOptions {
  folderClickBehavior: "collapse" | "link"
  folderDefaultState: "collapsed" | "open"
  useSavedState: boolean
  sortFn: (a: FileTrieNode, b: FileTrieNode) => number
  filterFn: (node: FileTrieNode) => boolean
  mapFn: (node: FileTrieNode) => void
  order: "sort" | "filter" | "map"[]
}

type FolderState = {
  path: string
  collapsed: boolean
}

// This corpus's document titles follow a small number of stable patterns, e.g.:
//   "NPC Advisory Opinion No. 2021-022 — Processing Personal Data For ..."
//   "NPC 22-117: CJJ vs. JJS and JB"                    (decisions)
//   "NPC BN 18-037: In re: Acesite (Phils.) Hotel Corporation"  (resolutions/orders)
//   "CID CDO 22-001: CID vs. PH-Check.com"
//   "Guidelines on Administrative Fines (Circular No. 2022-01)" (circulars/advisories)
//   "Data Privacy Act of 2012 (Republic Act No. 10173)"  (laws)
// Full titles like these wrap 3-4 lines in the ~320px-wide sidebar when there are
// ~900 entries. Derive a short "document number" label for the sidebar and keep the
// full title as a tooltip, falling back to the full title when no number is found
// (e.g. plain folder names like "Advisory Opinions" or "2021").
const ADVISORY_OPINION_RE = /^(?:NPC\s+)?Advisory Opinion No\.\s*([\d]{4}-[\d]+)/i
const CASE_NUMBER_RE =
  /^((?:NPC|CID)(?:\s[A-Z]{2,4})?\s[\d]{2,4}-[\d]+(?:\s(?:to|and)\s(?:NPC\s)?[\d]{2,4}-[\d]+)?)\s*:/
const PAREN_ISSUANCE_RE = /\(((?:NPC\s+|Joint\s+)?[A-Za-z ]*?No\.\s*[\d]{2,6}(?:-[\d]+)?)\)\s*$/

function getShortLabel(rawTitle: string): string {
  // Some titles open with a stray quotation mark left over from the source PDF.
  // Strip leading quotes/whitespace before matching so those entries still get a
  // short label instead of falling back to a truncated full title.
  const fullTitle = rawTitle.replace(/^[\s"'\u201c\u201d\u2018\u2019]+/, "")

  const aoMatch = fullTitle.match(ADVISORY_OPINION_RE)
  if (aoMatch) {
    return `AO ${aoMatch[1]}`
  }

  const caseMatch = fullTitle.match(CASE_NUMBER_RE)
  if (caseMatch) {
    return caseMatch[1]
  }

  const parenMatch = fullTitle.match(PAREN_ISSUANCE_RE)
  if (parenMatch) {
    return parenMatch[1].replace(/\bNo\.\s*/i, "").replace(/^Republic Act\b/i, "RA")
  }

  return fullTitle
}

function applyShortLabel(el: HTMLElement, fullTitle: string) {
  const shortLabel = getShortLabel(fullTitle)
  el.textContent = shortLabel
  // Always set the tooltip so the full subject is available on hover, even when
  // the short label happens to equal the full title (e.g. "Advisory Opinions").
  el.title = fullTitle
}

let currentExplorerState: Array<FolderState>
function isMobileExplorerToggle(toggle: Element | null): toggle is HTMLElement {
  return (
    toggle instanceof HTMLElement &&
    window.matchMedia("(max-width: 800px)").matches &&
    getComputedStyle(toggle).display !== "none"
  )
}

function syncExplorerState(explorer: HTMLElement) {
  const collapsed = explorer.classList.contains("collapsed")
  const expanded = (!collapsed).toString()
  explorer.setAttribute("aria-expanded", expanded)

  const explorerContent = explorer.querySelector(".explorer-content") as MaybeHTMLElement
  explorerContent?.setAttribute("aria-expanded", expanded)

  const explorerToggles = explorer.getElementsByClassName(
    "explorer-toggle",
  ) as HTMLCollectionOf<HTMLElement>
  for (const toggle of explorerToggles) {
    toggle.setAttribute("aria-expanded", expanded)
  }
}

function syncMobileExplorerLocks() {
  const quartzBody = document.getElementById("quartz-body")
  let shouldLock = false

  for (const explorer of document.getElementsByClassName(
    "explorer",
  ) as HTMLCollectionOf<HTMLElement>) {
    syncExplorerState(explorer)
    const mobileExplorer = explorer.querySelector(".mobile-explorer")
    if (isMobileExplorerToggle(mobileExplorer) && !explorer.classList.contains("collapsed")) {
      shouldLock = true
    }
  }

  quartzBody?.classList.toggle("lock-scroll", shouldLock)
  document.documentElement.classList.toggle("mobile-no-scroll", shouldLock)
}

function toggleExplorer(this: HTMLElement) {
  const nearestExplorer = this.closest(".explorer") as HTMLElement
  if (!nearestExplorer) return
  nearestExplorer.classList.toggle("collapsed")
  syncMobileExplorerLocks()
}

function toggleFolder(evt: MouseEvent) {
  evt.stopPropagation()
  const target = evt.target as MaybeHTMLElement
  if (!target) return

  // Check if target was svg icon or button
  const isSvg = target.nodeName === "svg"

  // corresponding <ul> element relative to clicked button/folder
  const folderContainer = (
    isSvg
      ? // svg -> div.folder-container
        target.parentElement
      : // button.folder-button -> div -> div.folder-container
        target.parentElement?.parentElement
  ) as MaybeHTMLElement
  if (!folderContainer) return
  const childFolderContainer = folderContainer.nextElementSibling as MaybeHTMLElement
  if (!childFolderContainer) return

  childFolderContainer.classList.toggle("open")

  // Collapse folder container
  const isCollapsed = !childFolderContainer.classList.contains("open")
  setFolderState(childFolderContainer, isCollapsed)

  const currentFolderState = currentExplorerState.find(
    (item) => item.path === folderContainer.dataset.folderpath,
  )
  if (currentFolderState) {
    currentFolderState.collapsed = isCollapsed
  } else {
    currentExplorerState.push({
      path: folderContainer.dataset.folderpath as FullSlug,
      collapsed: isCollapsed,
    })
  }

  const stringifiedFileTree = JSON.stringify(currentExplorerState)
  localStorage.setItem("fileTree", stringifiedFileTree)
}

function createFileNode(currentSlug: FullSlug, node: FileTrieNode): HTMLLIElement {
  const template = document.getElementById("template-file") as HTMLTemplateElement
  const clone = template.content.cloneNode(true) as DocumentFragment
  const li = clone.querySelector("li") as HTMLLIElement
  const a = li.querySelector("a") as HTMLAnchorElement
  a.href = resolveRelative(currentSlug, node.slug)
  a.dataset.for = node.slug
  applyShortLabel(a, node.displayName)

  if (currentSlug === node.slug) {
    a.classList.add("active")
  }

  return li
}

function createFolderNode(
  currentSlug: FullSlug,
  node: FileTrieNode,
  opts: ParsedOptions,
): HTMLLIElement {
  const template = document.getElementById("template-folder") as HTMLTemplateElement
  const clone = template.content.cloneNode(true) as DocumentFragment
  const li = clone.querySelector("li") as HTMLLIElement
  const folderContainer = li.querySelector(".folder-container") as HTMLElement
  const titleContainer = folderContainer.querySelector("div") as HTMLElement
  const folderOuter = li.querySelector(".folder-outer") as HTMLElement
  const ul = folderOuter.querySelector("ul") as HTMLUListElement

  const folderPath = node.slug
  folderContainer.dataset.folderpath = folderPath

  if (currentSlug === folderPath) {
    folderContainer.classList.add("active")
  }

  if (opts.folderClickBehavior === "link") {
    // Replace button with link for link behavior
    const button = titleContainer.querySelector(".folder-button") as HTMLElement
    const a = document.createElement("a")
    a.href = resolveRelative(currentSlug, folderPath)
    a.dataset.for = folderPath
    a.className = "folder-title"
    applyShortLabel(a, node.displayName)
    button.replaceWith(a)
  } else {
    const span = titleContainer.querySelector(".folder-title") as HTMLElement
    applyShortLabel(span, node.displayName)
  }

  // if the saved state is collapsed or the default state is collapsed
  const isCollapsed =
    currentExplorerState.find((item) => item.path === folderPath)?.collapsed ??
    opts.folderDefaultState === "collapsed"

  // if this folder is a prefix of the current path we
  // want to open it anyways
  const simpleFolderPath = simplifySlug(folderPath)
  const folderIsPrefixOfCurrentSlug =
    simpleFolderPath === currentSlug.slice(0, simpleFolderPath.length)

  if (!isCollapsed || folderIsPrefixOfCurrentSlug) {
    folderOuter.classList.add("open")
  }

  for (const child of node.children) {
    const childNode = child.isFolder
      ? createFolderNode(currentSlug, child, opts)
      : createFileNode(currentSlug, child)
    ul.appendChild(childNode)
  }

  return li
}

async function setupExplorer(currentSlug: FullSlug) {
  const allExplorers = document.querySelectorAll("div.explorer") as NodeListOf<HTMLElement>

  for (const explorer of allExplorers) {
    const dataFns = JSON.parse(explorer.dataset.dataFns || "{}")
    const opts: ParsedOptions = {
      folderClickBehavior: (explorer.dataset.behavior || "collapse") as "collapse" | "link",
      folderDefaultState: (explorer.dataset.collapsed || "collapsed") as "collapsed" | "open",
      useSavedState: explorer.dataset.savestate === "true",
      order: dataFns.order || ["filter", "map", "sort"],
      sortFn: new Function("return " + (dataFns.sortFn || "undefined"))(),
      filterFn: new Function("return " + (dataFns.filterFn || "undefined"))(),
      mapFn: new Function("return " + (dataFns.mapFn || "undefined"))(),
    }

    // Get folder state from local storage
    const storageTree = localStorage.getItem("fileTree")
    const serializedExplorerState = storageTree && opts.useSavedState ? JSON.parse(storageTree) : []
    const oldIndex = new Map<string, boolean>(
      serializedExplorerState.map((entry: FolderState) => [entry.path, entry.collapsed]),
    )

    const data = await window.fetchData
    const entries = [...Object.entries(data)] as [FullSlug, ContentDetails][]
    const trie = FileTrieNode.fromEntries(entries)

    // Apply functions in order
    for (const fn of opts.order) {
      switch (fn) {
        case "filter":
          if (opts.filterFn) trie.filter(opts.filterFn)
          break
        case "map":
          if (opts.mapFn) trie.map(opts.mapFn)
          break
        case "sort":
          if (opts.sortFn) trie.sort(opts.sortFn)
          break
      }
    }

    // Get folder paths for state management
    const folderPaths = trie.getFolderPaths()
    currentExplorerState = folderPaths.map((path) => {
      const previousState = oldIndex.get(path)
      return {
        path,
        collapsed:
          previousState === undefined ? opts.folderDefaultState === "collapsed" : previousState,
      }
    })

    const explorerUl = explorer.querySelector(".explorer-ul")
    if (!explorerUl) continue

    // Create and insert new content
    const fragment = document.createDocumentFragment()
    for (const child of trie.children) {
      const node = child.isFolder
        ? createFolderNode(currentSlug, child, opts)
        : createFileNode(currentSlug, child)

      fragment.appendChild(node)
    }
    explorerUl.insertBefore(fragment, explorerUl.firstChild)

    // restore explorer scrollTop position if it exists
    const scrollTop = sessionStorage.getItem("explorerScrollTop")
    if (scrollTop) {
      explorerUl.scrollTop = parseInt(scrollTop)
    } else {
      // try to scroll to the active element if it exists
      const activeElement = explorerUl.querySelector(".active")
      if (activeElement) {
        activeElement.scrollIntoView({ behavior: "smooth" })
      }
    }

    // Set up event handlers
    const explorerButtons = explorer.getElementsByClassName(
      "explorer-toggle",
    ) as HTMLCollectionOf<HTMLElement>
    for (const button of explorerButtons) {
      button.addEventListener("click", toggleExplorer)
      window.addCleanup(() => button.removeEventListener("click", toggleExplorer))
    }

    // Set up folder click handlers
    if (opts.folderClickBehavior === "collapse") {
      const folderButtons = explorer.getElementsByClassName(
        "folder-button",
      ) as HTMLCollectionOf<HTMLElement>
      for (const button of folderButtons) {
        button.addEventListener("click", toggleFolder)
        window.addCleanup(() => button.removeEventListener("click", toggleFolder))
      }
    }

    const folderIcons = explorer.getElementsByClassName(
      "folder-icon",
    ) as HTMLCollectionOf<HTMLElement>
    for (const icon of folderIcons) {
      icon.addEventListener("click", toggleFolder)
      window.addCleanup(() => icon.removeEventListener("click", toggleFolder))
    }

    syncExplorerState(explorer)
  }
}

document.addEventListener("prenav", async () => {
  // save explorer scrollTop position
  const explorer = document.querySelector(".explorer-ul")
  if (!explorer) return
  sessionStorage.setItem("explorerScrollTop", explorer.scrollTop.toString())
})

document.addEventListener("nav", async (e: CustomEventMap["nav"]) => {
  const currentSlug = e.detail.url
  try {
    await setupExplorer(currentSlug)
  } catch (error) {
    console.error("Failed to initialize Quartz explorer", error)
    return
  }

  // if mobile hamburger is visible, collapse by default
  for (const explorer of document.getElementsByClassName("explorer")) {
    const mobileExplorer = explorer.querySelector(".mobile-explorer")
    if (!mobileExplorer) continue

    if (isMobileExplorerToggle(mobileExplorer)) {
      explorer.classList.add("collapsed")
    } else {
      explorer.classList.remove("collapsed")
    }

    mobileExplorer.classList.remove("hide-until-loaded")
  }

  syncMobileExplorerLocks()
})

window.addEventListener("resize", syncMobileExplorerLocks)

function setFolderState(folderElement: HTMLElement, collapsed: boolean) {
  return collapsed ? folderElement.classList.remove("open") : folderElement.classList.add("open")
}
