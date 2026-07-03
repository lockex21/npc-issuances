import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "NPC Issuance Wiki",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "en-US",
    ignorePatterns: ["private", ".obsidian"],
    defaultDateType: "published",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Libre Franklin",
        body: "Newsreader",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#f4efe7",
          lightgray: "#dbd1c3",
          gray: "#9f9486",
          darkgray: "#59544c",
          dark: "#1f2328",
          secondary: "#0c5c56",
          tertiary: "#6f8f7e",
          highlight: "rgba(12, 92, 86, 0.14)",
          textHighlight: "#f4e29d",
        },
        darkMode: {
          light: "#161918",
          lightgray: "#33403a",
          gray: "#7a8b81",
          darkgray: "#d8d4cb",
          dark: "#f6f2ea",
          secondary: "#7cc7bc",
          tertiary: "#a0c0a9",
          highlight: "rgba(124, 199, 188, 0.16)",
          textHighlight: "#7a6b1a88",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: false,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
