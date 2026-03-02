from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine, Base
# Import models to ensure they are registered with SQLAlchemy
from app.models import image, video, post 

# Create tables (simple migration)
Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Cutesite API", 
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted hosts (fail-open in non-configured environments to avoid 400s)
allowed_hosts = ["localhost", "127.0.0.1"]
parsed_base_host = None
try:
    # Lazy import to avoid hard dependency if unused
    from urllib.parse import urlparse
    parsed = urlparse(settings.BASE_URL or "")
    if parsed.hostname:
        parsed_base_host = parsed.hostname
except Exception:
    parsed_base_host = None

if parsed_base_host and parsed_base_host not in allowed_hosts:
    allowed_hosts.append(parsed_base_host)

if settings.DOMAIN and settings.DOMAIN not in ["localhost", "127.0.0.1"]:
    # Add apex and wildcard subdomains
    if settings.DOMAIN not in allowed_hosts:
        allowed_hosts.append(settings.DOMAIN)
    wildcard = f"*.{settings.DOMAIN}"
    if wildcard not in allowed_hosts:
        allowed_hosts.append(wildcard)

# If still only localhost and no domain configured, allow all to prevent false 400 in deployments
if len(allowed_hosts) <= 2 and settings.DOMAIN in (None, "", "localhost"):
    allowed_hosts = ["*"]

app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# Security headers
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        return response

app.add_middleware(SecurityHeadersMiddleware)

app.include_router(api_router, prefix="/api/v1")

# Mount uploads directory to serve files directly (fallback if Caddy is bypassed)
# We assume uploads are in a directory relative to where the app is run or absolute path
uploads_dir = os.path.abspath(os.path.join(settings.UPLOAD_IMAGES_DIR, ".."))
if os.path.exists(uploads_dir):
    app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

@app.get("/health")
def health_check():
    return {"status": "ok"}
