from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str


class AddDocumentRequest(BaseModel):
    content: str
