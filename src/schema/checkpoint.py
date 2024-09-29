from pydantic import BaseModel


class Checkpoint(BaseModel):
    """A checkpoint crossed on the road."""

    name: str
    session_id: str
    fingerprint: str
