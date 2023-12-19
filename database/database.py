from __future__ import annotations

from copy import deepcopy

from environs import Env
from supabase import create_client, Client

from config_data.database_config_data import default_lang
from database.local_database import local_add_user, local_get_user, local_update_user, local_get_users_chat_ids

# Создаем шаблон заполнения словаря с пользователями
user_dict_template = {
    'chat_id': "",
    'lang': default_lang
}

# Читаем Env
env = Env()
env.read_env(None)

# Берем от туда нужные данные для supabase
url: str = env("SUPABASE_URL")
key: str = env("SUPABASE_KEY")

supabase: Client = create_client(url, key)


# Получение всех пользователей из таблицы users_tg через supabase
def supa_get_all_users() -> list[dict]:
    response = supabase.table("users_tg").select('*').execute()
    users = response.data

    return users


# Получение списка из id всех пользователей через локальную БД
def get_users_chat_ids() -> list[int]:
    users = local_get_users_chat_ids()
    return users


# Получение списка из id всех пользователей через Supabase
def supa_get_users_chat_ids() -> list[int]:
    response = supabase.table("users_tg").select("chat_id").execute()
    users = list(map(lambda d: int(list(d.values())[0]), response.data))
    return users


# Добавление нового пользователя в локальную БД и на Supabase
def add_user(chat_id: int | str) -> None:
    new_user = deepcopy(user_dict_template)
    new_user["chat_id"] = chat_id

    response = supabase.table("users_tg").insert(new_user).execute()
    response = supabase.table("settings").insert({"chat_id": chat_id}).execute()

    local_add_user(int(chat_id), default_lang)


# Получение информации о пользователе через локальную БД
def get_user(chat_id: int | str) -> dict:
    local_user = local_get_user(int(chat_id))

    if local_user is not None:
        local_user = dict(zip(('chat_id', 'lang'), local_user))
        return local_user

    return {'chat_id': chat_id, 'lang': 'en'}


# Получение информации о пользователе через Supabase
def supa_get_user(chat_id: int | str) -> dict:
    response = supabase.table("users_tg").select('*').eq("chat_id", str(chat_id)).execute()
    user = response.data[0]

    local_user = local_get_user(int(chat_id))

    return user


# Получение списка модулей пользователя через Supabase
def get_modules(chat_id: int | str) -> dict:
    response = supabase.table("modules").select('*').eq("chat_id", str(chat_id)).execute()
    return response.data


# Получение количества модулей пользователя через Supabase
def get_modules_number(chat_id: int | str) -> int:
    response = supabase.table("modules").select('id').eq("chat_id", str(chat_id)).execute()
    modules_number = len(response.data)
    return modules_number


# Получение модуля через Supabase
def get_module(id: int) -> dict | None:
    response = supabase.table("modules").select('*').eq("id", id).execute()
    return response.data[0] if response.data != [] else None


# Обновление пользователя в таблице users_tg
# (в основном это обновление языка)
def update_user(chat_id: int | str, update: dict) -> None:
    response = supabase.table("users_tg").update(update).eq("chat_id", chat_id).execute()
    local_update_user(chat_id, update)


# Сохранение модуля через Supabase
def save_module(chat_id: int | str, data: dict[str, any]) -> dict:
    new_module = {
        "chat_id": str(chat_id),
        "name": data['name'],
        "content": data['content'],
        "separator": data['separator']
    }

    response = supabase.table("modules").insert(new_module).execute()
    return response.data[0]


# Удаление модуля через Supabase
def delete_saved_module(module_id: int) -> bool:
    response = supabase.table("modules").delete().eq("id", module_id).execute()
    return True


# Обновление параметров пользователя
def update_settings(chat_id: int | str, update: dict) -> None:
    response = supabase.table("settings").update(update).eq("chat_id", chat_id).execute()


# Получение параметров пользователя
def get_settings(chat_id: int | str) -> dict:
    response = supabase.table("settings").select('*').eq("chat_id", chat_id).execute()
    return response.data[0]
