# frontend-visual-integration Specification

## Purpose
TBD - created by archiving change integrar-frontend-visual. Update Purpose after archive.
## Requirements
### Requirement: Shared visual tokens and utilities

The application SHALL provide shared CSS utility classes and design tokens in global styles so that routed screens use consistent colors, typography, cards, buttons, and badge appearance.

#### Scenario: Global utilities available

- **WHEN** any routed component renders
- **THEN** shared classes for primary buttons, cards, section headers, and summary grids are defined in `styles.css`
- **THEN** component styles progressively adopt CSS custom properties from `:root` instead of unrelated hardcoded palettes where equivalents exist

#### Scenario: Badge appearance unified without class renames

- **WHEN** the user views status badges across client, technician, and admin dashboards
- **THEN** badges share consistent colors, sizing, and border radius via global tokens or shared rules
- **THEN** existing component-specific badge class names are preserved where renaming would add unnecessary risk

### Requirement: Moderate cross-screen visual consistency

Priority screens for the academic report SHALL receive moderate visual alignment (spacing, headings, tokens, responsive basics) without changing functional behavior or Signal-based state logic.

#### Scenario: Priority screens visually aligned

- **WHEN** the user navigates among inicio, buscar-tecnicos, perfil-tecnico, login, solicitud-servicio, panel-cliente, detalle-solicitud, valorar-servicio, panel-tecnico, and panel-administrador
- **THEN** the screens share a coherent academic light theme derived from global tokens
- **THEN** no functional rules or Signal-based state management are removed or altered

#### Scenario: Build succeeds after visual integration

- **WHEN** `npm run build` is executed for the Angular 21 frontend
- **THEN** the build completes without errors

### Requirement: CSS budget mitigation without config changes

The application SHALL reduce duplicated component CSS by moving simple shared rules to global styles without raising `maximumWarning` in `angular.json`.

#### Scenario: Duplication reduced progressively

- **WHEN** panel component stylesheets are inspected after integration
- **THEN** obvious duplicated rules (e.g. primary buttons, summary grids, repeated color blocks) are consolidated into global styles where practical
- **THEN** `angular.json` CSS budget warning thresholds are not increased

#### Scenario: Residual warning acceptable

- **WHEN** a minor CSS budget warning remains after deduplication but the build completes without errors
- **THEN** the warning is acceptable for this academic sprint

### Requirement: ServiHogar flow text coherence

User-facing static text on integrated screens SHALL describe the ServiHogar prototype flow: publish a request, receive quotations, accept one quotation, and rate the service upon completion, using the official category vocabulary.

#### Scenario: Official category vocabulary used

- **WHEN** the user reads category labels on integrated screens
- **THEN** visible text uses Gasfitería menor, Electricidad básica, Mantenimiento de computadoras, Pintura básica, and Armado de muebles where applicable
- **THEN** "Fontanería" is avoided in visible text where Gasfitería menor is the correct term

#### Scenario: Flow described without backend implication

- **WHEN** the user reads integrated instructional text
- **THEN** the described flow includes publishing, quotations, acceptance, and rating
- **THEN** no text implies backend integration or real authentication

### Requirement: Narrative mock coherence rules

Integrated visible mocks SHALL avoid strong contradictions across screens while accepting that simulated data is not synchronized at runtime.

#### Scenario: Carlos Mendoza consistency

- **WHEN** Carlos Mendoza appears on perfil-tecnico, panel-tecnico, or related integrated text
- **THEN** he is associated with Gasfitería menor and Huancayo Centro
- **THEN** panel-tecnico shows him as validado

#### Scenario: Roberto Salas quoting preserved

- **WHEN** Roberto Salas appears in detalle-solicitud
- **THEN** he is shown as a technician providing a quotation
- **THEN** he is NOT shown as rechazado in administrator technician lists

#### Scenario: Unsynchronized mocks accepted

- **WHEN** counters or lists differ between screens
- **THEN** the application still presents a visually coherent prototype without global state synchronization

### Requirement: Basic responsive verification

Integrated priority screens SHALL remain readable on small viewports without horizontal page overflow.

#### Scenario: Small viewport on priority screens

- **WHEN** the viewport width is 375px or less
- **THEN** home usage steps display in a vertical layout
- **THEN** priority screens remain readable without horizontal page scroll

