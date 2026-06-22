-- =========================================================
-- rpc_admin_resumen()
-- Reemplaza: 12 consultas count individuales en AdminRepository.get_resumen_counts()
-- Uso:       SELECT * FROM rpc_admin_resumen();
-- =========================================================

create or replace function rpc_admin_resumen()
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select json_build_object(
    'total_usuarios', (select count(*) from usuarios),
    'total_clientes', (select count(*) from clientes),
    'total_tecnicos', (select count(*) from tecnicos),
    'total_solicitudes', (select count(*) from solicitudes_servicio),
    'solicitudes_pendientes', (select count(*) from solicitudes_servicio where estado = 'pendiente'),
    'solicitudes_en_proceso', (select count(*) from solicitudes_servicio where estado = 'en_proceso'),
    'solicitudes_finalizadas', (select count(*) from solicitudes_servicio where estado = 'finalizada'),
    'tecnicos_pendientes', (select count(*) from tecnicos where estado_validacion = 'pendiente'),
    'tecnicos_validados', (select count(*) from tecnicos where estado_validacion = 'validado'),
    'tecnicos_rechazados', (select count(*) from tecnicos where estado_validacion = 'rechazado'),
    'total_cotizaciones', (select count(*) from cotizaciones),
    'total_valoraciones', (select count(*) from valoraciones)
  ) into result_json;
  return result_json;
end;
$$;

-- =========================================================
-- rpc_admin_tecnicos_pendientes()
-- Reemplaza: client.table("tecnicos").select(...).eq("estado_validacion", "pendiente")
-- Incluye: usuarios, categorías, zonas
-- Orden:   fecha_solicitud_validacion DESC
-- Uso:     SELECT * FROM rpc_admin_tecnicos_pendientes();
-- =========================================================

create or replace function rpc_admin_tecnicos_pendientes()
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select coalesce(json_agg(
    json_build_object(
      'id_tecnico', t.id_tecnico,
      'descripcion', t.descripcion,
      'experiencia_anios', t.experiencia_anios,
      'estado_validacion', t.estado_validacion,
      'fecha_solicitud_validacion', t.fecha_solicitud_validacion,
      'usuarios', json_build_object(
        'nombres', u.nombres,
        'apellidos', u.apellidos,
        'telefono', u.telefono,
        'fecha_registro', u.fecha_registro
      ),
      'tecnico_categorias', coalesce(
        (select json_agg(
          json_build_object(
            'categorias_servicio', json_build_object(
              'nombre', cs.nombre
            )
          )
        )
        from tecnico_categorias tc
        join categorias_servicio cs on cs.id_categoria = tc.id_categoria
        where tc.id_tecnico = t.id_tecnico),
        '[]'::json
      ),
      'tecnico_zonas', coalesce(
        (select json_agg(
          json_build_object(
            'zonas', json_build_object(
              'nombre', z.nombre
            )
          )
        )
        from tecnico_zonas tz
        join zonas z on z.id_zona = tz.id_zona
        where tz.id_tecnico = t.id_tecnico),
        '[]'::json
      )
    )
    order by t.fecha_solicitud_validacion desc
  ), '[]'::json)
  into result_json
  from tecnicos t
  join usuarios u on u.id_usuario = t.id_usuario
  where t.estado_validacion = 'pendiente';

  return result_json;
end;
$$;

-- =========================================================
-- rpc_admin_get_tecnico_estado(p_id_tecnico bigint)
-- Reemplaza: client.table("tecnicos").select("id_tecnico, estado_validacion").eq("id_tecnico", id)
-- Devuelve:  { id_tecnico, estado_validacion } o null si no existe
-- Uso:       SELECT * FROM rpc_admin_get_tecnico_estado(1);
-- =========================================================

create or replace function rpc_admin_get_tecnico_estado(p_id_tecnico bigint)
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select json_build_object(
    'id_tecnico', t.id_tecnico,
    'estado_validacion', t.estado_validacion
  )
  into result_json
  from tecnicos t
  where t.id_tecnico = p_id_tecnico;

  return result_json;
end;
$$;

-- =========================================================
-- rpc_admin_actualizar_estado_tecnico(
--   p_id_tecnico bigint,
--   p_estado_validacion text
-- )
-- Reemplaza: client.table("tecnicos").update(...).eq(...).select(...)
-- Solo permite: 'validado', 'rechazado', 'pendiente'
-- Si es validado, actualiza fecha_validacion = now()
-- Respuestas:
--   Éxito:  { ok: true, tecnico: { id_tecnico, estado_validacion } }
--   No encontrado: { ok: false, code: 'not_found' }
--   Estado inválido: { ok: false, code: 'bad_request' }
-- Uso:      SELECT * FROM rpc_admin_actualizar_estado_tecnico(1, 'validado');
-- =========================================================

create or replace function rpc_admin_actualizar_estado_tecnico(
  p_id_tecnico bigint,
  p_estado_validacion text
)
returns json
language plpgsql
as $$
declare
  v_exists boolean;
  result_json json;
begin
  if p_estado_validacion not in ('validado', 'rechazado', 'pendiente') then
    return json_build_object('ok', false, 'code', 'bad_request');
  end if;

  select exists(select 1 from tecnicos where id_tecnico = p_id_tecnico) into v_exists;
  if not v_exists then
    return json_build_object('ok', false, 'code', 'not_found');
  end if;

  if p_estado_validacion = 'validado' then
    update tecnicos
    set estado_validacion = p_estado_validacion,
        fecha_validacion = now()
    where id_tecnico = p_id_tecnico;
  else
    update tecnicos
    set estado_validacion = p_estado_validacion
    where id_tecnico = p_id_tecnico;
  end if;

  select json_build_object(
    'ok', true,
    'tecnico', json_build_object(
      'id_tecnico', t.id_tecnico,
      'estado_validacion', t.estado_validacion
    )
  )
  into result_json
  from tecnicos t
  where t.id_tecnico = p_id_tecnico;

  return result_json;
end;
$$;

-- =========================================================
-- Grants (solo service_role)
-- =========================================================

grant execute on function rpc_admin_resumen to service_role;
grant execute on function rpc_admin_tecnicos_pendientes to service_role;
grant execute on function rpc_admin_get_tecnico_estado(bigint) to service_role;
grant execute on function rpc_admin_actualizar_estado_tecnico(bigint, text) to service_role;
