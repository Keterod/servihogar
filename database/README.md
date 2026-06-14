# Base de datos ServiHogar (Supabase)

La base de datos del proyecto **ServiHogar** se gestiona íntegramente en **[Supabase](https://supabase.com/)**. No se requiere instalar ni configurar PostgreSQL en la máquina local: Supabase proporciona **PostgreSQL administrado en la nube**, junto con autenticación, almacenamiento de archivos y panel de administración.

> **Nota:** el frontend y el backend de ServiHogar **aún no están conectados** a esta base de datos. Los scripts de esta carpeta definen la estructura y los datos iniciales para cuando se integre la aplicación real.

---

## Resumen

| Aspecto | Detalle |
|---------|---------|
| Plataforma | Supabase (PostgreSQL en la nube) |
| Base de datos local | **No requerida** |
| Autenticación | Supabase Auth (correo y contraseña) |
| Archivos (imágenes, PDF) | Supabase Storage |
| Metadatos en BD | Rutas/URLs en columnas de texto |
| Seguridad | RLS activado; políticas específicas pendientes de integración |

---

## Supabase como plataforma principal

Supabase agrupa en un solo servicio:

- **PostgreSQL** — motor relacional donde viven las tablas de ServiHogar.
- **Authentication** — registro, inicio de sesión y gestión de usuarios (`auth.users`).
- **Storage** — buckets para avatares, solicitudes, portafolio y documentos de técnicos.
- **SQL Editor** — ejecución de `schema.sql` y `seed.sql` desde el panel web.

Para trabajar en el proyecto solo necesitas una cuenta en Supabase y acceso al proyecto del equipo. **No es obligatorio** instalar PostgreSQL, pgAdmin ni levantar un servidor local.

---

## Modelo de usuarios y perfiles

### Vínculo con Supabase Auth

La tabla `usuarios` guarda el **perfil interno** de ServiHogar (nombres, teléfono, foto, estado). Se vincula con la identidad de autenticación mediante:

```text
usuarios.auth_user_id  →  auth.users.id
```

Supabase Auth se encarga del **correo**, la **contraseña** y el **inicio de sesión**. La tabla `usuarios` complementa esa identidad con datos propios de la plataforma.

### Perfiles múltiples

El modelo separa el usuario base de sus roles operativos:

| Tabla | Rol |
|-------|-----|
| `clientes` | Perfil cliente |
| `tecnicos` | Perfil técnico |
| `administradores` | Perfil administrador |

Cada perfil referencia `usuarios.id_usuario`. Un mismo usuario puede tener **varios perfiles a la vez** — por ejemplo, ser **cliente y técnico** — sin perder el historial de solicitudes, cotizaciones ni valoraciones asociadas a cada rol.

---

## Archivos e imágenes (Supabase Storage)

Los binarios **no** se guardan dentro de PostgreSQL. Se suben a **Supabase Storage** y la base de datos almacena solo la **ruta o URL** de referencia:

| Columna | Uso |
|---------|-----|
| `usuarios.foto_perfil_url` | Avatar del usuario |
| `imagenes_solicitud.imagen_url` | Fotos adjuntas a una solicitud |
| `documentos_tecnico.url_documento` | DNI, certificados y documentos de validación |
| `portafolio_tecnico.imagen_url` | Trabajos publicados en el portafolio del técnico |

### Buckets recomendados

| Bucket | Contenido |
|--------|-----------|
| `avatars` | Fotos de perfil |
| `solicitudes` | Imágenes de solicitudes de servicio |
| `portafolio-tecnicos` | Fotos del portafolio público |
| `documentos-tecnicos` | Documentos privados de validación |

Los buckets se crean en **Storage** del panel de Supabase cuando el proyecto vaya a manejar archivos reales.

---

## Archivos SQL de esta carpeta

### `schema.sql`

Contiene la **estructura completa** de la base de datos:

- Definición de tablas y relaciones
- Restricciones (`CHECK`, `UNIQUE`, claves foráneas)
- Índices recomendados
- Triggers (por ejemplo, actualización de `fecha_actualizacion`)
- Comentarios descriptivos en tablas

Ejecutar **una vez** en el **SQL Editor** de Supabase al configurar un proyecto nuevo (o al reiniciar el esquema en un entorno de prueba).

### `seed.sql`

Contiene **datos iniciales de prueba** vinculados a usuarios reales de **Supabase Auth**. Incluye ciudades, zonas, categorías, perfiles, solicitudes, cotizaciones, valoraciones y rutas de ejemplo hacia Storage.

> **Importante:** `seed.sql` referencia `auth_user_id` con UUID fijos. Los usuarios deben existir previamente en **Authentication** con esos identificadores, o el script debe adaptarse a los UUID generados al crearlos.

---

## Orden de configuración en Supabase

Sigue estos pasos en orden:

1. **Crear proyecto** en [Supabase Dashboard](https://supabase.com/dashboard).
2. **Ejecutar `schema.sql`** en **SQL Editor** (pegar contenido → Run).
3. **Crear usuarios** en **Authentication → Users** (correo y contraseña). Se necesitan **4 usuarios Auth** alineados con los UUID del seed.
4. **Ejecutar `seed.sql`** en **SQL Editor**.
5. **Crear buckets** en **Storage** (`avatars`, `solicitudes`, `portafolio-tecnicos`, `documentos-tecnicos`) si se van a usar archivos.

---

## Datos iniciales cargados (`seed.sql`)

Tras ejecutar el seed correctamente, la base incluye:

| Entidad | Cantidad |
|---------|----------|
| Usuarios Auth (referenciados) | 4 |
| Perfiles cliente | 1 |
| Perfiles técnico | 2 |
| Perfiles administrador | 1 |
| Solicitudes de servicio | 2 |
| Cotizaciones | 2 |
| Valoraciones | 1 |

Además del núcleo anterior, el seed carga datos de apoyo: ciudades, zonas, categorías de servicio, relaciones técnico–categoría, técnico–zona, documentos, portafolio e imágenes de solicitud.

---

## Row Level Security (RLS)

**RLS está activado** en las tablas del proyecto como capa base de seguridad en Supabase.

Las **políticas RLS específicas** (quién puede leer o escribir cada fila según el rol autenticado) se definirán cuando se conecte el **frontend** y el **backend** real. Hasta entonces, el acceso desde la aplicación no está implementado.

---

## Verificación después del seed

Ejecuta estas consultas en el **SQL Editor** para confirmar que los datos se cargaron:

```sql
select count(*) from usuarios;
select count(*) from clientes;
select count(*) from tecnicos;
select count(*) from administradores;
select count(*) from solicitudes_servicio;
select count(*) from cotizaciones;
select count(*) from valoraciones;
```

Resultados esperados (con seed completo y usuarios Auth correctos):

| Consulta | Cantidad esperada |
|----------|-------------------|
| `usuarios` | 4 |
| `clientes` | 1 |
| `tecnicos` | 2 |
| `administradores` | 1 |
| `solicitudes_servicio` | 2 |
| `cotizaciones` | 2 |
| `valoraciones` | 1 |

---

## Relación con el resto del repositorio

| Componente | Estado respecto a la BD |
|------------|-------------------------|
| `servihogar-frontend/` | Prototipo con datos simulados en memoria; **sin conexión** a Supabase todavía |
| `servihogar-backend/` | Planificado (FastAPI); **sin conexión** activa todavía |
| `database/` | Fuente de verdad del esquema y datos iniciales en Supabase |

La integración real (cliente Supabase, API, variables de entorno, políticas RLS finales) corresponderá a una fase posterior del proyecto.

---

## Estructura de esta carpeta

```
database/
├── schema.sql    # Estructura: tablas, relaciones, índices, triggers
├── seed.sql      # Datos iniciales vinculados a Supabase Auth
└── README.md     # Esta documentación
```

---

## Autor

Documentación del esquema de base de datos del proyecto académico **ServiHogar**, desarrollado por **Diego**.
