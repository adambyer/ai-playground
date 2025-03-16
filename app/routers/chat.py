import logging
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from .payloads import ChatRequest
from ..chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("/")
async def prompt_endpoint(request: ChatRequest):
    logger.info(f"ENDPOINT: /chat/: {request.prompt}")
    return StreamingResponse(
        ChatService.get_response(request.prompt), media_type="text/event-stream"
    )
