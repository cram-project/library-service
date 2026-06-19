import uuid
from typing import Protocol, runtime_checkable


@runtime_checkable
class ILibraryRepository(Protocol):
    async def get_by_id(self, obj_id: uuid.UUID):
        pass

    async def add(self, obj):
        pass

    async def remove(self, obj_id: uuid.UUID):
        pass