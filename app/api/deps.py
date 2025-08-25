from fastapi import Header
from typing import Optional
from app.core.config import settings


async def api_key_auth(x_api_key: Optional[str] = Header(default=None)):
    if settings.API_KEY and x_api_key != settings.API_KEY:
        raise PermissionError("Invalid API key")