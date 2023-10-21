from __future__ import annotations
from copy import deepcopy
from environs import Env

from supabase import create_client, Client
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
    response = supabase.table("users_tg").select("chat_id").execute()
    users = list(map(lambda d: int(list(d.values())[0]), response.data))
    return users


def add_user(chat_id: int | str) -> None:
    new_user = deepcopy(user_dict_template)
    new_user["chat_id"] = chat_id

    response = supabase.table("users_tg").insert(new_user).execute()


def get_user(chat_id: int | str) -> dict:
    response = supabase.table("users_tg").select('*').eq("chat_id", str(chat_id)).execute()
    user = response.data[0]
    return user


def update_value(chat_id: int | str, update: dict) -> None:
    response = supabase.table("users_tg").update(update).eq("chat_id", chat_id).execute()
