from copy import deepcopy

import firebase_admin
from firebase_admin import credentials, firestore

# Создаем шаблон заполнения словаря с пользователями
user_dict_template = {
    'state': None
}

# Подключаемся к firebase
cred = credentials.Certificate("serviceAccountKey.json")
app = firebase_admin.initialize_app(cred)

# Инициализируем "базу данных"
db = firestore.client()
users_db = db.collection('users_tg')


def get_users() -> list[str]:
    users = list(map(lambda x: x.id, users_db.stream()))
    return users


def add_user(uid: str) -> None:
    users_db.document(uid).set(deepcopy(user_dict_template))
