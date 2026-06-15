## MODIFIED Requirements

### Requirement: Backend API base URL

The application SHALL have a single configuration point for the backend API base URL, used by all service classes. The value SHALL be environment-specific: local development uses the localhost backend URL; production builds use the public Render backend URL supplied at build time.

#### Scenario: Base URL is a constant

- **WHEN** the application initializes
- **THEN** a constant with the backend base URL SHALL be available in `src/app/env.ts` (or generated replacement for production)

#### Scenario: Local development URL

- **WHEN** running locally with `ng serve --port 4300`
- **THEN** `API_BASE_URL` SHALL point to `http://127.0.0.1:8003` (or documented local default)

#### Scenario: Production build URL

- **WHEN** building for Render with `API_BASE_URL` set to the deployed backend URL
- **THEN** all services using `API_BASE_URL` SHALL target that URL
