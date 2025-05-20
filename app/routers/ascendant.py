from fastapi import APIRouter
from app.models import LocationRequest, AscendantResponse
from app.utils import get_ascendant_divineapi

router = APIRouter()

@router.post("/ascendant", response_model=AscendantResponse)
async def get_ascendant(request: LocationRequest):
    # Extract date and time components
    dt = request.date_time
    api_key = "YOUR_API_KEY"  # TODO: Replace with your actual API key
    auth_token = "YOUR_AUTH_TOKEN"  # TODO: Replace with your actual Auth token
    # You may want to pass these as environment variables for security
    result = get_ascendant_divineapi(
        api_key=api_key,
        auth_token=auth_token,
        full_name="Test User",
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=dt.hour,
        minute=dt.minute,
        second=dt.second,
        gender="other",
        place="Zurich, Switzerland",  # You can make this dynamic
        lat=request.latitude,
        lon=request.longitude,
        tzone=2,  # You can make this dynamic
        house_system="P"
    )
    # Parse the response
    sign = result["data"]["sign"]
    degrees = float(result["data"]["full_degree"]) % 30
    return AscendantResponse(sign=sign, degrees=round(degrees, 2))
