import io
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Response, UploadFile

from src.library_service.domain.entities.library import LibraryResponseSchema
from src.library_service.domain.entities.users import UserPayload
from src.library_service.domain.services.library import LibraryService
from src.library_service.infrastructure.security.deps import get_current_user
from src.library_service.presentation.deps import get_library_service

api_v1_router = APIRouter()

LibraryServiceDep = Annotated[LibraryService, Depends(get_library_service)]


@api_v1_router.post("/upload", response_model=LibraryResponseSchema, status_code=201)
async def upload_document(
        service: LibraryServiceDep,
        user: UserPayload = Depends(get_current_user),
        file: UploadFile = File(...),
        title: str = Form(...),
):
    content = await file.read()
    file_obj = io.BytesIO(content)
    return await service.upload_document(
        user_id=user.user_id,
        file_obj=file_obj,
        document_url=file.filename or "",
        title=title,
        content_type=file.content_type,
        original_size=len(content),
    )


@api_v1_router.get("/documents", response_model=list[LibraryResponseSchema])
async def list_documents(
        service: LibraryServiceDep,
        user: UserPayload = Depends(get_current_user),
):
    return await service.list_documents(user.user_id)


@api_v1_router.get("/documents/{document_id}", response_model=LibraryResponseSchema)
async def get_document(
        document_id: uuid.UUID,
        service: LibraryServiceDep,
        user: UserPayload = Depends(get_current_user),
):
    return await service.get_document(document_id, user.user_id)


@api_v1_router.get("/documents/{document_id}/object")
async def get_document_object(
        document_id: uuid.UUID,
        service: LibraryServiceDep,
        user: UserPayload = Depends(get_current_user),
):
    data, content_type = await service.get_document_bytes(document_id, user.user_id)
    return Response(content=data, media_type=content_type)


@api_v1_router.delete("/documents/{document_id}", status_code=204)
async def delete_document(
        document_id: uuid.UUID,
        service: LibraryServiceDep,
        user: UserPayload = Depends(get_current_user),
):
    await service.delete_document(document_id, user.user_id)
    return Response(status_code=204)
