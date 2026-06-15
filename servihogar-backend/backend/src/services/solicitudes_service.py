from src.repository.solicitudes_repository import SolicitudesRepository
from src.repository.tecnicos_repository import TecnicosRepository
from src.schemas.solicitud import (
    CotizacionDetalleResponse,
    ServicioAceptadoResponse,
    SolicitudDetalleResponse,
    SolicitudDisponibleResponse,
    SolicitudListResponse,
    SolicitudRequest,
    SolicitudResponse,
)


class SolicitudesService:
    def __init__(self):
        self._repo = SolicitudesRepository()
        self._tecnicos_repo = TecnicosRepository()

    def crear_solicitud(self, data: SolicitudRequest) -> SolicitudResponse | None:
        id_cliente = self._repo.get_demo_cliente_id()
        if id_cliente is None:
            return None

        record = {
            "id_cliente": id_cliente,
            "id_categoria": data.id_categoria,
            "id_zona": data.id_zona,
            "titulo": data.titulo,
            "descripcion": data.descripcion,
            "direccion_referencia": data.direccion_referencia,
        }

        result = self._repo.insert(record)
        if result is None:
            return None

        return SolicitudResponse(
            id_solicitud=result["id_solicitud"],
            id_cliente=result["id_cliente"],
            estado=result["estado"],
            fecha_publicacion=result["fecha_publicacion"],
        )

    def obtener_por_cliente(self) -> list[SolicitudListResponse]:
        id_cliente = self._repo.get_demo_cliente_id()
        if id_cliente is None:
            return []

        rows = self._repo.get_by_cliente_id(id_cliente)
        return [
            SolicitudListResponse(
                id_solicitud=r["id_solicitud"],
                titulo=r["titulo"],
                descripcion=r["descripcion"],
                direccion=r.get("direccion_referencia"),
                estado=r["estado"],
                fecha_publicacion=r["fecha_publicacion"],
                categoria_nombre=r["categoria_nombre"],
                zona_nombre=r["zona_nombre"],
                cotizaciones_count=r["cotizaciones_count"],
            )
            for r in rows
        ]

    def obtener_detalle(self, id_solicitud: int) -> SolicitudDetalleResponse | None:
        id_cliente = self._repo.get_demo_cliente_id()
        if id_cliente is None:
            return None

        row = self._repo.get_by_id_for_cliente(id_solicitud, id_cliente)
        if row is None:
            return None

        cotizaciones_rows = self._repo.get_cotizaciones_by_solicitud(id_solicitud)
        cotizaciones = [
            CotizacionDetalleResponse(
                id_cotizacion=c["id_cotizacion"],
                id_tecnico=c["id_tecnico"],
                tecnico_nombre=c["tecnico_nombre"],
                tecnico_descripcion=c.get("tecnico_descripcion"),
                precio=c["precio"],
                tiempo_estimado=c.get("tiempo_estimado"),
                descripcion_propuesta=c["descripcion_propuesta"],
                estado=c["estado"],
                fecha_creacion=c["fecha_creacion"],
            )
            for c in cotizaciones_rows
        ]

        return SolicitudDetalleResponse(
            id_solicitud=row["id_solicitud"],
            titulo=row["titulo"],
            descripcion=row["descripcion"],
            direccion=row.get("direccion_referencia"),
            estado=row["estado"],
            fecha_publicacion=row["fecha_publicacion"],
            categoria_nombre=row["categoria_nombre"],
            zona_nombre=row["zona_nombre"],
            cotizaciones=cotizaciones,
        )

    def obtener_solicitudes_disponibles_demo(self) -> list[SolicitudDisponibleResponse]:
        """Return pending solicitudes matching the demo technician's categories and zones.

        Only solicitudes with estado=pendiente are included. A solicitud must match
        both a category and a zone assigned to the demo technician in tecnico_categorias
        and tecnico_zonas. Already-quoted solicitudes remain in the list with
        ya_cotizada_por_tecnico=True.
        """
        id_tecnico = self._tecnicos_repo.get_demo_tecnico_id()
        if id_tecnico is None:
            return []

        categorias = self._tecnicos_repo.get_categorias_for_tecnico(id_tecnico)
        zonas = self._tecnicos_repo.get_zonas_for_tecnico(id_tecnico)
        rows = self._repo.get_disponibles_for_tecnico(id_tecnico, categorias, zonas)

        return [
            SolicitudDisponibleResponse(
                id_solicitud=r["id_solicitud"],
                titulo=r["titulo"],
                descripcion=r["descripcion"],
                direccion=r.get("direccion_referencia"),
                estado=r["estado"],
                fecha_publicacion=r["fecha_publicacion"],
                categoria_nombre=r["categoria_nombre"],
                zona_nombre=r["zona_nombre"],
                cliente_nombre=r.get("cliente_nombre"),
                cotizaciones_count=r["cotizaciones_count"],
                ya_cotizada_por_tecnico=r["ya_cotizada_por_tecnico"],
            )
            for r in rows
        ]

    def obtener_servicios_aceptados_demo(self) -> list[ServicioAceptadoResponse]:
        """Return in-progress solicitudes where the demo technician has an accepted cotización."""
        id_tecnico = self._tecnicos_repo.get_demo_tecnico_id()
        if id_tecnico is None:
            return []

        try:
            rows = self._repo.get_servicios_aceptados_for_tecnico(id_tecnico)
        except Exception:
            return []

        servicios: list[ServicioAceptadoResponse] = []
        for r in rows:
            try:
                servicios.append(
                    ServicioAceptadoResponse(
                        id_solicitud=r["id_solicitud"],
                        titulo=r.get("titulo") or "",
                        descripcion=r.get("descripcion") or "",
                        direccion=r.get("direccion_referencia"),
                        estado=r.get("estado") or "",
                        fecha_publicacion=r["fecha_publicacion"],
                        categoria_nombre=r.get("categoria_nombre") or "",
                        zona_nombre=r.get("zona_nombre") or "",
                        cliente_nombre=r.get("cliente_nombre"),
                        id_cotizacion=r["id_cotizacion"],
                        precio=r["precio"],
                        tiempo_estimado=r.get("tiempo_estimado"),
                        estado_cotizacion=r.get("estado_cotizacion") or "",
                    )
                )
            except Exception:
                continue

        return servicios
