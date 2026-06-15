## Context

The frontend public screens use hardcoded mock data. The backend now exposes `GET /categorias`, `GET /zonas`, and `GET /tecnicos`. The `BuscarTecnicos` component has filter Signals and `computed()` for filtered results but no loading, error, or empty states. Angular services exist as empty shells.

## Goals / Non-Goals

**Goals:**
- Create a frontend API config (`src/app/env.ts`) with base URL
- Implement `obtenerTecnicos()`, `obtenerCategorias()`, `obtenerZonas()` in existing services
- Update `Tecnico` model to match backend `TecnicoResponse` schema
- Rewrite `BuscarTecnicos` to fetch from services; add loading/error/empty signals
- Remove hardcoded mock data arrays from the component
- Keep filter Signals and `computed()` for real-time filtering
- Keep `provideHttpClient()` in app config (or add it if missing)
- Verify `npm run build` passes

**Non-Goals:**
- No authentication or authorization
- No Supabase direct calls from frontend
- No backend modifications (unless contract error found)
- No other screen changes (only /buscar-tecnicos)
- No visual redesign of the component

## Decisions

1. **`src/app/env.ts` over Angular environments** — The project has no `src/environments/` directory. A simple TypeScript constant file with the base URL is lighter and matches the prototype nature.

2. **`provideHttpClient()` in `app.config.ts`** — Angular standalone apps need `provideHttpClient()` for `HttpClient` injection. Must be added to the providers list.

3. **Fallback to empty arrays on error** — When the backend is unreachable, services return empty arrays. The component shows an error message. Filters still work (they filter empty arrays, showing "no results"). This prevents crashes.

4. **Keep filter options dynamic from backend** — Category and zone dropdowns are populated from API responses instead of hardcoded strings. The component no longer defines `CATEGORIAS_OFICIALES` or hardcoded zone strings.

5. **No `catchError` silencing** — Errors are caught in the component and exposed via an `error` signal. The UI shows a friendly message instead of silent failure.

## Risks / Trade-offs

- **[Low] Backend offline = empty filters** — Mitigation: The component shows an error banner. Filter dropdowns show nothing. User knows the backend is unavailable.
- **[Low] Tecnico model change is breaking** — The old `TecnicoSimulado` interface used `nombre`, `categoria`, `zona`, `valoracion`, `servicios`. The backend returns `nombres`, `apellidos`, `descripcion`, `experiencia_anios`, `calificacion`. The component template must be updated to use new field names and compute `nombre` from `nombres + apellidos`.
