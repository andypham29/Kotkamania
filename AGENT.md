# AGENT.md

Guide for AI agents working on this repository. Read this before making non-trivial changes.

## What this project is

A **Python monolith** for tracking NHL hockey stats, calculating fantasy points, and ranking players to support fantasy drafting and roster decisions. Players are scored from raw stats (goals, assists, shots, PP points, hits, blocks, +/-) using configurable weights, then surfaced through ranked lists, filters, and watchlists/draftboards.

**Stack**

| Layer | Technology |
|-------|------------|
| Backend | Python **Flask** (`app.py`, `wsgi.py`), local **SQLite** (`identifier.sqlite`) |
| Frontend | **HTML**, **JavaScript**, **CSS**, **Bootstrap 4.5**, **jQuery** — no build step, no SPA framework |
| Data jobs | Standalone scripts under `script/` (scrapers, fantasy prep) |

Templates live in `templates/`; static assets in `static/`. Flask serves server-rendered pages and JSON APIs (e.g. `/api/nhl/fantasy`, `/api/nhl/fantasyV2`).

## Architecture — hexagonal (ports & adapters)

This codebase follows **hexagonal architecture**. Treat that as the source of truth for where code belongs and how dependencies flow.

```mermaid
flowchart TB
  subgraph inbound["Inbound (HTTP)"]
    APP["app.py — Flask routes"]
  end
  subgraph core["Application core"]
    APP_LAYER["application/ — services & models (user-provided)"]
    DOM["domain/ — facades & services"]
  end
  subgraph outbound["Outbound adapters"]
    SPI["infra/spi/ — granular SPI modules"]
  end
  FE["templates/ + static/ — browser UI"]
  LEG["server/ — legacy (frozen)"]

  FE --> APP
  APP --> DOM
  APP --> APP_LAYER
  APP -.->|"existing routes only"| LEG
  DOM --> SPI
  APP_LAYER --> SPI
  SPI --> NHL["NHL API"]
  SPI --> DB["SQLite"]
  SPI --> SCR["Scrapers / files"]
```

**Dependency rule:** `domain/` must not import Flask, `app.py`, or `server/`. Domain code orchestrates use cases and may depend on `infra/spi/` adapters (and small shared helpers like `helper/`). `app.py` is the **composition root**: it wires HTTP to domain facades/services and returns JSON or rendered templates.

### `domain/` — facades for the UI

**Always implement business logic in `domain/` first.** Start with a facade or service class that **aggregates ports** (SPI adapters from `infra/spi/`) and **exposes domain-specific dataclasses** — not raw API/DB shapes. Wire HTTP in `app.py` only after that type exists.

The domain layer exposes **facades and services** that `app.py` calls. These types shape what the frontend receives (aggregated player stats, fantasy lists, gamelogs, grades, etc.) without knowing about HTTP or SQLite details.

Current modules (grow by feature, not by copy-pasting legacy `server/` patterns):

| Path | Role |
|------|------|
| `domain/fantasyplayer/` | Fantasy player queries and models |
| `domain/fantasygrade/` | Forward/defense grading; `fantasy_grader_facade.py` |
| `domain/gamelog/` | Player game logs |
| `domain/playerstat/` | Combined NHL skater stats; `nhl_player_stat_facade.py` |
| `domain/playerstatpercentile/` | Percentile calculations |
| `domain/nhlteam/` | Team-related domain (when used) |

**New features:** add or extend a facade/service under `domain/`, then register a route or API handler in `app.py` that calls it. Prefer facades when a use case composes multiple SPI calls (see `domain/playerstat/nhl_player_stat_facade.py`).

### `application/` — business services (user may supply)

`application/` holds **use-case services and domain models** the user defines. A service typically depends on a repository port (often left as `None` until the SPI exists) and works with plain `@dataclass` types — not DB/API shapes.

| Path | Role |
|------|------|
| `application/goaliestats/` | Goalie season stats; `GoalieStatService`, `GoalieStat` |

**When the user provides an `application/` service:** implement the **outbound SPI** under `infra/spi/` yourself. Do not put persistence or HTTP in `application/`. Wire the repository in the service constructor (or from `app.py` as composition root) once the SPI exists.

Example: `application/goaliestats/GoalieStatService` calls `save` / `find_all` / `find_by_player_id` on a repository → you implement a **SQLite** repository at `infra/spi/sqlite/goaliestat/` and add the table ORM class to `infra/spi/sqlite/models.py`. The user will state the SPI technology explicitly (e.g. `sqlite`, `nhlapi`); use that folder under `infra/spi/`.

### `infra/spi/` — many small outbound adapters

**SPI** (service provider interface) adapters live under `infra/spi/`. Keep them **granular**: one adapter (or small folder) per external concern — a single NHL endpoint family, one repository table, one scrape source, etc. Do not fold unrelated I/O into one large “god” adapter.

| Path | Role |
|------|------|
| `infra/spi/nhlapi/` | Public NHL API (gamelog, team, roster; `nhlskater/` for summary, realtime, TOI, puck possession, shot attempt count) |
| `infra/spi/sqlite/models.py` | Shared SQLite engine, `Session`, and **all** SQLAlchemy ORM table classes (`GoalieStatORM`, `InternalPlayerStatORM`, …) |
| `infra/spi/sqlite/<feature>/` | Per-feature repositories only (`fantasyplayer/`, `playerstat/`, `goaliestat/`, …) |
| `infra/spi/hockeyreference/` | Hockey Reference scrape adapters |
| `infra/rest/` | Optional inbound REST adapters (sparse today; most HTTP stays in `app.py`) |

Domain and `application/` services inject or construct SPI types as needed. Repositories map between persistence/API shapes and application/domain dataclasses; business rules stay in `application/` or `domain/`.

### `infra/spi/sqlite/models.py` — SQLite ORM tables

**All new SQLite ORM table classes go in `infra/spi/sqlite/models.py`.** That file owns the engine, `Base`, `Session`, and `create_all`. Do **not** add per-feature `model/*_orm.py` files or duplicate `db.py` engines for new tables.

| Rule | Detail |
|------|--------|
| Class name | `{ApplicationModel}ORM` (e.g. `GoalieStat` → `GoalieStatORM`) |
| Table name | `internal_<feature>` snake_case (e.g. `internal_goalie_stat`) |
| Columns | Same field names as the application/domain dataclass unless the user specifies otherwise |
| Repository | Lives under `infra/spi/sqlite/<feature>/`; imports `GoalieStatORM` and `Session` from `infra.spi.sqlite.models` |

Repositories map ORM rows ↔ application/domain dataclasses on read/write. Conversion helpers (`from_application`, `to_application`) belong on the repository or as small private methods — not as separate ORM dataclass files.

### Implementing SPI from an `application/` service

Use this workflow when the user hands you a service under `application/` (with or without a stub repository) and asks for an SPI.

1. **Read the application model and service** — method names, parameters, and return types define the repository contract (e.g. `GoalieStat`, `save`, `find_all`, `find_by_player_id`).
2. **Use the SPI technology the user names** — e.g. `sqlite` → `infra/spi/sqlite/<feature>/`, `nhlapi` → `infra/spi/nhlapi/...`. If they do not name one, ask; do not guess for new work.
3. **SPI persistence model** — unless the user specifies a different field set, the SQLite ORM class uses the **same field names and types** as the `application/` model.
4. **ORM suffix** — add a SQLAlchemy mapped class named **`{ApplicationModel}ORM`** to **`infra/spi/sqlite/models.py`** (e.g. `GoalieStat` → `GoalieStatORM`). Do not create a separate ORM file under the feature folder.
5. **Repository** — implement the port the service expects under `infra/spi/sqlite/<feature>/`; map `GoalieStatORM` rows ↔ `GoalieStat` on read/write. Mirror existing SQLite repos (`infra/spi/sqlite/playerstat/nhl_player_stat_repository.py`): session handling, upsert, filter by `playerId` / `seasonId` when present.
6. **Wire the service** — set `self.<repository> = ...` in `GoalieStatService.__init__` (default to the new repository class) unless the user wants composition only in `app.py`.

| Layer | Type | Example |
|-------|------|---------|
| `application/.../model/` | Application dataclass | `GoalieStat` |
| `infra/spi/sqlite/models.py` | SQLAlchemy ORM table class | `GoalieStatORM` |
| `infra/spi/sqlite/<feature>/` | Repository | `GoalieStatRepository` |

**Goalie stats reference (expected layout when user asks for SQLite SPI):**

- Service: `application/goaliestats/goalie_stat_service.py` — `GoalieStatService`
- Application model: `application/goaliestats/model/goalie_stat.py` — `GoalieStat`
- ORM table: `infra/spi/sqlite/models.py` — `GoalieStatORM` (`internal_goalie_stat`)
- Repository: `infra/spi/sqlite/goaliestat/goalie_stat_repository.py` — `GoalieStatRepository`

### `server/` — legacy (do not modify)

`server/` is the **legacy** layer from an older facade + service + repository layout (`admin/`, `commons/`, `internaldata/`, `mockdraft/`, `nhlapi/`, `twitterapi/`). It remains wired in `app.py` for some routes until migrated.

**Policy for agents:**

- **Do not modify any file under `server/`.** No edits, refactors, or “small fixes” there unless the user **explicitly** asks to change legacy code.
- **Do not read or search `server/` by default** when implementing new behavior — use `domain/` + `infra/spi/` instead. Only open `server/` when the user names it or you must understand an existing route you are not allowed to change yet.
- **Do not add new dependencies on `server/`** from new domain or infra code. New work migrates *away* from `server/`, not deeper into it.

`app.py` may still import legacy facades for backward compatibility; over time, routes should switch to `domain/` entry points only.

### Other backend paths

- `helper/` — cross-cutting utilities (e.g. `http_helper.py`).
- `setting.py` — configuration (API keys, etc.).
- `script/` — offline scrapers and data prep (not on the request hot path).

## Frontend

- `templates/` — Jinja2. `index.html` is the shell; feature pages in subfolders:
  - `templates/fantasy/` — fantasy table, scoring, filters, weights
  - `templates/nhl/` — player, team, stat, lineup pages
  - `templates/draftcenter/`, `draftsimulator/`, `prospectlist/`, `prospectpage/`, `news/`
  - `nav.html`, `logo.html`, `logoname.html` — chrome
- `static/` — `cookiehandler.js`, `fantasycookiehandler.js`, `chartjshandler.js`, `envvariables.js`, `styles/`

**Conventions**

- Plain JS in IIFEs inside template `<script>` blocks — see `templates/fantasy/fantasy_page.html` (state object, `renderTable`, `wireEvents`, jQuery `$.ajax`).
- Persistent list state → cookies via `fantasycookiehandler.js`; UI prefs (e.g. weights) → `localStorage`.
- No bundler, no React/Vue. CDN + `static/` only.

## Scripts

`script/` — jobs outside the request cycle (`elite_scrape.py`, `nhldotcome_fantasy_scrape.py`, `prospect_scrape.py`, `yahoo_eligibility_scrape.py`, `script/fantasy/`). Often triggered manually or via `/admin/script/<offset>` in `app.py`. Keep heavy I/O out of Flask route handlers.

## Running

- Dependencies: `requirements.txt`; runtime: `runtime.txt`
- Local: `python app.py` (`app` in `app.py`; production: `wsgi.py` / `Procfile`)
- DB: `identifier.sqlite` at repo root — developer-local; no migration framework (schema changes are manual)

## Working principles for agents

1. **Domain or application first.** New behavior starts in `domain/` or `application/` (user may supply the latter). Aggregate ports, return application/domain dataclasses; then add SPI adapters under `infra/spi/<technology>/`; last, expose via `app.py`.
2. **`server/` is frozen.** No modifications unless the user explicitly requests legacy changes.
3. **Facades face the frontend.** What pages and APIs need should be composed in `domain/` facades/services; `app.py` stays thin (parse request, call domain, `makeHttpResponse` / `render_template`).
4. **Granular SPIs.** Split new adapters by data source or API surface; mirror existing folder naming (`infra/spi/nhlapi/nhlskater/`, `infra/spi/sqlite/fantasyplayer/`).
5. **Monolith frontend rules.** jQuery + vanilla JS in templates; Bootstrap 4.5; no frontend framework or build pipeline.
6. **Cookies vs localStorage.** Player lists → cookies; tuning knobs → `localStorage`.
7. **SQLite only** for app persistence in new code paths unless the user specifies otherwise.
8. **SPI from application.** If the user gives you an `application/` service, implement the matching SPI in `infra/spi/` using the technology they specify; default SPI fields to match the application model; for SQLite, add the ORM table class to **`infra/spi/sqlite/models.py`** with an **`ORM`** suffix.

## Adding a direct NHL API adapter (`infra/spi/nhlapi/`)

Use when the user provides an NHL API URL and wants a new SPI service + model. Adapters call the public NHL API only; domain facades compose them later.

### Folder placement

| API pattern | Location |
|-------------|----------|
| `api.nhle.com/stats/rest/en/skater/...` | `infra/spi/nhlapi/nhlskater/` + `nhlskater/model/` |
| `api.nhle.com/stats/rest/en/goalie/...` | `infra/spi/nhlapi/nhlskater/` (or `nhlgoalie/` if many endpoints) |
| `api.nhle.com/stats/rest/en/team` | `infra/spi/nhlapi/` (e.g. `nhl_team_service.py`) |
| `api-web.nhle.com/v1/...` | `infra/spi/nhlapi/` (e.g. `nhl_gamelog_service.py`) |

### Naming

| Artifact | Pattern | Example |
|----------|---------|---------|
| Model file | `nhl_<entity>_<feature>.py` | `nhl_skater_puckpossession.py` |
| Model class | `Skater<Feature>` | `SkaterPuckPossession` |
| Service file | `nhl_<entity>_<feature>_service.py` | `nhl_skater_puckpossession_service.py` |
| Service class | `NHL<Feature>Service` | `NHLSkaterPuckPossessionService` |
| Field set | `_<FEATURE>_FIELDS` from `dataclasses.fields` | `_PUCKPOSSESSION_FIELDS` |
| Mapper | **`__to_model(self, row: dict)`** on new services | Filters JSON keys to dataclass fields |

Older services may use `__to_summary`, `__to_timeonice`, etc.; new adapters use `__to_model` only.

### Checklist

1. Get the canonical URL from the user (including `sort`, `cayenneExp`, `gameTypeId`, `seasonId` if present).
2. Smoke-test: stats REST returns `{"data": [ {...}, ... ], "total": N }`.
3. Create `model/nhl_*.py`: `@dataclass`, one `Optional` field per API key (names must match JSON camelCase exactly).
4. Create `*_service.py`: copy paging methods from `nhl_skater_timeonice_service.py`, swap path segment and `sort`, use `HttpHelper.get(url)["data"]`, map with `__to_model`.
5. Add `if __name__ == '__main__':` to print `players[0].__dict__` via `json.dumps`.
6. Wire `domain/` only when the user asks.

### `__to_model` pattern

```python
_FIELDS = {f.name for f in fields(SkaterYourFeature)}

def __to_model(self, row: dict) -> SkaterYourFeature:
    return SkaterYourFeature(**{k: v for k, v in row.items() if k in _FIELDS})
```

### Stats REST defaults

- `start` / `limit` as strings in the URL.
- `seasonId`: default `NhlYearConverter.get_current_season()`; cayenne `seasonId<={id} and seasonId>={id}`.
- `gameTypeId=2` for regular season unless specified otherwise.
- Team filter: `franchiseId={id}` in `cayenneExp`.

### Reference implementation

- Puck possession: `nhl_skater_puckpossession_service.py` → API path `puckPossessions`, sort `satPct`
- Shot attempt count: `nhl_skater_shotattemptcount_service.py` → API path `summaryshooting`, sort `satFor`

## Machine-readable ignore file

`AGENT.md` does not enforce tool behavior by itself. Respect **`.agentignore`** at the repo root when enumerating files to read or modify. It includes `server/`, virtualenvs, caches, and large data files. Skip ignored paths unless the user says otherwise.
