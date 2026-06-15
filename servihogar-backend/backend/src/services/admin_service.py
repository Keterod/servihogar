from src.repository.admin_repository import AdminRepository
from src.schemas.admin import (
    AdminResumenResponse,
    TecnicoPendienteAdminResponse,
    TecnicoValidacionResponse,
)


class AdminError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


class AdminService:
    def __init__(self):
        self._repo = AdminRepository()

    def obtener_resumen_demo(self) -> AdminResumenResponse:
        return AdminResumenResponse(**self._repo.get_resumen_counts())

    def obtener_tecnicos_pendientes_demo(
        self,
    ) -> list[TecnicoPendienteAdminResponse]:
        return [self._map_tecnico_pendiente(row) for row in self._repo.get_tecnicos_pendientes()]

    def aprobar_tecnico_demo(self, id_tecnico: int) -> TecnicoValidacionResponse:
        return self._actualizar_tecnico_pendiente(id_tecnico, "validado")

    def rechazar_tecnico_demo(self, id_tecnico: int) -> TecnicoValidacionResponse:
        return self._actualizar_tecnico_pendiente(id_tecnico, "rechazado")

    def _actualizar_tecnico_pendiente(
        self, id_tecnico: int, nuevo_estado: str
    ) -> TecnicoValidacionResponse:
        tecnico = self._repo.get_tecnico_estado(id_tecnico)
        if tecnico is None:
            raise AdminError("not_found", "Técnico no encontrado")

        estado_actual = tecnico.get("estado_validacion")
        if estado_actual != "pendiente":
            raise AdminError(
                "conflict",
                f"El técnico ya está en estado {estado_actual}",
            )

        actualizado = self._repo.update_tecnico_estado(id_tecnico, nuevo_estado)
        if actualizado is None:
            raise AdminError("failed", "No se pudo actualizar el técnico")

        return TecnicoValidacionResponse(
            id_tecnico=actualizado["id_tecnico"],
            estado_validacion=actualizado["estado_validacion"],
        )

    def _map_tecnico_pendiente(self, row: dict) -> TecnicoPendienteAdminResponse:
        usuario = self._unwrap_embedded(row.get("usuarios")) or {}
        fecha_registro = usuario.get("fecha_registro") or row["fecha_solicitud_validacion"]

        return TecnicoPendienteAdminResponse(
            id_tecnico=row["id_tecnico"],
            nombres=usuario.get("nombres", ""),
            apellidos=usuario.get("apellidos", ""),
            email=None,
            telefono=usuario.get("telefono"),
            descripcion=row.get("descripcion"),
            experiencia_anios=row["experiencia_anios"],
            fecha_registro=fecha_registro,
            estado_validacion=row["estado_validacion"],
            categorias=self._map_nombres(
                row.get("tecnico_categorias") or [], "categorias_servicio"
            ),
            zonas=self._map_nombres(row.get("tecnico_zonas") or [], "zonas"),
        )

    @staticmethod
    def _map_nombres(rows: list, embedded_key: str) -> list[str]:
        nombres = []
        for row in rows:
            item = AdminService._unwrap_embedded(row.get(embedded_key))
            if isinstance(item, dict) and item.get("nombre"):
                nombres.append(item["nombre"])
        return nombres

    @staticmethod
    def _unwrap_embedded(value):
        if isinstance(value, list):
            return value[0] if value else None
        return value
