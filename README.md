# RepeatRemindBot

[Русская версия](#русская-версия) | [English version](#english-version)

## Русская версия

`RepeatRemindBot` — мой старый pet-project: Telegram-бот для запоминания информации с карточек и удобного повторения готовых модулей. С этим проектом я занял призовое место на конкурсе проектов **«Высший пилотаж 2024–2025»**. Проект я делал один, еще в 8 классе.

Основная идея простая: не только повторять карточки, но и быстро создавать учебные модули разными способами, в том числе с помощью встроенных AI-инструментов.

### Что умеет бот

- Создавать модули вручную из пар `термин = ответ`
- Генерировать модуль по текстовому описанию через `YandexGPT API`
- Добавлять карточки голосом: бот распознает речь и превращает ее в пары для запоминания
- Извлекать текст с фото страницы учебника через `Tesseract OCR`
- Автоматически переводить и собирать полученные фразы в модуль
- Запускать повторение карточек по блокам внутри Telegram
- Открывать mini app-игру для повторения слов из отдельного репозитория: [RepeatRemindGame](https://github.com/VladSunny/RepeatRemindGame)

### Зачем это было сделано

Мне хотелось собрать в одном проекте более удобный способ учить слова, термины и короткие факты, чем просто вручную переписывать карточки. Поэтому в боте появился упор на быстрое создание модулей: текстом, голосом, по фото и через AI-генерацию по описанию.

### Технологии

- `Python`
- `aiogram`
- `Supabase`
- `YandexGPT API`
- `Tesseract OCR`
- `SpeechRecognition` / обработка голосовых сообщений
- `Telegram Bot API`
- `Telegram Mini App` для игровой части

---

## English Version

`RepeatRemindBot` is an old pet project of mine: a Telegram bot for memorizing information with flashcard-style modules and repeating them in a more convenient way. This project won me a prize-winning place in the **“Высший пилотаж / Higher Pilotage 2024–2025”** project competition. I built it solo in 8th grade.

The core idea is simple: not only to review cards, but also to make module creation much faster, including with built-in AI tools.

### What the bot does

- Creates study modules manually from `term = answer` pairs
- Generates modules from a text prompt via `YandexGPT API`
- Supports voice input and turns recognized speech into study pairs
- Extracts text from textbook photos with `Tesseract OCR`
- Auto-translates phrases and converts them into a learning module
- Runs repetition sessions by blocks directly in Telegram
- Opens a mini app game for extra practice from a separate repository: [RepeatRemindGame](https://github.com/VladSunny/RepeatRemindGame)

### Why this project matters

I wanted to build a simpler way to learn words, terms, and short facts than rewriting flashcards by hand. That is why the project focuses on fast module creation: by text, by voice, from a photo, and through AI generation from a short description.

### Tech stack

- `Python`
- `aiogram`
- `Supabase`
- `YandexGPT API`
- `Tesseract OCR`
- `SpeechRecognition`
- `Telegram Bot API`
- `Telegram Mini App`

