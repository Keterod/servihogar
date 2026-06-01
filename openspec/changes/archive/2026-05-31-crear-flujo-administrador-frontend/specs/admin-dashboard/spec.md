## ADDED Requirements

### Requirement: Admin dashboard summary

The admin dashboard SHALL display a general system summary grid with six counters derived using computed() from Signals.

#### Scenario: Six summary counters visible

- **WHEN** the user navigates to `/panel-administrador`
- **THEN** the page displays a grid with counters for total technicians, pending technicians, validated technicians, rejected technicians, categories, and registered users

#### Scenario: Counters use computed

- **WHEN** the admin dashboard loads or technician validation changes
- **THEN** summary counts are derived using computed() from technician, category, and user Signals

#### Scenario: Requests and quotations not in summary

- **WHEN** the user views the summary section
- **THEN** solicitudes and cotizaciones metrics are NOT displayed in the summary grid

### Requirement: Technician validation management

The admin dashboard SHALL display technicians in a single list with validation status badges and allow visual validate or reject actions for pending technicians only.

#### Scenario: Technician fields displayed

- **WHEN** the user views the technician list
- **THEN** each technician displays id, name, specialty, zone, validation status badge, and registration date

#### Scenario: Single list with badges

- **WHEN** the user views technicians
- **THEN** all technicians appear in one list (not grouped into separate sections) with status badges

#### Scenario: Initial validation states

- **WHEN** the admin dashboard loads
- **THEN** Carlos Mendoza appears with validado status
- **THEN** at least one technician appears as pendiente and one as rechazado
- **THEN** Roberto Salas does NOT appear in the technician list

#### Scenario: Validate pending technician

- **WHEN** the user clicks validate on a pendiente technician
- **THEN** the technician status updates to validado via Signal update
- **THEN** summary counters update reactively
- **THEN** a brief confirmation message is displayed (e.g. "Técnico validado correctamente")

#### Scenario: Reject pending technician

- **WHEN** the user clicks reject on a pendiente technician
- **THEN** the technician status updates to rechazado via Signal update
- **THEN** a brief confirmation message is displayed (e.g. "Técnico rechazado correctamente")

#### Scenario: No actions on validated or rejected

- **WHEN** a technician is validado or rechazado
- **THEN** validate and reject buttons are not available
- **THEN** no reversal actions are available in this sprint

### Requirement: Service category management

The admin dashboard SHALL display service categories using client-flow nomenclature and allow visually adding new categories.

#### Scenario: Initial categories listed

- **WHEN** the user views the categories section
- **THEN** at least five categories are displayed including Gasfitería menor, Electricidad básica, Mantenimiento de computadoras, Pintura básica, and Armado de muebles

#### Scenario: Add category with optional description

- **WHEN** the user fills a required category name and optional description and submits
- **THEN** a new category appears in the list and the form is cleared

#### Scenario: Duplicate category name prevented

- **WHEN** the user attempts to add a category with a name that already exists
- **THEN** a simple message is shown and the category is NOT added

#### Scenario: No backend on add category

- **WHEN** the user adds a category
- **THEN** no HTTP request is made to the backend

### Requirement: Registered users display

The admin dashboard SHALL display five simulated registered users with role and status.

#### Scenario: Five users visible

- **WHEN** the user views the users section
- **THEN** five users are displayed including Mariana Quispe (cliente), Carlos Mendoza (tecnico), Luis Arango (tecnico), Rosa Huamán (tecnico), and Administrador Demo (administrador)

#### Scenario: User role and status displayed

- **WHEN** the user views a registered user
- **THEN** the user displays name, role, and status (activo, pendiente, or rechazado)

### Requirement: Basic reports display

The admin dashboard SHALL display basic system reports as cards with fixed narrative values and computed values where applicable.

#### Scenario: Five report metrics visible

- **WHEN** the user views the reports section
- **THEN** cards display solicitudes publicadas, cotizaciones registradas, servicios finalizados, técnicos activos, and usuarios registrados

#### Scenario: Mixed fixed and computed report values

- **WHEN** the user views reports
- **THEN** solicitudes publicadas, cotizaciones registradas, and servicios finalizados use fixed narrative values from the reportes Signal
- **THEN** técnicos activos and usuarios registrados use computed values from local Signals

### Requirement: Single component layout with signals

The admin dashboard SHALL be implemented as a single panel-administrador component using Angular Signals for all local state.

#### Scenario: Single component structure

- **WHEN** the user navigates to `/panel-administrador`
- **THEN** all sections render within panel-administrador without subcomponents or tabs

#### Scenario: Core signals defined

- **WHEN** the admin dashboard loads
- **THEN** tecnicos, categorias, usuarios, reportes, formCategoria, and mensajeAccion are managed with Signals

### Requirement: Responsive admin dashboard

The admin dashboard SHALL adapt to small viewports without horizontal page overflow.

#### Scenario: Mobile layout

- **WHEN** the viewport width is 375px or less
- **THEN** dashboard sections remain readable without horizontal page scroll
