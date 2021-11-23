#!python3
# -*- coding: utf-8 -*-

import json
from pymongo import MongoClient

mongo_username = 'admin'
mongo_password = 'admin'
mongo_client = MongoClient('mongodb://%s:%s@127.0.0.1' % (mongo_username, mongo_password))
# Указатель на базу данных, может быть множество
mongo_db = mongo_client['hot_news']


if __name__ == "__main__":

    # Извлечение из БД одной новости
    first_news = mongo_db['hot_news'].find_one({})
    print(json.dumps(first_news, indent=2, ensure_ascii=False, default=str))

    # Кол-во документов в коллекции
    print(mongo_db['hot_news'].count_documents({}))

    # Очистка коллекции от документов
    mongo_db['hot_news'].delete_many({})
