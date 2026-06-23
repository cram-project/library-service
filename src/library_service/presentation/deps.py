from typing import Annotated

from fastapi import Depends

from src.library_service.config import settings
from src.library_service.domain.services.library import LibraryService
from src.library_service.infrastructure.database.repositories import LibraryRepository
from src.library_service.infrastructure.database.session import SessionDep
from src.library_service.infrastructure.messaging.noop_publisher import NoopMessagePublisher
from src.library_service.infrastructure.storage.document_storage import DocumentStorage


def get_document_storage() -> DocumentStorage:
    return DocumentStorage(settings)


def get_message_publisher() -> NoopMessagePublisher:
    return NoopMessagePublisher()


def get_library_repository(session: SessionDep) -> LibraryRepository:
    return LibraryRepository(session)


def get_library_service(
    repo: Annotated[LibraryRepository, Depends(get_library_repository)],
    storage: Annotated[DocumentStorage, Depends(get_document_storage)],
    events: Annotated[NoopMessagePublisher, Depends(get_message_publisher)],
) -> LibraryService:
    return LibraryService(repo, storage, events)
