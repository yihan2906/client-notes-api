from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.repository import InMemoryNotesRepository, NotesRepository
from app.routers.clients import router as clients_router
from app.routers.demo import router as demo_router
from app.routers.notes import router as notes_router


def create_app(repository: NotesRepository | None = None) -> FastAPI:
    application = FastAPI(title="Client Notes API", version="1.0.0")
    application.state.repository = repository or InMemoryNotesRepository()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "X-Author-Id"],
    )
    application.include_router(demo_router)
    application.include_router(clients_router)
    application.include_router(notes_router)

    @application.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()
