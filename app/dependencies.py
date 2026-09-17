from typing import Annotated

from fastapi import Header, Request

from app.repository import NotesRepository
from app.services import NotesService


def get_author_id(
    x_author_id: Annotated[str, Header(alias="X-Author-Id")],
) -> str:
    # A real app would validate a bearer token and read the subject from it.
    return x_author_id


def get_notes_service(request: Request) -> NotesService:
    repository: NotesRepository = request.app.state.repository
    return NotesService(repository)

