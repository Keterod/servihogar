## ADDED Requirements

### Requirement: Health endpoint

The application SHALL expose a `GET /health` endpoint that returns the current status of the backend.

#### Scenario: Health check returns ok
- **WHEN** a client sends `GET /health`
- **THEN** the server SHALL respond with HTTP 200 and JSON `{"status": "ok"}`

### Requirement: Modular directory layout

The backend source code SHALL follow the `main → enrutadores → servicios → repositorio` architectural flow, with each layer in its own subpackage under `src/`.

#### Scenario: Required directories exist as Python packages
- **WHEN** the project filesystem is inspected
- **THEN** the following directories SHALL exist as Python packages (contain `__init__.py`): `src/apis/`, `src/services/`, `src/repository/`, `src/schemas/`, `src/core/`

### Requirement: Centralized configuration

The application SHALL load environment variables through a centralized `Settings` class using `pydantic-settings`.

#### Scenario: Settings load from .env
- **WHEN** a `.env` file exists at the backend root
- **THEN** the `Settings` class SHALL load variables `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, and `ENVIRONMENT` from it

#### Scenario: Default environment is development
- **WHEN** no `ENVIRONMENT` variable is set
- **THEN** the `Settings` class SHALL default `ENVIRONMENT` to `"development"`

### Requirement: .env.example exists

The backend root SHALL contain a `.env.example` file documenting all required environment variables.

#### Scenario: Example file lists all variables
- **WHEN** the project repository is cloned
- **THEN** `backend/.env.example` SHALL contain placeholder entries for `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, and `ENVIRONMENT`
