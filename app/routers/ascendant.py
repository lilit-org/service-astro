from fastapi import APIRouter
from app.models import LocationRequest, AscendantResponse

router = APIRouter()

@router.post("/ascendant", response_model=AscendantResponse)
async def get_ascendant(request: LocationRequest):
    pass