import io
import uuid

from src.library_service.domain.services.library import LibraryService


class UploadDocumentUseCase:
    def __init__(self, service: LibraryService):
        self._service = service

    async def execute(
        self,
        user_id: uuid.UUID,
        file_content: bytes,
        filename: str,
        title: str,
        content_type: str | None = None,
    ):
        file_obj = io.BytesIO(file_content)
        return await self._service.upload_document(
            user_id=user_id,
            file_obj=file_obj,
            document_url=filename,
            title=title,
            content_type=content_type,
            original_size=len(file_content),
        )
