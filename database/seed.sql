-- =========================================================
-- SERVIHOGAR - SEED SQL PARA SUPABASE
-- Datos iniciales de prueba vinculados con Supabase Auth
-- =========================================================

-- =========================================================
-- 1. CIUDADES
-- =========================================================

insert into ciudades (nombre, departamento, pais, estado)
values
('Huancayo', 'Junín', 'Perú', 'activo')
on conflict (nombre, departamento, pais) do nothing;

-- =========================================================
-- 2. ZONAS
-- =========================================================

insert into zonas (id_ciudad, nombre, estado)
values
((select id_ciudad from ciudades where nombre = 'Huancayo' and departamento = 'Junín'), 'Huancayo Centro', 'activo'),
((select id_ciudad from ciudades where nombre = 'Huancayo' and departamento = 'Junín'), 'El Tambo', 'activo'),
((select id_ciudad from ciudades where nombre = 'Huancayo' and departamento = 'Junín'), 'Chilca', 'activo'),
((select id_ciudad from ciudades where nombre = 'Huancayo' and departamento = 'Junín'), 'Pilcomayo', 'activo')
on conflict (id_ciudad, nombre) do nothing;

-- =========================================================
-- 3. CATEGORÍAS DE SERVICIO
-- =========================================================

insert into categorias_servicio (nombre, descripcion, estado)
values
('Gasfitería menor', 'Reparación de fugas, caños, lavaderos, tuberías visibles y mantenimiento sanitario menor.', 'activo'),
('Electricidad básica', 'Instalación y reparación de tomacorrientes, luminarias, interruptores y revisiones eléctricas simples.', 'activo'),
('Carpintería', 'Reparación de puertas, muebles, bisagras, cerraduras simples y trabajos menores en madera.', 'activo'),
('Pintura', 'Pintado de habitaciones, retoques, paredes interiores y acabados menores.', 'activo'),
('Cerrajería', 'Cambio de chapas, apertura de puertas, duplicado básico y reparación de cerraduras.', 'activo'),
('Limpieza general', 'Limpieza doméstica, limpieza profunda por ambientes y apoyo en mantenimiento del hogar.', 'activo')
on conflict (nombre) do nothing;

-- =========================================================
-- 4. USUARIOS VINCULADOS A SUPABASE AUTH
-- =========================================================

insert into usuarios (auth_user_id, nombres, apellidos, telefono, foto_perfil_url, estado)
values
('ed960987-531f-4951-91af-4e1c471f869d', 'Administrador', 'ServiHogar', '900000001', 'avatars/admin-demo.jpg', 'activo'),
('eb65fb3b-d00b-40b5-82e8-933cd3cd346c', 'Ana', 'Torres', '900000002', 'avatars/cliente-demo.jpg', 'activo'),
('9ce2ac73-1b61-40de-ac53-bafc12b3eb29', 'Carlos', 'Mendoza', '900000003', 'avatars/tecnico-carlos.jpg', 'activo'),
('a4670a2e-3fe7-485f-8397-ddce113a47a2', 'Rosa', 'Quispe', '900000004', 'avatars/tecnico-rosa.jpg', 'activo')
on conflict (auth_user_id) do nothing;

-- =========================================================
-- 5. PERFILES
-- =========================================================

-- Cliente demo
insert into clientes (id_usuario, estado)
values (
    (select id_usuario from usuarios where auth_user_id = 'eb65fb3b-d00b-40b5-82e8-933cd3cd346c'),
    'activo'
)
on conflict (id_usuario) do nothing;

-- Técnico validado
insert into tecnicos (
    id_usuario,
    descripcion,
    experiencia_anios,
    estado_validacion,
    fecha_validacion
)
values (
    (select id_usuario from usuarios where auth_user_id = '9ce2ac73-1b61-40de-ac53-bafc12b3eb29'),
    'Técnico especializado en gasfitería menor y electricidad básica para hogares. Atiende reparaciones rápidas en Huancayo.',
    6,
    'validado',
    now()
)
on conflict (id_usuario) do nothing;

-- Técnico pendiente
insert into tecnicos (
    id_usuario,
    descripcion,
    experiencia_anios,
    estado_validacion
)
values (
    (select id_usuario from usuarios where auth_user_id = 'a4670a2e-3fe7-485f-8397-ddce113a47a2'),
    'Técnica con experiencia en limpieza general y mantenimiento básico del hogar. Pendiente de validación documental.',
    3,
    'pendiente'
)
on conflict (id_usuario) do nothing;

-- Administrador
insert into administradores (id_usuario, estado)
values (
    (select id_usuario from usuarios where auth_user_id = 'ed960987-531f-4951-91af-4e1c471f869d'),
    'activo'
)
on conflict (id_usuario) do nothing;

-- =========================================================
-- 6. CATEGORÍAS POR TÉCNICO
-- =========================================================

-- Carlos Mendoza
insert into tecnico_categorias (id_tecnico, id_categoria)
values
(
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = '9ce2ac73-1b61-40de-ac53-bafc12b3eb29'),
    (select id_categoria from categorias_servicio where nombre = 'Gasfitería menor')
),
(
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = '9ce2ac73-1b61-40de-ac53-bafc12b3eb29'),
    (select id_categoria from categorias_servicio where nombre = 'Electricidad básica')
)
on conflict do nothing;

-- Rosa Quispe
insert into tecnico_categorias (id_tecnico, id_categoria)
values
(
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = 'a4670a2e-3fe7-485f-8397-ddce113a47a2'),
    (select id_categoria from categorias_servicio where nombre = 'Limpieza general')
),
(
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = 'a4670a2e-3fe7-485f-8397-ddce113a47a2'),
    (select id_categoria from categorias_servicio where nombre = 'Carpintería')
)
on conflict do nothing;

-- =========================================================
-- 7. ZONAS POR TÉCNICO
-- =========================================================

-- Carlos Mendoza
insert into tecnico_zonas (id_tecnico, id_zona)
values
(
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = '9ce2ac73-1b61-40de-ac53-bafc12b3eb29'),
    (select id_zona from zonas where nombre = 'Huancayo Centro')
),
(
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = '9ce2ac73-1b61-40de-ac53-bafc12b3eb29'),
    (select id_zona from zonas where nombre = 'El Tambo')
)
on conflict do nothing;

-- Rosa Quispe
insert into tecnico_zonas (id_tecnico, id_zona)
values
(
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = 'a4670a2e-3fe7-485f-8397-ddce113a47a2'),
    (select id_zona from zonas where nombre = 'Chilca')
),
(
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = 'a4670a2e-3fe7-485f-8397-ddce113a47a2'),
    (select id_zona from zonas where nombre = 'Huancayo Centro')
)
on conflict do nothing;

-- =========================================================
-- 8. DOCUMENTOS DE TÉCNICO
-- =========================================================

insert into documentos_tecnico (
    id_tecnico,
    tipo_documento,
    url_documento,
    estado_revision,
    observacion
)
values
(
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = '9ce2ac73-1b61-40de-ac53-bafc12b3eb29'),
    'dni',
    'documentos-tecnicos/carlos/dni.pdf',
    'aprobado',
    'Documento validado correctamente.'
),
(
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = '9ce2ac73-1b61-40de-ac53-bafc12b3eb29'),
    'certificado',
    'documentos-tecnicos/carlos/certificado-gasfiteria.pdf',
    'aprobado',
    'Certificado de experiencia aceptado.'
),
(
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = 'a4670a2e-3fe7-485f-8397-ddce113a47a2'),
    'dni',
    'documentos-tecnicos/rosa/dni.pdf',
    'pendiente',
    'Documento pendiente de revisión.'
);

-- =========================================================
-- 9. PORTAFOLIO DEL TÉCNICO VALIDADO
-- =========================================================

insert into portafolio_tecnico (
    id_tecnico,
    titulo,
    descripcion,
    imagen_url,
    estado
)
values
(
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = '9ce2ac73-1b61-40de-ac53-bafc12b3eb29'),
    'Reparación de fuga en lavadero',
    'Cambio de conexión y sellado de fuga en cocina.',
    'portafolio-tecnicos/carlos/reparacion-lavadero.jpg',
    'visible'
),
(
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = '9ce2ac73-1b61-40de-ac53-bafc12b3eb29'),
    'Instalación de caño',
    'Instalación de caño nuevo en baño familiar.',
    'portafolio-tecnicos/carlos/instalacion-cano.jpg',
    'visible'
);

-- =========================================================
-- 10. SOLICITUDES DE SERVICIO
-- =========================================================

insert into solicitudes_servicio (
    id_cliente,
    id_categoria,
    id_zona,
    titulo,
    descripcion,
    direccion_referencia,
    direccion_exacta,
    estado
)
values
(
    (select c.id_cliente from clientes c join usuarios u on u.id_usuario = c.id_usuario where u.auth_user_id = 'eb65fb3b-d00b-40b5-82e8-933cd3cd346c'),
    (select id_categoria from categorias_servicio where nombre = 'Gasfitería menor'),
    (select id_zona from zonas where nombre = 'Huancayo Centro'),
    'Fuga de agua en lavadero de cocina',
    'El lavadero presenta una fuga constante debajo del caño. Se requiere revisión y reparación.',
    'Cerca del parque Constitución',
    'Jr. Real 123, departamento 202',
    'finalizada'
),
(
    (select c.id_cliente from clientes c join usuarios u on u.id_usuario = c.id_usuario where u.auth_user_id = 'eb65fb3b-d00b-40b5-82e8-933cd3cd346c'),
    (select id_categoria from categorias_servicio where nombre = 'Electricidad básica'),
    (select id_zona from zonas where nombre = 'El Tambo'),
    'Tomacorriente no funciona',
    'Un tomacorriente de la sala dejó de funcionar y se requiere revisión.',
    'A dos cuadras de la municipalidad de El Tambo',
    null,
    'pendiente'
);

-- =========================================================
-- 11. IMÁGENES DE SOLICITUD
-- =========================================================

insert into imagenes_solicitud (
    id_solicitud,
    imagen_url,
    descripcion
)
values
(
    (select id_solicitud from solicitudes_servicio where titulo = 'Fuga de agua en lavadero de cocina'),
    'solicitudes/fuga-lavadero-1.jpg',
    'Vista general de la fuga debajo del lavadero.'
),
(
    (select id_solicitud from solicitudes_servicio where titulo = 'Fuga de agua en lavadero de cocina'),
    'solicitudes/fuga-lavadero-2.jpg',
    'Detalle de la conexión afectada.'
),
(
    (select id_solicitud from solicitudes_servicio where titulo = 'Tomacorriente no funciona'),
    'solicitudes/tomacorriente-sala.jpg',
    'Tomacorriente de sala sin energía.'
);

-- =========================================================
-- 12. COTIZACIONES
-- =========================================================

insert into cotizaciones (
    id_solicitud,
    id_tecnico,
    monto,
    descripcion,
    tiempo_estimado,
    estado
)
values
(
    (select id_solicitud from solicitudes_servicio where titulo = 'Fuga de agua en lavadero de cocina'),
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = '9ce2ac73-1b61-40de-ac53-bafc12b3eb29'),
    85.00,
    'Incluye revisión, sellado de fuga y cambio de conexión menor si es necesario.',
    '1 a 2 horas',
    'aceptada'
),
(
    (select id_solicitud from solicitudes_servicio where titulo = 'Tomacorriente no funciona'),
    (select t.id_tecnico from tecnicos t join usuarios u on u.id_usuario = t.id_usuario where u.auth_user_id = '9ce2ac73-1b61-40de-ac53-bafc12b3eb29'),
    60.00,
    'Revisión del tomacorriente, diagnóstico de cableado y reparación básica.',
    '1 hora',
    'pendiente'
)
on conflict (id_solicitud, id_tecnico) do nothing;

-- =========================================================
-- 13. VALORACIÓN
-- =========================================================

insert into valoraciones (
    id_cotizacion,
    puntuacion,
    comentario,
    puntualidad,
    calidad,
    precio,
    trato
)
values
(
    (
        select co.id_cotizacion
        from cotizaciones co
        join solicitudes_servicio ss on ss.id_solicitud = co.id_solicitud
        where ss.titulo = 'Fuga de agua en lavadero de cocina'
          and co.estado = 'aceptada'
    ),
    5,
    'El técnico llegó puntual, resolvió la fuga rápidamente y explicó el trabajo realizado.',
    5,
    5,
    4,
    5
)
on conflict (id_cotizacion) do nothing;