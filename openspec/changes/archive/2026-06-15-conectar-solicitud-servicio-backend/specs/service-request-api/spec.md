## ADDED Requirements

### Requirement: POST /solicitudes endpoint

The backend SHALL expose a `POST /solicitudes` endpoint that creates a service request in the `solicitudes_servicio` table using a demo client ID.

#### Scenario: Creates solicitud with valid data

- **WHEN** a POST request is made to `/solicitudes` with `id_categoria`, `titulo`, `descripcion`, `direccion_referencia`, and `id_zona`
- **THEN** the response SHALL be HTTP 201 with the created solicitud including `id_solicitud`, `estado`, and `fecha_publicacion`

#### Scenario: Rejects missing required fields

- **WHEN** a POST request is made to `/solicitudes` missing `id_categoria` or `descripcion`
- **THEN** the response SHALL be HTTP 422 with validation error details

#### Scenario: Accepts optional id_tecnico

- **WHEN** a POST request is made to `/solicitudes` with an `id_tecnico` field
- **THEN** the endpoint SHALL accept the field but not insert it into the database
- **THEN** the response SHALL be HTTP 201
