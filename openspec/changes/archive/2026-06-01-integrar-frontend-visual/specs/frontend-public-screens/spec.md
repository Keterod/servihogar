## MODIFIED Requirements

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
