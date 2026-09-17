from datetime import datetime, timezone
from typing import Protocol

from app.models import Client, Note


class NotesRepository(Protocol):
    """Persistence boundary; a database implementation can replace this later."""

    def client_exists(self, client_id: str) -> bool: ...

    def is_assigned(self, author_id: str, client_id: str) -> bool: ...

    def list_notes(self, client_id: str) -> list[Note]: ...

    def add_note(self, note: Note) -> Note: ...


class InMemoryNotesRepository:
    def __init__(self) -> None:
        self.clients: dict[str, Client] = {
            "client-1": Client(id="client-1", name="Acme Health"),
            "client-2": Client(id="client-2", name="Northwind Clinic"),
        }
        self.assignments: set[tuple[str, str]] = {
            ("author-1", "client-1"),
            ("author-2", "client-2"),
        }
        self.notes: list[Note] = [
            Note(
                id="note-1",
                client_id="client-1",
                author_id="author-1",
                content="Initial client call completed.",
                created_at=datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc),
            )
        ]

    def client_exists(self, client_id: str) -> bool:
        return client_id in self.clients

    def is_assigned(self, author_id: str, client_id: str) -> bool:
        return (author_id, client_id) in self.assignments

    def list_notes(self, client_id: str) -> list[Note]:
        return sorted(
            (note for note in self.notes if note.client_id == client_id),
            key=lambda note: note.created_at,
        )

    def add_note(self, note: Note) -> Note:
        self.notes.append(note)
        return note

