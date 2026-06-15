# client-dashboard-api Specification

## Purpose

Provides a backend endpoint for fetching a demo client's service requests with category and zone names, and cotización count.

## Requirements

### Requirement: GET /clientes/demo/solicitudes endpoint

The backend SHALL expose a `GET /clientes/demo/solicitudes` endpoint returning all service requests for the demo client, including category name, zone name, and cotización count.

#### Scenario: Returns requests for demo client

- **WHEN** a GET request is made to `/clientes/demo/solicitudes`
- **THEN** the response SHALL be HTTP 200 with an array of solicitudes
- **THEN** each solicitud SHALL include `id_solicitud`, `titulo`, `descripcion`, `direccion`, `estado`, `fecha_publicacion`, `categoria_nombre`, `zona_nombre`, and `cotizaciones_count`

#### Scenario: Returns empty array when no requests exist

- **WHEN** the demo client has no service requests
- **THEN** the response SHALL be HTTP 200 with an empty array
