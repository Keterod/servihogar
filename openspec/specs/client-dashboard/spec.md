# client-dashboard Specification

## Purpose
Provides the client dashboard showing a summary of service requests.

## Requirements

### Requirement: Client dashboard display

The client dashboard SHALL display a summary of three simulated service requests.

#### Scenario: Requests list visible

- **WHEN** the user navigates to `/panel-cliente`
- **THEN** the page displays at least three simulated service requests

#### Scenario: Each request shows key information

- **WHEN** the user views a service request in the list
- **THEN** the request displays category, brief description, zone, tentative date, status, and number of quotations

### Requirement: Dashboard uses signals

The client dashboard SHALL use Angular Signals to manage the list of requests and derived state.

#### Scenario: Signals for request list

- **WHEN** the client dashboard loads
- **THEN** the list of requests is stored in an Angular Signal

#### Scenario: Computed values for summary

- **WHEN** the user views the dashboard
- **THEN** summary counts (pending, in-progress, completed, cancelled) are computed from the requests Signal

### Requirement: Request status display

The dashboard SHALL display the status of each request using the following states: pendiente, en_proceso, finalizado, cancelado.

#### Scenario: Status labels visible

- **WHEN** the user views a request in the list
- **THEN** the request displays its current status label
- **THEN** the status is one of: pendiente, en_proceso, finalizado, cancelado

### Requirement: Dashboard navigation

The client dashboard SHALL allow navigation to request details.

#### Scenario: Select request

- **WHEN** the user clicks "Ver detalle" on a service request
- **THEN** the application navigates to `/detalle-solicitud` without a full page reload

#### Scenario: Route accessible

- **WHEN** the user navigates to `/panel-cliente`
- **THEN** the client dashboard is displayed within the application layout
