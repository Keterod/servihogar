# Deploy backend — ServiHogar (Render Web Service)

FastAPI backend for Render. Root directory in Render: **`backend/`** (content of `servihogar-backend/backend/` in the monorepo).

## Local development

```bash
cd servihogar-backend/backend
uv sync
cp .env.example .env   # fill with real Supabase values locally
uvicorn src.main:app --reload --port 8003
```

Health: `GET http://127.0.0.1:8003/health` → `{"status":"ok"}`

## Render Web Service

| Setting | Value |
|---------|--------|
| **Runtime** | Python 3.13 |
| **Root directory** | `backend` (repo root after split) |
| **Build command** | `uv sync --frozen` |
| **Start command** | `uvicorn src.main:app --host 0.0.0.0 --port $PORT` |
| **Health check path** | `/health` |

Reference Blueprint: [`render.yaml`](./render.yaml) (optional).

### Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | Yes | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Yes | Service role key (**backend only**, never frontend) |
| `SUPABASE_ANON_KEY` | Optional | Anon key if needed server-side |
| `ENVIRONMENT` | Recommended | `production` on Render |
| `CORS_ORIGINS` | Yes (prod) | Comma-separated frontend origins, e.g. `https://servihogar-frontend.onrender.com,http://localhost:4300` |

If `CORS_ORIGINS` is unset, localhost origins (`4300`, `4200`) are allowed for local dev.

**Never commit `.env` or real secrets to git.**

## Qué copiar al repo `servihogar-backend`

From monorepo `ServiHogar/`:

```
servihogar-backend/backend/     → repo root (or keep as backend/ if you prefer)
database/                       → optional (schema.sql, seed.sql, README.md)
```

Minimum files:

- `src/`
- `pyproject.toml`, `uv.lock`
- `tests/`
- `.env.example`, `README_DEPLOY_BACKEND.md`, `render.yaml`

Do **not** copy `servihogar-frontend/`.

## Crear repos separados (GitHub)

From monorepo root, example using two new repos:

```bash
# Backend
mkdir ../servihogar-backend-repo && cd ../servihogar-backend-repo
git init
cp -r ../ServiHogar/servihogar-backend/backend/* .
cp -r ../ServiHogar/database ./database   # optional
git add .
git commit -m "Initial backend for Render deploy"
git remote add origin https://github.com/YOUR_USER/servihogar-backend.git
git push -u origin main
```

On Windows PowerShell, copy folders with `Copy-Item -Recurse` instead of `cp -r`.

## Post-deploy checklist

- [ ] `GET https://<backend-host>/health` returns 200
- [ ] `CORS_ORIGINS` includes the deployed frontend URL
- [ ] Frontend can call API without CORS errors
- [ ] Login via Supabase Auth works end-to-end
- [ ] Authenticated API routes return data (not 503 Supabase config errors)

## Deploy order

1. Deploy **backend** first and note the public URL (`https://servihogar-backend.onrender.com`).
2. Set `CORS_ORIGINS` with the **frontend** URL (can update after frontend deploy).
3. Deploy **frontend** with `API_BASE_URL` pointing to backend URL (see `README_DEPLOY_FRONTEND.md`).

## Rollback

Redeploy a previous commit in Render Dashboard → **Manual Deploy** → select commit.
