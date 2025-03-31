import logging
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from .payloads import ChatRequest, ChatResponseAgent
from ..chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("/")
def chat_endpoint(request: ChatRequest):
    logger.info(f"ENDPOINT: /chat/: {request.prompt}")
    return StreamingResponse(
        ChatService.get_response(request.prompt), media_type="text/event-stream"
    )


@router.get("/agent/deprecated")
def chat_agent_endpoint_deprecated(request: ChatRequest):
    logger.info(f"ENDPOINT: /chat/agent/deprecated: {request.prompt}")
    response = ChatService.get_response_from_agent_deprecated(request.prompt)
    return ChatResponseAgent(response=response)


@router.get("/agent")
async def chat_agent_endpoint(request: ChatRequest):
    logger.info(
        f"ENDPOINT: /chat/agent: prompt:{request.prompt} language:{request.language}"
    )
    response = await ChatService.get_response_from_agent(
        request.prompt, request.language
    )
    return ChatResponseAgent(response=response)
