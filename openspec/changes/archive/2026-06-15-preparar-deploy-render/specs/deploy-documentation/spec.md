## ADDED Requirements

### Requirement: Backend deploy README

The project SHALL include `README_DEPLOY_BACKEND.md` with:

- Render service type (Web Service)
- Root directory and Python version
- Install/build/start commands
- Health check path
- Required environment variables table (name, purpose, example format — no real secrets)
- CORS configuration steps
- Post-deploy smoke test checklist

#### Scenario: Operator can deploy backend from README alone

- **WHEN** a developer follows `README_DEPLOY_BACKEND.md` with valid Supabase credentials in Render env
- **THEN** they SHALL be able to configure a Render Web Service without reading monorepo AGENTS.md

### Requirement: Frontend deploy README

The project SHALL include `README_DEPLOY_FRONTEND.md` with:

- Render service type (Static Site)
- Build command and publish directory
- Build-time environment variables
- How to set backend URL after backend is deployed
- SPA routing note (`_redirects`)
- Post-deploy smoke test checklist

#### Scenario: Operator can deploy frontend from README alone

- **WHEN** a developer follows `README_DEPLOY_FRONTEND.md` with backend URL and Supabase anon key
- **THEN** they SHALL be able to configure a Render Static Site

### Requirement: Repository split guide

Deploy documentation SHALL describe how to split the monorepo into two independent repositories.

#### Scenario: Backend repo contents

- **WHEN** creating repo `servihogar-backend`
- **THEN** documentation SHALL list copying `servihogar-backend/backend/` as repo root (plus optional `database/`, `.env.example`, deploy README)

#### Scenario: Frontend repo contents

- **WHEN** creating repo `servihogar-frontend`
- **THEN** documentation SHALL list copying entire `servihogar-frontend/` excluding `node_modules`, `dist`, and cache directories

#### Scenario: Excluded secrets

- **WHEN** following the split guide
- **THEN** documentation SHALL explicitly state not to commit `.env`, service role keys, or backend-only secrets to the frontend repo

### Requirement: Deploy checklist

Both READMEs SHALL include a shared checklist covering:

- [ ] Backend `/health` returns 200
- [ ] Frontend loads home page
- [ ] Login works (Supabase Auth)
- [ ] API calls succeed (no CORS errors)
- [ ] Deep link to a panel route works after refresh

#### Scenario: Checklist verifiable after deploy

- **WHEN** deployment completes
- **THEN** each checklist item SHALL be testable in under 5 minutes
