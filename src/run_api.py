"""API entry point. Run this to start the API."""

import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_204_NO_CONTENT

# from common.logger import logger

load_dotenv()

from src.api import router as api_router
from src.api import root  # unused, but needed to load endpoints

logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("starlette").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

DEBUG = os.environ.get("DEBUG")
app = FastAPI()

# Allow CORS requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods="POST",  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(api_router, prefix="/api", tags=["api"])

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("ERROR", exc)
    try:
        body = await request.body()
    except RuntimeError:
        if str(exc) == "Stream consumed" and await request.is_disconnected():
            return Response(status_code=HTTP_204_NO_CONTENT)
        raise
    logger.error(f"Validation error: {exc.errors()}")
    logger.error(f"Request body: {body.decode()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc.errors()), "body": body.decode()},
    )
