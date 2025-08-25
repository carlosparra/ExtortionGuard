from fastapi import APIRouter
from . import reports, risk, appeals, urlcheck, health

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(risk.router, prefix="/risk", tags=["risk"])
api_router.include_router(appeals.router, prefix="/appeals", tags=["appeals"])
api_router.include_router(urlcheck.router, prefix="/url", tags=["url"])