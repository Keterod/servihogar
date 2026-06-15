## 1. Backend — Schemas

- [x] 1.1 Add `CotizacionActionResponse` Pydantic model with updated cotización fields and `solicitud_estado`
- [x] 1.2 Extend `CotizacionError` codes if needed for accept/reject (not_found, bad_request, conflict, failed)

## 2. Backend — Repository

- [x] 2.1 Add `CotizacionesRepository.get_by_id(id_cotizacion)` returning cotización with `id_solicitud` and `estado`
- [x] 2.2 Add `CotizacionesRepository.update_estado(id_cotizacion, estado)` 
- [x] 2.3 Add `CotizacionesRepository.reject_pending_others(id_solicitud, except_id_cotizacion)`
- [x] 2.4 Add `CotizacionesRepository.has_accepted_for_solicitud(id_solicitud)` (or equivalent query)
- [x] 2.5 Add `SolicitudesRepository.update_estado(id_solicitud, estado)` and reuse `get_by_id_for_cliente` / demo client lookup for ownership

## 3. Backend — Service & API

- [x] 3.1 Implement `CotizacionesService.aceptar_cotizacion_demo(id_cotizacion)` with validations and state transitions
- [x] 3.2 Implement `CotizacionesService.rechazar_cotizacion_demo(id_cotizacion)` with validations
- [x] 3.3 Add `PATCH /cotizaciones/{id_cotizacion}/aceptar` and `PATCH /cotizaciones/{id_cotizacion}/rechazar` to `apis/cotizaciones.py`
- [x] 3.4 Map errors to 200/400/404/409/503; keep existing `POST /cotizaciones` unchanged

## 4. Frontend — Model & Service

- [x] 4.1 Add `CotizacionActionResponse` interface to `models/solicitud.ts`
- [x] 4.2 Add `aceptarCotizacion(id_cotizacion)` and `rechazarCotizacion(id_cotizacion)` to `SolicitudService` calling PATCH endpoints
- [x] 4.3 Handle success, 400, 404, 409, and network errors with typed results

## 5. Frontend — DetalleSolicitud Component

- [x] 5.1 Add action loading/error signals (e.g. `accionCotizacionId`, `errorAccion`)
- [x] 5.2 Wire `aceptarCotizacion()` to service PATCH accept; update cotizaciones and solicitud signals on success
- [x] 5.3 Wire `rechazarCotizacion()` to service PATCH reject; update cotización signal on success
- [x] 5.4 Remove `localEstadoOverride` local-only simulation; derive estado from backend data
- [x] 5.5 Update template: loading/disabled states, error message, button guards for accepted/rejected/in-flight
- [x] 5.6 Keep timeline, navigation (`from=cliente|tecnico`), and technician read-only view behavior intact

## 6. Verify

- [x] 6.1 Test PATCH accept: pending cotización → 200, cotización `aceptada`, others `rechazada`, solicitud `en_proceso`
- [x] 6.2 Test PATCH reject: pending cotización → 200, cotización `rechazada`, solicitud unchanged
- [x] 6.3 Test 404 invalid id, 400 non-pending cotización, 409 accept when already accepted
- [x] 6.4 Verify `GET /solicitudes/{id}` and `/panel-cliente` show updated estado after reload
- [x] 6.5 Run `npm run build` in `servihogar-frontend/`
