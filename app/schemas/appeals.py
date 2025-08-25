from pydantic import BaseModel, Field


class AppealIn(BaseModel):
    phone: str
    country: str = "MX"
    message: str = Field(..., max_length=2000)
    claimant_token: str = Field(..., min_length=6, max_length=64)


class AppealOut(BaseModel):
    appeal_id: int
    status: str