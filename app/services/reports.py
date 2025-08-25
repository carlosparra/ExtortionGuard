from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.models import Number, Report
from app.schemas.reports import ReportIn, ReportOut
from app.utils.phone import normalize_phone
from app.core.security import phone_hash
from app.core.config import settings
from datetime import datetime, timezone


def create_report(db: Session, payload: ReportIn) -> ReportOut:
    e164, last4 = normalize_phone(payload.phone, payload.country)
    phash = phone_hash(e164)


    number = db.scalar(select(Number).where(Number.phone_hash == phash))
    if not number:
        number = Number(phone_hash=phash, country=payload.country, last4=last4)
    db.add(number)
    db.flush()


    # Anti-abuso por día (por simplicidad, por número)
    today = datetime.now(timezone.utc).date()
    start = datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc)
    end = datetime.combine(today, datetime.max.time(), tzinfo=timezone.utc)
    q_num_day = select(func.count()).select_from(Report).where(
    Report.number_id == number.id,
    Report.created_at >= start,
    Report.created_at <= end,
    )
    if db.scalar(q_num_day) >= 200:
        raise ValueError("Daily report limit for this number reached")


    rep = Report(
        number_id=number.id,
        channel=payload.channel,
        reason=payload.reason,
        details=(payload.details or "").strip(),
        evidence_url=payload.evidence_url,
        reporter_id=payload.reporter_id,
    )
    db.add(rep)
    db.commit()


    return ReportOut(report_id=rep.id, number_id=number.id, created_at=rep.created_at.isoformat())