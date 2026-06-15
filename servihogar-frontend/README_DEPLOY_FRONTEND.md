# Deploy frontend — ServiHogar (Render Static Site)

Angular 21 static site for Render. Uses **anon key only** for Supabase — never service role.

## Local development

```bash
cd servihogar-frontend
npm install
npm start          # http://localhost:4300
```

Defaults in `src/app/env.ts`:

- `API_BASE_URL` → `http://127.0.0.1:8003`
- Supabase URL + anon key for local Auth

Backend must run locally on port **8003**.

## Render Static Site

| Setting | Value |
|---------|--------|
| **Build command** | `npm ci && npm run build:render` |
| **Publish directory** | `dist/servihogar-frontend/browser` |

### Build-time environment variables

Set in Render **Environment** (available during build):

| Variable | Example | Description |
|----------|---------|-------------|
| `API_BASE_URL` | `https://servihogar-backend.onrender.com` | Public backend URL (no trailing slash) |
| `SUPABASE_URL` | `https://xxxx.supabase.co` | Supabase project URL |
| `SUPABASE_ANON_KEY` | `eyJ...` or publishable key | **Anon key only** |

`npm run build:render` runs `scripts/set-env.mjs` to generate `src/app/env.generated.ts` (gitignored), then builds with Angular `render` configuration.

Regular `npm run build` uses local `env.ts` defaults (for CI without secrets).

### SPA routing

`public/_redirects` maps all routes to `index.html` for deep links:

```
/*    /index.html   200
```

## Qué copiar al repo `servihogar-frontend`

From monorepo `ServiHogar/`:

```
servihogar-frontend/    → repo root
```

Include:

- `src/`, `public/`, `scripts/`
- `angular.json`, `package.json`, `package-lock.json`
- `tsconfig*.json`, `README_DEPLOY_FRONTEND.md`

Exclude:

- `node_modules/`, `dist/`, `.angular/cache/`
- `src/app/env.generated.ts` (created at build time)
- Backend code, `.env` files with secrets

## Crear repos separados (GitHub)

```bash
mkdir ../servihogar-frontend-repo && cd ../servihogar-frontend-repo
git init
cp -r ../ServiHogar/servihogar-frontend/* .
# remove node_modules and dist if copied
git add .
git commit -m "Initial frontend for Render deploy"
git remote add origin https://github.com/YOUR_USER/servihogar-frontend.git
git push -u origin main
```

On Windows: `Copy-Item -Recurse` and delete `node_modules`, `dist` before commit.

## Deploy order

1. Deploy **backend** first → copy public URL.
2. Create Static Site with `API_BASE_URL=https://<backend-url>`.
3. Update backend `CORS_ORIGINS` to include frontend URL (`https://<frontend>.onrender.com`).
4. Redeploy backend if CORS was updated.

## Post-deploy checklist

- [ ] Home page loads at frontend URL
- [ ] `GET /health` on backend returns 200
- [ ] Login works (Supabase Auth)
- [ ] API calls succeed (Network tab: no CORS errors)
- [ ] Deep link works: open `/panel-cliente` directly and refresh
- [ ] No `service_role` in frontend bundle (`grep -r service_role dist/` → empty)

## Security

- **Never** set `SUPABASE_SERVICE_ROLE_KEY` on the Static Site.
- **Never** commit `env.generated.ts` or real keys to git.
- Anon key in Render env vars is expected for client-side Supabase Auth.

## Rollback

Redeploy previous commit from Render Dashboard.
