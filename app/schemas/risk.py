from pydantic import BaseModel, Field
from typing import Optional


class RiskOut(BaseModel):
    risk_score: float = Field(..., ge=0.0, le=1.0)
    label: str
    reports_last_365d: int
    last_report_at: Optional[str]
    breakdown: dict