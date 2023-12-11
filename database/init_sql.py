import sqlite3
from database.database import supa_get_user, supa_get_all_users
from config_data.database_config_data import default_lang


# Функция инициализирования локальной БД
def init_local_database():
    conn = sqlite3.connect('database/users_language.db')

    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        chat_id INTEGER PRIMARY KEY,
        lang TEXT
    )
    ''')
    conn.commit()

    # Очистка таблицы
    cursor.execute('DELETE FROM users')
    conn.commit()

    # Получение всех пользователей с Supabase
    users = supa_get_all_users()

    rows_to_insert = [(user['chat_id'], user['lang']) for user in users]

    # Запись всех пользователей в локальную БД
    cursor.executemany('''
        INSERT INTO users (chat_id, lang) VALUES (?, ?)
    ''', rows_to_insert)
    conn.commit()

    cursor.execute('SELECT * FROM users')
    local_users = cursor.fetchall()

    conn.close()

    # Вывод для теста
    print(f"{len(local_users)}/{len(users)} users were added to sql")
