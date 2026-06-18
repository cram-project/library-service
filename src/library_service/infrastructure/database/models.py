import uuid
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from src.library_service.infrastructure.database.base import Base


class Library(Base):
    __tablename__ = "library"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), index=True)
    document_url: Mapped[str] = mapped_column(String(1024))
    # embedding: Mapped[Optional[list[float]]] = mapped_column(JSONB, nullable=True)
