## MODIFIED Requirements

### Requirement: Public navbar navigation

The navbar SHALL display the application name or logo, public navigation links for Inicio and Buscar técnicos, and session-aware authentication actions that route to `/login` when logged out or show the authenticated user and logout when logged in.

#### Scenario: Navbar shows public links only

- **WHEN** the user views the navbar
- **THEN** links to Inicio and Buscar técnicos are present
- **THEN** links to panel-cliente, panel-tecnico, and panel-administrador are NOT present in the navbar

#### Scenario: Navbar shows login actions when logged out

- **WHEN** no authenticated Supabase session is active
- **THEN** the navbar displays `Iniciar sesión` and `Registrarse` actions routing to `/login`

#### Scenario: Navbar shows user session when logged in

- **WHEN** an authenticated Supabase session and ServiHogar profile are available
- **THEN** the navbar displays the user's display name
- **THEN** the navbar displays a `Cerrar sesión` action

#### Scenario: SPA navigation without page reload

- **WHEN** the user clicks a navbar link or auth action
- **THEN** the application navigates to the target route or performs logout without a full page reload

## MODIFIED Requirements

### Requirement: Demo role access in footer

The footer SHALL provide separate demo navigation links to role dashboards on all routes without adding those links to the public navbar.

#### Scenario: Demo links visible on all routes

- **WHEN** the user views the footer on any page including role dashboards
- **THEN** demo links to `/panel-cliente`, `/panel-tecnico`, and `/panel-administrador` are displayed
- **THEN** the demo section is labeled exactly "Acceso demo (prototipo académico)"

#### Scenario: Only three role demo links

- **WHEN** the user views the footer demo section
- **THEN** links are limited to panel cliente, panel técnico, and panel administrador
- **THEN** links to solicitud-servicio, detalle-solicitud, or valorar-servicio are NOT present in the demo section

#### Scenario: Demo links not in navbar

- **WHEN** the user views the navbar
- **THEN** links to panel-cliente, panel-tecnico, and panel-administrador are NOT present in the navbar
- **THEN** public navigation remains limited to Inicio, Buscar técnicos, and session-aware auth actions

#### Scenario: Demo navigation without reload

- **WHEN** the user clicks a footer demo link
- **THEN** the application navigates to the target route without a full page reload
