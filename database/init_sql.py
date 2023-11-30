import sqlite3
from database.database import supa_get_user, supa_get_all_users


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
    users = supa_get_all_users()

    rows_to_insert = [(user['chat_id'], user['lang']) for user in users]

    cursor.executemany('''
        INSERT INTO users (chat_id, lang) VALUES (?, ?)
    ''', rows_to_insert)
    conn.commit()

    # Выполняем запрос на выборку данных
    cursor.execute('SELECT * FROM users')
    # Получаем все результаты
    local_users = cursor.fetchall()

    conn.close()

    print(f"{len(local_users)}/{len(users)} users were added to sql")
