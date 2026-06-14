## Why

The backend currently has a working FastAPI shell (`/health`) but no data connectivity. The next step is to connect to Supabase and expose public read endpoints for the foundational lookup data — categorías, zonas, and técnicos — so the frontend can begin consuming real data instead of hardcoded mocks.

## What Changes

- Add `supabase` Python client to `pyproject.toml` dependencies
- Create `src/repository/supabase_client.py` with a centralized Supabase client using credentials from `Settings`
- Create repository classes in `src/repository/` for read-only queries on `categorias_servicio`, `zonas`, and `tecnicos`
- Create service classes in `src/services/` that delegate from repositories (following the `main → apis → services → repository` flow)
- Create Pydantic response schemas in `src/schemas/` for each entity
- Create three FastAPI routers in `src/apis/` with public GET endpoints:
  - `GET /categorias`
  - `GET /zonas`
  - `GET /tecnicos`
- Wire new routers into `src/main.py`
- Verify `/health` still works and new endpoints respond with Supabase data

## Capabilities

### New Capabilities

- `supabase-connection`: Centralized Supabase client initialization and read-only repository layer for accessing `categorias_servicio`, `zonas`, and `tecnicos` tables.

### Modified Capabilities

- *(None — no existing specs are changed)*

## Impact

- **`pyproject.toml`** — add `supabase` dependency
- **`src/repository/supabase_client.py`** — new file: centralized Supabase client singleton
- **`src/repository/categorias_repository.py`** — new file: read-only repository for categorias_servicio
- **`src/repository/zonas_repository.py`** — new file: read-only repository for zonas
- **`src/repository/tecnicos_repository.py`** — new file: read-only repository for tecnicos (with usuario join)
- **`src/services/categorias_service.py`** — new file: service delegating to repository
- **`src/services/zonas_service.py`** — new file: service delegating to repository
- **`src/services/tecnicos_service.py`** — new file: service delegating to repository
- **`src/schemas/categoria.py`** — new file: Pydantic model for categoria response
- **`src/schemas/zona.py`** — new file: Pydantic model for zona response
- **`src/schemas/tecnico.py`** — new file: Pydantic model for tecnico response
- **`src/apis/categorias.py`** — new file: `GET /categorias` router
- **`src/apis/zonas.py`** — new file: `GET /zonas` router
- **`src/apis/tecnicos.py`** — new file: `GET /tecnicos` router
- **`src/main.py`** — wire new routers
