## Context

The frontend `PerfilTecnico` component displays hardcoded mock data for Carlos Mendoza. The backend already returns `GET /tecnicos` with `categorias` and `zonas` per technician (via `TecnicoResponse`). The `portafolio_tecnico` table exists in Supabase but is not exposed by the backend. The frontend `Tecnico` model already includes `categorias` and `zonas` arrays from a previous sync.

## Goals / Non-Goals

**Goals:**
- Backend: new endpoint `GET /tecnicos/{id_tecnico}` returning full profile + portfolio
- Backend: new schema `TecnicoDetalleResponse` extending base + `portafolio`
- Frontend: route `/perfil-tecnico` → `/perfil-tecnico/:id` with lazy loading
- Frontend: `TecnicoService.obtenerTecnicoPorId(id)` calling new endpoint
- Frontend: `PerfilTecnico` reads route param, fetches from backend, renders real data
- Frontend: add loading, error, not-found states
- Frontend: navigation from `BuscarTecnicos` passes `id_tecnico`
- Build passes on both backend and frontend

**Non-Goals:**
- No authentication or authorization
- No DB schema changes
- No changes to other screens (home, login, search list panel)
- No `RatingBar` mock data replacement (stays hardcoded until rating data exists)
- No image upload functionality for portfolio

## Decisions

1. **`TecnicoDetalleResponse` as child of `TecnicoResponse`** — Reuse the existing schema and add a `portafolio` list. Avoids duplication and keeps the response model consistent.

2. **Portfolio fetched in service layer** — The `TecnicosService.obtener_por_id` method queries Supabase for the technician by ID plus their portfolio items from `portafolio_tecnico`. This keeps the endpoint stateless from the caller's perspective.

3. **Frontend route param** — Use `:id` route param with Angular's `ActivatedRoute` (via `inject()`). The route config changes from `perfil-tecnico` to `perfil-tecnico/:id`.

4. **Signal-based state** — `PerfilTecnico` uses `signal()` for `loading`, `error`, `notFound`, and `tecnico`. A shared `TecnicoDetalle` model extends `Tecnico` with `portafolio: PortafolioItem[]`.

5. **Error on backend offline** — Service catches error and returns `of(null)`. Component shows error banner. 404 from backend sets `notFound` signal.

6. **Navigation from search** — Change the static `routerLink="/perfil-tecnico"` to `[routerLink]="['/perfil-tecnico', tecnico.id_tecnico]"` in the existing template.

## Risks / Trade-offs

- **[Low] Backend offline** → Component shows error message. Mitigation: `catchError` returns `null`, component checks and sets `error` signal.
- **[Low] 404 for invalid ID** → Component shows "Técnico no encontrado" message. Mitigation: backend returns 404, frontend checks null response.
- **[Low] Portfolio images are URLs, not blob data** — The frontend renders `imagen_url` as `<img src>` directly. No image optimization is implemented.
