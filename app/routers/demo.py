from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_notes_service
from app.models import Author
from app.services import NotesService

router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/authors", response_model=list[Author])
def list_demo_authors(
    service: Annotated[NotesService, Depends(get_notes_service)],
) -> list[Author]:
    """Expose fake identities for the demo UI; remove when real auth is added."""
    return service.list_demo_authors()
