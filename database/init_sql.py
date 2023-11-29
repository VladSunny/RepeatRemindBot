import sqlite3
from database.database import supa_get_users_chat_ids, supa_get_user


def init_local_database():
    conn = sqlite3.connect('database/users_language.db')

    cursor = conn.cursor()

    # create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        chat_id INTEGER PRIMARY KEY,
        lang TEXT DEFAULT 'en'
    )
    ''')
    conn.commit()

    # clear table
    cursor.execute('DELETE FROM users')
    conn.commit()

    # add users
    chat_ids: list[int] = supa_get_users_chat_ids()
    for chat_id in chat_ids:
        lang = supa_get_user(chat_id)['lang']
        cursor.execute('''
        INSERT OR IGNORE INTO users (chat_id, lang) VALUES (?, ?)
        ''', (chat_id, lang))
    conn.commit()

    # Выполняем запрос на выборку данных
    cursor.execute('SELECT * FROM users')
    # Получаем все результаты
    users = cursor.fetchall()

    conn.close()

    print(f"{len(users)} users were added to sql")
