import aiosqlite


async def local_add_user(chat_id: int):
    async with aiosqlite.connect('users_language.db') as conn:
        cursor = await conn.execute('''
                INSERT OR IGNORE INTO users (chat_id) VALUES (?)
                ''', (chat_id,))
        await conn.commit()


async def local_get_user(chat_id: int):
    async with aiosqlite.connect('users_language.db') as conn:
        cursor = await conn.execute('''
        SELECT * FROM users
        WHERE chat_id = ?
        ''', (chat_id,))

        user = await cursor.fetchone()
        return user


async def local_get_users_chat_ids():
    async with aiosqlite.connect('users_language.db') as conn:
        cursor = await conn.execute('''
        SELECT chat_id FROM users
        ''')

        users_chat_ids = await cursor.fetchall()
        return users_chat_ids


async def local_update_user(chat_id: int, update: dict):
    new_lang = update['lang']

    async with aiosqlite.connect('users_language.db') as conn:
        await conn.execute('''UPDATE users SET lang=? WHERE chat_id=?''', (new_lang, chat_id))
        await conn.commit()
