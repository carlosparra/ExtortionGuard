from pydantic import BaseModel


class URLCheckIn(BaseModel):
    url: str


class URLCheckOut(BaseModel):
    unsafe: bool
    reason: str | None = None