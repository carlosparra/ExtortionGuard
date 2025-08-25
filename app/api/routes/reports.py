from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.reports import ReportIn, ReportOut
from app.services.reports import create_report


router = APIRouter()


@router.post("", response_model=ReportOut)
def submit_report(payload: ReportIn, db: Session = Depends(get_db)):
    try:
        return create_report(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))