## Why

The frontend's public screens (`/buscar-tecnicos`) still use hardcoded mock data. The backend now exposes `GET /categorias`, `GET /zonas`, and `GET /tecnicos`. Connecting these endpoints replaces mock data with real data while keeping the existing UX and Signal-based filtering.

## What Changes

- Create a frontend API config with a base URL pointing to the local backend
- Implement `HttpClient` calls in three existing Angular services (tecnico, categoria-servicio, zona)
- Update `Tecnico` model to match the backend's `TecnicoResponse` schema
- Rewrite `BuscarTecnicos` to fetch data from services instead of using hardcoded arrays
- Add loading, empty, and error states to the component
- Remove hardcoded `TECNICOS_SIMULADOS` and `CATEGORIAS_OFICIALES` from the component
- Keep all filter Signals and `computed()` logic intact
- Run `npm run build`

## Capabilities

### New Capabilities

- `frontend-api-connection`: Centralized backend API base URL configuration and `HttpClient`-based service layer for consuming public FastAPI endpoints from the Angular frontend.

### Modified Capabilities

- `frontend-public-screens`: The `/buscar-tecnicos` screen changes from mock-only data to fetching real data from the backend. Loading, empty, and error states are added. The visual UI and filter behavior remain identical.

## Impact

- **`src/app/env.ts`** — new file: API base URL (e.g., `http://127.0.0.1:8003`)
- **`src/app/services/tecnico.service.ts`** — add `obtenerTecnicos()` with `HttpClient`
- **`src/app/services/categoria-servicio.service.ts`** — add `obtenerCategorias()` with `HttpClient`
- **`src/app/services/zona.service.ts`** — add `obtenerZonas()` with `HttpClient`
- **`src/app/models/tecnico.ts`** — update to align with `TecnicoResponse` (id_tecnico, nombres, apellidos, descripcion, experiencia_anios, calificacion)
- **`src/app/components/buscar-tecnicos/buscar-tecnicos.ts`** — replace mock data with service calls; add `loading`, `error`, `categorias`, `zonas` signals
- **`src/app/components/buscar-tecnicos/buscar-tecnicos.html`** — add `@if (loading)` and `@if (error)` blocks
