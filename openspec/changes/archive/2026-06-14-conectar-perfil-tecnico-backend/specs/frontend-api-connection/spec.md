## ADDED Requirements

### Requirement: Service methods return typed observables

#### Scenario: TecnicoService.obtenerTecnicoPorId returns observable

- **WHEN** `obtenerTecnicoPorId(1)` is called
- **THEN** it SHALL return `Observable<TecnicoDetalle | null>` from `GET /tecnicos/1`
