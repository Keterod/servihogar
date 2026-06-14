# AGENTS.md — ServiHogar

## Monorepo layout

| Path                          | Purpose                                                            |
| ----------------------------- | ------------------------------------------------------------------ |
| `servihogar-frontend/`        | Angular 21 app (standalone components, Signals, Bootstrap via CDN) |
| `servihogar-backend/backend/` | FastAPI backend (Python 3.13, uv, Pydantic, Supabase-only, no ORM) |
| `database/`                   | Supabase schema (cloud PostgreSQL, no local DB needed)             |
| `openspec/`                   | Spec-driven dev workflow (OpenSpec)                                |
| `prototipos/`                 | UI mockup images                                                   |
| `docs/`                       | Report and evidence                                                |

## Dev commands

```bash
# Frontend (from servihogar-frontend/)
npm install               # deps locked via package-lock.json
ng serve                  # default :4200 (conflict)
ng serve --port 4300      # use this if port 4200 occupied
npm start                 # same as ng serve
npm run build             # production build
npm test                  # runs vitest (NOT Karma/Jasmine)
npx prettier --check src  # format check (singleQuote, printWidth 100)

# Backend (from servihogar-backend/backend/)
uv sync                   # install deps from uv.lock (Python 3.13)
uvicorn src.main:app      # run dev server (when main.py wired)
```

## Critical constraints

- **Frontend is a prototype** — all data is mocked in-memory via Signals. No real backend or Supabase connection. Do NOT wire real auth/API unless the task explicitly asks.
- **No ORM in backend** — access Supabase through the Supabase client/repository layer. Do not use local Postgres.
- **Bootstrap via CDN only** — never install it via npm or configure in `angular.json`.
- **Angular standalone components** — no NgModules. Lazy loading required via `loadComponent`.
- **Signals** for state. Pattern: `signal()` + `computed()`, `update()`/`set()`, never `mutate()`.

## Sub-package instruction files

- `servihogar-frontend/AGENTS.md` — Angular/TypeScript/Bootstrap/Signal coding rules
- `servihogar-backend/backend/AGENTS.md` — FastAPI layers, Supabase, env vars, security rules

Both override the root file for their domain. Read the relevant one before working in each package.

## OpenSpec workflow

Commands available via OpenCode or Cursor: `/opsx-propose`, `/opsx-apply`, `/opsx-explore`, `/opsx-archive`.
Changes live in `openspec/changes/<name>/`. Spec-driven development: proposal → design → tasks → implement → archive.

## Git

Branches: `main` (stable), `feature/<name>` for new work.

## Known quirks

- `test` target uses Vitest (configured in `angular.json`, not Karma)
  Backend entrypoint should be `src/main.py`. Any root-level `main.py` is only a placeholder and should not contain application logic.
- No `.env.example` exists yet despite being listed as expected in backend AGENTS.md

Para cambios de base de datos, revisar primero `database/README.md`, `database/schema.sql` y `database/seed.sql`.
