# render-frontend-deploy Specification

## Purpose
TBD - created by archiving change preparar-deploy-render. Update Purpose after archive.
## Requirements
### Requirement: Production API base URL configurable at build time

The frontend production build SHALL obtain `API_BASE_URL` from environment variables at build time (not hardcoded to localhost), while local development SHALL continue using `http://127.0.0.1:8003` by default.

#### Scenario: Local development default

- **WHEN** running `ng serve --port 4300` without production env overrides
- **THEN** `API_BASE_URL` SHALL resolve to the local backend URL (`http://127.0.0.1:8003` or documented equivalent)

#### Scenario: Render production build

- **WHEN** building for Render Static Site with `API_BASE_URL=https://servihogar-backend.onrender.com`
- **THEN** all HTTP services SHALL call that public backend URL

### Requirement: Supabase client uses anon key only

The frontend build SHALL configure Supabase with `SUPABASE_URL` and `SUPABASE_ANON_KEY` only. The service role key MUST NOT appear in frontend source, build output, or Render environment for the Static Site.

#### Scenario: No service role in frontend bundle

- **WHEN** searching the production build output for `service_role` or `SERVICE_ROLE`
- **THEN** no matches SHALL be found

### Requirement: SPA deep linking on Render Static Site

The frontend SHALL include a static redirect rule so client-side routes work on refresh and direct URL access.

#### Scenario: Direct navigation to protected route

- **WHEN** a user opens `https://<frontend-host>/panel-cliente` directly
- **THEN** Render SHALL serve `index.html` and Angular SHALL load the route

#### Scenario: Redirects file present

- **WHEN** the production static assets are published
- **THEN** a `_redirects` file (or Render-equivalent) SHALL map `/*` to `/index.html` with status 200

### Requirement: Render build command documented

The frontend deploy documentation SHALL specify:

- Build command: `npm ci && npm run build:render` (or documented equivalent)
- Publish directory: `dist/servihogar-frontend/browser`
- Required build-time env vars: `API_BASE_URL`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`

#### Scenario: Production build succeeds

- **WHEN** required env vars are set and build runs
- **THEN** `npm run build` (or `build:render`) SHALL complete without errors

