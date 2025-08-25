from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ReportIn(BaseModel):
    phone: str = Field(...)
    country: str = Field(default="MX", min_length=2, max_length=2)
    channel: str = Field(..., pattern=r"^(call|sms|wa)$")
    reason: str = Field(..., pattern=r"^(threat|spoof|payment|impersonation|other)$")
    details: str = Field("", max_length=2000)
    evidence_url: Optional[str] = Field(default=None, max_length=512)
    reporter_id: Optional[str] = Field(default=None, max_length=64)


    @field_validator("country")
    @classmethod
    def upper_country(cls, v: str) -> str:
        return v.upper()


class ReportOut(BaseModel):
    report_id: int
    number_id: int
    created_at: str