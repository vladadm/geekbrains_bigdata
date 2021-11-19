#!python3
# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
from pprint import pprint
import re

from pymongo import MongoClient as mg_cli

# Задание
# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB
# и реализовать функцию, которая будет добавлять только новые вакансии/продукты в вашу базу.

# 2. Для тех, кто выполнил задание с Росконтролем - напишите запрос
# для поиска продуктов с рейтингом не ниже введенного или качеством не ниже введенного
# (то есть цифра вводится одна, а запрос проверяет оба поля)

mongo_username = 'admin'
mongo_password = 'admin'
mongo_client = mg_cli('mongodb://%s:%s@127.0.0.1' % (mongo_username, mongo_password))
# Указатель на базу данных, может быть множество
mongo_db = mongo_client['products']


class Roscontrol:
    def __init__(self, url, page_count):
        self.page_count = range(0, page_count)
        self.url = url
        self.headers = {
            'Content-Type' : 'text/html; charset=utf-8',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
        }

    def request(self, path):
        req = requests.get(self.url + path, headers=self.headers)
        # print(json.dumps(dict(req.headers), indent=2))
        if req.text:
            print(f'Receive Page: {self.url + path}')
            return req.text
        else:
            raise Exception('Text not received')

    def goods(self, pages, to_dataframe=False, mongo=False):
        print(f'Запрошено страниц: {pages}')
        goods = []
        path = '/category/produkti/myasnie_produkti/polukopchenaya-i-vareno-kopchenaya-kolbasa/'
        pages = range(1, pages + 1)
        for page in pages:
            item = self.products_page(path + f'?page={str(page)}')
            # print(item)
            goods = goods + item
            # goods
            print(len(goods))
        if to_dataframe:
            dict_df = {
                'title': [x['title'] for x in goods],
                'security': [x['security'] for x in goods],
                'nature': [x['nature'] for x in goods],
                'nutritional_value': [x['nutritional_value'] for x in goods],
                'quality': [x['quality'] for x in goods],
                'rate': [x['rate'] for x in goods],
                'site': [x['site'] for x in goods],
                'page': [x['page'] for x in goods],
            }
            goods = pd.DataFrame(dict_df)

        if mongo:
            for product in goods:
                to_mongo(product)

        return goods

    def products_page(self, path):

        dom = bs(self.request(path), 'html.parser')
        catalog = dom.find('div', {'class': 'wrap-testlab-view wrap-container-view testlab-view-typecolumn'})
        grid = catalog.find('div', {'class': 'grid-row'}, recursive=False)
        items = grid.findAll('div', {
            'class': 'wrap-product-catalog__item grid-padding grid-column-4 grid-column-large-6 grid-column-middle-12 grid-column-small-12 grid-left js-product__item'
            }
        )
        _items = []
        # max_pages = dom.findAll('span')
        # max_pages = [x for x in dom.findAll('a', {'href': re.compile(r'.*page=.*')})]
        # print(max_pages)
        for item in items:
            _item = {
                'title': item.find('img')['alt'].strip(),
                # 'rate': None,
                # 'params': {
                #     'security': None,
                #     'nutritional_value': None,
                #     'nature': None,
                #     'quality': None
                # },
                'site': self.url,
                'page': self.url + item.find('a', {'class': 'block-product-catalog__item js-activate-rate util-hover-shadow clear'})['href']
            }
            params = {}
            params_val = [int(x['data-width']) for x in item.findAll('i')]
            if item.find('div', {'class': re.compile(r'rate.*')}):
                _item['rate'] = item.find('div', {'class': re.compile(r'rate.*')}).text.strip()
            if item.find('div', {'class': 'product-no-recommended'}):
                _item['rate'] = -1
                params_val = [-1, -1, -1, -1]

            if item.find('div', {'class': 'product-rating_notest'}):
                _item['rate'] = 0
                params_val = [-0, -0, -0, -0]

            params['security'], params['nutritional_value'], params['nature'], params['quality'] = params_val
            _item.update(params)
            print(params)
            print(_item)

            _items.append(_item)
        return _items


def to_mongo(json):
    products = mongo_db.products_collection
    if not mongo_db['products'].find({'title': json['title']}).count() > 0:
        mongo_db.products.insert_one(json)
        print("=== Новый товар: сохранено\n")
    print('=== Товар уже содежиться в БД\n')


def find_quality_goods(value):
    # find({ operator: [{valueA: {lt: 123}}, {valueB: {key: 'value'}}]}
    oper = {
        '==': '$eq',
        '!=': '$ne',
        '>': '$gt',
        '=>': '$gte',
        '<': '$lt',
        '<=': '$lte',
        'in': '$in',
        'notin': '$nin',
        'or': '$or',
    }
    goods = mongo_db['products'].find(
        {oper.get('or'): [
            {'rate': {oper.get('=>'): value}},
            {'quality': {oper.get('=>'): value}}
        ]}
    )
    print(f'Вакансии с компенсацие {value} и выше:\n {json.dumps([x for x in goods], default=str, indent=2, ensure_ascii=False)}')


if __name__ == "__main__":
    # === Параметры класса
    #url = 'http://Росконтроль.рф' #  закончился срок оренды домена на nic
    url = 'https://roscontrol.com'
    page_count = 4

    # === Скрапим rаталог продуктов
    rc = Roscontrol(url, page_count)
    req = rc.request('/category/produkti/myasnie_produkti/polukopchenaya-i-vareno-kopchenaya-kolbasa/')

    # === Скрапим продукты и записываем в mongoDB
    df = rc.goods(page_count, mongo=True)

    # === Ищем проукты по рейтингу и качеству
    find_quality_goods(60)

