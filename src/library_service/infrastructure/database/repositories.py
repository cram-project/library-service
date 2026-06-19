import uuid

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from src.library_service.domain.entities.library import LibraryCreateSchema, LibraryResponseSchema
from src.library_service.infrastructure.database.models import Library
from src.library_service.infrastructure.database.session import SessionDep


class LibraryRepository:
    def __init__(self, session: SessionDep):
        self._session = session

    async def save(self, obj: LibraryCreateSchema):
        row = Library(
            user_id=obj.user_id,
            title=obj.title,
            document_url=obj.document_url,
            file_type=obj.file_type,
        )
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)

        return HTTPException(status_code=201, detail="Document saved")

    async def get_by_id(self, obj_id: uuid.UUID):
        query = select(Library).where(Library.id == obj_id)
        result = await self._session.execute(query)

        row = result.scalars().one_or_none()

        return row if row is not None else None

    async def delete(self, obj_id: uuid.UUID, user_id: uuid.UUID):
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

    async def list_by_user(self, user_id: uuid.UUID):
        query = select(Library).where(Library.user_id == user_id)

        result = await self._session.execute(query)

        return result.scalars().all()
