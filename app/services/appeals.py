from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Number, Appeal
from app.schemas.appeals import AppealIn, AppealOut
from app.core.security import phone_hash
from app.utils.phone import normalize_phone
import hashlib
from app.core.config import settings


def create_appeal(db: Session, payload: AppealIn) -> AppealOut:
    e164, last4 = normalize_phone(payload.phone, payload.country)
    phash = phone_hash(e164)
    number = db.scalar(select(Number).where(Number.phone_hash == phash))
    if not number:
        number = Number(phone_hash=phash, country=payload.country, last4=last4)
        db.add(number)
        db.flush()
    token = hashlib.sha256((payload.claimant_token + settings.PEPPER).encode()).hexdigest()
    appeal = Appeal(number_id=number.id, claimant_token=token, message=payload.message)
    db.add(appeal)
    db.commit()
    return AppealOut(appeal_id=appeal.id, status=appeal.status)