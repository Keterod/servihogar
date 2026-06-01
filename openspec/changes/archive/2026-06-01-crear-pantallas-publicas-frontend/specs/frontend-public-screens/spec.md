## ADDED Requirements

### Requirement: Home page content

The home page SHALL present the ServiHogar purpose, featured service categories, usage steps reflecting the real ServiHogar flow, and a call-to-action to search for technicians.

#### Scenario: Purpose and categories visible

- **WHEN** the user navigates to `/inicio`
- **THEN** the page displays a description of ServiHogar's purpose
- **THEN** the page displays at least three featured service categories
- **THEN** the page displays four usage steps: search technicians by category and zone, review profiles and ratings, publish a service request, and technicians send quotations for the client to choose from

#### Scenario: Navigation to search from home

- **WHEN** the user clicks the primary call-to-action on the home page
- **THEN** the application navigates to `/buscar-tecnicos` without a full page reload

### Requirement: Technician search page

The search page SHALL display functional in-memory filters for category, zone, and minimum rating, and a list of simulated technicians filtered accordingly.

#### Scenario: Filters and results visible

- **WHEN** the user navigates to `/buscar-tecnicos`
- **THEN** the page displays filter controls for category, zone, and minimum rating
- **THEN** the page displays at least three simulated technician cards with name, specialty, zone, and rating

#### Scenario: In-memory filtering

- **WHEN** the user changes category, zone, or minimum rating filters
- **THEN** the displayed technician list updates to show only simulated technicians matching the selected criteria
- **THEN** no HTTP requests are made to the backend

#### Scenario: Navigate to technician profile

- **WHEN** the user selects a simulated technician from the search results
- **THEN** the application navigates to `/perfil-tecnico` without a full page reload

### Requirement: Technician profile page

The technician profile page SHALL display complete referential information for a simulated technician including specialty, experience, zone, and rating, with a single call-to-action to request service that navigates to login.

#### Scenario: Profile information visible

- **WHEN** the user navigates to `/perfil-tecnico`
- **THEN** the page displays the technician's name, specialty, experience, zone, and rating
- **THEN** the page displays a button labeled "Solicitar servicio"
- **THEN** the page does NOT display a "Solicitar cotización" button or equivalent client-facing quotation action

#### Scenario: Request service navigates to login

- **WHEN** the user clicks the "Solicitar servicio" button on the profile page
- **THEN** the application navigates to `/login` without a full page reload
- **THEN** auxiliary text is visible near the button stating that the user must sign in as a client to continue

### Requirement: Login and registration page

The login and registration page SHALL use a single screen with visual tabs for sign-in and registration, and visible role options for client and technician only.

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

#### Scenario: Forms are visual only

- **WHEN** the user interacts with login or registration forms
- **THEN** no real authentication is performed
- **THEN** form submission does not connect to a backend API

### Requirement: Public flow navigation

The public screens SHALL support the basic navigation flow from home through search, technician profile, and login/registration using existing routes.

#### Scenario: Existing routes remain functional

- **WHEN** the user navigates to `/inicio`, `/buscar-tecnicos`, `/perfil-tecnico`, or `/login`
- **THEN** each route renders its respective public screen within the application layout

#### Scenario: Navbar navigation preserved

- **WHEN** the user uses the navbar links for Inicio, Buscar técnicos, or Iniciar sesión
- **THEN** navigation works without a full page reload
- **THEN** the target public screen displays with its visual content

### Requirement: Responsive public screens

The four public screens SHALL adapt to small viewports with readable content and without horizontal page overflow.

#### Scenario: Mobile layout on public screens

- **WHEN** the viewport width is 375px or less
- **THEN** each public screen content remains readable and accessible
- **THEN** lists, filters, and profile sections adapt without horizontal page scroll

### Requirement: Simulated data only

The public screens SHALL use static or simulated data defined within components without connecting to the backend API.

#### Scenario: No backend calls from public screens

- **WHEN** the user views or interacts with the four public screens
- **THEN** no HTTP requests are made to the FastAPI backend
- **THEN** displayed technician and category data comes from static or in-component simulated data
