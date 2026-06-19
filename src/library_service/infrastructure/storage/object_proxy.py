import uuid

from src.library_service.config import settings


def object_proxy(obj_id: uuid.UUID) -> str:
    base = settings.PUBLIC_BASE_URL.rstrip("/")
    return f"{base}/documents/{obj_id}/object"