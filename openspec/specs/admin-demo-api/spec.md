# admin-demo-api Specification

## Purpose
TBD - created by archiving change conectar-panel-administrador-backend. Update Purpose after archive.
## Requirements
### Requirement: Demo administrator summary endpoint
The backend SHALL expose `GET /admin/demo/resumen` returning real system metrics calculated from Supabase.

#### Scenario: Summary returns real counters
- **WHEN** the administrator demo requests `GET /admin/demo/resumen`
- **THEN** the response includes numeric fields `total_usuarios`, `total_clientes`, `total_tecnicos`, `total_solicitudes`, `solicitudes_pendientes`, `solicitudes_en_proceso`, `solicitudes_finalizadas`, `tecnicos_pendientes`, `tecnicos_validados`, `tecnicos_rechazados`, `total_cotizaciones`, and `total_valoraciones`

#### Scenario: Request state counters use existing solicitud states
- **WHEN** the summary is calculated
- **THEN** `solicitudes_pendientes`, `solicitudes_en_proceso`, and `solicitudes_finalizadas` count rows in `solicitudes_servicio` with states `pendiente`, `en_proceso`, and `finalizada`

#### Scenario: Technician validation counters use existing validation states
- **WHEN** the summary is calculated
- **THEN** `tecnicos_pendientes`, `tecnicos_validados`, and `tecnicos_rechazados` count rows in `tecnicos` with `estado_validacion` values `pendiente`, `validado`, and `rechazado`

### Requirement: Pending technicians endpoint
The backend SHALL expose `GET /admin/demo/tecnicos-pendientes` returning technicians whose `estado_validacion` is `pendiente`.

#### Scenario: Pending technicians are listed
- **WHEN** the administrator demo requests `GET /admin/demo/tecnicos-pendientes`
- **THEN** every returned technician has `estado_validacion` equal to `pendiente`

#### Scenario: Pending technician response includes display fields
- **WHEN** a pending technician is returned
- **THEN** the technician includes `id_tecnico`, `nombres`, `apellidos`, `email`, `telefono`, `descripcion`, `experiencia_anios`, `fecha_registro`, `categorias`, and `zonas`

#### Scenario: Email may be unavailable
- **WHEN** the backend cannot obtain an email for the technician from the current data model
- **THEN** the technician response includes `email` as `null` without failing the request

#### Scenario: Categories and zones are returned as arrays
- **WHEN** a pending technician has related rows in `tecnico_categorias` or `tecnico_zonas`
- **THEN** `categorias` and `zonas` are arrays of display names from `categorias_servicio` and `zonas`

### Requirement: Approve pending technician endpoint
The backend SHALL expose `PATCH /admin/demo/tecnicos/{id_tecnico}/aprobar` to change a pending technician to `validado`.

#### Scenario: Pending technician is approved
- **WHEN** the administrator demo approves an existing technician with `estado_validacion` equal to `pendiente`
- **THEN** the backend updates `estado_validacion` to `validado`
- **THEN** the response includes `id_tecnico` and the current `estado_validacion`

#### Scenario: Technician does not exist when approving
- **WHEN** the administrator demo approves an `id_tecnico` that does not exist
- **THEN** the backend returns a controlled not-found error

#### Scenario: Technician is not pending when approving
- **WHEN** the administrator demo approves an existing technician whose `estado_validacion` is not `pendiente`
- **THEN** the backend returns a controlled conflict response or payload indicating the current `estado_validacion`

### Requirement: Reject pending technician endpoint
The backend SHALL expose `PATCH /admin/demo/tecnicos/{id_tecnico}/rechazar` to change a pending technician to `rechazado`.

#### Scenario: Pending technician is rejected
- **WHEN** the administrator demo rejects an existing technician with `estado_validacion` equal to `pendiente`
- **THEN** the backend updates `estado_validacion` to `rechazado`
- **THEN** the response includes `id_tecnico` and the current `estado_validacion`

#### Scenario: Technician does not exist when rejecting
- **WHEN** the administrator demo rejects an `id_tecnico` that does not exist
- **THEN** the backend returns a controlled not-found error

#### Scenario: Technician is not pending when rejecting
- **WHEN** the administrator demo rejects an existing technician whose `estado_validacion` is not `pendiente`
- **THEN** the backend returns a controlled conflict response or payload indicating the current `estado_validacion`

### Requirement: Backend architecture and scope boundaries
The administrator demo API SHALL follow the backend layer architecture and preserve existing application behavior.

#### Scenario: Endpoint logic uses layers
- **WHEN** an administrator demo endpoint handles a request
- **THEN** FastAPI routes delegate business logic to services and data access to repositories
- **THEN** request and response data are validated with Pydantic schemas

#### Scenario: No database migration is required
- **WHEN** the administrator demo API is implemented
- **THEN** `database/schema.sql` and `database/seed.sql` are not modified

#### Scenario: Existing endpoints remain available
- **WHEN** the administrator demo API is added to the FastAPI app
- **THEN** existing endpoints for public technician search, technician profile, service requests, dashboards, quotations, and ratings remain registered

