## ADDED Requirements

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
- **THEN** the public navbar links remain Inicio, Buscar técnicos, and Iniciar sesión only

#### Scenario: Demo navigation without reload

- **WHEN** the user clicks a footer demo link
- **THEN** the application navigates to the target route without a full page reload

## MODIFIED Requirements

### Requirement: Global base styles

The application SHALL apply global base styles including a minimal CSS reset, CSS custom properties for colors and typography, shared utility classes for buttons, cards, badges, grids, and containers, and a consistent light academic visual theme.

#### Scenario: Global styles applied

- **WHEN** the application loads
- **THEN** the page uses the defined global typography and color tokens from `styles.css`
- **THEN** shared utility classes for buttons, cards, badges, and summary grids are available to all components

#### Scenario: Document language and title

- **WHEN** the application HTML document is inspected
- **THEN** the `lang` attribute is `es`
- **THEN** the document title is `ServiHogar`

### Requirement: Static footer

The footer SHALL display static project information including the ServiHogar project name, an academic project mention, and demo access links to role dashboards labeled as academic prototype access.

#### Scenario: Footer content visible

- **WHEN** the user views any page in the application
- **THEN** the footer displays the ServiHogar name and academic project text
- **THEN** the footer displays "Acceso demo (prototipo académico)" with links to client, technician, and administrator panels
