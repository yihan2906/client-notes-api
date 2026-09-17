from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_author_id, get_notes_service
from app.models import Client
from app.services import NotesService

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=list[Client])
def list_assigned_clients(
    author_id: Annotated[str, Depends(get_author_id)],
    service: Annotated[NotesService, Depends(get_notes_service)],
) -> list[Client]:
    return service.list_assigned_clients(author_id)
