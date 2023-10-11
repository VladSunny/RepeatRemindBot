from copy import deepcopy
from typing import Union

import firebase_admin
from firebase_admin import credentials, firestore

# Создаем шаблон заполнения словаря с пользователями
user_dict_template = {
    'state': None,
    'lang': 'en'
}

# Подключаемся к firebase
cred = credentials.Certificate("serviceAccountKey.json")
app = firebase_admin.initialize_app(cred)

# Инициализируем "базу данных"
db = firestore.client()
users_db = db.collection('users_tg')


def get_users() -> list[int]:
    users = list(map(lambda x: int(x.id), users_db.stream()))
    return users


def add_user(uid: Union[int, str]) -> None:
    users_db.document(str(uid)).set(deepcopy(user_dict_template))


def get_user(uid: Union[int, str]) -> dict:
    user = users_db.document(str(uid)).get()
    return user.to_dict()


def is_user_updated(uid: Union[int, str]) -> bool:
    return set(get_user(uid).keys()) == set(user_dict_template.keys())


def update_user(uid: Union[int, str]) -> None:
    old_user = get_user(uid)
    new_user = deepcopy(user_dict_template)

    for key in old_user.keys():
        if new_user.get(key):
            new_user[key] = old_user[key]

    users_db.document(str(uid)).update(new_user)


def update_value(uid: Union[int, str], update: dict) -> None:
    user = users_db.document(str(uid))
    user.update(update)
