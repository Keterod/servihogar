## ADDED Requirements

### Requirement: Service request form fields

The service request form SHALL display six input fields: category (select), zone (select), description (textarea), tentative date (date input), preferred schedule (select or text), and approximate address (text input).

#### Scenario: Form fields visible

- **WHEN** the user navigates to `/solicitud-servicio`
- **THEN** the form displays select controls for category and zone
- **THEN** the form displays a textarea for description
- **THEN** the form displays a date input for tentative date
- **THEN** the form displays a select or text input for preferred schedule
- **THEN** the form displays a text input for approximate address

#### Scenario: Category options

- **WHEN** the user interacts with the category select
- **THEN** the options display: Gasfitería menor, Electricidad básica, Mantenimiento de computadoras, Pintura básica, Armado de muebles

#### Scenario: Zone options

- **WHEN** the user interacts with the zone select
- **THEN** the options display: Huancayo Centro, El Tambo, Chilca, San Carlos

### Requirement: Form uses signals for state

The service request form SHALL use Angular Signals to manage the state of each form field.

#### Scenario: Signals for form fields

- **WHEN** the user fills in the form fields
- **THEN** each field value is stored in an Angular Signal
- **THEN** the Signal values update on input changes

### Requirement: Form submission

The form SHALL provide visual feedback when the user submits the request.

#### Scenario: Submit button present

- **WHEN** the user views the service request form
- **THEN** a submit button labeled "Publicar solicitud" is visible

#### Scenario: Submission simulated

- **WHEN** the user clicks the submit button
- **THEN** the form shows a visual confirmation message
- **THEN** a button to navigate to `/panel-cliente` is displayed
- **THEN** no HTTP request is made to the backend

### Requirement: Form navigation

The service request screen SHALL be accessible via the existing route.

#### Scenario: Route accessible

- **WHEN** the user navigates to `/solicitud-servicio`
- **THEN** the service request form is displayed within the application layout

#### Scenario: Navigation after submission

- **WHEN** the user clicks the navigation button after submission
- **THEN** the application navigates to `/panel-cliente` without a full page reload
