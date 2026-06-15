from src.repository.cotizaciones_repository import CotizacionesRepository
from src.repository.solicitudes_repository import SolicitudesRepository
from src.repository.valoraciones_repository import ValoracionesRepository
from src.schemas.valoracion import ValoracionRequest, ValoracionResponse


class ValoracionError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


class ValoracionesService:
    _ELIGIBLE_ESTADOS = frozenset({"en_proceso", "finalizada"})

    def __init__(self):
        self._repo = ValoracionesRepository()
        self._cotizaciones_repo = CotizacionesRepository()
        self._solicitudes_repo = SolicitudesRepository()

    def _get_solicitud_para_cliente(self, id_solicitud: int, id_cliente: int) -> dict:
        solicitud = self._solicitudes_repo.get_by_id_for_cliente(id_solicitud, id_cliente)
        if solicitud is not None:
            return solicitud

        exists = self._solicitudes_repo.get_solicitud_by_id(id_solicitud)
        if exists is None:
            raise ValoracionError("not_found", "Solicitud no encontrada")
        raise ValoracionError(
            "forbidden",
            "No tienes permiso para valorar esta solicitud",
        )

    def crear_valoracion_para_cliente(
        self, id_cliente: int, data: ValoracionRequest
    ) -> ValoracionResponse:
        solicitud = self._get_solicitud_para_cliente(data.id_solicitud, id_cliente)

        estado = solicitud.get("estado")
        if estado not in self._ELIGIBLE_ESTADOS:
            raise ValoracionError(
                "bad_request",
                "La solicitud no está en un estado válido para valorar",
            )

        cotizacion = self._cotizaciones_repo.get_accepted_for_solicitud(data.id_solicitud)
        if cotizacion is None:
            raise ValoracionError(
                "bad_request",
                "La solicitud no tiene una cotización aceptada",
            )

        id_cotizacion = cotizacion["id_cotizacion"]
        if self._repo.exists_for_cotizacion(id_cotizacion):
            raise ValoracionError(
                "conflict",
                "Esta solicitud ya fue valorada",
            )

        record = {
            "id_cotizacion": id_cotizacion,
            "puntuacion": data.calificacion,
            "comentario": data.comentario,
            "puntualidad": data.puntualidad,
            "calidad": data.calidad,
            "trato": data.trato,
            "precio": data.precio,
        }
        inserted = self._repo.insert(record)
        if inserted is None:
            raise ValoracionError("failed", "No se pudo guardar la valoración")

        solicitud_estado = estado
        if estado == "en_proceso":
            updated = self._solicitudes_repo.update_estado(data.id_solicitud, "finalizada")
            if updated is None:
                raise ValoracionError("failed", "No se pudo actualizar el estado de la solicitud")
            solicitud_estado = updated["estado"]

        return ValoracionResponse(
            id_valoracion=inserted["id_valoracion"],
            id_cotizacion=id_cotizacion,
            id_solicitud=data.id_solicitud,
            puntuacion=inserted["puntuacion"],
            comentario=inserted.get("comentario"),
            puntualidad=inserted.get("puntualidad"),
            calidad=inserted.get("calidad"),
            precio=inserted.get("precio"),
            trato=inserted.get("trato"),
            fecha_valoracion=inserted["fecha_valoracion"],
            solicitud_estado=solicitud_estado,
        )

    def crear_valoracion_demo(self, data: ValoracionRequest) -> ValoracionResponse:
        id_cliente = self._solicitudes_repo.get_demo_cliente_id()
        if id_cliente is None:
            raise ValoracionError("failed", "Cliente demo no disponible")
        return self.crear_valoracion_para_cliente(id_cliente, data)
