import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.auth import APIKeyMiddleware
from app.routers import ascendant, planets

########################################################
#           Settings
########################################################
MESSAGE = "LILIT's astrological API"

app = FastAPI(
    title=MESSAGE,
    description="API for performing astrological calculations",
    version="0.0.1",
)

app.add_middleware(APIKeyMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dotenv.load_dotenv()

########################################################
#           Endpoints
########################################################
app.include_router(planets.router)
app.include_router(ascendant.router)


@app.get("/")
async def root():
    return {"message": MESSAGE}
