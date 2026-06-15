## MODIFIED Requirements

### Requirement: Rating submission

The rating form SHALL submit the valoración to the backend and provide appropriate feedback.

#### Scenario: Submit button present

- **WHEN** the user views the rating form
- **THEN** a submit button labeled "Enviar valoración" is visible

#### Scenario: Successful submission

- **WHEN** the user submits a valid rating for a solicitud with an accepted cotización
- **THEN** the application SHALL POST to `/valoraciones` with `id_solicitud`, `calificacion`, and optional `comentario`
- **THEN** on HTTP 201 the form SHALL display a success confirmation message
- **THEN** a button to navigate to `/panel-cliente` SHALL be displayed

#### Scenario: Submission loading state

- **WHEN** the user submits the rating form and the POST request is in flight
- **THEN** the submit button SHALL be disabled
- **THEN** a loading indication SHALL be visible

#### Scenario: Submission error state

- **WHEN** the backend returns an error other than success
- **THEN** the form SHALL display a clear error message
- **THEN** the rating SHALL NOT be marked as successfully submitted

#### Scenario: Duplicate submission

- **WHEN** the backend returns HTTP 409 because the solicitud was already rated
- **THEN** the form SHALL display a message indicating the service was already valued
- **THEN** the user SHALL be able to navigate back to the panel or detail

### Requirement: Rating screen access

The rating screen SHALL load context for the solicitud being rated.

#### Scenario: Route accessible with solicitud id

- **WHEN** the user navigates to `/valorar-servicio?idSolicitud={id}`
- **THEN** the rating form is displayed within the application layout
- **THEN** the screen loads solicitud context from the backend when available

#### Scenario: Solicitud context visible

- **WHEN** solicitud detail is loaded successfully
- **THEN** the screen displays the solicitud number, accepted technician name, and service/category reference from the backend

#### Scenario: Missing solicitud id

- **WHEN** the user navigates to `/valorar-servicio` without `idSolicitud`
- **THEN** the screen displays an error or guidance message
- **THEN** the user can navigate back to the client panel

#### Scenario: Service status display

- **WHEN** the user views the rating screen for an eligible solicitud
- **THEN** the screen displays the solicitud estado from the backend (e.g. `en_proceso` or `finalizada`)

## MODIFIED Requirements

### Requirement: Rating uses signals

The service rating screen SHALL use Angular Signals to manage rating values and submission state.

#### Scenario: Signals for rating values

- **WHEN** the user fills in the rating form
- **THEN** each criterion rating is stored in an Angular Signal

#### Scenario: Computed average

- **WHEN** the user completes all criteria ratings
- **THEN** the overall rating is computed from individual Signals using computed()

#### Scenario: Submission state signal

- **WHEN** the user submits or receives a response from the backend
- **THEN** loading, success, and error states are tracked in Angular Signals
