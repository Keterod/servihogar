## 1. Backend — Schema & Service

- [x] 1.1 Add `PortafolioItem` schema (id_portafolio, titulo, descripcion, imagen_url) and `TecnicoDetalleResponse` (extends TecnicoResponse with portafolio) to `schemas/tecnico.py`
- [x] 1.2 Add `get_by_id()` method to `TecnicosRepository` (fetch by id_tecnico with user join)
- [x] 1.3 Add `obtener_portafolio()` and `obtener_por_id()` methods to `TecnicosService` (query Supabase portafolio_tecnico, return TecnicoDetalleResponse)
- [x] 1.4 Add `GET /tecnicos/{id_tecnico}` endpoint to `apis/tecnicos.py` returning `TecnicoDetalleResponse`, with 404 for missing ID

## 2. Frontend — Model & Service

- [x] 2.1 Add `PortafolioItem` interface and `TecnicoDetalle` interface (extends Tecnico with portafolio) to `models/tecnico.ts`
- [x] 2.2 Add `obtenerTecnicoPorId(id: number)` method to `TecnicoService` returning `Observable<TecnicoDetalle | null>` from `GET /tecnicos/{id}`

## 3. Frontend — Route & Navigation

- [x] 3.1 Update `app.routes.ts`: change `perfil-tecnico` to `perfil-tecnico/:id` with lazy loading
- [x] 3.2 Update `buscar-tecnicos.html`: change `routerLink="/perfil-tecnico"` to `[routerLink]="['/perfil-tecnico', tecnico.id_tecnico]"`

## 4. Frontend — PerfilTecnico Component

- [x] 4.1 Rewrite `PerfilTecnico`: inject `ActivatedRoute` + `TecnicoService`, read `:id` param, add `loading`, `error`, `notFound`, `tecnico` signals
- [x] 4.2 On init, fetch `obtenerTecnicoPorId(id)`; set signals accordingly
- [x] 4.3 Update template: wrap in `@if (loading())`, `@if (error())`, `@if (notFound())` states; bind real data fields (nombres+apellidos, descripcion, experiencia_anios, calificacion, categorias, zonas, portafolio)
- [x] 4.4 Remove all hardcoded mock data (`TecnicoPerfil`, `galeria`, `ratingBars`); keep `RatingBar` section as static placeholder if no backend rating data exists

## 5. Build & Verify

- [x] 5.1 Run `npm run build` (frontend) and fix errors
- [x] 5.2 Verify `uvicorn src.main:app` starts without import errors
