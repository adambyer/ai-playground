import logging
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from .payloads import ChatRequest, ChatResponseLangChain
from ..chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("/")
def prompt_endpoint(request: ChatRequest):
    logger.info(f"ENDPOINT: /chat/: {request.prompt}")
    return StreamingResponse(
        ChatService.get_response(request.prompt), media_type="text/event-stream"
    )


@router.get("/langchain")
def prompt_emdpoint_langchain(request: ChatRequest):
    logger.info(f"ENDPOINT: /chat/langchain: {request.prompt}")
    response = ChatService.get_response_langchain(request.prompt)
    return ChatResponseLangChain(response=response)
