import copy

import pytesseract
from PIL import Image
import platform
import os
import asyncio
from icecream import ic
import re

os_name = platform.system()
if os_name == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def clear_text(text_from_photo: str) -> list[str]:
    # Сначала разделяем текст на выражения по запятым
    text = copy.deepcopy(text_from_photo)
    text = text.replace('\n', ' ')
    expressions = [expr.strip() for expr in text.split(',')]

    # Потом очищаем каждое выражение от лишних символов, оставляя буквы, цифры, пробелы и дефисы
    clean_expressions = []
    for expr in expressions:
        if expr:  # игнорируем пустые строки после разделения
            # Убираем все символы, которые не являются буквами, цифрами, пробелами и дефисами
            clean_expr = re.sub(r'[^\w\s-]', '', expr)
            clean_expressions.append(clean_expr)

    return clean_expressions


async def async_image_to_string(image_path):
    loop = asyncio.get_running_loop()

    # Функция предобработки в черно-белое изображение
    def preprocess_image(image_path):
        with Image.open(image_path) as image:
            # Конвертация изображения в градации серого
            gray_image = image.convert('L')
            # Преобразование изображения в черно-белый (бинаризация)
            bw_image = gray_image.point(lambda x: 0 if x < 128 else 255, '1')
            return bw_image

    # Функция OCR с предобработкой
    def run_tesseract(image_path):
        # Получаем изображение, предварительно обработано в черно-белый формат
        bw_image = preprocess_image(image_path)
        # Указываем настройки для Tesseract
        custom_config = r'--oem 1' \
                        r' --psm 6' \
                        r' --user-patterns tesseract_pattern.txt' \
                        r' -l eng'
        # Применяем Tesseract к обработанному изображению с нашей кастомной конфигурацией
        return pytesseract.image_to_string(bw_image, config=custom_config)

    # Используем executor для выполнения функции OCR асинхронно
    return await loop.run_in_executor(
        None,
        run_tesseract, image_path
    )


async def get_eng_from_photo(path: str, delete_photo: bool = True) -> str:
    try:
        text = await async_image_to_string(path)
        return text
    finally:
        if delete_photo:
            os.remove(path)
