import os
from typing import List

import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.auth import APIKeyMiddleware
from app.routers import ascendant, planets

########################################################
#           Settings
########################################################
MESSAGE = "LILIT's astrological API"
dotenv.load_dotenv()

# Get allowed origins from environment variable, default to empty list
ALLOWED_ORIGINS: List[str] = (
    os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []
)

app = FastAPI(
    title=MESSAGE,
    description="API for performing astrological calculations",
    version="0.0.1",
)
app.add_middleware(APIKeyMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=[
        "API_KEY",
        "Content-Type",
    ],
    expose_headers=["API_KEY"],
    max_age=int(os.getenv("CORS_MAX_AGE", "3600")),
)

########################################################
#           Endpoints
########################################################
app.include_router(planets.router)
app.include_router(ascendant.router)


@app.get("/")
async def root():
    return {"message": MESSAGE}
