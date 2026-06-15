## 1. Backend — Schemas

- [x] 1.1 Add `CotizacionDetalleResponse` Pydantic model with fields: `id_cotizacion`, `id_tecnico`, `tecnico_nombre`, `tecnico_descripcion`, `precio`, `tiempo_estimado`, `descripcion_propuesta`, `estado`, `fecha_creacion`
- [x] 1.2 Add `SolicitudDetalleResponse` Pydantic model extending list fields with `cotizaciones: list[CotizacionDetalleResponse]`

## 2. Backend — Repository

- [x] 2.1 Add `get_by_id_for_cliente(id_solicitud, id_cliente)` to `SolicitudesRepository` querying `solicitudes_servicio` with joins to `categorias_servicio` and `zonas`
- [x] 2.2 Add `get_cotizaciones_by_solicitud(id_solicitud)` querying `cotizaciones` with joins to `tecnicos` and `usuarios` for technician name and description

## 3. Backend — Service & API

- [x] 3.1 Add `obtener_detalle(id_solicitud)` to `SolicitudesService` validating demo client ownership and mapping to `SolicitudDetalleResponse`
- [x] 3.2 Add `GET /solicitudes/{id_solicitud}` route in `apis/solicitudes.py` returning 200 or 404

## 4. Frontend — Model & Service

- [x] 4.1 Add `CotizacionDetalle` and `SolicitudDetalle` interfaces to `models/solicitud.ts` matching backend schemas
- [x] 4.2 Add `obtenerDetalle(id: number)` to `SolicitudService` calling `GET /solicitudes/{id}` with 404 → null and other errors propagated

## 5. Frontend — DetalleSolicitud Component

- [x] 5.1 Rewrite `detalle-solicitud.ts`: inject `ActivatedRoute` + `SolicitudService`, add `loading`, `error`, `notFound`, `solicitud`, `cotizaciones` signals and derived `computed()` for timeline/selection
- [x] 5.2 Fetch on init when `:id` param is present; map backend fields to template bindings
- [x] 5.3 Update `detalle-solicitud.html`: loading/error/notFound states, bind real solicitud fields, empty cotizaciones message, bind cotizaciones from backend
- [x] 5.4 Keep accept/reject as local signal updates only; do not simulate cotizaciones when backend returns empty list

## 6. Verify

- [x] 6.1 Test `GET /solicitudes/1` (with cotizaciones) and a solicitud without cotizaciones; test 404 for invalid id
- [x] 6.2 Verify `/detalle-solicitud/9` shows real data for solicitud 9 from panel navigation
- [x] 6.3 Run `npm run build` and verify backend starts without import errors
