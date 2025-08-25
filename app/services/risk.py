from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.models import Number, Report
from app.core.security import phone_hash
from app.utils.phone import normalize_phone
from app.services.scoring import time_now, decay_weight, compute_score
from app.schemas.risk import RiskOut


def lookup_risk(db: Session, phone: str, country: str) -> RiskOut:
    e164, _ = normalize_phone(phone, country)
    phash = phone_hash(e164)
    number = db.scalar(select(Number).where(Number.phone_hash == phash))
    if not number:
        return RiskOut(risk_score=0.05, label="minimal", reports_last_365d=0, last_report_at=None, breakdown={"reason": {}})


    one_year_ago = time_now() - timedelta(days=365)
    rows = db.execute(
    select(Report.reason, Report.created_at)
    .where(Report.number_id == number.id, Report.created_at >= one_year_ago)
    .order_by(Report.created_at.desc())
    ).all()


    decayed_sum = 0.0
    breakdown: dict[str, float] = {}
    last_at = None
    now = time_now()
    for reason, created_at in rows:
        age_days = (now - created_at).total_seconds() / 86400.0
        w = decay_weight(age_days)
        decayed_sum += w
        breakdown[reason] = breakdown.get(reason, 0.0) + w
        if last_at is None or created_at > last_at:
            last_at = created_at


    score, label = compute_score(decayed_sum, total_reports=len(rows))
    total_w = sum(breakdown.values()) or 1.0
    bd_norm = {k: round(v / total_w, 4) for k, v in breakdown.items()}


    return RiskOut(
    risk_score=round(score, 4),
    label=label,
    reports_last_365d=len(rows),
    last_report_at=last_at.isoformat() if last_at else None,
    breakdown={"reason": bd_norm},
    )