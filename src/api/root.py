import json
import os
from datetime import datetime, timezone, timedelta

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from api import router
from common.custom_types import Coordinate
from common.logger import logger
from common.traffic_recommendation import recommend


@router.get("/")
async def home():
    current_time = datetime.now().strftime("%H:%M:%S")
    mod_time_seconds = os.path.getmtime("..")
    mod_time = datetime.fromtimestamp(mod_time_seconds)
    mod_time_readable = mod_time.strftime("%Y-%m-%d %H:%M:%S")
    return f"Hello, the current time is {current_time}. Last update was {mod_time_readable}."


@router.websocket("/recommend")
async def ws_recommend(websocket: WebSocket, user_id: str = None):
    await websocket.accept()
    last_recommendation = None
    try:
        while True:
            data = await websocket.receive_json()
            client_datetime = datetime.fromtimestamp(data["timestamp"], timezone.utc)
            server_datetime = datetime.now(timezone.utc)
            time_diff = server_datetime - client_datetime
            if time_diff > timedelta(milliseconds=200):
                logger.warning(
                    f"Client {user_id}'s timestamp is {time_diff.total_seconds()} seconds before server's"
                )
            coordinates = Coordinate.from_str(data["coordinates"])
            logger.debug(f"Received coordinates: `{coordinates}`")
            lane = recommend(coordinates)
            if lane is not last_recommendation:
                last_recommendation = lane
                logger.debug("Lane recommended:", lane)
                if lane:
                    text = json.dumps(lane.as_json())
                else:
                    text = "None"
                await websocket.send_text(text)

    except WebSocketDisconnect:
        logger.debug("Client disconnected from ws_recommend as expected.")
    except Exception as e:
        logger.error(
            f"Client disconnected from ws_recommend with error: {e.__class__.__name__}: {e}"
        )
