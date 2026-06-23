import os
import uuid

from fastapi import HTTPException, status

from src.library_service.domain.abstractions.library import ILibraryRepository
from src.library_service.domain.abstractions.messaging import IMessagePublisher
from src.library_service.domain.abstractions.minio import IDocumentStorage
from src.library_service.domain.entities.library import (
    ALLOWED_EXTENSIONS,
    LibraryCreateSchema,
    LibraryResponseSchema,
    build_minio_key,
)


class LibraryService:
    def __init__(
        self,
        repo: ILibraryRepository,
        storage: IDocumentStorage,
        events: IMessagePublisher,
    ):
        self._repo = repo
        self._storage = storage
        self._events = events

    async def upload_document(
        self,
        user_id: uuid.UUID,
        file_obj,
        document_url: str,
        title: str,
        content_type: str | None = None,
        original_size: int | None = None,
    ) -> LibraryResponseSchema:
        item_id = uuid.uuid4()
        ext = self._resolve_extension(document_url, content_type)
        key = build_minio_key(user_id, item_id, ext)

        await self._storage.upload_document(file_obj, key, content_type=content_type)

        saved = await self._repo.save(
            LibraryCreateSchema(
                id=item_id,
                user_id=user_id,
                title=title,
                document_url=document_url,
                file_type=ext,
                original_size=original_size,
            )
        )

        await self._events.publish(f"document.uploaded:{item_id}")

        return saved

    async def get_document(self, document_id: uuid.UUID, user_id: uuid.UUID) -> LibraryResponseSchema:
        row = await self._repo.get_by_id(document_id)
        if row is None or row.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        return row

    async def list_documents(self, user_id: uuid.UUID) -> list[LibraryResponseSchema]:
        return await self._repo.list_by_user(user_id)

    async def get_document_bytes(
        self,
        document_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> tuple[bytes, str]:
        document = await self.get_document(document_id, user_id)
        return await self._storage.get_bytes(document.minio_raw_key)

    async def delete_document(self, document_id: uuid.UUID, user_id: uuid.UUID) -> None:
        document = await self.get_document(document_id, user_id)
        await self._storage.delete_object(document.minio_raw_key)
        deleted = await self._repo.delete(document_id, user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    @staticmethod
    def _resolve_extension(filename: str, content_type: str | None) -> str:
        ext = os.path.splitext(filename or "")[1].lstrip(".").lower()
        if ext in ALLOWED_EXTENSIONS:
            return ext

        mime_map = {
            "application/pdf": "pdf",
            "application/msword": "doc",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
            "text/plain": "txt",
            "application/rtf": "rtf",
        }
        if content_type and content_type in mime_map:
            return mime_map[content_type]

        return "pdf"
