from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str
    language: str = "english"


class ChatResponse(BaseModel):
    response: str


class AddDocumentRequest(BaseModel):
    content: str
