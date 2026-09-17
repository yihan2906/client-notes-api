from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import get_author_id, get_notes_service
from app.models import Note, NoteCreate
from app.services import NotesService

router = APIRouter(prefix="/clients/{client_id}/notes", tags=["notes"])


@router.get("", response_model=list[Note])
def list_notes(
    client_id: str,
    author_id: Annotated[str, Depends(get_author_id)],
    service: Annotated[NotesService, Depends(get_notes_service)],
) -> list[Note]:
    return service.list_notes(client_id, author_id)


@router.post("", response_model=Note, status_code=status.HTTP_201_CREATED)
def add_note(
    client_id: str,
    payload: NoteCreate,
    author_id: Annotated[str, Depends(get_author_id)],
    service: Annotated[NotesService, Depends(get_notes_service)],
) -> Note:
    return service.add_note(client_id, author_id, payload)

