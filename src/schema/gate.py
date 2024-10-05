from pydantic import BaseModel


class Gate(BaseModel):
    """A gate crossed on the road."""

    name: str
    session_id: str
    fingerprint: str
