import hashlib, hmac
from app.core.config import settings


def phone_hash(e164: str) -> str:
    return hmac.new(settings.PEPPER.encode(), e164.encode(), hashlib.sha256).hexdigest()