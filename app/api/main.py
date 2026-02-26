from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.core.logging import configure_logging
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.api.routes import api_router

configure_logging()
app = FastAPI(title=settings.APP_NAME, version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security and traceability middlewares
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Main routes under /api
app.include_router(api_router, prefix=settings.API_PREFIX)

# --- Useful extras ---

# Redirect from / to documentation (Swagger UI)
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# Simple global healthcheck
@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
