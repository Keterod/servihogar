## ADDED Requirements

### Requirement: Routes use lazy loading

All application routes SHALL use `loadComponent` with dynamic `import()` instead of eager `component:` references.

#### Scenario: Inicio route loads lazily
- **WHEN** the user navigates to `/inicio`
- **THEN** the Home component is loaded via dynamic import, not imported eagerly at module load time

#### Scenario: All component imports are removed from app.routes.ts
- **WHEN** the application module is evaluated
- **THEN** `app.routes.ts` SHALL contain zero top-level imports of page components

### Requirement: Bootstrap included via CDN

The application SHALL load Bootstrap 5 CSS and JavaScript via CDN links in `index.html`.

#### Scenario: Bootstrap CSS loads from CDN
- **WHEN** the page is loaded in a browser
- **THEN** the `<head>` of `index.html` SHALL contain a `<link>` to Bootstrap 5 CSS on jsDelivr

#### Scenario: Bootstrap JS loads from CDN
- **WHEN** the page is loaded in a browser
- **THEN** the end of `<body>` SHALL contain a `<script>` to Bootstrap 5 JavaScript bundle on jsDelivr

### Requirement: Login-register form uses Signals

The `login-register` component SHALL manage its form fields using `signal({...})` and validate with `computed()`.

#### Scenario: Form state is a single signal
- **WHEN** the component initializes
- **THEN** SHALL have a `signal` containing all form fields (nombre, email, password, confirmPassword, especialidad, zona, telefono)

#### Scenario: Submit button disabled when fields are empty
- **WHEN** required fields (email and password) are empty
- **THEN** the submit button SHALL have `disabled` attribute bound to a `computed()` value
