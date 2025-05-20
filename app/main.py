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

ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "").split(",")

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
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
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
