import json
import requests
from app.core.config import settings
from fastapi import HTTPException, APIRouter
from fastapi import status
from app.schemas.image import ImageData

# Create a router
router = APIRouter()


@router.post("/generate_image")
def generate_image(image_data: ImageData):
    # POST request to the Image microservice
    try:
        response = requests.post(
            url=settings.GENERATE_IMAGE_URL,
            json=image_data.dict()
        )
    except requests.exceptions.RequestException as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Image microservice is currently unavailable"
        ) from err

    # Handling the response
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Image microservice error: {response.text}"
        )

    # Extract the data from the response
    image = response.json()['message']

    return {"status": "success", "image": image}
