# render-backend-deploy Specification

## Purpose
TBD - created by archiving change preparar-deploy-render. Update Purpose after archive.
## Requirements
### Requirement: Render start command binds public port

The backend SHALL be startable on Render with a command that listens on `0.0.0.0` and uses the `$PORT` environment variable provided by Render.

#### Scenario: Start command documented

- **WHEN** deploying to Render Web Service
- **THEN** the documented start command SHALL be equivalent to `uvicorn src.main:app --host 0.0.0.0 --port $PORT` after dependency install via `uv sync --frozen`

#### Scenario: Local dev unchanged

- **WHEN** running locally on port 8003
- **THEN** developers SHALL still be able to start with `uvicorn src.main:app --reload --port 8003` without Render-specific configuration

### Requirement: Health check endpoint

The backend SHALL expose `GET /health` returning HTTP 200 and JSON `{"status":"ok"}` for Render health checks.

#### Scenario: Health check success

- **WHEN** a client sends `GET /health`
- **THEN** the response status SHALL be 200 and body SHALL include `"status":"ok"`

### Requirement: CORS origins configurable via environment

The backend SHALL read allowed CORS origins from the `CORS_ORIGINS` environment variable as a comma-separated list. If unset, it SHALL default to local Angular dev origins (`localhost:4300`, `127.0.0.1:4300`, and `:4200` variants).

#### Scenario: Production frontend origin allowed

- **WHEN** `CORS_ORIGINS` includes `https://servihogar-frontend.onrender.com`
- **AND** a browser request from that origin includes `Authorization` and `Content-Type`
- **THEN** the response SHALL include appropriate CORS headers allowing the origin

#### Scenario: Local development default

- **WHEN** `CORS_ORIGINS` is not set
- **THEN** requests from `http://localhost:4300` SHALL be allowed

### Requirement: Required environment variables documented

The backend deploy documentation SHALL list required environment variables without example secret values:

- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_ANON_KEY` (optional if unused server-side)
- `ENVIRONMENT` (e.g. `production`)
- `CORS_ORIGINS`

#### Scenario: Missing Supabase config fails safely

- **WHEN** required Supabase variables are missing at runtime
- **THEN** database operations SHALL fail with a controlled error response, not an unhandled crash without CORS headers

### Requirement: No localhost hardcoded for production-only paths

Production CORS and bind configuration SHALL NOT require editing Python source to add a new Render frontend URL.

#### Scenario: Add preview URL without code change

- **WHEN** a new frontend preview URL is deployed on Render
- **THEN** an operator SHALL add it to `CORS_ORIGINS` in Render dashboard only

