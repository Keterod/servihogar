## Context

The backend has a working FastAPI shell (main.py, health router, core config, pyproject.toml with fastapi/uvicorn/pydantic-settings). The `src/repository/`, `src/services/`, and `src/schemas/` directories exist as empty Python packages. Supabase has been provisioned with the schema from `database/schema.sql` and seed data from `database/seed.sql`.

## Goals / Non-Goals

**Goals:**
- Install the `supabase` Python client
- Create a centralized Supabase client singleton at `src/repository/supabase_client.py`
- Build three read-only repositories (categorias, zonas, tecnicos)
- Build three corresponding services that delegate to repositories
- Create Pydantic response schemas for each entity
- Expose three public GET endpoints via `APIRouter` in `src/apis/`
- Wire all routers into `src/main.py`
- Verify `/health` still responds and new endpoints return Supabase data

**Non-Goals:**
- No write endpoints (create, update, delete)
- No authentication or authorization
- No connection pooling configuration beyond defaults
- No frontend changes
- No database schema changes

## Decisions

1. **Official `supabase` PyPI package** — Use `supabase>=2.0.0`. This is the maintained Python client that wraps `postgrest` and provides typed access to Supabase REST APIs.

2. **Client singleton with lazy initialization** — `supabase_client.py` creates a single `create_client(url, key)` instance and reuses it. This prevents multiple connections and keeps config centralized.

3. **Service layer even though endpoints are read-only** — The AGENTS.md mandates `main → apis → services → repository`. Every endpoint must go through a service, even for simple pass-through queries. This keeps the architecture consistent for future write operations.

4. **POST /rpc for tecnico data** — The `tecnicos` endpoint needs to join `tecnicos` + `usuarios` + `tecnico_categorias` + `tecnico_zonas`. Supabase Python client can do chained queries, but for multi-table joins a stored procedure or raw SQL via `rpc()` may be cleaner. Decision: use the Supabase client's `.select()` with a `foreignKey` join where possible, or fall back to multiple queries assembled in the service layer.

## Risks / Trade-offs

- **[Medium] Supabase credentials not configured** — Mitigation: The app will start without a `.env` file but endpoints will raise an HTTP 503 or connection error. The `.env.example` documents required vars.
- **[Low] Supabase client API changes** — Mitigation: Pin `supabase>=2.0.0,<3` in pyproject.toml.
- **[Low] Service layer is a pass-through for now** — Trade-off accepted for architectural consistency. Will be valuable when write logic, validation, and permissions are added later.
