from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Client(BaseModel):
    id: str
    name: str


class Author(BaseModel):
    id: str
    name: str


class Note(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    client_id: str
    author_id: str
    content: str
    created_at: datetime


class NoteCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2_000)
