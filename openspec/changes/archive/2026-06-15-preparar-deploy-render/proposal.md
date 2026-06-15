## Why

ServiHogar está listo funcionalmente pero aún acoplado a un monorepo con URLs y CORS hardcodeados para localhost. Para publicar en Render con backend (Web Service) y frontend (Static Site) en repositorios separados, hace falta configuración de producción, variables de entorno y documentación de despliegue sin romper el flujo local actual.

## What Changes

- Backend FastAPI preparado para Render: escuchar en `0.0.0.0`, usar `$PORT`, healthcheck, CORS configurable por env.
- Frontend Angular preparado para Render Static Site: `API_BASE_URL` y credenciales Supabase configurables en build, SPA routing (`_redirects`), sin service role.
- Archivos de configuración mínimos para Render (`render.yaml` o equivalente documentado por servicio).
- Documentación de deploy: `README_DEPLOY_BACKEND.md`, `README_DEPLOY_FRONTEND.md`.
- Guía para separar el monorepo en dos repos (`servihogar-backend`, `servihogar-frontend`) indicando qué carpetas copiar.
- `.env.example` actualizado en backend (sin secretos reales); frontend con patrón de env de build documentado.
- Desarrollo local intacto: backend `:8003`, frontend `:4300`.

## Capabilities

### New Capabilities

- `render-backend-deploy`: Requisitos de producción del backend en Render (start command, env vars, CORS, health).
- `render-frontend-deploy`: Requisitos de producción del frontend en Render Static Site (build, env, SPA routing, Supabase anon only).
- `deploy-documentation`: READMEs de deploy, checklist y guía de separación de repositorios.

### Modified Capabilities

- `frontend-api-connection`: La URL base del API debe ser configurable por entorno (local vs producción Render), no solo constante localhost.

## Impact

- `servihogar-backend/backend/src/main.py` — CORS desde settings.
- `servihogar-backend/backend/src/core/config.py` — nuevas variables (`CORS_ORIGINS`, `PORT` implícito vía uvicorn).
- `servihogar-frontend/src/app/env.ts` y/o `environment.production.ts` — API URL configurable.
- `servihogar-frontend/public/_redirects` — fallback SPA para Render.
- Nuevos docs en raíz de cada paquete o monorepo según design.
- Sin cambios a lógica de negocio, schema SQL ni secretos en repo.
