# frontend-api-connection Specification

## Purpose
TBD - created by syncing delta from change conectar-frontend-backend-publico.

## Requirements

### Requirement: Backend API base URL

The application SHALL have a single configuration point for the backend API base URL, used by all service classes.

#### Scenario: Base URL is a constant

- **WHEN** the application initializes
- **THEN** a constant with the backend base URL (e.g., `http://127.0.0.1:8003`) SHALL be available in `src/app/env.ts`

### Requirement: HttpClient configured for DI

The application SHALL register `provideHttpClient()` in the Angular providers to enable dependency injection of `HttpClient`.

#### Scenario: HttpClient is injectable

- **WHEN** a service class requests `HttpClient` in its constructor
- **THEN** Angular SHALL provide a working `HttpClient` instance

### Requirement: Service methods return typed observables

Each service class SHALL expose methods that return an `Observable` typed with the corresponding model interface.

#### Scenario: CategoriaServicioService.obtenerCategorias returns observable

- **WHEN** `obtenerCategorias()` is called
- **THEN** it SHALL return `Observable<CategoriaServicio[]>` from `GET /categorias`

#### Scenario: ZonaService.obtenerZonas returns observable

- **WHEN** `obtenerZonas()` is called
- **THEN** it SHALL return `Observable<Zona[]>` from `GET /zonas`

#### Scenario: TecnicoService.obtenerTecnicos returns observable

- **WHEN** `obtenerTecnicos()` is called
- **THEN** it SHALL return `Observable<Tecnico[]>` from `GET /tecnicos`

#### Scenario: TecnicoService.obtenerTecnicoPorId returns observable

- **WHEN** `obtenerTecnicoPorId(1)` is called
- **THEN** it SHALL return `Observable<TecnicoDetalle | null>` from `GET /tecnicos/1`
