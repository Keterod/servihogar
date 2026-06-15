## MODIFIED Requirements

### Requirement: POST /solicitudes endpoint

The backend SHALL expose a `POST /solicitudes` endpoint that creates a service request in the `solicitudes_servicio` table for the authenticated client (`require_cliente`). Image metadata SHALL be registered separately via `POST /solicitudes/{id_solicitud}/imagenes` after Storage upload.

#### Scenario: Creates solicitud for authenticated client

- **WHEN** an authenticated client POSTs to `/solicitudes` with `id_categoria`, `titulo`, `descripcion`, `direccion_referencia`, and `id_zona`
- **THEN** the response SHALL be HTTP 201 with the created solicitud including `id_solicitud`, `id_cliente`, `estado`, and `fecha_publicacion`

#### Scenario: Rejects missing required fields

- **WHEN** a POST request is made to `/solicitudes` missing `id_categoria` or `descripcion`
- **THEN** the response SHALL be HTTP 422 with validation error details

#### Scenario: Rejects without token

- **WHEN** POST is made without Authorization
- **THEN** the response SHALL be HTTP 401

#### Scenario: Accepts optional id_tecnico without persisting

- **WHEN** a POST request includes an `id_tecnico` field
- **THEN** the endpoint SHALL accept the field but not insert it into the database
- **THEN** the response SHALL be HTTP 201
