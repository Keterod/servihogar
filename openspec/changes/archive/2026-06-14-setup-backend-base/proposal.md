## Why

The backend directory has an empty `src/` structure with no running application. Before implementing any domain logic or Supabase integration, a minimal FastAPI base must be wired — following the mandated `main → enrutadores → servicios → repositorio` flow — so that subsequent features can build on a consistent foundation.

## What Changes

- Replace empty `src/main.py` with a working FastAPI app that includes a health-check router
- Create `src/core/config.py` for centralized settings via `pydantic-settings`
- Add `pydantic-settings` to `pyproject.toml` dependencies
- Add `__init__.py` files to all `src/` subpackages (apis, services, repository, schemas, core)
- Create `.env.example` at the backend root with the 4 required variables
- Wire the health router into main and verify `GET /health` responds with `{"status": "ok"}`

## Capabilities

### New Capabilities

- `backend-base`: Provide the foundational FastAPI application shell — directory structure, configuration, health endpoint, and dependency wiring — without any domain logic or Supabase connectivity.

### Modified Capabilities

- *(None — no existing specs are changed)*

## Impact

- **`servihogar-backend/backend/src/main.py`** — rewrite from empty to working FastAPI app
- **`servihogar-backend/backend/src/core/config.py`** — new file with `pydantic-settings` `BaseSettings`
- **`servihogar-backend/backend/src/core/__init__.py`** — new package init
- **`servihogar-backend/backend/src/apis/__init__.py`** — new package init
- **`servihogar-backend/backend/src/apis/health.py`** — new router with `GET /health`
- **`servihogar-backend/backend/src/services/__init__.py`** — new package init
- **`servihogar-backend/backend/src/repository/__init__.py`** — new package init
- **`servihogar-backend/backend/src/schemas/__init__.py`** — new package init
- **`servihogar-backend/backend/pyproject.toml`** — add `pydantic-settings` dependency
- **`servihogar-backend/backend/.env.example`** — new file with 4 env vars
