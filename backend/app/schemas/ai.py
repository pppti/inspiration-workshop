from pydantic import BaseModel


class ChatRequest(BaseModel):
    conversation_id: int | None = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    reply: str


class AiSearchRequest(BaseModel):
    query: str


class AiSearchResponse(BaseModel):
    results: list[dict]
    summary: str


class AiInspireRequest(BaseModel):
    direction: str


class AiInspireResponse(BaseModel):
    suggestions: str


class AiSummarizeRequest(BaseModel):
    note_ids: list[int]


class AiSummarizeResponse(BaseModel):
    summary: str


class ImportRequest(BaseModel):
    text: str


class ImportResponse(BaseModel):
    title: str
    body: str
    category: str | None = None
    tags: list[str] = []


class AiMessageResponse(BaseModel):
    id: int; role: str; content: str; created_at: str


class AiConversationResponse(BaseModel):
    id: int; title: str; created_at: str
    messages: list[AiMessageResponse] = []


class AiConversationListResponse(BaseModel):
    items: list[AiConversationResponse]
