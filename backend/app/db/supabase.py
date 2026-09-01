from supabase import Client,create_client
from app.core.config import settings

def get_supabase_client() -> Client:
    if not settings.SUPABASE_URL:
        raise RuntimeError("SUPABASE URL is not configured")
    if not settings.SUPABASE_KEY:
        raise RuntimeError("SUPABASE_KEy is not configured")
    return create_client(settings.SUPABASE_URL , settings.SUPABASE_KEY)