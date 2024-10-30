from pydantic import BaseModel

class Coords(BaseModel):
    speed: float
    accuracy: float
    altitudeAccuracy: float
    altitude: float
    longitude: float
    latitude: float
    heading: float

class Position(BaseModel):
    coords: Coords
    timestamp: int

class Events(BaseModel):
    event_num: int
    gate_name: str
    timestamp: int

class TripData(BaseModel):
    device_id: str
    device_info: str
    session_id: str
    start_time: int
    end_time: int
    positions: list[Position]
    events: list[Events]
