import os
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

load_dotenv()

########################################################
#           Settings
########################################################
RATE_LIMIT_WINDOW = int(os.environ.get("RATE_LIMIT_WINDOW", "3600"))
MAX_REQUESTS_PER_WINDOW = int(
    os.environ.get("MAX_REQUESTS_PER_WINDOW", "1000")
)
MAX_FAILED_ATTEMPTS = int(os.environ.get("MAX_FAILED_ATTEMPTS", "5"))
BLOCK_DURATION = int(os.environ.get("BLOCK_DURATION", "300"))

# In-memory storage for rate limiting and failed attempts
request_counts: Dict[str, Dict[str, Any]] = defaultdict(
    lambda: {"count": 0, "window_start": time.time()}
)
failed_attempts: Dict[str, Dict[str, Any]] = defaultdict(
    lambda: {"count": 0, "blocked_until": None}
)

# Load the invalid API key template
INVALID_API_TEMPLATE = Path("app/templates/invalid_api.html").read_text()

# List of paths that don't require API key authentication
PUBLIC_PATHS = {"/docs", "/openapi.json", "/"}


########################################################
#           Utility functions
########################################################
def is_rate_limited(ip: str) -> bool:
    now = time.time()
    data = request_counts[ip]
    if now - data["window_start"] > RATE_LIMIT_WINDOW:
        data["count"] = 0
        data["window_start"] = now
    if (
        failed_attempts[ip]["blocked_until"]
        and now < failed_attempts[ip]["blocked_until"]
    ):
        return True
    data["count"] += 1
    return data["count"] > MAX_REQUESTS_PER_WINDOW


def record_failed_attempt(ip: str) -> None:
    now = time.time()
    data = failed_attempts[ip]
    if data["blocked_until"] and now > data["blocked_until"]:
        data["count"] = 0
        data["blocked_until"] = None
    data["count"] += 1
    if data["count"] >= MAX_FAILED_ATTEMPTS:
        data["blocked_until"] = now + BLOCK_DURATION


class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.valid_api_keys = self._load_api_keys()

    def _load_api_keys(self) -> list[str]:
        api_keys = os.getenv("API_KEYS", "")
        if api_keys:
            return [key.strip() for key in api_keys.split(",")]
        single_key = os.getenv("API_KEY")
        return [single_key] if single_key else []

    async def dispatch(self, request: Request, call_next):
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)
        client_ip = request.client.host if request.client else "unknown"
        if is_rate_limited(client_ip):
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later.",
            )
        api_key = request.headers.get("API_KEY")
        if not api_key or api_key not in self.valid_api_keys:
            record_failed_attempt(client_ip)
            return HTMLResponse(content=INVALID_API_TEMPLATE, status_code=403)
        return await call_next(request)
