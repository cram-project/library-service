import uuid

from src.library_service.infrastructure.database.session import SessionDep


class LibraryRepository:
    def __init__(self, session: SessionDep):
        self._session = session

    async def get_by_id(self, id: uuid.UUID):
        pass
