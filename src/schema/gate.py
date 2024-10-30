from pydantic import BaseModel

class Gate(BaseModel):
    name: str
    road_name: str
    direction: str
    type: str
    next_express_lane: str
    gate_coords: tuple[tuple[float, float], tuple[float, float]]
