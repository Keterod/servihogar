## ADDED Requirements

### Requirement: Technician portfolio management section

The technician dashboard SHALL include a portfolio section where the authenticated validated technician can view their portfolio items and add new work evidence images.

#### Scenario: Portfolio section loads authenticated data

- **WHEN** a validated technician navigates to `/panel-tecnico`
- **THEN** the page SHALL fetch `GET /tecnicos/me/portafolio` with Bearer token
- **THEN** existing items SHALL display titulo, descripcion, thumbnail from `imagen_url`, and fecha

#### Scenario: Add portfolio item form

- **WHEN** the technician opens the add form
- **THEN** fields for titulo, optional descripcion, and one image file SHALL be shown
- **THEN** submit SHALL upload to Storage and POST `/tecnicos/me/portafolio`

#### Scenario: Portfolio blocked when not validated

- **WHEN** `estado_validacion` is pendiente or rechazado
- **THEN** the add portfolio form SHALL be disabled with explanatory text

#### Scenario: Portfolio uses authenticated technician identity

- **WHEN** technician Diego uploads portfolio content
- **THEN** Storage paths and metadata SHALL use Diego's `id_tecnico`, not a demo technician id
