## 1. Backend — Schemas

- [x] 1.1 Add `ValoracionRequest` Pydantic model (`id_solicitud`, `calificacion`, optional `comentario`, optional sub-scores)
- [x] 1.2 Add `ValoracionResponse` with DB-aligned fields plus `id_solicitud` and `solicitud_estado`
- [x] 1.3 Add `ValoracionError` or reuse service exception pattern with codes (not_found, bad_request, conflict, failed)

## 2. Backend — Repository

- [x] 2.1 Add `ValoracionesRepository.exists_for_cotizacion(id_cotizacion)`
- [x] 2.2 Add `ValoracionesRepository.insert(data)` mapping to `valoraciones` columns (`puntuacion`, `comentario`, etc.)
- [x] 2.3 Add helper in `SolicitudesRepository` or `CotizacionesRepository` to get accepted cotización for solicitud owned by demo client
- [x] 2.4 Reuse `SolicitudesRepository.get_by_id_for_cliente` and `update_estado` for ownership and finalization

## 3. Backend — Service & API

- [x] 3.1 Implement `ValoracionesService.crear_valoracion_demo(data)` with validations and state transitions
- [x] 3.2 Add `POST /valoraciones` to new `apis/valoraciones.py`
- [x] 3.3 Register valoraciones router in `main.py`
- [x] 3.4 Map errors to 201/400/404/409/422/503; keep existing endpoints unchanged

## 4. Frontend — Model & Service

- [x] 4.1 Add `ValoracionRequest` and `ValoracionResponse` interfaces
- [x] 4.2 Add `crearValoracion()` to service (new `ValoracionService` or extend `SolicitudService`) calling POST `/valoraciones`
- [x] 4.3 Handle success, 400, 404, 409, 422, and network errors with typed results

## 5. Frontend — ValorarServicio Component

- [x] 5.1 Read `idSolicitud` from query params; load solicitud context via `GET /solicitudes/{id}`
- [x] 5.2 Replace mock technician/service header with backend data (solicitud #, técnico aceptado, categoría/título)
- [x] 5.3 Wire submit to POST with computed `calificacion` and optional sub-scores; keep Signals/computed
- [x] 5.4 Add loading, success, error, and duplicate (409) states
- [x] 5.5 Handle missing `idSolicitud` with error/guidance UI
- [x] 5.6 On success, show confirmation and navigation to panel cliente

## 6. Frontend — DetalleSolicitud Navigation

- [x] 6.1 Update `irAValorar()` to navigate to `/valorar-servicio?idSolicitud={id}`
- [x] 6.2 Show rating action only when solicitud is `en_proceso` or `finalizada`
- [x] 6.3 Remove or replace test-only label on rating button

## 7. Verify

- [x] 7.1 Test POST success: accepted solicitud → 201, row in `valoraciones`, solicitud `finalizada`
- [x] 7.2 Test 404 invalid/not-owned solicitud, 400 no accepted cotización, 409 duplicate
- [x] 7.3 Test navigation from detalle → valorar → submit → panel reflects `finalizada`
- [x] 7.4 Run `npm run build` in `servihogar-frontend/`
