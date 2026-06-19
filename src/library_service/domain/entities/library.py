import uuid
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


class LibraryResponseSchema(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    document_url: str
    title: str
    file_type: str

    minio_raw_key:str
    minio_compressed_key: Optional[str] = None
    original_size: Optional[int] = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class LibraryCreateSchema(BaseModel):
    user_id: uuid.UUID
    document_url: str
    title: str
    file_type: str
    minio_raw_key: str

    minio_compressed_key: Optional[str] = None
    original_size: Optional[int] = None


