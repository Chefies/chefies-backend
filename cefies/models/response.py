from pydantic import BaseModel


class MessageResponse(BaseModel):
    error: bool
    message: str
