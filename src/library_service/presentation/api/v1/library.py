from fastapi import APIRouter, Depends

from src.library_service.domain.entities.library import LibraryResponseSchema
from src.library_service.domain.entities.users import UserPayload
from src.library_service.infrastructure.security.deps import get_current_user

api_v1_router = APIRouter()


@api_v1_router.post('/upload', response_model=LibraryResponseSchema)
async def upload_document(
        service: ...,
        user: UserPayload = Depends(get_current_user),
):
    ...