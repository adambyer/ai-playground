import logging
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from .payloads import ChatRequest, ChatResponse
from ..chat_handler import ChatHandler

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("/model")
def chat_model_endpoint(request: ChatRequest):
    logger.info(f"ENDPOINT: /chat/model/: {request.prompt}")
    return StreamingResponse(
        ChatHandler.get_response_from_model(request.prompt),
        media_type="text/event-stream",
    )


@router.get("/agent/deprecated")
def chat_agent_endpoint_deprecated(request: ChatRequest):
    logger.info(f"ENDPOINT: /chat/agent/deprecated: {request.prompt}")
    response = ChatHandler.get_response_from_agent_deprecated(request.prompt)
    return ChatResponse(response=response)


@router.get("/")
async def chat_service_endpoint(request: ChatRequest):
    logger.info(
        f"ENDPOINT: /chat/: prompt:{request.prompt} language:{request.language}"
    )
    response = await ChatHandler.get_response_from_service(
        request.prompt, request.language
    )
    return ChatResponse(response=response)


@router.get("/agent")
async def chat_agent_service_endpoint(request: ChatRequest):
    logger.info(f"ENDPOINT: /chat/agent/: prompt:{request.prompt}")
    response = await ChatHandler.get_response_from_agent_service(request.prompt)
    return ChatResponse(response=response)
