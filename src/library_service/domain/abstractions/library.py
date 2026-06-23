import uuid
from typing import Protocol, runtime_checkable

from src.library_service.domain.entities.library import (
    LibraryCreateSchema,
    LibraryResponseSchema,
)


@runtime_checkable
class ILibraryRepository(Protocol):
    async def save(self, obj: LibraryCreateSchema) -> LibraryResponseSchema:
        pass

    async def get_by_id(self, obj_id: uuid.UUID):
        pass

    async def delete(self, obj_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        pass

    async def list_by_user(self, user_id: uuid.UUID) -> list[LibraryResponseSchema]:
        pass
