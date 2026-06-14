## Context

The backend at `servihogar-backend/backend/src/` has the correct subdirectory layout (apis/, services/, repository/, schemas/) but all are empty. `src/main.py` is an empty file. `pyproject.toml` lists `fastapi` and `uvicorn` but not `pydantic-settings`. No `.env.example` exists. The `src/core/` directory has not been created. No `__init__.py` files exist, so Python package resolution will fail.

The AGENTS.md specifies a strict architectural flow (`main → enrutadores → servicios → repositorio`), centralized config via `pydantic-settings`, and a `.env.example` with 4 specific variables.

## Goals / Non-Goals

**Goals:**
- Make `src/` a working Python application package with `__init__.py` files
- Create `src/core/config.py` with `pydantic-settings` `BaseSettings`
- Wire `GET /health` via an `APIRouter` in `src/apis/health.py`
- Add `pydantic-settings` dependency to `pyproject.toml`
- Create `.env.example` at the backend root
- Verify the app starts and `/health` returns `{"status": "ok"}`

**Non-Goals:**
- No Supabase client initialization or connection
- No authentication or user management
- No domain endpoints (usuarios, solicitudes, etc.)
- No database schema changes
- No frontend modifications
- No test suite setup

## Decisions

1. **`pydantic-settings` over `python-dotenv`** — `pydantic-settings` is the modern FastAPI-aligned approach. It integrates with Pydantic v2 natively and supports `.env` file loading, type casting, and validation. `python-dotenv` would require manual parsing.

2. **Single health router in `apis/health.py`** — Follows the `APIRouter` pattern mandated by AGENTS.md. The health endpoint has no dependencies on services or repository layers (by design — it's a connectivity check).

3. **`__init__.py` files export key symbols** — Each package init either stays empty (for namespace packages) or exports the primary class/function. This follows standard Python packaging and enables clean imports like `from src.core.config import settings`.

4. **Core config reads from `.env` automatically** — `pydantic-settings` `SettingsConfigDict(env_file=".env")` loads the file from the backend root. No manual dotenv loading needed.

## Risks / Trade-offs

- **[Low] `.env` not present at first run** — Mitigation: `SettingsConfigDict` will raise a clear error. The `.env.example` provides a template, and `ENVIRONMENT` defaults to `"development"` in code to avoid hard failures.
- **[Low] ModuleNotFoundError if Python path is wrong** — Mitigation: Run `uvicorn src.main:app` from the `backend/` directory. This is documented in the project README and AGENTS.md.
