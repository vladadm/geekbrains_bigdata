#!python3
# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
from pprint import pprint
import re

from pymongo import MongoClient

# ====== Задание 1 ======
# Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB
# и реализовать функцию, которая будет добавлять только новые вакансии/продукты в вашу базу.

mongo_username = 'admin'
mongo_password = 'admin'
mongo_client = MongoClient('mongodb://%s:%s@127.0.0.1' % (mongo_username, mongo_password))
# Указатель на базу данных, может быть множество
mongo_db = mongo_client['vacancies']

class HH:
    def __init__(self, url, position, list_count):
        self.list_count = range(0, list_count)
        self.position = position.replace(' ', '+')
        self.url = url
        self.headers = {
            'Content-Type' : 'text/html; charset=utf-8',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
        }

    def get_position(self, page=0, mongo=False):
        path = f'/search/vacancy?text={self.position}&items_on_page=20'
        dom = bs(self.request(path), 'html.parser')
        first_page = dom.findAll('a', {'data-qa': 'pager-page'})[0].string
        last_page = dom.findAll('a', {'data-qa': 'pager-page'})[-1].string
        vac_result = dom.find('div', {'class': 'vacancy-serp'})
        vac = vac_result.find_all('div', {'data-qa': re.compile(r'vacancy-serp__vacancy.*')}, recursive=False)
        print("Items on page: ", len(vac))
        if len(vac) > 20:
            print("Last Page...")
        vac_batch = []
        count = 0
        for i in vac:
            count += 1
            dd = {}
            # Название вакансии
            title = i.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text

            # Размер компенсации
            if i.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}):
                compensation = i.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text #.encode("ascii", "ignore").decode('utf-8')

                compensation = compensation.split(' ')
                print(f'=== compensation raw:\n {compensation}')

                vvvv = {
                    'min': None,
                    'max': None,
                    'currency': None,
                }
                try:
                    if len(compensation) > 1:
                        if 'руб' in compensation[-1]:
                            vvvv['currency'] = 'RUB'
                            compensation[-1] = 'RUB'
                        if 'от' in compensation[0] and len(compensation) == 3:
                            vvvv['min'] = int(compensation[1].encode("ascii", "ignore"))
                            vvvv['max'] = None
                        if 'до' in compensation[0] and len(compensation) <= 3:
                            vvvv['min'] = None
                            vvvv['max'] = int(compensation[1].encode("ascii", "ignore"))
                        compensation = [x.encode("ascii", "ignore").decode('utf-8') for x in compensation]
                        compensation = ' '.join(compensation).split()
                        if len(compensation) == 3:
                            vvvv['min'] = int(compensation[0])
                            vvvv['max'] = int(compensation[1])
                        vvvv['currency'] = compensation[-1]

                        compensation = list(vvvv.values())
                        print(f'=== compensation final:\n', compensation)
                    else:
                        compensation = [None, None, None]
                        print("=== compensation empty:\n", compensation)
                except Exception as exc:
                    print(exc)
                    raise Exception('Error')
                    compensation = [None, None, None]

                print(compensation, '\n', vvvv, '\n')
            else:
                compensation = [None, None, None]

            # Страница вакансии
            href = i.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href'].split('?')[0]

            # Название работодателя
            if i.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}):
                empl = i.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text
            else:
                empl = None

            # Город
            if i.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}):
                city = i.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
            else:
                city = None

            # Дата размещения вакансии
            if i.find('span', {'class': 'vacancy-serp-item__publication-date vacancy-serp-item__publication-date_short'}):
                post_date = i.find('span', {'class': 'vacancy-serp-item__publication-date vacancy-serp-item__publication-date_short'}).text
            else:
                post_date = None

            # Класс вакансии (standard|standard_pro|premium)
            vac_class = i['data-qa'].split('__')[-1]

            print(
                f'Class: {vac_class} \nTitle: {title} \nCompensation: {compensation} \nLink: {href} \nSite: {url} \nEmployer: {empl} \nCity: {city} \nPublic_Date: {post_date}')
            # Обобщающий словарь по вакансии
            dd.update({
                # 'id': count,
                'site': url,
                'vacancy_url': href,
                'vac_class': vac_class,
                'title': title,
                'company': empl,
                'city': city,
                'compensation_min': compensation[0],
                'compensation_max': compensation[1],
                'currency': compensation[-1],
            })

            vac_batch.append(dd)
            if mongo:
                to_mongo(dd)

        #print(dd)
        print(json.dumps(vac_batch, indent=2, ensure_ascii=False, default=str))
        print(f'Кол-во обработанных вакансий: {len(vac_batch)} \nПервая вакансия: {vac_batch[0]["title"]}\n\t{vac_batch[0]["company"]} \nПоследняя вакансия: {vac_batch[-1]["title"]}\n\t{vac_batch[-1]["company"]}')
        return vac_batch

    def request(self, path):
        req = requests.get(self.url + path, headers=self.headers)
        if req.text:
            print(f'Receive Page: {self.url + path}')
            return req.text
        else:
            raise Exception('Text not received')

    def get_positions(self, mongo=False):
        positions = []
        for page in self.list_count:
            positions = positions + self.get_position(page, mongo)
        return positions

    def to_dataframe(self, filename, json_data=''):
        if json_data:
            json = json_data
        else:
            json = self.get_positions()
        dict_df = {
            'site': [x['site'] for x in json],
            'vacancy_url': [x['vacancy_url'] for x in json],
            'vac_class': [x['vac_class'] for x in json],
            'title': [x['title'] for x in json],
            'company': [x['company'] for x in json],
            'city': [x['city'] for x in json],
            'compensation_min': [x['compensation_min'] for x in json],
            'compensation_max': [x['compensation_max'] for x in json],
            'currency': [x['currency'] for x in json],
        }
        df = pd.DataFrame(dict_df)
        df.to_csv(filename, index=False)
        return df


def to_mongo(json):
    vacancies = mongo_db.vac_collection
    if not mongo_db['vacancies'].count_documents({'vacancy_url': json['vacancy_url']}) > 0:
        mongo_db.vacancies.insert_one(json)
        print("=== Новая вакансия: сохранено\n")
    print('=== Вакансия уже содежиться в БД\n')


def find_vacancies(compens):
    # find({ operator: [{valueA: {lt: 123}}, {valueB: {key: 'value'}}]}
    oper = {
        '==': '$eq',
        '!=': '$ne',
        '>': '$gt',
        '>=': '$gte',
        '<': '$lt',
        '=<': '$lte',
        'in': '$in',
        'notin': '$nin',
        'or': '$or',
    }
    vacs = mongo_db['vacancies'].find(
        {oper.get('or'): [
            {'compensation_min': {oper.get('>='): compens}},
            {'compensation_max': {oper.get('>='): compens}}
        ]}
    )
    print(f'Вакансии с компенсацие {compens} и выше:\n {json.dumps([x for x in vacs], default=str, indent=2, ensure_ascii=False)}')




if __name__ == "__main__":
    # === Параметры класса
    url = 'https://hh.ru'
    default_position = 'Data engineer'
    position = default_position
    page_count = 1

    # === Скрапим вакансии и записываем в монгу
    hh = HH(url, position, page_count)
    _list = hh.get_positions(mongo=True)
    # print(_list)
    print(f'=== Кол-во вакансий в БД: {len([ x for x in mongo_db["vacancies"].find({})])}')

    # Поиск вакансий с заработной платой больше введённой суммы
    find_vacancies(300000)

    # === Создаем DataFrame и сохраняем его в файл
    # df_file = f'hh_vacancies_{position.replace(" ", "_")}.csv'
    # hh.to_dataframe(df_file, _list)


