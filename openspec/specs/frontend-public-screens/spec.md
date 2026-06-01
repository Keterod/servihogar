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

The search page SHALL display functional in-memory filters for category using the official category vocabulary, zone, and minimum rating, and a list of simulated technicians filtered accordingly.

#### Scenario: Filters aligned with official categories

- **WHEN** the user navigates to `/buscar-tecnicos`
- **THEN** the category filter includes the five official categories (Gasfitería menor, Electricidad básica, Mantenimiento de computadoras, Pintura básica, Armado de muebles)
- **THEN** the page displays at least three simulated technician cards with name, specialty, zone, and rating

#### Scenario: Carlos Mendoza in search results

- **WHEN** the user views simulated technicians
- **THEN** Carlos Mendoza appears with Gasfitería menor specialty and Huancayo Centro zone

#### Scenario: In-memory filtering unchanged

- **WHEN** the user changes category, zone, or minimum rating filters
- **THEN** the displayed technician list updates to show only simulated technicians matching the selected criteria
- **THEN** no HTTP requests are made to the backend

#### Scenario: Navigate to technician profile

- **WHEN** the user selects a simulated technician from the search results
- **THEN** the application navigates to `/perfil-tecnico` without a full page reload

### Requirement: Technician profile page

The technician profile page SHALL display complete referential information for Carlos Mendoza including Gasfitería menor specialty, Huancayo Centro zone, experience, and rating, with a single call-to-action to request service that navigates to login.

#### Scenario: Carlos Mendoza profile information visible

- **WHEN** the user navigates to `/perfil-tecnico`
- **THEN** the page displays Carlos Mendoza's name, Gasfitería menor specialty, Huancayo Centro zone, experience, and rating
- **THEN** the page displays a button labeled "Solicitar servicio"

#### Scenario: Request service navigates to login

- **WHEN** the user clicks the "Solicitar servicio" button on the profile page
- **THEN** the application navigates to `/login` without a full page reload

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

