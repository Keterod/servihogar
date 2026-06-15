## Context

Monorepo actual:

| Path | Rol en deploy |
|------|----------------|
| `servihogar-backend/backend/` | Raíz del repo `servihogar-backend` |
| `servihogar-frontend/` | Raíz del repo `servihogar-frontend` |
| `database/` | Referencia SQL; vive en repo backend o docs compartidos |
| `openspec/`, `docs/`, `prototipos/` | Opcional en repos de deploy; no bloquean runtime |

Backend usa FastAPI + uv + Supabase (service role solo en servidor). Frontend Angular 21 consume API vía `API_BASE_URL` y Supabase Auth con anon key. CORS hoy está hardcodeado a localhost en `main.py`. `env.ts` apunta a `http://127.0.0.1:8003`.

Render asigna `$PORT` dinámicamente; el proceso debe bind `0.0.0.0`.

## Goals / Non-Goals

**Goals:**

- Comandos build/start documentados y probados para Render.
- CORS y API URL configurables sin editar código en cada deploy.
- Healthcheck en `/health` usable por Render.
- SPA Angular funcional en Static Site (deep links).
- READMEs con checklist y variables de entorno.
- Guía clara para split de repos.
- Local dev sin regresiones (`8003` / `4300`).

**Non-Goals:**

- CI/CD avanzado (GitHub Actions) salvo mención opcional.
- Migración automática de git history al split.
- Configurar Supabase Storage/RLS (cambio previo).
- Desplegar efectivamente en Render (manual post-merge).
- Commitear `.env` reales.

## Decisions

### 1. CORS vía variable de entorno `CORS_ORIGINS`

**Decisión:** Lista separada por comas en env, parseada en `Settings`. Default incluye localhost para dev.

**Alternativa descartada:** Hardcodear URL de Render en código — requiere redeploy por cada preview.

Ejemplo producción:

```env
CORS_ORIGINS=https://servihogar-frontend.onrender.com,http://localhost:4300
```

### 2. Start command Render backend

**Decisión:**

```bash
uv sync --frozen && uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

Root directory en Render: `backend/` (contenido de `servihogar-backend/backend/`).

**Alternativa:** Gunicorn + workers — innecesario para MVP FastAPI async.

### 3. Frontend: file replacement en build de producción

**Decisión:** Crear `src/app/env.production.ts` (o `environment.production.ts`) con placeholders sustituidos en Render via **Environment Variables** + script pre-build, **o** usar `env.ts` que lee `import.meta`/window si Angular lo permite.

En Angular 21 sin `@angular/build:application` fileReplacements configurados aún, la opción más simple y Render-friendly:

- `env.ts` — default local (`http://127.0.0.1:8003`)
- `env.production.ts` — exporta constantes leídas de variables inyectadas en build time via script `scripts/set-env.js` que genera `env.generated.ts` desde `process.env.API_BASE_URL`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`
- `angular.json` production fileReplacements: `env.ts` → `env.generated.ts` (generado en CI/Render pre-build, gitignored)

**Alternativa más simple para MVP:** Documentar editar `env.production.ts` en repo frontend con URL pública del backend (no ideal pero válido para curso). **Preferida:** script `npm run build:render` que genera env antes de `ng build`.

### 4. SPA routing en Render Static Site

**Decisión:** Añadir `public/_redirects`:

```
/*    /index.html   200
```

Render Static Site respeta `_redirects` (formato Netlify-compatible).

### 5. Supabase en frontend

**Decisión:** Mover keys de `supabase.env.ts` a mismo mecanismo que `API_BASE_URL` (generado en build). Anon key only; nunca service role.

### 6. Documentación de split de repos

**Decisión:** `README_DEPLOY_BACKEND.md` en `servihogar-backend/backend/` (o raíz repo backend) y `README_DEPLOY_FRONTEND.md` en frontend. Sección "Qué copiar del monorepo" en cada uno.

**Backend repo incluye:**

- Todo `servihogar-backend/backend/` (src, pyproject.toml, uv.lock, tests)
- Opcional: `database/` (schema, seed, README)
- Opcional: `.env.example`, `README_DEPLOY_BACKEND.md`

**Frontend repo incluye:**

- Todo `servihogar-frontend/` excepto `node_modules`, `dist`, `.angular/cache`
- `README_DEPLOY_FRONTEND.md`

**No incluir en frontend:** backend, service role, `.env` backend.

### 7. Healthcheck Render

**Decisión:** Path `/health`, respuesta `{"status":"ok"}`. Render Health Check Path: `/health`.

### 8. render.yaml (opcional)

Documentar en README; archivo `render.yaml` por servicio como referencia, no obligatorio si se configura UI.

## Risks / Trade-offs

| Riesgo | Mitigación |
|--------|------------|
| Olvidar añadir URL frontend en `CORS_ORIGINS` | Checklist en README; default dev localhost |
| Build frontend sin env generado | Script `build:render` falla si faltan vars |
| Split repos desincroniza schema | Copiar `database/` al repo backend |
| Supabase keys en repo | Solo anon en frontend via env de Render, gitignore generated files |
| Cold start Render free tier | Documentar en README, no bloqueante |

## Migration Plan

1. Implementar config env backend + CORS.
2. Implementar env build frontend + `_redirects`.
3. Escribir READMEs y `.env.example`.
4. Verificar local + `npm run build` + pytest.
5. Crear repos GitHub separados y copiar carpetas según guía.
6. Crear Web Service + Static Site en Render con variables.
7. Probar login, API y rutas deep link.

## Open Questions

- ¿URL final de producción Render (custom domain vs `*.onrender.com`)? Se documenta como placeholder.
- ¿Incluir `render.yaml` commiteado o solo instrucciones UI? → Ambos en docs; yaml opcional en repo.
