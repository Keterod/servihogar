## 1. Backend — Schemas

- [x] 1.1 Add `SolicitudDisponibleResponse` Pydantic model with fields: `id_solicitud`, `titulo`, `descripcion`, `direccion`, `estado`, `fecha_publicacion`, `categoria_nombre`, `zona_nombre`, `cliente_nombre`, `cotizaciones_count`, `ya_cotizada_por_tecnico`

## 2. Backend — Repository

- [x] 2.1 Add `get_demo_tecnico_id()` to resolve demo technician (Carlos Mendoza) by fixed `auth_user_id`
- [x] 2.2 Add method to load demo technician's category ids from `tecnico_categorias` and zone ids from `tecnico_zonas`
- [x] 2.3 Add `get_disponibles_for_tecnico(id_tecnico, categorias, zonas)` querying `solicitudes_servicio` with estado `pendiente`, category/zone filters, joins for categoria, zona, and cliente nombre
- [x] 2.4 Batch-fetch cotización counts and technician's own cotización ids to populate `cotizaciones_count` and `ya_cotizada_por_tecnico`

## 3. Backend — Service & API

- [x] 3.1 Add `obtener_solicitudes_disponibles_demo()` to `SolicitudesService` with documented filter logic mapping rows to `SolicitudDisponibleResponse`
- [x] 3.2 Add `GET /tecnicos/demo/solicitudes-disponibles` route in `apis/tecnicos.py` returning 200 with array (empty when none match)

## 4. Frontend — Model & Service

- [x] 4.1 Add `SolicitudDisponible` interface to `models/solicitud.ts` matching backend schema
- [x] 4.2 Add `solicitudesDisponiblesTecnico()` to `SolicitudService` calling `GET /tecnicos/demo/solicitudes-disponibles` with error → null

## 5. Frontend — PanelTecnico Component

- [x] 5.1 Update `panel-tecnico.ts`: inject `SolicitudService`, add `cargando` and `error` signals, fetch available solicitudes on init (mirror `PanelCliente` pattern)
- [x] 5.2 Replace mock `solicitudesDisponibles` initial data with backend response; add `computed()` for total disponibles, pendientes de cotizar, and ya cotizadas
- [x] 5.3 Update `panel-tecnico.html`: loading/error/empty states for available section; bind real fields (titulo, categoria, zona, fecha, direccion, estado, cliente)
- [x] 5.4 Add "Ver detalle" action with `RouterLink` to `/detalle-solicitud/:id`; keep "Enviar cotización" as visual-only local form flow (no POST)
- [x] 5.5 Keep mock data for `cotizacionesEnviadas` and `serviciosAceptados` unchanged

## 6. Verify

- [x] 6.1 Test `GET /tecnicos/demo/solicitudes-disponibles`: excludes finalizada; includes pendiente matching Carlos categories/zones; sets `ya_cotizada_por_tecnico` correctly for seed cotización
- [x] 6.2 Verify `/panel-tecnico` shows loading, loaded, empty, and error states; navigation to `/detalle-solicitud/:id` works
- [x] 6.3 Confirm `/panel-cliente`, `/detalle-solicitud/:id`, and `/solicitud-servicio` still work unchanged
- [x] 6.4 Run `npm run build` in `servihogar-frontend/` and verify success
