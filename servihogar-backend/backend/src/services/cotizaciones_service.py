from src.repository.cotizaciones_repository import CotizacionesRepository
from src.repository.solicitudes_repository import SolicitudesRepository
from src.repository.tecnicos_repository import TecnicosRepository
from src.schemas.cotizacion import (
    CotizacionActionResponse,
    CotizacionRequest,
    CotizacionResponse,
)


class CotizacionError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


class CotizacionesService:
    def __init__(self):
        self._repo = CotizacionesRepository()
        self._solicitudes_repo = SolicitudesRepository()
        self._tecnicos_repo = TecnicosRepository()

    @staticmethod
    def _to_action_response(row: dict, solicitud_estado: str) -> CotizacionActionResponse:
        return CotizacionActionResponse(
            id_cotizacion=row["id_cotizacion"],
            id_solicitud=row["id_solicitud"],
            precio=float(row["monto"]),
            tiempo_estimado=row.get("tiempo_estimado"),
            descripcion_propuesta=row["descripcion"],
            estado=row["estado"],
            fecha_creacion=row["fecha_envio"],
            solicitud_estado=solicitud_estado,
        )

    def _get_cotizacion_for_cliente(
        self, id_cotizacion: int, id_cliente: int
    ) -> tuple[dict, dict]:
        cotizacion = self._repo.get_by_id(id_cotizacion)
        if cotizacion is None:
            raise CotizacionError("not_found", "Cotización no encontrada")

        solicitud = self._solicitudes_repo.get_by_id_for_cliente(
            cotizacion["id_solicitud"], id_cliente
        )
        if solicitud is None:
            raise CotizacionError(
                "forbidden",
                "No tienes permiso para gestionar esta cotización",
            )

        return cotizacion, solicitud

    def _get_cotizacion_for_demo_client(self, id_cotizacion: int) -> tuple[dict, dict]:
        id_cliente = self._solicitudes_repo.get_demo_cliente_id()
        if id_cliente is None:
            raise CotizacionError("failed", "Cliente demo no disponible")
        return self._get_cotizacion_for_cliente(id_cotizacion, id_cliente)

    def crear_cotizacion_demo(self, data: CotizacionRequest) -> CotizacionResponse:
        id_tecnico = self._tecnicos_repo.get_demo_tecnico_id()
        if id_tecnico is None:
            raise CotizacionError("failed", "Técnico demo no disponible")
        return self.crear_cotizacion_para_tecnico(id_tecnico, data)

    def crear_cotizacion_para_tecnico(
        self, id_tecnico: int, data: CotizacionRequest
    ) -> CotizacionResponse:
        categorias = self._tecnicos_repo.get_categorias_for_tecnico(id_tecnico)
        zonas = self._tecnicos_repo.get_zonas_for_tecnico(id_tecnico)

        solicitud = self._solicitudes_repo.get_solicitud_for_cotizacion(
            data.id_solicitud, categorias, zonas
        )
        if solicitud is None:
            exists = self._solicitudes_repo.get_solicitud_by_id(data.id_solicitud)
            if exists is None:
                raise CotizacionError("not_found", "Solicitud no encontrada")
            if exists["estado"] != "pendiente":
                raise CotizacionError(
                    "bad_request",
                    "Solo se pueden cotizar solicitudes en estado pendiente",
                )
            raise CotizacionError(
                "bad_request",
                "La solicitud no corresponde a las categorías o zonas del técnico",
            )

        if self._repo.exists_for_tecnico(data.id_solicitud, id_tecnico):
            raise CotizacionError(
                "duplicate",
                "Ya enviaste una cotización para esta solicitud",
            )

        record = {
            "id_solicitud": data.id_solicitud,
            "id_tecnico": id_tecnico,
            "monto": data.precio,
            "descripcion": data.descripcion_propuesta,
            "tiempo_estimado": data.tiempo_estimado,
        }
        result = self._repo.insert(record)
        if result is None:
            raise CotizacionError("failed", "No se pudo crear la cotización")

        return CotizacionResponse(
            id_cotizacion=result["id_cotizacion"],
            id_solicitud=result["id_solicitud"],
            id_tecnico=result["id_tecnico"],
            precio=float(result["monto"]),
            tiempo_estimado=result.get("tiempo_estimado"),
            descripcion_propuesta=result["descripcion"],
            estado=result["estado"],
            fecha_creacion=result["fecha_envio"],
        )

    def aceptar_cotizacion_para_cliente(
        self, id_cotizacion: int, id_cliente: int
    ) -> CotizacionActionResponse:
        cotizacion, solicitud = self._get_cotizacion_for_cliente(id_cotizacion, id_cliente)

        if cotizacion["estado"] != "pendiente":
            raise CotizacionError(
                "bad_request",
                "Solo se pueden aceptar cotizaciones en estado pendiente",
            )

        if solicitud["estado"] != "pendiente":
            raise CotizacionError(
                "bad_request",
                "Solo se pueden aceptar cotizaciones de solicitudes en estado pendiente",
            )

        if self._repo.has_accepted_for_solicitud(cotizacion["id_solicitud"]):
            raise CotizacionError(
                "conflict",
                "Esta solicitud ya tiene una cotización aceptada",
            )

        updated = self._repo.update_estado(id_cotizacion, "aceptada")
        if updated is None:
            raise CotizacionError("failed", "No se pudo aceptar la cotización")

        if not self._repo.reject_pending_others(
            cotizacion["id_solicitud"], id_cotizacion
        ):
            raise CotizacionError("failed", "No se pudo actualizar las cotizaciones")

        solicitud_updated = self._solicitudes_repo.update_estado(
            cotizacion["id_solicitud"], "en_proceso"
        )
        if solicitud_updated is None:
            raise CotizacionError("failed", "No se pudo actualizar la solicitud")

        return self._to_action_response(updated, solicitud_updated["estado"])

    def rechazar_cotizacion_para_cliente(
        self, id_cotizacion: int, id_cliente: int
    ) -> CotizacionActionResponse:
        cotizacion, solicitud = self._get_cotizacion_for_cliente(id_cotizacion, id_cliente)

        if cotizacion["estado"] != "pendiente":
            raise CotizacionError(
                "bad_request",
                "Solo se pueden rechazar cotizaciones en estado pendiente",
            )

        updated = self._repo.update_estado(id_cotizacion, "rechazada")
        if updated is None:
            raise CotizacionError("failed", "No se pudo rechazar la cotización")

        return self._to_action_response(updated, solicitud["estado"])

    def aceptar_cotizacion_demo(self, id_cotizacion: int) -> CotizacionActionResponse:
        id_cliente = self._solicitudes_repo.get_demo_cliente_id()
        if id_cliente is None:
            raise CotizacionError("failed", "Cliente demo no disponible")
        return self.aceptar_cotizacion_para_cliente(id_cotizacion, id_cliente)

    def rechazar_cotizacion_demo(self, id_cotizacion: int) -> CotizacionActionResponse:
        id_cliente = self._solicitudes_repo.get_demo_cliente_id()
        if id_cliente is None:
            raise CotizacionError("failed", "Cliente demo no disponible")
        return self.rechazar_cotizacion_para_cliente(id_cotizacion, id_cliente)
