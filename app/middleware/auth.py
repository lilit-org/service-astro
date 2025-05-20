import os
import time
from collections import defaultdict

from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

load_dotenv()

########################################################
#           Settings
########################################################
API_KEY_HEADER = APIKeyHeader(name="API_KEY", auto_error=True)
RATE_LIMIT_WINDOW = int(os.environ.get("RATE_LIMIT_WINDOW", "3600"))
MAX_REQUESTS_PER_WINDOW = int(
    os.environ.get("MAX_REQUESTS_PER_WINDOW", "1000")
)
MAX_FAILED_ATTEMPTS = int(os.environ.get("MAX_FAILED_ATTEMPTS", "5"))
BLOCK_DURATION = int(os.environ.get("BLOCK_DURATION", "300"))
INVALID_API_KEY = "Invalid API Key"

# In-memory storage for rate limiting and failed attempts
request_counts = defaultdict(lambda: {"count": 0, "window_start": time.time()})
failed_attempts = defaultdict(lambda: {"count": 0, "blocked_until": None})


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


def record_failed_attempt(ip: str):
    now = time.time()
    data = failed_attempts[ip]
    if data["blocked_until"] and now > data["blocked_until"]:
        data["count"] = 0
        data["blocked_until"] = None
    data["count"] += 1
    if data["count"] >= MAX_FAILED_ATTEMPTS:
        data["blocked_until"] = now + BLOCK_DURATION


async def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    if api_key_header not in APIKeyMiddleware.valid_api_keys:
        raise HTTPException(status_code=403, detail=INVALID_API_KEY)
    return api_key_header


class APIKeyMiddleware(BaseHTTPMiddleware):
    valid_api_keys = []
    api_keys = os.getenv("API_KEYS", "")
    if api_keys:
        valid_api_keys = [key.strip() for key in api_keys.split(",")]
    else:
        single_key = os.getenv("API_KEY")
        if single_key:
            valid_api_keys = [single_key]

    async def dispatch(self, request: Request, call_next):
        if (
            request.url.path == "/docs"
            or request.url.path == "/openapi.json"
            or request.url.path == "/"
        ):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"

        if is_rate_limited(client_ip):
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later.",
            )

        api_key = None
        if request.url.path == "/planets":
            api_key = request.query_params.get("API_KEY")
            if not api_key:
                api_key = request.headers.get("API_KEY")
        else:
            api_key = request.headers.get("API_KEY")

        if not api_key:
            record_failed_attempt(client_ip)
            raise HTTPException(
                status_code=403,
                detail="API key is required.",
            )

        if api_key not in self.valid_api_keys:
            record_failed_attempt(client_ip)
            raise HTTPException(status_code=403, detail=INVALID_API_KEY)

        return await call_next(request)
