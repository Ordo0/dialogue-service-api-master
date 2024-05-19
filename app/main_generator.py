from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from typing import Literal
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import logging
import os
import time

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Определяем модель запроса
class ImageRequest(BaseModel):
    text: str
    format: Literal["png", "jpeg"]


app = FastAPI()


@app.post("/generate_image")
async def generate_image(image_request: ImageRequest):
    # Выводим сообщение в лог
    logger.info(f'Received text: {image_request.text}, format: {image_request.format}')

    # Создаем изображение с текстом
    img = Image.new('RGB', (200, 100), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((10, 10), image_request.text, fill=(255, 255, 0))

    # Определяем путь к временному файлу
    file_path = f'temp.{image_request.format}'

    # Проверяем, существует ли уже файл с таким именем
    if os.path.exists(file_path):
        # Если существует, удаляем его
        os.remove(file_path)
    try:
        # Сохраняем изображение в файл
        img.save(file_path)
    except Exception as e:
        # Логируем исключение и возвращаем HTTP-ошибку с соответствующим сообщением
        logger.error(f'Failed to save image: {str(e)}')
        raise HTTPException(status_code=500, detail='Failed to generate image')

    return JSONResponse(content={'message': f'Это картинка, но это не точно. На ней изображено: {image_request.text}'})
    # Отдаем изображение в ответ
    # return FileResponse(file_path, media_type=f'image/{image_request.format}')


@app.get("/generate")
async def root(prompt: str):
    time.sleep(5)
    return JSONResponse(content={'message': f'Это картинка, но это не точно. На ней изображено: {prompt}'})
