from typing import Protocol, runtime_checkable


@runtime_checkable
class IDocumentStorage(Protocol):
    async def upload_document(
        self,
        file_obj,
        key: str,
        *,
        content_type: str | None = None,
    ):
        pass

    async def get_bytes(self, key: str) -> tuple[bytes, str]:
        pass

    async def delete_object(self, key: str):
        pass
