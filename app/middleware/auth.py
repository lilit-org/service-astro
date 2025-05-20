from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import os

API_KEY_NAME = "zA5lvzxwOBLSbG0koNHU0g7flp9yfsHL"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
INVALID_API_KEY = "Invalid API Key"

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=403,
            detail=INVALID_API_KEY
        )
    return api_key_header


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/docs" or request.url.path == "/openapi.json" or request.url.path == "/":
            return await call_next(request)
            
        if request.url.path == "/planets":
            api_key = request.query_params.get(API_KEY_NAME)
            if not api_key:
                api_key = request.headers.get(API_KEY_NAME)
        else:
            api_key = request.headers.get(API_KEY_NAME)
            
        if not api_key or api_key != os.getenv("API_KEY"):
            raise HTTPException(
                status_code=403,
                detail=INVALID_API_KEY
            )
        return await call_next(request)
