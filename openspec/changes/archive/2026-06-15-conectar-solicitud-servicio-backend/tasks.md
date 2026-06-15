## 1. Backend — Schema

- [x] 1.1 Create `SolicitudRequest` schema (id_categoria, id_zona, titulo, descripcion, direccion_referencia, id_tecnico optional) and `SolicitudResponse` schema (id_solicitud, id_cliente, estado, fecha_publicacion) in `schemas/solicitud.py`

## 2. Backend — Repository & Service

- [x] 2.1 Create `SolicitudesRepository` with `insert(data)` method in `repository/solicitudes_repository.py`
- [x] 2.2 Create `SolicitudesService` with `crear_solicitud(data)` method that resolves demo client ID and calls repository, in `services/solicitudes_service.py`

## 3. Backend — Endpoint & Registration

- [x] 3.1 Create `POST /solicitudes` endpoint in `apis/solicitudes.py` returning `SolicitudResponse` with 201
- [x] 3.2 Register the solicitudes router in `main.py`

## 4. Frontend — Service

- [x] 4.1 Create `SolicitudService` in `services/solicitud.service.ts` with `crearSolicitud(data)` returning `Observable<SolicitudResponse | null>` from `POST /solicitudes`

## 5. Frontend — Navigation from PerfilTecnico

- [x] 5.1 Update `perfil-tecnico.html`: change "Solicitar cotización" `routerLink="/login"` to `[routerLink]="['/solicitud-servicio']"` with query params `tecnicoId` and `tecnicoNombre`

## 6. Frontend — SolicitudServicio Component

- [x] 6.1 Rewrite `SolicitudServicio`: inject `ActivatedRoute`, read query params (`tecnicoId`, `tecnicoNombre`), add `loading`, `success`, `error`, `categorias`, `zonas`, `tecnicoNombre` signals
- [x] 6.2 OnInit fetch categorias and zonas from backend services; pre-fill form fields if query params provide defaults
- [x] 6.3 Add `onSubmit()` that builds payload (`id_categoria`, `id_zona`, `titulo`, `descripcion`, `direccion_referencia`) and calls `SolicitudService.crearSolicitud()`; set loading/success/error signals
- [x] 6.4 Update template: bind dynamic categorias/zonas, technician reference card from query params, loading spinner on submit button, error message, success confirmation with navigation to panel-cliente

## 7. Build & Verify

- [x] 7.1 Run `npm run build` (frontend) and fix errors
- [x] 7.2 Verify `uvicorn src.main:app` starts without import errors
