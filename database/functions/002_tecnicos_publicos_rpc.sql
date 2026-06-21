-- =========================================================
-- Función: rpc_listar_tecnicos_publicos
-- Reemplaza: client.table("tecnicos").select(...).eq("estado_validacion", "validado")
-- Incluye: usuario, categorías, zonas, calificación promedio
-- Uso:       SELECT * FROM rpc_listar_tecnicos_publicos();
-- =========================================================

create or replace function rpc_listar_tecnicos_publicos()
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
      'usuarios', json_build_object(
        'id_usuario', u.id_usuario,
        'nombres', u.nombres,
        'apellidos', u.apellidos
      ),
      'tecnico_categorias', coalesce(
        (select json_agg(
          json_build_object(
            'categorias_servicio', json_build_object(
              'id_categoria', cs.id_categoria,
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
              'id_zona', z.id_zona,
              'nombre', z.nombre
            )
          )
        )
        from tecnico_zonas tz
        join zonas z on z.id_zona = tz.id_zona
        where tz.id_tecnico = t.id_tecnico),
        '[]'::json
      ),
      'calificacion', (
        select round(avg(v.puntuacion)::numeric, 1)::double precision
        from cotizaciones ct
        join valoraciones v on v.id_cotizacion = ct.id_cotizacion
        where ct.id_tecnico = t.id_tecnico
      )
    )
    order by u.nombres, u.apellidos
  ), '[]'::json)
  into result_json
  from tecnicos t
  join usuarios u on u.id_usuario = t.id_usuario
  where t.estado_validacion = 'validado';

  return result_json;
end;
$$;

-- =========================================================
-- Función: rpc_get_tecnico_publico_by_id(p_id_tecnico bigint)
-- Reemplaza: client.table("tecnicos").select(...).eq("id_tecnico", id).eq("estado_validacion", "validado")
--            + get_portafolio() + _calcular_calificacion()
-- Incluye: usuario, categorías, zonas, calificación, portafolio visible
-- Uso:      SELECT * FROM rpc_get_tecnico_publico_by_id(1);
-- =========================================================

create or replace function rpc_get_tecnico_publico_by_id(p_id_tecnico bigint)
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select json_build_object(
    'id_tecnico', t.id_tecnico,
    'descripcion', t.descripcion,
    'experiencia_anios', t.experiencia_anios,
    'usuarios', json_build_object(
      'id_usuario', u.id_usuario,
      'nombres', u.nombres,
      'apellidos', u.apellidos
    ),
    'tecnico_categorias', coalesce(
      (select json_agg(
        json_build_object(
          'categorias_servicio', json_build_object(
            'id_categoria', cs.id_categoria,
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
            'id_zona', z.id_zona,
            'nombre', z.nombre
          )
        )
      )
      from tecnico_zonas tz
      join zonas z on z.id_zona = tz.id_zona
      where tz.id_tecnico = t.id_tecnico),
      '[]'::json
    ),
    'calificacion', (
      select round(avg(v.puntuacion)::numeric, 1)::double precision
      from cotizaciones ct
      join valoraciones v on v.id_cotizacion = ct.id_cotizacion
      where ct.id_tecnico = t.id_tecnico
    ),
    'portafolio', coalesce(
      (select json_agg(
        json_build_object(
          'id_portafolio', pt.id_portafolio,
          'titulo', pt.titulo,
          'descripcion', pt.descripcion,
          'imagen_url', pt.imagen_url
        )
        order by pt.fecha_subida desc
      )
      from portafolio_tecnico pt
      where pt.id_tecnico = t.id_tecnico
        and pt.estado = 'visible'),
      '[]'::json
    )
  )
  into result_json
  from tecnicos t
  join usuarios u on u.id_usuario = t.id_usuario
  where t.id_tecnico = p_id_tecnico
    and t.estado_validacion = 'validado';

  return result_json;
end;
$$;
