from pydantic import BaseModel


class Checkpoint(BaseModel):
    """A checkpoint crossed on the road."""

    session_id: str
    fingerprint: str
    coordinate: list[float]
