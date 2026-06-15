# client-service-request Specification

## Purpose
Provides the service request form for clients to publish new service requests.
## Requirements
### Requirement: Service request form fields

The service request form SHALL display six input fields: category (select populated from backend), zone (select populated from backend), description (textarea), tentative date (date input), preferred schedule (select), and approximate address (text input). When a technician is referenced via query params, a technician info card SHALL be displayed.

#### Scenario: Form fields visible

- **WHEN** the user navigates to `/solicitud-servicio`
- **THEN** the form displays select controls for category and zone populated from `GET /categorias` and `GET /zonas`
- **THEN** the form displays a textarea for description
- **THEN** the form displays a date input for tentative date
- **THEN** the form displays a select for preferred schedule
- **THEN** the form displays a text input for approximate address

#### Scenario: Category options from backend

- **WHEN** the user interacts with the category select
- **THEN** the options are fetched from `GET /categorias`
- **THEN** categories include at least Gasfitería menor, Electricidad básica, and Pintura básica when seed data exists

#### Scenario: Zone options from backend

- **WHEN** the user interacts with the zone select
- **THEN** the options are fetched from `GET /zonas`
- **THEN** zones include at least Huancayo Centro and El Tambo when seed data exists

#### Scenario: Technician reference from query params

- **WHEN** the user navigates to `/solicitud-servicio?tecnicoId=1&tecnicoNombre=Carlos+Mendoza`
- **THEN** the page displays a technician card with the name "Carlos Mendoza"
- **THEN** the card includes a reference to the selected technician

### Requirement: Form uses signals for state

The service request form SHALL use Angular Signals to manage the state of each form field.

#### Scenario: Signals for form fields

- **WHEN** the user fills in the form fields
- **THEN** each field value is stored in an Angular Signal
- **THEN** the Signal values update on input changes

### Requirement: Form submission

The form SHALL submit the service request to `POST /solicitudes` and display success or error feedback.

#### Scenario: Submit button present

- **WHEN** the user views the service request form
- **THEN** a submit button labeled "Enviar solicitud" is visible
- **THEN** the button is disabled when required fields are empty

#### Scenario: Submission via POST /solicitudes

- **WHEN** the user fills all required fields and clicks submit
- **THEN** the form sends a POST request to `/solicitudes` with the field data
- **THEN** the form shows a loading state while the request is in flight
- **THEN** on success the form displays a confirmation message with the solicitud details
- **THEN** a button to navigate to `/panel-cliente` is displayed

#### Scenario: Error state on backend failure

- **WHEN** the backend is unreachable or returns an error
- **THEN** the form SHALL display an error message
- **THEN** the form fields remain editable so the user can retry

### Requirement: Form navigation

The service request screen SHALL be accessible via the existing route.

#### Scenario: Route accessible

- **WHEN** the user navigates to `/solicitud-servicio`
- **THEN** the service request form is displayed within the application layout

#### Scenario: Navigation after submission

- **WHEN** the user clicks the navigation button after submission
- **THEN** the application navigates to `/panel-cliente` without a full page reload

#### Scenario: Route accessible from perfil-tecnico

- **WHEN** the user clicks "Solicitar cotización" on `/perfil-tecnico/1`
- **THEN** the application navigates to `/solicitud-servicio?tecnicoId=1&tecnicoNombre=Carlos+Mendoza` without a full page reload

### Requirement: Optional image attachments on service request

The service request form SHALL allow the authenticated client to attach up to 5 optional photos that are uploaded to Supabase Storage and registered via the backend after the solicitud is created.

#### Scenario: Image attachment control visible

- **WHEN** an authenticated client navigates to `/solicitud-servicio`
- **THEN** the form SHALL display a file input or drop zone accepting JPEG, PNG, and WebP up to 5 MB each
- **THEN** the control SHALL indicate a maximum of 5 images

#### Scenario: Images uploaded after successful submit

- **WHEN** the client submits a valid solicitud with 2 selected images
- **THEN** the application SHALL POST `/solicitudes` with Bearer token
- **THEN** after HTTP 201 the application SHALL upload both images and register metadata for the new `id_solicitud`

#### Scenario: Submit succeeds without images

- **WHEN** the client submits without selecting images
- **THEN** no Storage upload or image metadata calls SHALL occur
- **THEN** success feedback and navigation behave as today

