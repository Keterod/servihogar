## 1. Backend — configuración producción

- [x] 1.1 Extender `Settings` con `CORS_ORIGINS` (lista comma-separated, default localhost)
- [x] 1.2 Actualizar `main.py` para usar CORS desde settings (métodos GET/POST/PATCH/DELETE/OPTIONS; headers Authorization, Content-Type)
- [x] 1.3 Crear/actualizar `.env.example` con variables requeridas (sin valores reales)
- [x] 1.4 Documentar start command Render: `uv sync --frozen && uvicorn src.main:app --host 0.0.0.0 --port $PORT`
- [x] 1.5 Verificar `GET /health` responde 200 (ya existe; confirmar en tests o smoke)

## 2. Backend — documentación deploy

- [x] 2.1 Crear `README_DEPLOY_BACKEND.md` (Web Service, env vars, CORS, healthcheck, checklist)
- [x] 2.2 Incluir sección "Qué copiar al repo `servihogar-backend`" (backend/, opcional database/)
- [x] 2.3 Incluir ejemplo `render.yaml` o tabla equivalente para UI de Render (opcional)

## 3. Frontend — configuración producción

- [x] 3.1 Implementar mecanismo build-time para `API_BASE_URL`, `SUPABASE_URL`, `SUPABASE_ANON_KEY` (script `set-env` + fileReplacements o equivalente)
- [x] 3.2 Mantener defaults locales en dev (`127.0.0.1:8003`, supabase.env actual)
- [x] 3.3 Añadir `public/_redirects` para SPA (`/* /index.html 200`)
- [x] 3.4 Añadir script `npm run build:render` (genera env + `ng build`)
- [x] 3.5 Confirmar que no hay service role en frontend (grep en src y dist)

## 4. Frontend — documentación deploy

- [x] 4.1 Crear `README_DEPLOY_FRONTEND.md` (Static Site, build cmd, publish dir, env vars, checklist)
- [x] 4.2 Incluir sección "Qué copiar al repo `servihogar-frontend`"
- [x] 4.3 Documentar orden de deploy: backend primero → copiar URL → build frontend

## 5. Verificación

- [x] 5.1 Backend local sigue en `:8003` con CORS localhost
- [x] 5.2 Frontend local sigue en `:4300` consumiendo backend local
- [x] 5.3 `uv run pytest` OK (backend)
- [x] 5.4 `npm run build` OK (frontend)
- [x] 5.5 Simular build producción con env vars de ejemplo (sin secretos reales en repo)
- [x] 5.6 Revisar que `.env` real no se commitea; `.gitignore` cubre `env.generated.ts` si aplica

## 6. Split repos (manual post-implementación)

- [x] 6.1 Documentar comandos git para crear repos separados en GitHub
- [x] 6.2 Checklist final de deploy en Render (backend + frontend + CORS + login smoke)
