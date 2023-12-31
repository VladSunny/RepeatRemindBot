import asyncio
import copy
import os
import platform
import re

import pytesseract
from PIL import Image

os_name = platform.system()

print(os_name)

if os_name == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Перевести полученные фразы в текст
def format_phrases_to_text(phrases: list[str]):
    text = ""

    for i in range(len(phrases)):
        text += f"{i + 1}. {phrases[i]}\n"

    return text


# Очистить считанный текст и достать фразы
def clear_text(text_from_photo: str, sep: str) -> list[str]:
    # Сначала разделяем текст на выражения по запятым
    text = copy.deepcopy(text_from_photo)
    if sep != '\n':
        text = text.replace('\n', ' ')

    expressions = [expr.strip() for expr in text.split(sep)]

    # Потом очищаем каждое выражение от лишних символов, оставляя буквы, цифры, пробелы и дефисы
    clean_expressions = []
    for expr in expressions:
        if expr:  # игнорируем пустые строки после разделения
            # Убираем все символы, которые не являются буквами, цифрами, пробелами и дефисами
            clean_expr = re.sub(r'[^\w\s-]', '', expr)
            clean_expr = clean_expr.strip().lower()
            clean_expressions.append(clean_expr)

    return clean_expressions


# Считать текст с изображения
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


# Получить текст с изображения и удалить его из памяти
async def get_eng_from_photo(path: str, delete_photo: bool = True) -> str:
    try:
        text = await async_image_to_string(path)
        return text
    finally:
        if delete_photo:
            os.remove(path)
