## MODIFIED Requirements

### Requirement: GET /solicitudes/{id_solicitud} endpoint

The backend SHALL expose a `GET /solicitudes/{id_solicitud}` endpoint requiring Bearer token. Access SHALL be granted to the owning client, authorized technicians, or administrators per role-based rules. The response SHALL include solicitud detail, cotizaciones, and an `imagenes` array.

#### Scenario: Returns detail for authorized client

- **WHEN** the owning client GETs `/solicitudes/12`
- **THEN** the response SHALL be HTTP 200
- **THEN** the response SHALL include `id_solicitud`, `titulo`, `descripcion`, `direccion`, `estado`, `fecha_publicacion`, `categoria_nombre`, `zona_nombre`, `cotizaciones`, and `imagenes`

#### Scenario: Returns cotizaciones with technician info

- **WHEN** the solicitud has cotizaciones
- **THEN** each cotización SHALL include `id_cotizacion`, `id_tecnico`, `tecnico_nombre`, `precio`, `descripcion_propuesta`, `estado`, and `fecha_creacion`

#### Scenario: Returns empty imagenes array

- **WHEN** the solicitud has no images
- **THEN** `imagenes` SHALL be an empty array

#### Scenario: Returns 401 without token

- **WHEN** GET is made without Authorization
- **THEN** the response SHALL be HTTP 401

#### Scenario: Returns 403 for unauthorized user

- **WHEN** a user without access GETs the solicitud
- **THEN** the response SHALL be HTTP 403

#### Scenario: Returns 404 for nonexistent solicitud

- **WHEN** GET is made to `/solicitudes/99999`
- **THEN** the response SHALL be HTTP 404
