# client-service-rating Specification

## Purpose
Provides the service rating screen for clients to evaluate completed services.

## Requirements

### Requirement: Service rating form

The service rating screen SHALL display a rating form with five criteria for evaluating the completed service.

#### Scenario: Rating criteria visible

- **WHEN** the user navigates to `/valorar-servicio`
- **THEN** the form displays rating criteria for: punctuality, quality, treatment, cleanliness, and price compliance

#### Scenario: Rating inputs

- **WHEN** the user interacts with each criterion
- **THEN** the form displays a rating input (1-5 using select or simple numeric buttons)

### Requirement: Rating uses signals

The service rating screen SHALL use Angular Signals to manage rating values.

#### Scenario: Signals for rating values

- **WHEN** the user fills in the rating form
- **THEN** each criterion rating is stored in an Angular Signal

#### Scenario: Computed average

- **WHEN** the user completes all criteria ratings
- **THEN** the overall rating is computed from individual Signals using computed()

### Requirement: Additional rating fields

The rating form SHALL include an optional comment field and a "would hire again" checkbox.

#### Scenario: Comment field visible

- **WHEN** the user views the rating form
- **THEN** a textarea for optional comments is displayed

#### Scenario: Would hire again checkbox visible

- **WHEN** the user views the rating form
- **THEN** a checkbox labeled "Volvería a contratar" is displayed

### Requirement: Rating submission

The rating form SHALL provide visual feedback when submitted.

#### Scenario: Submit button present

- **WHEN** the user views the rating form
- **THEN** a submit button labeled "Enviar valoración" is visible

#### Scenario: Submission simulated

- **WHEN** the user clicks the submit button
- **THEN** the form shows a visual confirmation message
- **THEN** a button to navigate to `/panel-cliente` is displayed
- **THEN** no HTTP request is made to the backend

### Requirement: Rating screen access

The rating screen SHALL display the service as completed.

#### Scenario: Route accessible

- **WHEN** the user navigates to `/valorar-servicio`
- **THEN** the rating form is displayed within the application layout

#### Scenario: Service status display

- **WHEN** the user views the rating screen
- **THEN** the screen displays the service status as "Finalizado"

### Requirement: Navigation after rating

The rating screen SHALL allow navigation back to the client dashboard.

#### Scenario: Navigate to dashboard

- **WHEN** the user clicks the navigation button after submission
- **THEN** the application navigates to `/panel-cliente` without a full page reload
