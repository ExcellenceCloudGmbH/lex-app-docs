import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

/**
 * Sidebar order.
 *
 * The docs are arranged in the order you hit things — install, model, compute,
 * track, secure, ship — and alphabetical sorting destroys exactly that. Left
 * to the default, the sections read: access, calculations, history, migrating,
 * model, reference, ship, start-here, using. "Start here" ninth.
 *
 * The whole ranking has to live INSIDE the function. Explorer serialises this
 * with `sortFn.toString()` and re-evaluates it in the browser, so anything it
 * closes over is undefined by the time it runs.
 */
const explorerOptions = {
  sortFn: (a: any, b: any) => {
    const ORDER = [
      // top level
      "start-here", "model-your-data", "calculations", "history-and-audit",
      "access-and-dashboards", "ship-and-operate", "using-the-app",
      "reference", "migrating-from-v1",
      // inside start-here: the tutorial comes after the setup pages, which
      // folders-first sorting would otherwise reverse
      "installation", "project-structure", "running-your-app", "tutorial",
      // inside using-the-app
      "navigation", "the-grid", "record-detail", "themes",
    ]
    const rank = (n: any) => {
      const i = ORDER.indexOf(n.slugSegment)
      return i === -1 ? ORDER.length : i
    }
    const ra = rank(a)
    const rb = rank(b)
    if (ra !== rb) return ra - rb

    // Unranked siblings keep Quartz's own behaviour: folders first, then
    // alphabetical with numeric collation so "Part 2" precedes "Part 10".
    if (a.isFolder !== b.isFolder) return a.isFolder ? -1 : 1
    return a.displayName.localeCompare(b.displayName, undefined, {
      numeric: true,
      sensitivity: "base",
    })
  },
}

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      GitHub: "https://github.com/jackyzha0/quartz",
      "Discord Community": "https://discord.gg/cRFFHYye7t",
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
    Component.Explorer(explorerOptions),
  ],
  right: [
    Component.Graph(),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks(),
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
    Component.Explorer(explorerOptions),
  ],
  right: [],
}
