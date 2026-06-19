from src.library_service.config import Settings


class DocumentStorage:
    def __init__(self, settings: Settings):
        self._settings = settings

    async def upload_document(
            self,
            file_obj,
            key: str,

    ):
        pass
