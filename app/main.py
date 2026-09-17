from fastapi import FastAPI

from app.repository import InMemoryNotesRepository, NotesRepository
from app.routers.notes import router as notes_router


def create_app(repository: NotesRepository | None = None) -> FastAPI:
    application = FastAPI(title="Client Notes API", version="1.0.0")
    application.state.repository = repository or InMemoryNotesRepository()
    application.include_router(notes_router)

    @application.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()

