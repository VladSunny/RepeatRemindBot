import sqlite3
from icecream import ic


# Добавление нового человека в локальную БД
def local_add_user(chat_id: int, lang: str):
    conn = sqlite3.connect('database/users_language.db')
    cursor = conn.cursor()

    cursor.execute('''
            INSERT OR IGNORE INTO users (chat_id, lang) VALUES (?, ?)
            ''', (chat_id, lang))

    conn.commit()
    conn.close()


# Получение информации о пользователе из локальной БД
def local_get_user(chat_id: int):
    conn = sqlite3.connect('database/users_language.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM users
    WHERE chat_id = ?
    ''', (chat_id,))

    user = cursor.fetchone()

    conn.commit()
    conn.close()

    return user


# Получение списка id всех пользователей из локальной БД
def local_get_users_chat_ids():
    conn = sqlite3.connect('database/users_language.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT chat_id FROM users''')

    users = [i[0] for i in cursor.fetchall()]

    conn.commit()
    conn.close()

    return users


# Обновление языка пользователя
def local_update_user(chat_id: int, update: dict):
    new_lang = update['lang']

    conn = sqlite3.connect('database/users_language.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE users SET lang=? WHERE chat_id=?''', (new_lang, chat_id))

    conn.commit()
    conn.close()
