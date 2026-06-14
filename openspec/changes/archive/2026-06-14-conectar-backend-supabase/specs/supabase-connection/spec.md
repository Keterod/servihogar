## ADDED Requirements

### Requirement: Centralized Supabase client

The application SHALL initialize a single Supabase client from the centralized `Settings` config, accessible to all repository classes.

#### Scenario: Client created from settings
- **WHEN** the application starts
- **THEN** a Supabase client SHALL be created using `SUPABASE_URL` and `SUPABASE_ANON_KEY` from `Settings`

### Requirement: GET /categorias returns categorias_servicio

The application SHALL expose a public `GET /categorias` endpoint that returns all active categorias from Supabase.

#### Scenario: Returns categorias list
- **WHEN** a client sends `GET /categorias`
- **THEN** the server SHALL respond with HTTP 200 and a JSON array of objects with `id_categoria`, `nombre`, and `descripcion`

### Requirement: GET /zonas returns zonas

The application SHALL expose a public `GET /zonas` endpoint that returns all active zonas from Supabase.

#### Scenario: Returns zonas list
- **WHEN** a client sends `GET /zonas`
- **THEN** the server SHALL respond with HTTP 200 and a JSON array of objects with `id_zona`, `nombre`, and `id_ciudad`

### Requirement: GET /tecnicos returns tecnicos with usuario data

The application SHALL expose a public `GET /tecnicos` endpoint that returns técnicos whose `estado_validacion` is `'validado'`, including basic user info.

#### Scenario: Returns tecnicos list with user names
- **WHEN** a client sends `GET /tecnicos`
- **THEN** the server SHALL respond with HTTP 200 and a JSON array of objects containing `id_tecnico`, `nombres`, `apellidos`, `descripcion`, `experiencia_anios`, and `calificacion` (average valoracion puntuacion)

### Requirement: Health endpoint still works

The existing `GET /health` endpoint SHALL continue to function after adding new routers.

#### Scenario: Health check unaffected
- **WHEN** a client sends `GET /health`
- **THEN** the server SHALL still respond with HTTP 200 and `{"status": "ok"}`
