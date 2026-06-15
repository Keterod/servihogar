## MODIFIED Requirements

### Requirement: Request detail navigation

The request detail screen SHALL be accessible from the client dashboard with the solicitud id in the route and SHALL link to the rating screen when eligible.

#### Scenario: Route accessible with id

- **WHEN** the user navigates to `/detalle-solicitud/:id`
- **THEN** the request detail screen is displayed within the application layout
- **THEN** the displayed solicitud matches the id in the URL

#### Scenario: Navigation to rating

- **WHEN** the solicitud estado is `en_proceso` or `finalizada` and the user chooses to rate the service
- **THEN** the application navigates to `/valorar-servicio?idSolicitud={id}` without a full page reload

#### Scenario: Rating link hidden when not eligible

- **WHEN** the solicitud estado is `pendiente` or `cancelada`
- **THEN** the rating action SHALL NOT be shown or SHALL be disabled with clear guidance
