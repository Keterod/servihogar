from postgrest.exceptions import APIError
from supabase import create_client
from supabase._sync.client import SupabaseException

from src.core.config import settings


def _format_api_error(exc: APIError, context: str) -> str:
    parts = [f"Supabase query failed ({context})"]
    if exc.message:
        parts.append(exc.message)
    if exc.code:
        parts.append(f"code={exc.code}")
    if exc.details:
        parts.append(f"details={exc.details}")
    if exc.hint:
        parts.append(f"hint={exc.hint}")
    return " | ".join(parts)


class SupabaseClient:
    """Singleton Supabase client for backend data access.

    Uses SUPABASE_SERVICE_ROLE_KEY to bypass RLS until public policies are defined.
    SUPABASE_ANON_KEY remains in settings for future frontend/client use only.
    """

    _instance = None

    @classmethod
    def get(cls):
        if cls._instance is None:
            if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
                raise SupabaseException(
                    "Supabase not configured. Set SUPABASE_URL and "
                    "SUPABASE_SERVICE_ROLE_KEY in .env"
                )
            cls._instance = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_ROLE_KEY,
            )
        return cls._instance

    @staticmethod
    def execute(query, *, context: str = "consulta Supabase"):
        """Run a Supabase query and map API errors to SupabaseException."""
        try:
            return query.execute()
        except APIError as exc:
            raise SupabaseException(_format_api_error(exc, context)) from exc
