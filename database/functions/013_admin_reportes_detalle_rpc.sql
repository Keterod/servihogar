-- =========================================================
-- rpc_admin_reporte_usuarios()
-- Lista todos los usuarios registrados con su rol detectado
-- Uso: SELECT * FROM rpc_admin_reporte_usuarios();
-- =========================================================

create or replace function rpc_admin_reporte_usuarios()
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select coalesce(json_agg(
    json_build_object(
      'id_usuario', u.id_usuario,
      'nombres', u.nombres,
      'apellidos', u.apellidos,
      'telefono', u.telefono,
      'estado', u.estado,
      'fecha_registro', u.fecha_registro,
      'rol', case
        when a.id_administrador is not null then 'administrador'
        when t.id_tecnico is not null then 'tecnico'
        when c.id_cliente is not null then 'cliente'
        else 'sin_rol'
      end
    )
    order by u.fecha_registro desc
  ), '[]'::json)
  into result_json
  from usuarios u
  left join clientes c on c.id_usuario = u.id_usuario
  left join tecnicos t on t.id_usuario = u.id_usuario
  left join administradores a on a.id_usuario = u.id_usuario;

  return result_json;
end;
$$;

-- =========================================================
-- rpc_admin_reporte_solicitudes()
-- Lista todas las solicitudes publicadas con detalles
-- Uso: SELECT * FROM rpc_admin_reporte_solicitudes();
-- =========================================================

create or replace function rpc_admin_reporte_solicitudes()
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
      'categoria', c.nombre,
      'zona', z.nombre,
      'cliente', trim(coalesce(u.nombres, '') || ' ' || coalesce(u.apellidos, '')),
      'estado', s.estado,
      'fecha_publicacion', s.fecha_publicacion
    )
    order by s.fecha_publicacion desc
  ), '[]'::json)
  into result_json
  from solicitudes_servicio s
  join categorias_servicio c on c.id_categoria = s.id_categoria
  join zonas z on z.id_zona = s.id_zona
  join clientes cl on cl.id_cliente = s.id_cliente
  join usuarios u on u.id_usuario = cl.id_usuario;

  return result_json;
end;
$$;

-- =========================================================
-- rpc_admin_reporte_cotizaciones()
-- Lista todas las cotizaciones registradas con detalles
-- Uso: SELECT * FROM rpc_admin_reporte_cotizaciones();
-- =========================================================

create or replace function rpc_admin_reporte_cotizaciones()
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select coalesce(json_agg(
    json_build_object(
      'id_cotizacion', ct.id_cotizacion,
      'solicitud', s.titulo,
      'tecnico', trim(coalesce(u.nombres, '') || ' ' || coalesce(u.apellidos, '')),
      'monto', ct.monto::double precision,
      'estado', ct.estado,
      'fecha_envio', ct.fecha_envio
    )
    order by ct.fecha_envio desc
  ), '[]'::json)
  into result_json
  from cotizaciones ct
  join solicitudes_servicio s on s.id_solicitud = ct.id_solicitud
  join tecnicos t on t.id_tecnico = ct.id_tecnico
  join usuarios u on u.id_usuario = t.id_usuario;

  return result_json;
end;
$$;

-- =========================================================
-- rpc_admin_reporte_servicios_finalizados()
-- Lista solicitudes en estado 'finalizada' con técnico aceptado
-- Uso: SELECT * FROM rpc_admin_reporte_servicios_finalizados();
-- =========================================================

create or replace function rpc_admin_reporte_servicios_finalizados()
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
      'cliente', trim(coalesce(uc.nombres, '') || ' ' || coalesce(uc.apellidos, '')),
      'tecnico', trim(coalesce(ut.nombres, '') || ' ' || coalesce(ut.apellidos, '')),
      'estado', s.estado,
      'fecha_publicacion', s.fecha_publicacion
    )
    order by s.fecha_publicacion desc
  ), '[]'::json)
  into result_json
  from solicitudes_servicio s
  join clientes cl on cl.id_cliente = s.id_cliente
  join usuarios uc on uc.id_usuario = cl.id_usuario
  join cotizaciones ct on ct.id_solicitud = s.id_solicitud and ct.estado = 'aceptada'
  join tecnicos t on t.id_tecnico = ct.id_tecnico
  join usuarios ut on ut.id_usuario = t.id_usuario
  where s.estado = 'finalizada';

  return result_json;
end;
$$;

-- =========================================================
-- rpc_admin_reporte_tecnicos_activos()
-- Lista técnicos validados con categorías y zonas
-- Uso: SELECT * FROM rpc_admin_reporte_tecnicos_activos();
-- =========================================================

create or replace function rpc_admin_reporte_tecnicos_activos()
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
      'nombres', u.nombres,
      'apellidos', u.apellidos,
      'telefono', u.telefono,
      'experiencia_anios', t.experiencia_anios,
      'categorias', coalesce(
        (select json_agg(cs.nombre)
         from tecnico_categorias tc
         join categorias_servicio cs on cs.id_categoria = tc.id_categoria
         where tc.id_tecnico = t.id_tecnico),
        '[]'::json
      ),
      'zonas', coalesce(
        (select json_agg(z.nombre)
         from tecnico_zonas tz
         join zonas z on z.id_zona = tz.id_zona
         where tz.id_tecnico = t.id_tecnico),
        '[]'::json
      ),
      'fecha_validacion', t.fecha_validacion
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
-- Grants (solo service_role)
-- =========================================================

grant execute on function rpc_admin_reporte_usuarios to service_role;
grant execute on function rpc_admin_reporte_solicitudes to service_role;
grant execute on function rpc_admin_reporte_cotizaciones to service_role;
grant execute on function rpc_admin_reporte_servicios_finalizados to service_role;
grant execute on function rpc_admin_reporte_tecnicos_activos to service_role;
