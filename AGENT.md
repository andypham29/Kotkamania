# AGENT.md

Guide for AI agents working on this repository. Read this before making non-trivial changes.

## What this project is

A tool for tracking NHL hockey stats, calculating fantasy points for players, and ranking them based on performance to support fantasy drafting and roster decisions. Players are scored from raw stats (goals, assists, shots, PP points, hits, blocks, +/-) using configurable weights, then surfaced through ranked lists, filters, and watchlists/draftboards.

## Components

The project has three top-level concerns:

1. **Backend** — Python Flask app served from `app.py` / `wsgi.py`, persisting to a local **SQLite** database (`identifier.sqlite`). Exposes both HTML routes (server-rendered templates) and JSON APIs (e.g. `/api/nhl/fantasy`).
2. **Frontend** — Pure HTML/CSS/JS with **jQuery** and Bootstrap 4.5. No build step, no framework. Templates live in `templates/`, client assets in `static/`.
3. **Scripts** — Standalone scrapers / data-prep utilities under `script/` (e.g. `elite_scrape.py`, `nhldotcome_fantasy_scrape.py`, `prospect_scrape.py`, `yahoo_eligibility_scrape.py`). These populate or refresh data used by the app.

## Backend architecture — hexagonal refactor in progress

The backend is **mid-refactor toward a full hexagonal (ports & adapters) architecture**. The end-state goal is full hexa; the current codebase is mixed.

Layout reflects this transition:

- `domain/` — pure domain layer (the target shape). Contains business models and services that do not depend on Flask, SQLite, or external HTTP.
  - `domain/gamelog/{model,service}/`
  - `domain/nhlplayerstat/{model,...}/`
  - `domain/fantasygrade.py`
- `infra/` — adapters.
  - `infra/rest/` — inbound/REST adapters (sparse so far).
  - `infra/spi/nhlapi/` — outbound adapters calling the public NHL API (gamelog, skater summary, realtime, time-on-ice).
  - `infra/spi/sqlite/` — outbound adapters for SQLite persistence.
- `server/` — **legacy / transitional layer** still using the older facade+service+repository pattern. Modules here (`admin/`, `commons/`, `internaldata/`, `mockdraft/`, `nhlapi/`, `twitterapi/`) are the next candidates to migrate into `domain/` + `infra/`.
- `helper/` — small cross-cutting utilities (e.g. `http_helper.py`).
- `app.py` — Flask entrypoint; wires routes to facades/services from both the new and legacy layers.
- `setting.py` — config (API keys, etc.).

**Guidance for new backend code:** prefer placing new business logic in `domain/` with adapters in `infra/spi/...`. When extending `server/...` code, keep changes minimal and consistent with that module's existing style — but flag opportunities to migrate it.

## Frontend

- `templates/` — Jinja2 templates. Top-level `index.html` is the shell; feature pages are in subfolders:
  - `templates/fantasy/` — fantasy players table, scoring, filters, weights panel.
  - `templates/nhl/` — NHL player / team / stat / lineup pages and modals.
  - `templates/draftcenter/`, `templates/draftsimulator/`, `templates/prospectlist/`, `templates/prospectpage/`, `templates/news/`.
  - `templates/nav.html`, `logo.html`, `logoname.html` — chrome.
- `static/` — JS and CSS.
  - `cookiehandler.js` — generic `getCookie` / `setCookie` helpers.
  - `fantasycookiehandler.js` — fantasy-specific list cookies (favorites, watchlist, draftboard, etc.) on top of `cookiehandler.js`.
  - `chartjshandler.js`, `envvariables.js`, `styles/`.

**Frontend conventions:**
- Plain JS in IIFEs inside the template `<script>` block is the norm — see `templates/fantasy/fantasy_page.html` for the canonical pattern (state object, `renderTable`, `wireEvents`, jQuery `$.ajax` for data).
- Persistent client state goes in cookies via the `fantasycookiehandler.js` helpers; ephemeral UI prefs (e.g. fantasy weights) go in `localStorage`.
- No bundler. Keep dependencies inline or via CDN/`static/`.

## Scripts

`script/` contains data-collection jobs run outside the request cycle:

- `elite_scrape.py`, `nhldotcome_fantasy_scrape.py`, `prospect_scrape.py`, `yahoo_eligibility_scrape.py` — scrapers feeding the SQLite DB or JSON files (`data.json`, `player.json`, `nhl_data.csv`, `espn_data.csv`).
- `script/fantasy/` — fantasy-specific data prep.
- `playground.py` — ad-hoc experimentation; do not rely on it.

These are typically invoked manually or via the admin endpoint (`/admin/script/<offset>` in `app.py`), not on every request.

## Running

- Python deps: `requirements.txt`. Runtime pinned in `runtime.txt`.
- Local dev: `python app.py` (Flask app object is `app` in `app.py`; `wsgi.py` is the production entrypoint via the `Procfile`).
- DB: `identifier.sqlite` in repo root — treat as developer-local data, not source of truth.

## Working principles for agents

- **Respect the hexa direction.** New backend features should land in `domain/` + `infra/`, not in `server/`, unless extending existing legacy code is genuinely simpler for the task at hand.
- **Don't introduce a frontend framework or build step.** Match the existing jQuery + vanilla-JS-in-templates style.
- **Cookies vs localStorage on the frontend:** persistent player-list state → cookies (use `fantasycookiehandler.js`); UI tuning knobs → `localStorage`.
- **Scripts are not request-path code.** Keep heavy scraping/IO out of Flask routes.
- **SQLite is the only datastore.** No migrations framework is in place; schema changes are handled manually.

<!-- Agent behavior: do not read legacy server/ files by default -->
- **Avoid reading or ingesting `server/` when adding code.** The `server/` directory is legacy/transitional and can contain large, tightly-coupled modules. When creating or modifying code, agents should not scan or read files under `server/` by default. Only access or change `server/` files when the user explicitly requests it or when a change must be made to maintain backward compatibility. This reduces accidental edits, speeds up analysis, and keeps agents focused on the preferred `domain/` + `infra/` architecture.

## Machine-readable ignore file

Note: `AGENT.md` is documentation and does not automatically restrict tools or code-search utilities. To make the exclusion policy enforceable by tooling, this repository provides a machine-readable ignore file named `.agentignore` at the repo root. All automated agents and scripts should respect `.agentignore` when enumerating files to read or modify.

Typical entries in `.agentignore` include legacy or large folders that agents should avoid by default (for example `server/`, virtual environments, caches, and large data files). If you are writing an agent or a script, consult `.agentignore` and skip any matching paths unless the user requests otherwise.

