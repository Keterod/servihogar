# frontend-public-screens Specification

## Purpose
TBD - created by archiving change crear-pantallas-publicas-frontend. Update Purpose after archive.
## Requirements
### Requirement: Home page content

The home page SHALL present the ServiHogar purpose with a brief hero mentioning the complete prototype flow, five official service categories, five usage steps including service rating, and a call-to-action to search for technicians.

#### Scenario: Hero and categories visible

- **WHEN** the user navigates to `/inicio`
- **THEN** the hero briefly mentions publishing requests, receiving quotations, and rating the service upon completion
- **THEN** the page displays the five official categories: Gasfitería menor, Electricidad básica, Mantenimiento de computadoras, Pintura básica, and Armado de muebles

#### Scenario: Five usage steps with responsive layout

- **WHEN** the user views the usage steps section
- **THEN** five steps are displayed covering search technicians, review profiles, publish a service request, choose a quotation, and rate the service after completion
- **THEN** steps use a grid layout on desktop and a vertical layout on viewports 375px or less

#### Scenario: Navigation to search from home

- **WHEN** the user clicks the primary call-to-action on the home page
- **THEN** the application navigates to `/buscar-tecnicos` without a full page reload

### Requirement: Technician search page

The search page SHALL display filters for category (populated from the backend), zone (populated from the backend), and minimum rating, and a list of technicians fetched from the backend `GET /tecnicos` endpoint, filtered accordingly.

#### Scenario: Filters populated from backend categories and zones

- **WHEN** the user navigates to `/buscar-tecnicos`
- **THEN** the category filter options SHALL be fetched from `GET /categorias`
- **THEN** the zone filter options SHALL be fetched from `GET /zonas`
- **THEN** the page displays at least three technician cards when the backend has seed data

#### Scenario: Filtering is client-side with Signals

- **WHEN** the user changes category, zone, or minimum rating filters
- **THEN** the displayed technician list updates using `computed()` and filtering is done client-side on the fetched data
- **THEN** no additional backend requests are made per filter change

#### Scenario: Loading state displayed

- **WHEN** the user navigates to `/buscar-tecnicos` and data is being fetched
- **THEN** the page SHALL show a loading indicator or message

#### Scenario: Error state displayed

- **WHEN** the backend is unreachable or returns an error
- **THEN** the page SHALL display an error message indicating the backend is unavailable
- **THEN** filter dropdowns SHALL be empty

#### Scenario: Empty state displayed

- **WHEN** the backend returns zero technicians
- **THEN** the page SHALL display a "no technicians found" message (distinct from loading and error states)

### Requirement: Technician profile page

The technician profile page SHALL display the selected technician's data fetched from `GET /tecnicos/{id}` including name, description, experience, rating, categories, zones, and portfolio images, with a single call-to-action to request service that navigates to `/solicitud-servicio` with the technician's ID and name as query params.

#### Scenario: Profile loaded from backend by ID

- **WHEN** the user navigates to `/perfil-tecnico/1`
- **THEN** the page fetches technician data from `GET /tecnicos/1`
- **THEN** the page displays the technician's full name, description, experience, rating, categories, zones, and portfolio images

#### Scenario: Loading state displayed

- **WHEN** the user navigates to `/perfil-tecnico/:id` and data is being fetched
- **THEN** the page SHALL show a loading indicator or message

#### Scenario: Error state displayed when backend is unavailable

- **WHEN** the backend is unreachable or returns an error for `/tecnicos/:id`
- **THEN** the page SHALL display an error message indicating the backend is unavailable

#### Scenario: Not-found state for invalid ID

- **WHEN** the backend returns 404 for `/tecnicos/:id`
- **THEN** the page SHALL display a "Técnico no encontrado" message

#### Scenario: Request service navigates to solicitud-servicio with query params

- **WHEN** the user clicks the "Solicitar cotización" button on the profile page
- **THEN** the application navigates to `/solicitud-servicio?tecnicoId={id}&tecnicoNombre={name}` without a full page reload
- **THEN** `tecnicoId` is the numeric ID of the displayed technician
- **THEN** `tecnicoNombre` is the full name (nombres + apellidos) of the displayed technician

#### Scenario: Navigation from search results passes ID

- **WHEN** the user clicks "Ver perfil" on a technician card in `/buscar-tecnicos`
- **THEN** the application navigates to `/perfil-tecnico/{id_tecnico}` without a full page reload

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

