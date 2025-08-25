from datetime import datetime, timezone, timedelta
from app.core.config import settings


def time_now() -> datetime:
    return datetime.now(timezone.utc)


def decay_weight(age_days: float) -> float:
    return 0.5 ** (age_days / settings.HALF_LIFE_DAYS)


def compute_score(decayed_sum: float, total_reports: int) -> tuple[float, str]:
    a, b = settings.BETA_PRIOR_A, settings.BETA_PRIOR_B
    posterior = (a + decayed_sum) / (a + b + decayed_sum)
    if total_reports >= settings.MIN_REPORTS_FOR_HIGH and posterior >= 0.8:
        label = "high"
    elif posterior >= 0.5:
        label = "medium"
    elif posterior >= 0.2:
        label = "low"
    else:
        label = "minimal"
    posterior = max(0.0, min(1.0, posterior))
    return posterior, label