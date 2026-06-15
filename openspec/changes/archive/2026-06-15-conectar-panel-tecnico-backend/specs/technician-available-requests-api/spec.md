## ADDED Requirements

### Requirement: GET /tecnicos/demo/solicitudes-disponibles endpoint

The backend SHALL expose a `GET /tecnicos/demo/solicitudes-disponibles` endpoint returning pending service requests that the demo technician (Carlos Mendoza, validated) can quote, filtered by the technician's assigned categories and zones.

#### Scenario: Returns matching pending solicitudes

- **WHEN** a GET request is made to `/tecnicos/demo/solicitudes-disponibles`
- **THEN** the response SHALL be HTTP 200 with an array of solicitudes
- **THEN** each solicitud SHALL include `id_solicitud`, `titulo`, `descripcion`, `direccion`, `estado`, `fecha_publicacion`, `categoria_nombre`, `zona_nombre`, `cotizaciones_count`, and `ya_cotizada_por_tecnico`
- **THEN** `cliente_nombre` SHALL be included when available from the client user record

#### Scenario: Filters by technician categories and zones

- **WHEN** a GET request is made to `/tecnicos/demo/solicitudes-disponibles`
- **THEN** only solicitudes whose `id_categoria` is in the demo technician's categories AND whose `id_zona` is in the demo technician's zones SHALL be returned
- **THEN** solicitudes in non-matching categories or zones SHALL NOT be included

#### Scenario: Only pending solicitudes returned

- **WHEN** a GET request is made to `/tecnicos/demo/solicitudes-disponibles`
- **THEN** only solicitudes with `estado = pendiente` SHALL be returned
- **THEN** solicitudes with estado `finalizada`, `en_proceso`, or `cancelada` SHALL NOT be included

#### Scenario: Indicates if technician already quoted

- **WHEN** the demo technician has an existing cotización for a pending solicitud
- **THEN** that solicitud SHALL still appear in the response
- **THEN** `ya_cotizada_por_tecnico` SHALL be `true` for that solicitud

#### Scenario: Returns empty array when none match

- **WHEN** no pending solicitudes match the demo technician's categories and zones
- **THEN** the response SHALL be HTTP 200 with an empty array

#### Scenario: Uses demo technician without auth

- **WHEN** a GET request is made without authentication headers
- **THEN** the endpoint SHALL resolve the demo technician by fixed demo user identifier server-side
- **THEN** no Supabase credentials or secrets SHALL be exposed in the response
