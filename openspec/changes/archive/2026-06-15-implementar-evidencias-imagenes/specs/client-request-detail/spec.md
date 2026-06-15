## ADDED Requirements

### Requirement: Solicitud image gallery

The request detail screen SHALL display images returned in the `imagenes` array from `GET /solicitudes/{id_solicitud}` for authorized viewers.

#### Scenario: Gallery shows solicitud photos

- **WHEN** the user views `/detalle-solicitud/12` and the API returns 3 images
- **THEN** the page SHALL display all 3 with resolvable URLs

#### Scenario: Technician view includes gallery

- **WHEN** a technician opens detalle with `from=tecnico` and is authorized
- **THEN** the same gallery SHALL be visible read-only

#### Scenario: No mock images

- **WHEN** the API returns an empty `imagenes` array
- **THEN** the page SHALL NOT display placeholder stock photos
