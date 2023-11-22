import pytesseract
from PIL import Image
import platform
import os
import asyncio
from icecream import ic

os_name = platform.system()
if os_name == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


async def async_image_to_string(image_path):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        pytesseract.image_to_string, Image.open(image_path), 'eng'
    )


async def get_eng_from_photo(path: str, delete_photo: bool = True) -> str:
    try:
        text = await async_image_to_string(path)
        return text
    finally:
        if delete_photo:
            os.remove(path)
