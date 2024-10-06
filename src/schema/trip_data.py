from pydantic import BaseModel


class Coords(BaseModel):
    altitude: float
    altitudeAccuracy: float
    longitude: float
    latitude: float
    speed: float
    accuracy: float
    heading: float


class Position(BaseModel):
    coords: Coords
    timestamp: int


class Events(BaseModel):
    event_num: int
    gate_name: str
    timestamp: int


class TripData(BaseModel):
    """Data received from a completed trip"""

    session_id: str
    fingerprint: str
    start_time: int
    end_time: int
    events: list[Events]
    positions: list[Position]
