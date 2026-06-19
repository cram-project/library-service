from src.library_service.domain.abstractions.library import ILibraryRepository
from src.library_service.domain.abstractions.messaging import IMessagePublisher
from src.library_service.domain.abstractions.minio import IDocumentStorage


class LibraryService:
    def __init__(
            self,
            repo: ILibraryRepository,
            storage: IDocumentStorage,
            events: IMessagePublisher
    ):
        self._repo = repo
        self._storage = storage
        self._events = events

    async def execute(
            self,

    ):
