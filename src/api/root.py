import os
from datetime import datetime
import json

#for websockets#    from fastapi import WebSocket
from starlette.requests import Request
#for websockets#    from starlette.websockets import WebSocketDisconnect

from src.api import router
#for websockets#    from common.communication_manager import CommunicationManager
#used in websockets only#   from common.logger import logger
""" from common.traffic_recommendation import recommend """
from src.schema.trip_data import TripData
from src.schema.gate import Gate
from src.common.custom_types import Coordinate
from src.data_collection.traffic_data import get_duration_in_traffic

with open("../Object-models/All_US36_express_lanes.json", "r") as f:
    express_lanes = json.load(f)


@router.post("/durations")
async def durations(request: Request, gate: Gate):
    express_lane_name = gate.name.split('_')[-1]
    express_lane_road = gate.road_name
    express_lane_direction = gate.travel_direction
    print(express_lane_name, express_lane_road, express_lane_direction)
    for lane in express_lanes:
        #TODO: Add effective_start and effective_end for querying
        start_coordinate = Coordinate(**lane["lines_start"])
        end_coordinate = Coordinate(**lane["lines_end"])
        if all([
            lane["lane_name"] == express_lane_name,
            lane["road_name"] == express_lane_road,
            lane["direction"] == express_lane_direction
        ]):
            print("calling api", lane)
            duration, duration_in_traffic = get_duration_in_traffic(start_coordinate, end_coordinate)
            print(duration, duration_in_traffic)
            return {"duration": duration, "duration_in_traffic": duration_in_traffic}
        
    return {"error": "No lane found"}


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




### Higher level idea, not currently used or implemented - may be deleted later
@router.get("/recommend")
async def recommend_express_lane(request: Request, gate: Gate):
    do_recommend, estimated_time_saving, lane, comment = recommend(gate.name)
    data = lane.as_json()
    data["estimated_time_saving"] = estimated_time_saving
    data["comment"] = comment
    return data

### This is the deprecated websocket endpoint
'''
@router.websocket("/ws")
async def ws(websocket: WebSocket, user_id: str = None):
    """Main websocket for communication between server and client."""
    raise DeprecationWarning(
        "This websocket is deprecated and will be removed in a future release."
    )
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
'''