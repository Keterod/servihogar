# perfil-tecnico-backend Specification

## Purpose
TBD - created by syncing delta from change conectar-perfil-tecnico-backend.
## Requirements
### Requirement: GET /tecnicos/{id_tecnico} endpoint

The backend SHALL expose a `GET /tecnicos/{id_tecnico}` endpoint returning the full technician profile including categories, zones, and visible portfolio items with Storage-backed `imagen_url` values.

#### Scenario: Returns full profile for existing technician

- **WHEN** a GET request is made to `/tecnicos/1`
- **THEN** the response SHALL include `id_tecnico`, `nombres`, `apellidos`, `descripcion`, `experiencia_anios`, `calificacion`, `categorias`, `zonas`, and `portafolio`

#### Scenario: Returns 404 for nonexistent technician

- **WHEN** a GET request is made to `/tecnicos/9999`
- **THEN** the response SHALL be HTTP 404 with a descriptive error message

#### Scenario: Portfolio items include resolvable image URLs

- **WHEN** a GET request is made to `/tecnicos/1`
- **THEN** each `portafolio` item SHALL include `id_portafolio`, `titulo`, `descripcion`, and `imagen_url` pointing to Supabase Storage

#### Scenario: Hidden portfolio items excluded

- **WHEN** a technician has items with `estado=oculto`
- **THEN** those items SHALL NOT appear in the public profile response

