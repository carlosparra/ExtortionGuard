from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.appeals import AppealIn, AppealOut
from app.services.appeals import create_appeal


router = APIRouter()


@router.post("", response_model=AppealOut)
def appeal(payload: AppealIn, db: Session = Depends(get_db)):
    return create_appeal(db, payload)