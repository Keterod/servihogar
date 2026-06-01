## ADDED Requirements

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

The footer SHALL display static project information including the ServiHogar project name and an academic project mention.

#### Scenario: Footer content visible

- **WHEN** the user views any page in the application
- **THEN** the footer displays the ServiHogar name and academic project text

### Requirement: Global base styles

The application SHALL apply global base styles including a minimal CSS reset, CSS custom properties for colors and typography, and a consistent light academic visual theme.

#### Scenario: Global styles applied

- **WHEN** the application loads
- **THEN** the page uses the defined global typography and color tokens from `styles.css`

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
