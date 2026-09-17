from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status

from app.models import Note, NoteCreate
from app.repository import NotesRepository


class NotesService:
    def __init__(self, repository: NotesRepository) -> None:
        self.repository = repository

    def list_notes(self, client_id: str, author_id: str) -> list[Note]:
        self._authorize(client_id, author_id)
        return self.repository.list_notes(client_id)

    def add_note(
        self, client_id: str, author_id: str, payload: NoteCreate
    ) -> Note:
        self._authorize(client_id, author_id)
        note = Note(
            id=str(uuid4()),
            client_id=client_id,
            author_id=author_id,
            content=payload.content,
            created_at=datetime.now(timezone.utc),
        )
        return self.repository.add_note(note)

    def _authorize(self, client_id: str, author_id: str) -> None:
        if not self.repository.client_exists(client_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        if not self.repository.is_assigned(author_id, client_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not assigned to this client",
            )

