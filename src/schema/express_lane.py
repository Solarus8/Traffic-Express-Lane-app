from pydantic import BaseModel

class ExpressLane(BaseModel):
    lane_name: str
    road_name: str
    direction: str
    lines_start: tuple[float, float]
    lines_end: tuple[float, float]
    effective_start: tuple[float, float]
    effective_end: tuple[float, float]
    lines_length: float
    effective_length: float
    hours_tolls: dict[str, float]