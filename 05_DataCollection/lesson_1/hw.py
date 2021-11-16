#!python3
# -*- coding: utf-8 -*-

# 1. Посмотреть документацию к API GitHub, разобраться как вывести список
# репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json


class GitHub:
    def __init__(self):
        self.url = 'https://api.github.com'
        self.user = ''
        self.headers = {'Content-Type' : 'application/json'}
        self.api_key = self.load_api_key()

    def directory(self):
        req = requests.get(self.url, headers=self.headers)
        if req.status_code != 200:
            raise Exception(f"Bad status {req.status_code}")
        print(json.dumps(req.json(), indent=2))

    def public_repos(self, username):
        req = requests.get(self.url + f'/users/{username}/repos', headers=self.headers)
        if req.status_code != 200:
            raise ConnectionError(f'Bad status: {req.status_code}')
        # print(f'Response: {req.json()}')
        return req.json()

    def write_json(self, filename, data):
        with open(filename, 'w') as file:
            file.write(data)

    def private_repos(self, username):
        self.headers.update({'Authorization': f'token {self.api_key}'})
        req = requests.get(self.url + f'/search/repositories?q=user:{username}', headers=self.headers)

        if req.status_code != 200:
            raise ConnectionError(f'Bad status: {req.status_code}')
        #print(f'Response: {json.dumps(req.json(), indent=4)}')
        return req.json()

    def load_api_key(self):
        with open('./api_key', 'r') as key:
            return key.read()


if __name__ == "__main__":
    gh = GitHub()
    # ======= Задание 1 =======
    username = 'vladadm'
    public_repo_list = [x['name'] for x in gh.public_repos(username)]
    data = {
        'user': username,
        'public_repos': public_repo_list
    }
    gh.write_json('hw_task1.json', json.dumps(data, indent=2))

    # ======= Задание 2 ======
    username = 'vladadm'
    all_repo_list = [x['name'] for x in gh.private_repos(username)['items']]
    data = {
        'user': username,
        'all_repos': all_repo_list
    }
    gh.write_json('hw_task2.json', json.dumps(data, indent=2))
