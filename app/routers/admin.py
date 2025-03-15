import logging

from fastapi import APIRouter, status
from fastapi.responses import Response, JSONResponse

from app.vector_db import VectorDB

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get("/collection/count/")
async def get_collection_count_endpoint():
    logger.info("ENDPOINT: /collection/count/")
    return JSONResponse(
        content={"count": VectorDB.get_collection_count()},
        status_code=status.HTTP_200_OK,
    )


@router.post("/collection/reset/")
async def reset_collection_endpoint():
    logger.info(f"ENDPOINT: /collection/clear/")
    VectorDB.reset_collection()
    return Response(status_code=status.HTTP_200_OK)
