from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.risk import RiskOut
from app.services.risk import lookup_risk


router = APIRouter()


@router.get("/lookup", response_model=RiskOut)
def risk_lookup(phone: str = Query(...), country: str = Query("MX"), db: Session = Depends(get_db)):
    return lookup_risk(db, phone, country)