# auth-me-api Specification

## Purpose
TBD - created by archiving change conectar-auth-supabase. Update Purpose after archive.
## Requirements
### Requirement: Authenticated current user endpoint

The backend SHALL expose `GET /auth/me` that returns the authenticated ServiHogar user profile for a valid Supabase JWT.

#### Scenario: Valid token returns profile

- **WHEN** a request includes `Authorization: Bearer <valid_supabase_access_token>`
- **THEN** the backend returns HTTP 200 with the linked user profile

#### Scenario: Missing authorization header

- **WHEN** a request is made without an `Authorization` header
- **THEN** the backend returns HTTP 401

#### Scenario: Invalid or expired token

- **WHEN** a request includes a missing, malformed, or expired Bearer token
- **THEN** the backend returns HTTP 401

#### Scenario: Auth user without usuarios row

- **WHEN** the Bearer token is valid in Supabase Auth but no matching row exists in `usuarios.auth_user_id`
- **THEN** the backend returns HTTP 404

### Requirement: Current user response fields

The `GET /auth/me` response SHALL include identity and role metadata needed by the frontend for routing and guards.

#### Scenario: Response includes core identity fields

- **WHEN** the authenticated user has a linked `usuarios` row
- **THEN** the response includes `id_usuario`, `auth_user_id`, `nombres`, `apellidos`, `email`, `tipo_usuario`, and `estado`

#### Scenario: Client profile identifiers included

- **WHEN** the authenticated user is linked to a `clientes` row
- **THEN** the response includes `tipo_usuario` equal to `cliente`
- **THEN** the response includes `id_cliente`
- **THEN** `id_tecnico`, `id_administrador`, and `estado_validacion` are null or omitted when not applicable

#### Scenario: Validated technician profile identifiers included

- **WHEN** the authenticated user is linked to a `tecnicos` row
- **THEN** the response includes `tipo_usuario` equal to `tecnico`
- **THEN** the response includes `id_tecnico` and `estado_validacion`

#### Scenario: Administrator profile identifiers included

- **WHEN** the authenticated user is linked to an `administradores` row
- **THEN** the response includes `tipo_usuario` equal to `administrador`
- **THEN** the response includes `id_administrador`

#### Scenario: Email comes from Supabase Auth

- **WHEN** the authenticated user profile is returned
- **THEN** `email` is taken from the validated Supabase Auth user, not from a non-existent `usuarios.email` column

### Requirement: Auth endpoint architecture and scope

The auth endpoint SHALL follow backend layering and preserve existing demo APIs.

#### Scenario: Endpoint uses service and repository layers

- **WHEN** `GET /auth/me` handles a request
- **THEN** the FastAPI route delegates token validation and profile assembly to services and repositories
- **THEN** request and response data are validated with Pydantic schemas

#### Scenario: Demo endpoints remain available

- **WHEN** the auth endpoint is added
- **THEN** existing demo and public business endpoints remain registered and unchanged in this change

#### Scenario: No database migration required

- **WHEN** the auth endpoint is implemented
- **THEN** `database/schema.sql` and `database/seed.sql` are not modified

#### Scenario: No service role exposure

- **WHEN** the auth endpoint is implemented
- **THEN** service role credentials are not returned to clients and are not required by the frontend

