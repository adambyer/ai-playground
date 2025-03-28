from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str


class ChatResponseLangChain(BaseModel):
    response: str


class AddDocumentRequest(BaseModel):
    content: str
