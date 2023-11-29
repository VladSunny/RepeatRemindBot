from __future__ import annotations
from copy import deepcopy
from environs import Env

from supabase import create_client, Client
from database.local_database import local_add_user, local_get_user, local_update_user, local_get_users_chat_ids
from icecream import ic

# Создаем шаблон заполнения словаря с пользователями
user_dict_template = {
    'lang': 'en'
}

env = Env()
env.read_env(None)

url: str = env("SUPABASE_URL")
key: str = env("SUPABASE_KEY")

supabase: Client = create_client(url, key)


def get_users_chat_ids() -> list[int]:
    users = local_get_users_chat_ids()
    return users


def supa_get_users_chat_ids() -> list[int]:
    response = supabase.table("users_tg").select("chat_id").execute()
    users = list(map(lambda d: int(list(d.values())[0]), response.data))
    return users


def add_user(chat_id: int | str) -> None:
    new_user = deepcopy(user_dict_template)
    new_user["chat_id"] = chat_id

    response = supabase.table("users_tg").insert(new_user).execute()
    response = supabase.table("settings").insert({"chat_id": chat_id}).execute()
    response = supabase.table("learning").insert({"chat_id": chat_id}).execute()

    local_add_user(int(chat_id))


def get_user(chat_id: int | str) -> dict:
    local_user = local_get_user(int(chat_id))

    if local_user is not None:
        local_user = dict(zip(('chat_id', 'lang'), local_user))
        return local_user

    return {'chat_id': chat_id, 'lang': 'en'}


def supa_get_user(chat_id: int | str) -> dict:
    response = supabase.table("users_tg").select('*').eq("chat_id", str(chat_id)).execute()
    user = response.data[0]

    local_user = local_get_user(int(chat_id))

    return user


def get_modules(chat_id: int | str) -> dict:
    response = supabase.table("modules").select('*').eq("chat_id", str(chat_id)).execute()
    return response.data


def get_module(id: int) -> dict | None:
    response = supabase.table("modules").select('*').eq("id", id).execute()
    return response.data[0] if response.data != [] else None


def update_user(chat_id: int | str, update: dict) -> None:
    response = supabase.table("users_tg").update(update).eq("chat_id", chat_id).execute()
    local_update_user(chat_id, update)


def save_module(chat_id: int | str, data: dict[str, any]) -> dict:
    new_module = {
        "chat_id": str(chat_id),
        "name": data['name'],
        "content": data['content'],
        "separator": data['separator']
    }

    response = supabase.table("modules").insert(new_module).execute()
    return response.data[0]


def delete_saved_module(module_id: int) -> bool:
    response = supabase.table("modules").delete().eq("id", module_id).execute()
    return True


def update_settings(chat_id: int | str, update: dict) -> None:
    response = supabase.table("settings").update(update).eq("chat_id", chat_id).execute()


def get_settings(chat_id: int | str) -> dict:
    response = supabase.table("settings").select('*').eq("chat_id", chat_id).execute()
    return response.data[0]


def update_learning(chat_id: int | str, update: dict) -> None:
    response = supabase.table("learning").update(update).eq("chat_id", chat_id).execute()


def get_learning_data(chat_id: int | str) -> dict:
    response = supabase.table("learning").select('learning_content').eq("chat_id", chat_id).execute()
    return response.data[0]


def get_module_by_id(id: int) -> dict | None:
    response = supabase.table("modules").select('*').eq("id", id).execute()
    if not len(response.data):
        return None
    return response.data[0]

