from typing import Optional
from pydantic import BaseModel


class ImageData(BaseModel):
    text: str
    image_resolution: Optional[str] = None
    format: str
    additional_params: Optional[dict] = None
