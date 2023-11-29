import sqlite3
from icecream import ic


def local_add_user(chat_id: int):
    conn = sqlite3.connect('users_language.db')
    cursor = conn.cursor()

    cursor.execute('''
            INSERT OR IGNORE INTO users (chat_id) VALUES (?)
            ''', (chat_id,))

    conn.commit()
    conn.close()


def local_get_user(chat_id: int):
    conn = sqlite3.connect('users_language.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM users
    WHERE chat_id = ?
    ''', (chat_id,))

    user = cursor.fetchone()

    conn.commit()
    conn.close()

    return user


def local_get_users_chat_ids():
    conn = sqlite3.connect('users_language.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT chat_id FROM users''')

    users = [i[0] for i in cursor.fetchall()]

    conn.commit()
    conn.close()

    return users


def local_update_user(chat_id: int, update: dict):
    new_lang = update['lang']

    conn = sqlite3.connect('users_language.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE users SET lang=? WHERE chat_id=?''', (new_lang, chat_id))

    conn.commit()
    conn.close()
