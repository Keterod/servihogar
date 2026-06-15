## ADDED Requirements

### Requirement: GET /tecnicos/me/portafolio endpoint

The backend SHALL expose `GET /tecnicos/me/portafolio` requiring Bearer token and `require_tecnico_validado`. The response SHALL list all portafolio rows for the authenticated technician ordered by `fecha_subida` descending.

#### Scenario: Returns portfolio for authenticated technician

- **WHEN** a validated technician GETs `/tecnicos/me/portafolio`
- **THEN** the response SHALL be HTTP 200 with items containing `id_portafolio`, `titulo`, `descripcion`, `imagen_url`, `estado`, and `fecha_subida`

#### Scenario: Rejects without token

- **WHEN** GET is made without Authorization
- **THEN** the response SHALL be HTTP 401

#### Scenario: Rejects pending technician

- **WHEN** a technician with `estado_validacion=pendiente` requests the endpoint
- **THEN** the response SHALL be HTTP 403

### Requirement: POST /tecnicos/me/portafolio endpoint

The backend SHALL expose `POST /tecnicos/me/portafolio` requiring `require_tecnico_validado`. The body SHALL include `titulo`, `imagen_url`, and optional `descripcion`. The backend SHALL insert into `portafolio_tecnico` with `estado=visible` and `id_tecnico` from the token.

#### Scenario: Creates portfolio item after storage upload

- **WHEN** a validated technician POSTs `{ "titulo": "Instalación eléctrica", "descripcion": "Tablero nuevo", "imagen_url": "tecnicos/3/portafolio/1710000000-trabajo.webp" }`
- **THEN** the response SHALL be HTTP 201 with `id_portafolio`, `titulo`, `descripcion`, `imagen_url`, `estado`, and `fecha_subida`

#### Scenario: Validates imagen_url path prefix

- **WHEN** `imagen_url` does not start with `tecnicos/{id_tecnico}/portafolio/` for the authenticated technician
- **THEN** the response SHALL be HTTP 422

#### Scenario: Enforces portfolio item limit

- **WHEN** the technician already has 20 visible portfolio items
- **THEN** the response SHALL be HTTP 400

### Requirement: Public technician profile exposes visible portfolio only

The existing `GET /tecnicos/{id_tecnico}` SHALL continue returning only `portafolio_tecnico` rows with `estado=visible`. New uploads SHALL appear after successful POST.

#### Scenario: New upload visible on public profile

- **WHEN** a technician adds a portfolio item via POST and a public GET is made to `/tecnicos/{id}`
- **THEN** the new item SHALL appear in the `portafolio` array with resolvable `imagen_url`
