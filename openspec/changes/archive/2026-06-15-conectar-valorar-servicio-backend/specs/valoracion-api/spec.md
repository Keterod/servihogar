## ADDED Requirements

### Requirement: POST /valoraciones endpoint

The backend SHALL expose a `POST /valoraciones` endpoint that creates a valoración in the `valoraciones` table for the demo client (Ana Torres).

#### Scenario: Creates valoración with valid data

- **WHEN** a POST request is made to `/valoraciones` with `id_solicitud`, `calificacion` between 1 and 5, and optional `comentario`
- **THEN** the response SHALL be HTTP 201
- **THEN** the backend SHALL resolve the accepted cotización for that solicitud and persist `id_cotizacion`, `puntuacion` (from `calificacion`), and `comentario` using real DB column names
- **THEN** the response SHALL include `id_valoracion`, `id_cotizacion`, `id_solicitud`, `puntuacion`, `comentario`, and `fecha_valoracion`

#### Scenario: Finalizes solicitud after rating

- **WHEN** a valoración is created successfully for a solicitud with `estado = en_proceso`
- **THEN** the solicitud SHALL be persisted with `estado = finalizada`
- **THEN** the response SHALL include the updated `solicitud_estado`

#### Scenario: Rejects missing or invalid calificación

- **WHEN** a POST request is made without required fields or with `calificacion` outside 1–5
- **THEN** the response SHALL be HTTP 422 with validation error details

#### Scenario: Rejects solicitud not found

- **WHEN** a POST request is made with a nonexistent `id_solicitud`
- **THEN** the response SHALL be HTTP 404 with a descriptive error message

#### Scenario: Rejects solicitud not owned by demo client

- **WHEN** a POST request is made for a solicitud that does not belong to the demo client
- **THEN** the response SHALL be HTTP 404 with a descriptive error message

#### Scenario: Rejects solicitud without accepted cotización

- **WHEN** a POST request is made for a solicitud that has no cotización with `estado = aceptada`
- **THEN** the response SHALL be HTTP 400 with a descriptive error message

#### Scenario: Rejects solicitud not eligible for rating

- **WHEN** a POST request is made for a solicitud whose `estado` is `pendiente` or `cancelada`
- **THEN** the response SHALL be HTTP 400 with a descriptive error message

#### Scenario: Rejects duplicate valoración

- **WHEN** a valoración already exists for the accepted cotización of the solicitud
- **THEN** the response SHALL be HTTP 409 with a descriptive error message

#### Scenario: Uses demo client without auth

- **WHEN** a POST request is made without authentication headers
- **THEN** ownership SHALL be validated against the demo client resolved server-side
- **THEN** no Supabase credentials or secrets SHALL be exposed in the response

#### Scenario: Optional sub-scores persisted when provided

- **WHEN** a POST request includes optional sub-scores `puntualidad`, `calidad`, `trato`, or `precio` each between 1 and 5
- **THEN** the corresponding DB columns SHALL be persisted
- **THEN** omitted sub-scores SHALL remain null in the database
