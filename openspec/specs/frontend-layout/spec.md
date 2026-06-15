# frontend-layout Specification

## Purpose
TBD - created by archiving change crear-layout-base-frontend. Update Purpose after archive.
## Requirements
### Requirement: Application shell layout

The application SHALL display a persistent layout composed of a navbar at the top, a main content area in the center, and a footer at the bottom on every routed view.

#### Scenario: Layout visible on initial load

- **WHEN** the user opens the application at any valid route
- **THEN** the navbar, main content area, and footer are all visible

#### Scenario: Routed content renders inside layout

- **WHEN** the user navigates to `/inicio`, `/buscar-tecnicos`, or any other defined route
- **THEN** the route component renders inside the main content area between the navbar and footer

### Requirement: Public navbar navigation

The navbar SHALL display the application name or logo and three public navigation links: Inicio (`/inicio`), Buscar técnicos (`/buscar-tecnicos`), and Iniciar sesión (`/login`).

#### Scenario: Navbar shows public links only

- **WHEN** the user views the navbar
- **THEN** links to Inicio, Buscar técnicos, and Iniciar sesión are present
- **THEN** links to panel-cliente, panel-tecnico, and panel-administrador are NOT present in the navbar

#### Scenario: SPA navigation without page reload

- **WHEN** the user clicks a navbar link
- **THEN** the application navigates to the target route without a full page reload

### Requirement: Active route indication

The navbar SHALL visually distinguish the link that corresponds to the current active route.

#### Scenario: Active link highlighted on Inicio

- **WHEN** the user is on route `/inicio`
- **THEN** the Inicio link displays an active visual state distinct from inactive links

#### Scenario: Active link highlighted on other routes

- **WHEN** the user is on route `/buscar-tecnicos` or `/login`
- **THEN** the corresponding navbar link displays the active visual state

### Requirement: Static footer

The footer SHALL display static project information including the ServiHogar project name, an academic project mention, and demo access links to role dashboards labeled as academic prototype access.

#### Scenario: Footer content visible

- **WHEN** the user views any page in the application
- **THEN** the footer displays the ServiHogar name and academic project text
- **THEN** the footer displays "Acceso demo (prototipo académico)" with links to client, technician, and administrator panels

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

### Requirement: Responsive layout

The layout SHALL adapt to small viewports without horizontal overflow and with readable navigation.

#### Scenario: Small viewport adaptation

- **WHEN** the viewport width is 375px or less
- **THEN** the navbar links remain accessible without horizontal page scroll
- **THEN** the layout maintains navbar, content area, and footer structure

### Requirement: Vertical flex layout with sticky footer

The root application shell SHALL use a vertical flex layout where the main content area grows to fill available space and the footer stays at the bottom of the viewport on pages with minimal content.

#### Scenario: Footer at bottom on short pages

- **WHEN** the user views a page with little content (e.g. `/inicio` placeholder)
- **THEN** the footer is positioned at the bottom of the viewport

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

