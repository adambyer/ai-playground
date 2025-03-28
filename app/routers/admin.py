import logging

from fastapi import APIRouter, status, File, UploadFile
from fastapi.responses import Response, JSONResponse

from app.admin_service import AdminService
from app.vector_db import VectorDB
from .payloads import AddDocumentRequest

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get("/collection/count/")
def get_collection_count_endpoint():
    logger.info("ENDPOINT: /collection/count/")
    return JSONResponse(
        content={"count": VectorDB.get_collection_count()},
        status_code=status.HTTP_200_OK,
    )


@router.post("/collection/reset/")
def reset_collection_endpoint():
    logger.info("ENDPOINT: /collection/clear/")
    VectorDB.reset_collection()
    return Response(status_code=status.HTTP_200_OK)


@router.post("/collection/document/add/")
def add_document_endpoint(request: AddDocumentRequest):
    logger.info("ENDPOINT: /collection/document/add/")
    AdminService.add_document(request.content)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/collection/document/upload")
async def upload_document_endpoint(file: UploadFile = File(...)):
    logger.info(f"ENDPOINT: /document/: {file.filename}")

    content = await file.read()
    await AdminService.add_document_from_bytes(content, file.filename)
    return Response(status_code=status.HTTP_201_CREATED)
