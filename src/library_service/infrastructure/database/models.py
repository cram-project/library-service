import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from src.library_service.infrastructure.database.base import Base


class Library(Base):
    __tablename__ = "library"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), index=True)
    document_url: Mapped[str] = mapped_column(String(1024))
    embedding: Mapped[Optional[list[float]]] = mapped_column(JSONB, nullable=True)
    title: Mapped[str] = mapped_column(String(500))
    file_type: Mapped[str] = mapped_column(String(20))
    minio_raw_key: Mapped[str] = mapped_column(String(512), unique=True)
    minio_compressed_key: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    original_size: Mapped[int] = mapped_column(Integer)
