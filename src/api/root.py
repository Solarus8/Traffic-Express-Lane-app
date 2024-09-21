import json
import os
from datetime import datetime

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
async def ws_recommend(websocket: WebSocket):
    last_recommendation = None
    try:
        while True:
            coordinates = await websocket.receive_text()
            logger.debug(f"Received coordinates: `{coordinates}`")
            coordinates = Coordinate.from_str(coordinates)
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
        logger.debug("Client disconnected from websocket `recommend` as expected.")
    except Exception as e:
        logger.error(
            f"Client disconnected from 24hr_price_ticker with error: {e.__class__.__name__}: {e}"
        )
