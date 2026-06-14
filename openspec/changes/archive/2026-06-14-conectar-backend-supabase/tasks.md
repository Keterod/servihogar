## 1. Supabase Client & Dependencies

- [x] 1.1 Add `supabase>=2.0.0,<3` to `pyproject.toml` dependencies and run `uv sync`
- [x] 1.2 Create `src/repository/supabase_client.py` with a singleton Supabase client using `Settings` config

## 2. Repositories

- [x] 2.1 Create `src/repository/categorias_repository.py` — read-only query on `categorias_servicio` (all active)
- [x] 2.2 Create `src/repository/zonas_repository.py` — read-only query on `zonas` (all active)
- [x] 2.3 Create `src/repository/tecnicos_repository.py` — read-only query joining `tecnicos` + `usuarios` for validated tecnicos

## 3. Pydantic Schemas

- [x] 3.1 Create `src/schemas/categoria.py` — CategoriaResponse with id_categoria, nombre, descripcion
- [x] 3.2 Create `src/schemas/zona.py` — ZonaResponse with id_zona, nombre, id_ciudad
- [x] 3.3 Create `src/schemas/tecnico.py` — TecnicoResponse with id_tecnico, nombres, apellidos, descripcion, experiencia_anios

## 4. Services

- [x] 4.1 Create `src/services/categorias_service.py` — delegates to CategoriasRepository
- [x] 4.2 Create `src/services/zonas_service.py` — delegates to ZonasRepository
- [x] 4.3 Create `src/services/tecnicos_service.py` — delegates to TecnicosRepository (with calificacion aggregation)

## 5. API Routers

- [x] 5.1 Create `src/apis/categorias.py` — `GET /categorias` returning CategoriaResponse list
- [x] 5.2 Create `src/apis/zonas.py` — `GET /zonas` returning ZonaResponse list
- [x] 5.3 Create `src/apis/tecnicos.py` — `GET /tecnicos` returning TecnicoResponse list

## 6. Wiring & Verification

- [x] 6.1 Wire the three new routers into `src/main.py`
- [x] 6.2 Start the server and verify: `GET /health` returns `{"status": "ok"}`; data endpoints return 503 gracefully when Supabase not configured, will return data once `.env` is set up
