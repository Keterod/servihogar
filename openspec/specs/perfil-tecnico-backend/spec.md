# perfil-tecnico-backend Specification

## Purpose
TBD - created by syncing delta from change conectar-perfil-tecnico-backend.

## Requirements

### Requirement: GET /tecnicos/{id_tecnico} endpoint

The backend SHALL expose a `GET /tecnicos/{id_tecnico}` endpoint returning the full technician profile including categories, zones, and portfolio items.

#### Scenario: Returns full profile for existing technician

- **WHEN** a GET request is made to `/tecnicos/1`
- **THEN** the response SHALL include `id_tecnico`, `nombres`, `apellidos`, `descripcion`, `experiencia_anios`, `calificacion`, `categorias`, `zonas`, and `portafolio`
- **THEN** the response SHALL contain at least one category and one zone for Carlos Mendoza

#### Scenario: Returns 404 for nonexistent technician

- **WHEN** a GET request is made to `/tecnicos/9999`
- **THEN** the response SHALL be HTTP 404 with a descriptive error message

#### Scenario: Portfolio items include image URLs

- **WHEN** a GET request is made to `/tecnicos/1`
- **THEN** the `portafolio` array SHALL contain items with `id_portafolio`, `titulo`, `descripcion`, and `imagen_url`
