import logging
import uvicorn

from fastapi import FastAPI, status
from fastapi.responses import Response, JSONResponse

from .routers import chat, admin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(admin.router)
app.include_router(chat.router)


@app.get("/healthcheck")
async def healthcheck():
    logger.info("ENDPOINT: /healthcheck")
    return JSONResponse({"status": "UP"}, status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
