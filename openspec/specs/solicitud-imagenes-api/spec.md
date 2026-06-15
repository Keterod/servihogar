# solicitud-imagenes-api Specification

## Purpose
TBD - created by archiving change implementar-evidencias-imagenes. Update Purpose after archive.
## Requirements
### Requirement: POST /solicitudes/{id_solicitud}/imagenes endpoint

The backend SHALL expose `POST /solicitudes/{id_solicitud}/imagenes` requiring Bearer token and `require_cliente`. The authenticated client MUST own the solicitud. The endpoint SHALL insert a row into `imagenes_solicitud` with `imagen_url` and optional `descripcion`.

#### Scenario: Registers image metadata for owned solicitud

- **WHEN** an authenticated client POSTs `{ "imagen_url": "solicitudes/12/1710000000-foto.jpg", "descripcion": "Fuga visible" }` for a solicitud they own
- **THEN** the response SHALL be HTTP 201 with `id_imagen`, `id_solicitud`, `imagen_url`, and `fecha_subida`

#### Scenario: Rejects solicitud not owned by client

- **WHEN** an authenticated client POSTs image metadata for a solicitud belonging to another client
- **THEN** the response SHALL be HTTP 403

#### Scenario: Rejects without token

- **WHEN** a POST is made without Authorization header
- **THEN** the response SHALL be HTTP 401

#### Scenario: Enforces maximum images per solicitud

- **WHEN** the solicitud already has 5 images registered
- **THEN** the response SHALL be HTTP 400 with a descriptive error

#### Scenario: Validates imagen_url path prefix

- **WHEN** `imagen_url` does not start with `solicitudes/{id_solicitud}/`
- **THEN** the response SHALL be HTTP 422

### Requirement: GET /solicitudes/{id_solicitud}/imagenes endpoint

The backend SHALL expose `GET /solicitudes/{id_solicitud}/imagenes` requiring Bearer token. Access SHALL follow the same rules as `GET /solicitudes/{id_solicitud}` (cliente owner, técnico autorizado, administrador).

#### Scenario: Returns images for authorized user

- **WHEN** an authorized user GETs `/solicitudes/12/imagenes`
- **THEN** the response SHALL be HTTP 200 with an array of `{ id_imagen, imagen_url, descripcion, fecha_subida }`

#### Scenario: Returns empty array when no images

- **WHEN** the solicitud has no rows in `imagenes_solicitud`
- **THEN** the response SHALL be HTTP 200 with `[]`

#### Scenario: Forbidden for unauthorized user

- **WHEN** a user without access to the solicitud requests images
- **THEN** the response SHALL be HTTP 403 or 404 per existing detalle policy

### Requirement: Solicitud detail includes imagenes array

The backend SHALL include an `imagenes` array in `GET /solicitudes/{id_solicitud}` responses when the caller is authorized, loaded from `imagenes_solicitud` ordered by `fecha_subida`.

#### Scenario: Detail response includes imagenes

- **WHEN** an authorized GET is made to `/solicitudes/12` and solicitud 12 has 2 images
- **THEN** the response SHALL include `imagenes` with 2 items each containing `id_imagen`, `imagen_url`, `descripcion`, and `fecha_subida`

