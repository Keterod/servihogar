# AGENTS.md — Backend ServiHogar

Eres experto en Python, FastAPI y desarrollo web escalable. Escribes código funcional, mantenible, performante y accesible.

## Arquitectura y estructura

- Todas las carpetas y archivos del backend deben crearse dentro de la carpeta `src`.
- `src/apis/`: contiene los enrutadores y endpoints de FastAPI.
- `src/services/`: contiene la lógica de negocio.
- `src/repository/`: contiene el acceso a datos y comunicación con Supabase.
- `src/schemas/`: contiene los esquemas Pydantic para validación de entrada y salida de datos.
- El flujo obligatorio debe ser: `main -> enrutadores -> servicios -> repositorio`.
- Los endpoints no deben acceder directamente a Supabase; deben pasar por servicios y repositorios.
- Los servicios no deben contener detalles de conexión; eso corresponde al repositorio o configuración.
- `src/main.py`: punto de entrada principal de la aplicación FastAPI.

## Base de datos

- La base de datos se gestiona únicamente con **Supabase**.
- Supabase proporciona **PostgreSQL administrado en la nube**.
- No se debe usar **Firebase Realtime Database**.
- No se requiere configurar PostgreSQL local como base principal del proyecto.
- No se debe usar **ORM**.
- El acceso a datos debe hacerse desde `src/repository/`.
- Los scripts oficiales de base de datos están en:
  - `../database/schema.sql`
  - `../database/seed.sql`
  - `../database/README.md`
- No modificar `schema.sql` ni `seed.sql` salvo indicación explícita.

## Supabase

- **Supabase Auth** maneja correo, contraseña e inicio de sesión.
- **Supabase Storage** almacena imágenes y documentos.
- La tabla `usuarios` guarda el perfil interno y se vincula con `auth.users` mediante `auth_user_id`.
- No guardar contraseñas en tablas propias.
- No guardar imágenes ni documentos como binarios en PostgreSQL; guardar rutas o URLs.
- No exponer claves privadas ni **service role key** en el código.

## FastAPI

- Usar `APIRouter` para separar rutas.
- Separar endpoints por dominio cuando se implemente:
  - usuarios
  - clientes
  - tecnicos
  - solicitudes
  - cotizaciones
  - valoraciones
  - categorias
  - zonas
- Los endpoints deben validar datos con esquemas Pydantic desde `src/schemas/`.
- Los endpoints deben delegar la lógica a `src/services/`.
- No colocar lógica de negocio compleja dentro de los endpoints.

## Variables de entorno

- Usar archivo `.env` para configuración local.
- Mantener `.env.example` con nombres de variables necesarias.
- No subir `.env` real al repositorio.
- Variables esperadas:
  - `SUPABASE_URL`
  - `SUPABASE_ANON_KEY`
  - `SUPABASE_SERVICE_ROLE_KEY` (solo si se requiere en backend y **nunca** en frontend)
  - `ENVIRONMENT`
- Las variables deben leerse desde una configuración central en `src`.

## Seguridad

- No exponer claves privadas.
- Validar entrada de datos con Pydantic.
- No confiar en datos enviados por el cliente.
- Verificar autenticación antes de permitir acciones protegidas.
- No permitir que un usuario acceda a datos de otro usuario sin autorización.
- Tener cuidado con **RLS** de Supabase.

## Restricciones

- No modificar frontend si la tarea es backend.
- No modificar base de datos si la tarea es solo API.
- No inventar autenticación propia si se usará Supabase Auth.
- No crear conexión local a PostgreSQL salvo indicación explícita.
- No agregar dependencias innecesarias.
