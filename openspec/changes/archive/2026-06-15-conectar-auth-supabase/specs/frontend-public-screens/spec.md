## MODIFIED Requirements

### Requirement: Login and registration page

The login and registration page SHALL use a single screen with visual tabs for sign-in and registration, visible role options for client and technician only, and real Supabase Auth login for the sign-in tab.

#### Scenario: Single screen with tabs and roles

- **WHEN** the user navigates to `/login`
- **THEN** the page displays visual tabs or sections for "Iniciar sesión" and "Crear cuenta" on one screen
- **THEN** the page displays role options for client and technician

#### Scenario: Client and technician options visible

- **WHEN** the user switches between sign-in and registration tabs
- **THEN** the page displays appropriate visual forms for the selected mode and role (client or technician)

#### Scenario: Administrator registration not available

- **WHEN** the user views the login and registration page
- **THEN** no public registration or login option for administrator role is displayed

#### Scenario: Real login submits to Supabase Auth

- **WHEN** the user submits the sign-in form with valid credentials
- **THEN** the application performs real authentication through Supabase Auth
- **THEN** the application resolves the ServiHogar profile through FastAPI `GET /auth/me`

#### Scenario: Login failure shows controlled error

- **WHEN** sign-in fails due to invalid credentials or missing profile
- **THEN** the page displays a controlled error message without exposing sensitive details

#### Scenario: Pending technician message after login

- **WHEN** a technician with `estado_validacion` equal to `pendiente` signs in successfully
- **THEN** the page displays a pending-account message instead of navigating to `/panel-tecnico`
