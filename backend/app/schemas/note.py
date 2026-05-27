from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str | None = None
    body: str
    category: str | None = None
    source: str | None = None
    tags: list[str] = []


class NoteUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    category: str | None = None
    source: str | None = None
    tags: list[str] | None = None


class NoteResponse(BaseModel):
    id: int
    title: str | None = None
    body: str
    category: str | None = None
    source: str | None = None
    tags: list[str] = []
    created_at: str
    updated_at: str


class NoteListResponse(BaseModel):
    items: list[NoteResponse]
    total: int
    page: int
    limit: int
