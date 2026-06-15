## ADDED Requirements

### Requirement: POST /cotizaciones endpoint

The backend SHALL expose a `POST /cotizaciones` endpoint that creates a cotización in the `cotizaciones` table for the demo technician (Carlos Mendoza, validated).

#### Scenario: Creates cotización with valid data

- **WHEN** a POST request is made to `/cotizaciones` with `id_solicitud`, `precio` greater than 0, non-empty `descripcion_propuesta`, and `tiempo_estimado`
- **THEN** the response SHALL be HTTP 201
- **THEN** the response SHALL include `id_cotizacion`, `id_solicitud`, `id_tecnico`, `precio`, `descripcion_propuesta`, `tiempo_estimado`, `estado`, and `fecha_creacion`
- **THEN** `estado` SHALL be `pendiente`
- **THEN** the row SHALL be persisted in Supabase with `monto`, `descripcion`, and `tiempo_estimado` mapped from the request

#### Scenario: Rejects missing or invalid fields

- **WHEN** a POST request is made to `/cotizaciones` missing required fields or with `precio` less than or equal to 0
- **THEN** the response SHALL be HTTP 422 with validation error details

#### Scenario: Rejects solicitud not found

- **WHEN** a POST request is made to `/cotizaciones` with a nonexistent `id_solicitud`
- **THEN** the response SHALL be HTTP 404 with a descriptive error message

#### Scenario: Rejects solicitud not pending

- **WHEN** a POST request is made to `/cotizaciones` for a solicitud whose estado is not `pendiente`
- **THEN** the response SHALL be HTTP 400 with a descriptive error message

#### Scenario: Rejects solicitud outside technician categories or zones

- **WHEN** a POST request is made to `/cotizaciones` for a solicitud whose category or zone is not assigned to the demo technician
- **THEN** the response SHALL be HTTP 400 with a descriptive error message

#### Scenario: Rejects duplicate cotización

- **WHEN** the demo technician already has a cotización for the given `id_solicitud`
- **THEN** the response SHALL be HTTP 409 with a descriptive error message indicating the solicitud was already quoted

#### Scenario: Uses demo technician without auth

- **WHEN** a POST request is made without authentication headers
- **THEN** the endpoint SHALL assign `id_tecnico` from the demo technician resolved server-side
- **THEN** no Supabase credentials or secrets SHALL be exposed in the response
