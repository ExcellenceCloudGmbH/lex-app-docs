---
title: "Custom frontend"
---

A hosted instance serves the standard interface — the process admin client — from its own pod (see [[ship-and-operate/deploying#The interface|Deploying → The interface]]). That pod can serve **your own frontend** instead: any [Vite](https://vite.dev) app, in a GitHub repository of its own, installed with npm, yarn or bun.

Your frontend takes the standard interface's place exactly. It is served on the instance's own host, so it talks to the lex-app backend on the same origin, with the same session, the same CSRF protection and the same websockets — nothing in the backend needs configuring for it.

| Page section | Answers |
|---|---|
| [What the repository needs](#what-the-repository-needs) | Which apps can be deployed this way |
| [Setting it up in the Instance Controller](#setting-it-up-in-the-instance-controller) | Turning the repository into a frontend project, building it, putting it on an instance |
| [Build secrets](#build-secrets) | Private registries and other tokens the build needs |
| [What your app is given at runtime](#what-your-app-is-given-at-runtime) | `window.__LEX_ENV__`, and the keys in it |
| [Talking to lex-app](#talking-to-lex-app) | Signing in, the REST API, websockets |
| [Releases and compliance](#releases-and-compliance) | How a frontend reaches production |

## What the repository needs

- **A Vite app.** `vite` must be a dependency of the app's `package.json`; the build refuses anything else.
- **A lockfile for the package manager you choose**: `package-lock.json` (or `npm-shrinkwrap.json`) for npm, `yarn.lock` for yarn, `bun.lock` (or `bun.lockb`) for bun. Dependencies are installed from it exactly — `npm ci`, `yarn install --frozen-lockfile` (yarn 1) or `--immutable` (yarn 2+), `bun install --frozen-lockfile` — so a lockfile that is out of date fails the build rather than drifting.
- **A `build` script**, unless you give the build command yourself. `tsc -b && vite build` is fine.
- **`base: '/'`** (Vite's default). The app is served from the root of the instance's host.
- **A single-page app.** Any path that is not a file is answered with `index.html`, so client-side routing works on reload. There is no server-side rendering.

A monorepo is fine: the lockfile can sit in one directory (where dependencies are installed) and the app in another (where it is built). If `package.json` names a `packageManager`, it must be the one you chose; its version is used.

## Setting it up in the Instance Controller

1. **Install the GitHub App on the repository** the way you would for a lex-app project. It appears under *Projects* like any other repository.
2. **Make it a frontend project.** In the project's actions, choose *Use as frontend project*. This is only possible while the project has never had instances and none of its workflows (other than the default build) have run — a frontend project cannot host instances, and a lex-app project cannot be served as a frontend.
3. **Fill in the build settings** (*Build settings* tab): package manager, Node version (default 24), the directories, and optionally the install command, build command (default `<package manager> run build`), output directory (default `dist`) and build variables.
4. **Build it.** The project's *Build Frontend Image* workflow, or any workflow of yours with a build step — on push, for example — builds a commit into an image. Builds are listed per commit, as for lex-app projects.
5. **Bind an instance to it.** In the instance's configuration, under *Frontend*, choose the frontend project. Binding needs permission to *use* the frontend project, and only test and production instances can be bound.
6. **Release a commit onto it** — from the instance page, or with a release step in one of the frontend project's workflows. The instance serves that commit from then on.

You can switch an instance back to the standard interface at any time; the binding and the commit it last served are kept, so switching back again is one click. Unbinding forgets both.

> [!important] Binding is trust
> Once an instance is bound, people who can run the frontend project's workflows can release frontends onto it. A frontend runs on the instance's own origin, with its users' session, so treat binding like granting release rights. Only an admin of an instance can make it a release target of a frontend workflow.

Build variables and runtime settings are **public**. Anything a Vite build reads ends up in the bundle every visitor downloads, and runtime settings are published to the browser — never put a secret in either. Secrets the build itself needs go in [build secrets](#build-secrets).

## Build secrets

Some builds need a secret: a token for a private npm registry, a Sentry auth token to upload source maps, a licence key. Add them under *Build settings → Secrets*. A secret's value is stored in Secret Manager; it can be replaced or deleted, never read back.

Each secret is exposed in one of two ways, to the install step, the build step or both:

| Kind | What the build sees | Typical use |
|---|---|---|
| **Environment variable** | A variable named like the secret | `NPM_TOKEN` read by a committed `.npmrc` (`//npm.pkg.github.com/:_authToken=${NPM_TOKEN}`), `SENTRY_AUTH_TOKEN` |
| **File** | The value as a file at a path you choose: relative to the repository root, or `~/…` for the build user's home | `.npmrc`, `~/.npmrc`, `.yarnrc.yml`, `bunfig.toml` |

A file secret replaces any file of the same name for the duration of the step and is removed — or the original restored — before the step ends, so it is not left in the image. A secret never appears in the workflow's inputs, and its lines are masked in the build log.

> [!warning] Not `VITE_`
> Vite compiles every `VITE_` variable it sees into the public bundle, so a secret with that prefix would be published. The Instance Controller refuses to store one.

## What your app is given at runtime

One image is built per commit and served by every instance it is released onto, so the instance-specific values cannot be compiled in. They are published when the pod starts, as a script the build adds to the `<head>` of every page:

```html
<script src="/lex-env.js"></script>
```

which defines `window.__LEX_ENV__` before your app's own scripts run. It is never cached.

| Key | Value |
|---|---|
| `API_BASE_PATH` | `/api/` — the backend, on the same origin |
| `WS_BASE_PATH` | `/api/ws/` — the backend's websockets |
| `INSTANCE_URL` | The instance's canonical URL (informational: build URLs from `location`, the instance can be reached on more than one host) |
| `INSTANCE_ID`, `INSTANCE_NAME` | Which instance this is |
| `KEYCLOAK_URL`, `KEYCLOAK_REALM`, `KEYCLOAK_CLIENT_ID` | The instance's identity provider and public client |
| `STORAGE_TYPE` | The instance's file storage |
| `DOMAIN_BASE` | The platform's base domain |
| `GRAFANA_DASHBOARD_URL` | The instance's monitoring dashboard |
| `STREAMLIT_URL`, `REFLEX_URL` | The instance's dashboards, or an empty string when they are off |
| `FRONTEND_VERSION`, `BACKEND_VERSION` | The commits the instance's frontend and backend run |
| *your own keys* | The instance's runtime settings (configuration → *Frontend*): upper-case names, up to 50 of them |

A small helper keeps the rest of the app independent of where the values come from, and lets `vite dev` fall back to `.env` files (`VITE_LEX_API_BASE_PATH=...`):

```ts
// src/lexEnv.ts
declare global {
  interface Window {
    __LEX_ENV__?: Readonly<Record<string, string>>
  }
}

export function lexEnv(key: string, fallback = ''): string {
  return window.__LEX_ENV__?.[key] ?? import.meta.env[`VITE_LEX_${key}`] ?? fallback
}
```

## Talking to lex-app

Your app is on the backend's own origin, so it uses lex-app exactly as the standard interface does:

- **REST** is under `/api/api/<route>` — the first `/api/` is the instance's backend, the second lex-app's own API prefix. `GET /api/api/user/` returns the signed-in user.
- **Signing in** is lex-app's: when a call answers 401 or 403, send the browser to `/api/oidc/authenticate?next=<where to come back to>`. Signing out is `/api/oidc/total_logout?next=<url>&fail=<url>`.
- **Requests** go with `credentials: 'include'`, and anything that changes data sends the `csrftoken` cookie's value as the `X-CSRFToken` header.
- **Websockets** connect to `wss://${location.host}/api/ws/<route>` (for example `calculations`), with the session cookie.

```ts
const api = (route: string) => new URL(`api/${route}`, new URL(lexEnv('API_BASE_PATH', '/api/'), location.origin))

export async function lexFetch(route: string, init: RequestInit = {}) {
  const csrf = document.cookie.match(/(?:^|; )csrftoken=([^;]*)/)?.[1]
  const response = await fetch(api(route), {
    ...init,
    credentials: 'include',
    headers: { ...(init.headers ?? {}), ...(csrf ? { 'X-CSRFToken': decodeURIComponent(csrf) } : {}) },
  })
  if (response.status === 401 || response.status === 403) {
    location.href = `${lexEnv('API_BASE_PATH', '/api/')}oidc/authenticate?next=${encodeURIComponent(location.href)}`
  }
  return response
}
```

Files under `/assets/` — Vite's content-hashed output — are cached for a year; everything else, `index.html` included, is not cached, so a release is picked up on the next page load.

## Releases and compliance

A frontend release is a release: it is recorded in the instance's release history (as a *frontend* release, with the frontend repository and commit), and on a project with a compliance framework it follows the same rules as a backend release.

- A **production** instance of such a project cannot be released to directly. The frontend project has its own *Compliance Frontend Release* workflow: it builds, releases to a test instance, waits for a second admin's approval, and only then releases to production. The test and production instances of one run must belong to the same lex-app project.
- If the instance's project restricts releases to named branches, the frontend repository has to name its own in its `lex_compliance.yaml` (`release_branches: [main]`); until it does, production releases of the frontend are refused.
- Creating an instance with a frontend already on it is recorded, as for the backend, but not blocked.

## Related

- [[ship-and-operate/deploying|Deploying]] — the pods an installation runs
- [[ship-and-operate/upgrading|Upgrading]] — the interface and the backend move independently
