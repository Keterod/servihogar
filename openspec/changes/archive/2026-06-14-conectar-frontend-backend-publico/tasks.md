## 1. API Config & HttpClient

- [x] 1.1 Create `src/app/env.ts` with `API_BASE_URL` pointing to the backend
- [x] 1.2 Add `provideHttpClient()` to `src/app/app.config.ts` providers

## 2. Models

- [x] 2.1 Update `src/app/models/tecnico.ts` to match backend `TecnicoResponse` (id_tecnico, nombres, apellidos, descripcion, experiencia_anios, calificacion)
- [x] 2.2 Verify `src/app/models/categoria-servicio.ts` matches backend `CategoriaResponse` (id_categoria, nombre, descripcion)
- [x] 2.3 Verify `src/app/models/zona.ts` matches backend `ZonaResponse` (id_zona, nombre, id_ciudad)

## 3. Services

- [x] 3.1 Implement `obtenerCategorias()` in `CategoriaServicioService` (GET /categorias)
- [x] 3.2 Implement `obtenerZonas()` in `ZonaService` (GET /zonas)
- [x] 3.3 Implement `obtenerTecnicos()` in `TecnicoService` (GET /tecnicos)

## 4. BuscarTecnicos Component

- [x] 4.1 Inject services in `BuscarTecnicos`; add `loading`, `error`, `categorias`, `zonas` signals
- [x] 4.2 Fetch categorias, zonas, and tecnicos on init; update template with loading/error/empty states
- [x] 4.3 Update filter dropdowns to use dynamic `categorias()` and `zonas()` from backend
- [x] 4.4 Update template bindings for new Tecnico model fields (nombres+apellidos, calificacion, etc.)
- [x] 4.5 Remove hardcoded `CATEGORIAS_OFICIALES` and `TECNICOS_SIMULADOS` from component

## 5. Build

- [x] 5.1 Run `npm run build` and fix any errors
