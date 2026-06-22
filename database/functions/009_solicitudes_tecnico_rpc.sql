-- =========================================================
-- Función: rpc_solicitudes_disponibles_tecnico
-- Reemplaza: get_disponibles_for_tecnico()
--   - Busca solicitudes pendientes que coinciden con
--     categorías y zonas del técnico (joins internos)
--   - Incluye ya_cotizada_por_tecnico y cotizaciones_count
--   - Excluye solicitudes donde el técnico ya cotizó
-- Uso: SELECT * FROM rpc_solicitudes_disponibles_tecnico(1);
-- =========================================================

create or replace function rpc_solicitudes_disponibles_tecnico(p_id_tecnico bigint)
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select coalesce(json_agg(
    json_build_object(
      'id_solicitud', s.id_solicitud,
      'titulo', s.titulo,
      'descripcion', s.descripcion,
      'direccion_referencia', s.direccion_referencia,
      'estado', s.estado,
      'fecha_publicacion', s.fecha_publicacion,
      'categoria_nombre', c.nombre,
      'zona_nombre', z.nombre,
      'cliente_nombre', trim(
        coalesce(u.nombres, '') || ' ' || coalesce(u.apellidos, '')
      ),
      'cotizaciones_count', (
        select count(*)::int
        from cotizaciones ct
        where ct.id_solicitud = s.id_solicitud
      ),
      'ya_cotizada_por_tecnico', (
        select exists(
          select 1
          from cotizaciones ct
          where ct.id_solicitud = s.id_solicitud
            and ct.id_tecnico = p_id_tecnico
        )
      )
    )
    order by s.fecha_publicacion desc
  ), '[]'::json)
  into result_json
  from solicitudes_servicio s
  join categorias_servicio c on c.id_categoria = s.id_categoria
  join zonas z on z.id_zona = s.id_zona
  join clientes cl on cl.id_cliente = s.id_cliente
  join usuarios u on u.id_usuario = cl.id_usuario
  where s.estado = 'pendiente'
    and s.id_categoria = any(
      select tc.id_categoria
      from tecnico_categorias tc
      where tc.id_tecnico = p_id_tecnico
    )
    and s.id_zona = any(
      select tz.id_zona
      from tecnico_zonas tz
      where tz.id_tecnico = p_id_tecnico
    );

  return result_json;
end;
$$;


-- =========================================================
-- Función: rpc_servicios_aceptados_tecnico
-- Reemplaza: get_servicios_aceptados_for_tecnico()
--   - Busca cotizaciones aceptadas del técnico con
--     solicitudes en estado 'en_proceso'
--   - Incluye datos de categoría, zona y cliente
-- Uso: SELECT * FROM rpc_servicios_aceptados_tecnico(1);
-- =========================================================

create or replace function rpc_servicios_aceptados_tecnico(p_id_tecnico bigint)
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select coalesce(json_agg(
    json_build_object(
      'id_solicitud', s.id_solicitud,
      'titulo', coalesce(s.titulo, ''),
      'descripcion', coalesce(s.descripcion, ''),
      'direccion_referencia', s.direccion_referencia,
      'estado', coalesce(s.estado, ''),
      'fecha_publicacion', s.fecha_publicacion,
      'categoria_nombre', coalesce(c.nombre, ''),
      'zona_nombre', coalesce(z.nombre, ''),
      'cliente_nombre', trim(
        coalesce(u.nombres, '') || ' ' || coalesce(u.apellidos, '')
      ),
      'id_cotizacion', ct.id_cotizacion,
      'precio', ct.monto::float8,
      'tiempo_estimado', ct.tiempo_estimado,
      'estado_cotizacion', coalesce(ct.estado, '')
    )
    order by ct.fecha_envio desc
  ), '[]'::json)
  into result_json
  from cotizaciones ct
  join solicitudes_servicio s on s.id_solicitud = ct.id_solicitud
  join categorias_servicio c on c.id_categoria = s.id_categoria
  join zonas z on z.id_zona = s.id_zona
  join clientes cl on cl.id_cliente = s.id_cliente
  join usuarios u on u.id_usuario = cl.id_usuario
  where ct.id_tecnico = p_id_tecnico
    and ct.estado = 'aceptada'
    and s.estado = 'en_proceso';

  return result_json;
end;
$$;


-- =========================================================
-- Seguridad: solo service_role
-- =========================================================

revoke execute on function rpc_solicitudes_disponibles_tecnico(bigint) from public, anon, authenticated;
revoke execute on function rpc_servicios_aceptados_tecnico(bigint) from public, anon, authenticated;

grant execute on function rpc_solicitudes_disponibles_tecnico(bigint) to service_role;
grant execute on function rpc_servicios_aceptados_tecnico(bigint) to service_role;
