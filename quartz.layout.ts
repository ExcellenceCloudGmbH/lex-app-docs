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
 * ── Two rules this function must obey ────────────────────────────────────
 *
 * Explorer serialises this with `sortFn.toString()` into a data attribute and
 * the client runs `new Function("return " + str)()`. That evaluates in global
 * scope, so the body must reference NOTHING outside itself.
 *
 *   1. No closure over outer variables. Hence ORDER declared inside.
 *   2. **No inner function declarations, not even an arrow assigned to a
 *      const.** This is the one that actually broke the sidebar. esbuild runs
 *      with --keep-names, which rewrites `const rank = (n) => …` into
 *      `const rank = __name((n) => …, "rank")`. `__name` is a bundle-scope
 *      helper that does not exist where the string is evaluated, so the first
 *      comparison threw ReferenceError, `trie.sort()` died and the Explorer
 *      rendered empty. Verified against esbuild directly: a body with an
 *      inner arrow emits `__name` inside it; a body without one does not.
 *
 * So: straight-line code only. It is repetitive on purpose.
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
    const ia = ORDER.indexOf(a.slugSegment)
    const ib = ORDER.indexOf(b.slugSegment)
    const ra = ia === -1 ? ORDER.length : ia
    const rb = ib === -1 ? ORDER.length : ib
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
