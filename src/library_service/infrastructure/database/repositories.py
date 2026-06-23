import uuid

from sqlalchemy import delete, select

from src.library_service.domain.entities.library import (
    LibraryCreateSchema,
    LibraryResponseSchema,
    build_minio_key,
)
from src.library_service.infrastructure.database.models import Library
from src.library_service.infrastructure.database.session import SessionDep


def _to_response(row: Library) -> LibraryResponseSchema:
    return LibraryResponseSchema(
        id=row.id,
        user_id=row.user_id,
        document_url=row.document_url,
        title=row.title,
        file_type=row.file_type,
        minio_raw_key=build_minio_key(row.user_id, row.id, row.file_type),
        minio_compressed_key=row.minio_compressed_key,
        original_size=row.original_size,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class LibraryRepository:
    def __init__(self, session: SessionDep):
        self._session = session

    async def save(self, obj: LibraryCreateSchema) -> LibraryResponseSchema:
        row = Library(
            id=obj.id,
            user_id=obj.user_id,
            title=obj.title,
            document_url=obj.document_url,
            file_type=obj.file_type,
            minio_compressed_key=obj.minio_compressed_key,
            original_size=obj.original_size,
        )
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return _to_response(row)

    async def get_by_id(self, obj_id: uuid.UUID) -> LibraryResponseSchema | None:
        query = select(Library).where(Library.id == obj_id)
        result = await self._session.execute(query)
        row = result.scalars().one_or_none()
        return _to_response(row) if row is not None else None

    async def delete(self, obj_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        query = delete(Library).where(
            Library.id == obj_id,
            Library.user_id == user_id,
        )
        try:
            result = await self._session.execute(query)
            await self._session.commit()
            return result.rowcount > 0
        except Exception:
            await self._session.rollback()
            raise

    async def list_by_user(self, user_id: uuid.UUID) -> list[LibraryResponseSchema]:
        query = select(Library).where(Library.user_id == user_id)
        result = await self._session.execute(query)
        return [_to_response(row) for row in result.scalars().all()]
