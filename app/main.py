import logging
import uvicorn

from fastapi import FastAPI

from .routers import chat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(chat.router)


@app.get("/healthcheck")
async def healthcheck():
    logger.info("ENDPOINT: /healthcheck")
    return {"message": "UP!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
