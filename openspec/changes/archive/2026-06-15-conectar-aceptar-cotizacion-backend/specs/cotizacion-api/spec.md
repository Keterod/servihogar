## ADDED Requirements

### Requirement: PATCH /cotizaciones/{id_cotizacion}/aceptar endpoint

The backend SHALL expose a `PATCH /cotizaciones/{id_cotizacion}/aceptar` endpoint allowing the demo client to accept a pending cotización on their solicitud.

#### Scenario: Accepts pending cotización successfully

- **WHEN** a PATCH request is made to `/cotizaciones/{id_cotizacion}/aceptar` for a cotización with `estado = pendiente` whose solicitud belongs to the demo client and has `estado = pendiente`
- **THEN** the response SHALL be HTTP 200
- **THEN** the target cotización SHALL be persisted with `estado = aceptada`
- **THEN** all other cotizaciones on the same `id_solicitud` with `estado = pendiente` SHALL be persisted with `estado = rechazada`
- **THEN** the solicitud SHALL be persisted with `estado = en_proceso`
- **THEN** the response SHALL include the updated cotización and the new `solicitud_estado`

#### Scenario: Rejects accept when cotización not found

- **WHEN** a PATCH request is made to `/cotizaciones/99999/aceptar` for a nonexistent cotización
- **THEN** the response SHALL be HTTP 404 with a descriptive error message

#### Scenario: Rejects accept when solicitud not owned by demo client

- **WHEN** a PATCH request is made to accept a cotización whose solicitud does not belong to the demo client
- **THEN** the response SHALL be HTTP 404 with a descriptive error message

#### Scenario: Rejects accept when cotización is not pending

- **WHEN** a PATCH request is made to accept a cotización whose `estado` is not `pendiente`
- **THEN** the response SHALL be HTTP 400 with a descriptive error message

#### Scenario: Rejects accept when solicitud is not pending

- **WHEN** a PATCH request is made to accept a cotización on a solicitud whose `estado` is not `pendiente`
- **THEN** the response SHALL be HTTP 400 with a descriptive error message

#### Scenario: Rejects accept when another cotización is already accepted

- **WHEN** the solicitud already has a cotización with `estado = aceptada`
- **THEN** the response SHALL be HTTP 409 with a descriptive error message

#### Scenario: Uses demo client without auth

- **WHEN** a PATCH request is made without authentication headers
- **THEN** ownership SHALL be validated against the demo client resolved server-side
- **THEN** no Supabase credentials or secrets SHALL be exposed in the response

### Requirement: PATCH /cotizaciones/{id_cotizacion}/rechazar endpoint

The backend SHALL expose a `PATCH /cotizaciones/{id_cotizacion}/rechazar` endpoint allowing the demo client to reject a pending cotización on their solicitud.

#### Scenario: Rejects pending cotización successfully

- **WHEN** a PATCH request is made to `/cotizaciones/{id_cotizacion}/rechazar` for a cotización with `estado = pendiente` whose solicitud belongs to the demo client
- **THEN** the response SHALL be HTTP 200
- **THEN** the target cotización SHALL be persisted with `estado = rechazada`
- **THEN** the solicitud estado SHALL remain unchanged when no cotización is accepted on that solicitud
- **THEN** the response SHALL include the updated cotización and the current `solicitud_estado`

#### Scenario: Rejects reject when cotización not found

- **WHEN** a PATCH request is made to `/cotizaciones/99999/rechazar` for a nonexistent cotización
- **THEN** the response SHALL be HTTP 404 with a descriptive error message

#### Scenario: Rejects reject when solicitud not owned by demo client

- **WHEN** a PATCH request is made to reject a cotización whose solicitud does not belong to the demo client
- **THEN** the response SHALL be HTTP 404 with a descriptive error message

#### Scenario: Rejects reject when cotización is not pending

- **WHEN** a PATCH request is made to reject a cotización whose `estado` is not `pendiente`
- **THEN** the response SHALL be HTTP 400 with a descriptive error message

#### Scenario: Does not change solicitud when rejecting without accepted cotización

- **WHEN** the demo client rejects a pending cotización and no cotización on that solicitud has `estado = aceptada`
- **THEN** the solicitud SHALL remain in its previous estado (typically `pendiente`)
