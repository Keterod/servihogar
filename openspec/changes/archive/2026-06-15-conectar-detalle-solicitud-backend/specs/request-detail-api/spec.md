## ADDED Requirements

### Requirement: GET /solicitudes/{id_solicitud} endpoint

The backend SHALL expose a `GET /solicitudes/{id_solicitud}` endpoint returning the full detail of a service request belonging to the demo client, including associated cotizaciones.

#### Scenario: Returns detail for existing demo-client solicitud

- **WHEN** a GET request is made to `/solicitudes/1` and solicitud 1 belongs to the demo client
- **THEN** the response SHALL be HTTP 200
- **THEN** the response SHALL include `id_solicitud`, `titulo`, `descripcion`, `direccion`, `estado`, `fecha_publicacion`, `categoria_nombre`, `zona_nombre`, and `cotizaciones`

#### Scenario: Returns cotizaciones with technician info

- **WHEN** a GET request is made to `/solicitudes/1` and solicitud 1 has cotizaciones in seed data
- **THEN** each cotización in the response SHALL include `id_cotizacion`, `id_tecnico`, `tecnico_nombre`, `precio`, `descripcion_propuesta`, `estado`, and `fecha_creacion`
- **THEN** `tecnico_descripcion` or equivalent specialty field SHALL be included when available from the technician profile

#### Scenario: Returns empty cotizaciones array

- **WHEN** a GET request is made to `/solicitudes/{id}` for a solicitud with no cotizaciones
- **THEN** the response SHALL be HTTP 200
- **THEN** `cotizaciones` SHALL be an empty array

#### Scenario: Returns 404 for nonexistent solicitud

- **WHEN** a GET request is made to `/solicitudes/99999`
- **THEN** the response SHALL be HTTP 404 with a descriptive error message

#### Scenario: Returns 404 for solicitud not owned by demo client

- **WHEN** a GET request is made to `/solicitudes/{id}` for a solicitud that exists but belongs to a different client
- **THEN** the response SHALL be HTTP 404 with a descriptive error message
