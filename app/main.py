import os

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
ALLOWED_ORIGINS = (
    os.getenv("ALLOWED_ORIGINS", "").split(",")
    if os.getenv("ALLOWED_ORIGINS")
    else []
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
    allow_methods=["GET", "POST"],  # Only allow necessary methods
    allow_headers=["API_KEY", "Content-Type"],  # Only allow necessary headers
    max_age=3600,  # Cache preflight requests for 1 hour
)

########################################################
#           Endpoints
########################################################
app.include_router(planets.router)
app.include_router(ascendant.router)


@app.get("/")
async def root():
    return {"message": MESSAGE}
