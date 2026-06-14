## 1. Package Structure

- [x] 1.1 Create `src/core/__init__.py` and `src/core/config.py`
- [x] 1.2 Add `__init__.py` to `src/apis/`, `src/services/`, `src/repository/`, `src/schemas/` (if missing)
- [x] 1.3 Add `pydantic-settings` to `pyproject.toml` dependencies
- [x] 1.4 Run `uv sync` to install the new dependency

## 2. Configuration

- [x] 2.1 Implement `src/core/config.py` with a `Settings` class using `pydantic-settings` `BaseSettings`
- [x] 2.2 Create `.env.example` at backend root with `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `ENVIRONMENT`

## 3. Health Endpoint

- [x] 3.1 Create `src/apis/__init__.py` (if missing)
- [x] 3.2 Create `src/apis/health.py` with `APIRouter` and `GET /health` returning `{"status": "ok"}`

## 4. Main Entry Point

- [x] 4.1 Rewrite `src/main.py` with FastAPI app creation, import and include the health router
- [x] 4.2 Verify the app starts: run `uvicorn src.main:app` and test `GET /health` returns `{"status": "ok"}`
