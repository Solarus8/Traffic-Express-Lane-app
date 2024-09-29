from pydantic import BaseModel


class ExpressLane(BaseModel):
    name: str
    entered_at: list[float]
    recommendation: bool
    used: bool


class Events(BaseModel):
    entered_freeway: list[float]
    express_lanes: list[ExpressLane]
    exited_freeway: list[float]


class TripData(BaseModel):
    """Data received from a completed trip"""

    session_id: str
    fingerprint: str
    events: Events
    positions: list[list[float]]
