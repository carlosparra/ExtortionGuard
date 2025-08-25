# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request
# class SecurityHeadersMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         response = await call_next(request)
#         response.headers.update({
#             "X-Content-Type-Options": "nosniff",
#             "X-Frame-Options": "DENY",
#             "Referrer-Policy": "no-referrer",
#             "Permissions-Policy": "microphone=(), camera=()",
#             "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
#         })
#         return response

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Rutas de documentación y assets
DOCS_ALLOW = (
    "/docs", "/redoc", "/openapi.json",
    "/static/swagger-ui", "/static/redoc", "/static/swagger-ui-bundle.js",
    "/static/swagger-ui.css", "/static/redoc.standalone.js"
)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Headers base (seguros)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("Permissions-Policy", "microphone=(), camera=()")

        path = request.url.path

        # 🔓 NO aplicar CSP en docs/recursos de docs (evita pantalla en blanco)
        if any(path.startswith(p) for p in DOCS_ALLOW):
            # eliminar CSP si algún handler previo lo puso
            if "Content-Security-Policy" in response.headers:
                del response.headers["Content-Security-Policy"]
        else:
            # 🔒 CSP estricta para el resto de la API
            response.headers["Content-Security-Policy"] = (
                "default-src 'none'; frame-ancestors 'none'"
            )

        return response
