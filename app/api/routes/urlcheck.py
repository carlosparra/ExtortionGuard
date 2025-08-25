from fastapi import APIRouter
from app.schemas.urlcheck import URLCheckIn, URLCheckOut
from app.services.urlrisk import check_url, check_url_v2


router = APIRouter()


@router.post("/check", response_model=URLCheckOut)
def url_check(payload: URLCheckIn):
    return check_url(payload.url)


@router.post("/check/v2", response_model=URLCheckOut)
def url_check_v2(payload: URLCheckIn):
    return check_url_v2(payload.url)