import os
import time
from collections import defaultdict

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

########################################################
#           Settings
########################################################
API_KEY_NAME = os.getenv("API_KEY_NAME", "API_KEY")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
INVALID_API_KEY = "Invalid API Key"
RATE_LIMIT_WINDOW = 3600  # 1 hour in seconds
MAX_REQUESTS_PER_WINDOW = 1000  # Maximum requests per hour per IP
MAX_FAILED_ATTEMPTS = 5  # Maximum failed attempts before temporary block
BLOCK_DURATION = 300  # 5 minutes in seconds
# In-memory storage for rate limiting and failed attempts
request_counts = defaultdict(lambda: {"count": 0, "window_start": time.time()})
failed_attempts = defaultdict(lambda: {"count": 0, "blocked_until": None})


########################################################
#           Utility functions
########################################################
def get_valid_api_keys():
    """Get list of valid API keys from environment variables."""
    api_keys = os.getenv("API_KEYS", "")
    if not api_keys:
        # Fallback to single API_KEY for backward compatibility
        single_key = os.getenv("API_KEY")
        return [single_key] if single_key else []
    return [key.strip() for key in api_keys.split(",")]


def is_rate_limited(ip: str) -> bool:
    """Check if an IP is rate limited."""
    now = time.time()
    data = request_counts[ip]

    # Reset counter if window has passed
    if now - data["window_start"] > RATE_LIMIT_WINDOW:
        data["count"] = 0
        data["window_start"] = now

    # Check if blocked due to too many failed attempts
    if (
        failed_attempts[ip]["blocked_until"]
        and now < failed_attempts[ip]["blocked_until"]
    ):
        return True

    # Increment counter and check rate limit
    data["count"] += 1
    return data["count"] > MAX_REQUESTS_PER_WINDOW


def record_failed_attempt(ip: str):
    """Record a failed authentication attempt."""
    now = time.time()
    data = failed_attempts[ip]

    # Reset counter if block duration has passed
    if data["blocked_until"] and now > data["blocked_until"]:
        data["count"] = 0
        data["blocked_until"] = None

    data["count"] += 1
    if data["count"] >= MAX_FAILED_ATTEMPTS:
        data["blocked_until"] = now + BLOCK_DURATION


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header not in get_valid_api_keys():
        raise HTTPException(status_code=403, detail=INVALID_API_KEY)
    return api_key_header


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth for documentation and root
        if (
            request.url.path == "/docs"
            or request.url.path == "/openapi.json"
            or request.url.path == "/"
        ):
            return await call_next(request)

        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Check rate limiting
        if is_rate_limited(client_ip):
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later.",
            )

        # Get API key from appropriate location
        api_key = None
        if request.url.path == "/planets":
            # For planets endpoint, try query param first, then header
            api_key = request.query_params.get(API_KEY_NAME)
            if not api_key:
                api_key = request.headers.get(API_KEY_NAME)
        else:
            # For all other endpoints, only use header
            api_key = request.headers.get(API_KEY_NAME)

        # Validate API key
        if not api_key:
            record_failed_attempt(client_ip)
            raise HTTPException(
                status_code=403,
                detail="API key is required.",
            )

        if api_key not in get_valid_api_keys():
            record_failed_attempt(client_ip)
            raise HTTPException(status_code=403, detail=INVALID_API_KEY)

        return await call_next(request)
