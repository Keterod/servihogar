# technician-dashboard Specification

## Purpose
TBD - created by archiving change crear-flujo-tecnico-frontend. Update Purpose after archive.
## Requirements
### Requirement: Technician summary display

The technician dashboard SHALL display a summary of the simulated technician Carlos Mendoza including name, specialty (gasfitería/fontanería), zone (Huancayo Centro), rating, and validation status.

#### Scenario: Technician info visible on load

- **WHEN** the user navigates to `/panel-tecnico`
- **THEN** the page displays Carlos Mendoza's name, specialty, zone Huancayo Centro, and rating
- **THEN** the page displays validation status as validado for the demo technician

#### Scenario: Validation states visually supported

- **WHEN** the user views the validation badge
- **THEN** the UI supports visual distinction for pendiente, validado, and rechazado states

### Requirement: Available service requests as cards

The technician dashboard SHALL display available service requests fetched from `GET /tecnicos/demo/solicitudes-disponibles`, showing only pending requests matching the demo technician's categories and zones from the backend.

#### Scenario: Available requests loaded from backend

- **WHEN** the user navigates to `/panel-tecnico`
- **THEN** the page fetches available requests from `GET /tecnicos/demo/solicitudes-disponibles`
- **THEN** each request displays id, category name, description, zone name, publication date, approximate address, and estado

#### Scenario: Loading state for available requests

- **WHEN** the user navigates to `/panel-tecnico` and data is being fetched
- **THEN** the page SHALL show a loading indicator or message for the available requests section

#### Scenario: Error state for available requests

- **WHEN** the backend is unreachable or returns an error while loading available requests
- **THEN** the page SHALL display an error message indicating the backend is unavailable

#### Scenario: Empty state for available requests

- **WHEN** the backend returns an empty array of available requests
- **THEN** the page SHALL display a message indicating no solicitudes are available

#### Scenario: Finalized requests not shown

- **WHEN** the user views available service requests from the backend
- **THEN** solicitudes with estado finalizada SHALL NOT appear in the available list

#### Scenario: Navigate to request detail

- **WHEN** the user clicks "Ver detalle" on an available request
- **THEN** the application navigates to `/detalle-solicitud/{id_solicitud}` without a full page reload

#### Scenario: Visual cotización action without backend submit

- **WHEN** the user clicks "Enviar cotización" on an available request
- **THEN** the UI SHALL present the quotation form or equivalent visual flow
- **THEN** no HTTP POST request for cotización SHALL be made

### Requirement: Request selection and detail

The technician dashboard SHALL allow selecting an available request card and viewing its basic details.

#### Scenario: Select a request

- **WHEN** the user clicks an available service request card
- **THEN** the request is stored in solicitudSeleccionada Signal
- **THEN** the detail displays category, description, zone, tentative date, and approximate address

#### Scenario: Form cleared on selection change

- **WHEN** the user selects a different available request without submitting a quotation
- **THEN** the formCotizacion Signal is reset to empty values

### Requirement: Visual quotation form with signals

The technician dashboard SHALL provide a quotation form with estimated price (numeric, S/), estimated time (text), and propuesta fields managed by a formCotizacion Signal.

#### Scenario: Form visible when request selected

- **WHEN** the user selects an available service request
- **THEN** a quotation form with precio estimado, tiempo estimado, and propuesta fields is displayed

#### Scenario: Minimum validation

- **WHEN** the user attempts to submit a quotation
- **THEN** precio must be greater than 0 and all fields must be non-empty for submission to succeed

### Requirement: One quotation per request

The technician dashboard SHALL allow only one quotation per service request per session.

#### Scenario: Submit valid quotation

- **WHEN** the user fills a valid quotation and submits while validated
- **THEN** a new card appears in sent quotations with pendiente status and simulated send date
- **THEN** the request is removed from available requests
- **THEN** the request cannot be quoted again in the same session

#### Scenario: Quotation blocked when not validated

- **WHEN** the technician validation status is pendiente or rechazado
- **THEN** the submit quotation button is visually disabled

#### Scenario: No backend on submit

- **WHEN** the user submits a quotation
- **THEN** no HTTP request is made to the backend

### Requirement: Sent quotations as cards

The technician dashboard SHALL display sent quotations as cards with full quotation information.

#### Scenario: Initial sent quotation for solicitud id 1

- **WHEN** the user navigates to `/panel-tecnico`
- **THEN** at least one pre-loaded sent quotation for solicitud id 1 by Carlos Mendoza is visible with pendiente status

#### Scenario: Sent quotation card fields

- **WHEN** the user views a sent quotation card
- **THEN** the card displays associated request id, category, brief description, price, estimated time, propuesta, status (pendiente, aceptada, or rechazada), and simulated send date

#### Scenario: New quotation appears after submit

- **WHEN** the user submits a new quotation
- **THEN** the sent quotations list updates reactively

### Requirement: Accepted services as cards

The technician dashboard SHALL display accepted services as cards.

#### Scenario: Accepted services visible

- **WHEN** the user navigates to `/panel-tecnico`
- **THEN** at least one simulated accepted service card is displayed

#### Scenario: Accepted service card fields

- **WHEN** the user views an accepted service card
- **THEN** the card displays category, description, zone, simulated client name, status, and date

### Requirement: Single component layout

The technician dashboard SHALL be implemented as a single panel-tecnico component with vertically stacked sections and vertical scroll, without subcomponents or tabs.

#### Scenario: Single component structure

- **WHEN** the user navigates to `/panel-tecnico`
- **THEN** all dashboard sections render within the panel-tecnico component

### Requirement: Signals and computed values

The technician dashboard SHALL use Angular Signals for local state and computed() for derived values.

#### Scenario: Core signals defined

- **WHEN** the technician dashboard loads
- **THEN** tecnico, solicitudesDisponibles, cotizacionesEnviadas, serviciosAceptados, solicitudSeleccionada, formCotizacion, estadoValidacion, cargando, and error are managed with Signals

#### Scenario: Computed summary and validation

- **WHEN** the user views the dashboard
- **THEN** counts for available requests, pending-to-quote requests, and already-quoted available requests are computed from the backend-fetched solicitudesDisponibles Signal
- **THEN** counts for sent quotations and accepted services remain computed from their respective Signals
- **THEN** puedeEnviarCotizacion is computed from form validity, selected request, and validation status

### Requirement: Responsive technician dashboard

The technician dashboard SHALL adapt to small viewports without horizontal page overflow.

#### Scenario: Mobile layout

- **WHEN** the viewport width is 375px or less
- **THEN** dashboard sections and cards remain readable without horizontal page scroll

