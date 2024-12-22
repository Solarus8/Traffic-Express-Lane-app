from pydantic import BaseModel

class Gate(BaseModel):
    name: str
    spoken_name: str
    road_name: str
    travel_direction: str
    type: str
    next_express_lane: str
    gate_coords: tuple[object, object]
