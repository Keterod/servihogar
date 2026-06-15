## 1. Backend — Repository

- [x] 1.1 Add `get_by_cliente_id()` method to `SolicitudesRepository` that queries `solicitudes_servicio` joined with `categorias_servicio` and `zonas` for a given `id_cliente`, and counts cotizaciones per solicitud

## 2. Backend — Service

- [x] 2.1 Add `obtener_por_cliente()` method to `SolicitudesService` that calls the repository and maps results to `SolicitudListResponse` schema
- [x] 2.2 Create `SolicitudListResponse` Pydantic model with fields: `id_solicitud`, `titulo`, `descripcion`, `direccion`, `estado`, `fecha_publicacion`, `categoria_nombre`, `zona_nombre`, `cotizaciones_count`

## 3. Backend — API Endpoint

- [x] 3.1 Add `GET /clientes/demo/solicitudes` route in `apis/solicitudes.py` that resolves the demo client ID, calls the service, and returns the solicitud list

## 4. Frontend — Service

- [x] 4.1 Add `solicitudesCliente()` method to the frontend `SolicitudService` (or create a new service) that calls `GET /clientes/demo/solicitudes` and returns typed observables
- [x] 4.2 Define `SolicitudListResponse` interface matching the backend schema

## 5. Frontend — PanelCliente Component

- [x] 5.1 Rewrite `panel-cliente.ts` to inject `SolicitudService`, add signals for `solicitudes`, `cargando`, `error`, fetch on init
- [x] 5.2 Update `panel-cliente.html` with loading state (`@if cargando()`), error state (`@if error()`), empty state (`@if solicitudes().length === 0`), and the existing table for the data case
- [x] 5.3 Update "Ver detalle" button to navigate to `/detalle-solicitud/{{ solicitud.id_solicitud }}`

## 6. Verify

- [x] 6.1 Run `uv sync` and `npm install` if needed
- [x] 6.2 Run `npm run build` (frontend) and verify no type errors
- [x] 6.3 Verify backend syntax with `uv run uvicorn src.main:app`
