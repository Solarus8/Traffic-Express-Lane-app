import os
from datetime import datetime

from fastapi import WebSocket
from starlette.requests import Request
from starlette.websockets import WebSocketDisconnect

from api import router
from common.communication_manager import CommunicationManager
from common.logger import logger
from schema.trip_data import TripData


@router.get("/")
async def home():
    current_time = datetime.now().strftime("%H:%M:%S")
    mod_time_seconds = os.path.getmtime("..")
    mod_time = datetime.fromtimestamp(mod_time_seconds)
    mod_time_readable = mod_time.strftime("%Y-%m-%d %H:%M:%S")
    return f"Hello, the current time is {current_time}. Last update was {mod_time_readable}."


@router.post("/trip")
async def trip_data(request: Request, data: TripData):
    path = f"trip_data/{data.fingerprint}"
    if not os.path.exists(path):
        os.makedirs(path)

    with open(f"{path}/{data.session_id}.json", "w") as f:
        text = data.model_dump_json(indent=2)
        f.write(text)


@router.websocket("/ws")
async def ws(websocket: WebSocket, user_id: str = None):
    """Main websocket for communication between server and client."""
    await websocket.accept()
    manager = CommunicationManager(websocket, user_id)
    try:
        while True:
            await manager.update()

    except WebSocketDisconnect:
        logger.debug("Client disconnected from ws_recommend as expected.")
    except Exception as e:
        logger.error(
            f"Client disconnected from ws_recommend with error: {e.__class__.__name__}: {e}"
        )
