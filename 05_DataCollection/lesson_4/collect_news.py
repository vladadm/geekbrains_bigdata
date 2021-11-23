#!python3
# -*- coding: utf-8 -*-

import requests
from lxml import html
from pprint import pprint
from datetime import datetime
from pymongo import MongoClient

mongo_username = 'admin'
mongo_password = 'admin'
mongo_client = MongoClient('mongodb://%s:%s@127.0.0.1' % (mongo_username, mongo_password))
# Указатель на базу данных, может быть множество
mongo_db = mongo_client['hot_news']

NEWS_json = {
    'published_time': '',
    'published_date': '',
    'title': '',
    'source': '',
    'href': '',
}

stat = {
    'saved': 0,
    'unsaved': 0,
}


def get_dom(url):
    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    data = requests.get(url, headers=headers)
    print(data.url)
    if 'showcaptcha' in data.url:
        print(data.url)
        raise Exception(f'Сайт {data.url.split("/")[2]} требует капчу!')
    dom = html.fromstring(data.text)
    # print(real_url)
    return [data.url, dom]


def lenta_news():
    print('=== Топ новости (lenta.ru)')
    url = 'https://lenta.ru'

    dom = get_dom(url)[1]
    top_block_news = dom.xpath("//section[@class='row b-top7-for-main js-top-seven']")[0]
    top_news = top_block_news.xpath(".//div[contains(@class, 'item')]")

    for n in top_news:
        _n = {}

        _n['title'] = n.xpath(".//a/text()")[0].replace('\xa0', ' ')
        href = n.xpath(".//a/@href")[0]
        if href.startswith('http'):
            _n['source'] = href.split('/')[2]
            _n['href'] = href
        else:
            _n['source'] = url.split('/')[2]
            _n['href'] = url + n.xpath(".//a/@href")[0]

        date = n.xpath(".//a/time/@datetime")[0].strip()
        _n['published_date'], _n['published_time'] = date_convert(date, url)
        print(_n)
        to_mongo(_n)

    print('=== Главные новости (lenta.ru)')
    url = 'https://lenta.ru'
    dom = get_dom(url)[1]
    main_block_news = dom.xpath("//div[@class='b-yellow-box__wrap']")[0]
    main_news = main_block_news.xpath(".//div[@class='item']")
    for n in main_news:
        _n = {}
        _n['title'] = n.xpath(".//a/text()")[0].replace('\xa0', ' ')
        _n['href'] = url + n.xpath(".//a/@href")[0]
        _n['source'] = url.split('/')[2]
        _url, news_dom = get_dom(_n['href'])
        # print(_n['href'])
        # print(_url)
        if _url != _n['href']:
            _n['href'] = _url
            _n['source'] = _url.split('/')[2]
            _n['published'] = None
        else:
            date = news_dom.xpath("//div[@class='b-topic__info']/time/text()")[0].strip()
            _n['published_date'], _n['published_time'] = date_convert(date, url)

        print(_n)
        to_mongo(_n)


def mail_news():
    print('=== Топ новости (news.mail.ru)')
    url = 'https://news.mail.ru'
    dom = get_dom(url)[1]
    day_news = dom.xpath("//table[@class='daynews__inner']")[0]
    _day_news = day_news.xpath(".//a[contains(@class, 'photo photo_')]")
    _top_news = dom.xpath("//ul[@data-module='TrackBlocks']/li[@class='list__item']")

    for n in _day_news:
        _n = {}
        _n['title'] = n.xpath(".//span[contains(@class, 'photo__title photo__title')]/text()")[0].replace('\xa0', ' ')
        _n['href'] = n.xpath("../a[contains(@class, 'photo photo_')]/@href")[0]
        _n['source'] = url.split('/')[2]

        _url, news_dom = get_dom(_n['href'])
        if _url != _n['href']:
            _n['href'] = _url
            _n['source'] = _url.split('/')[2]
            _n['published'] = None
        else:
            date = news_dom.xpath(".//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0].strip()
            _n['published_date'], _n['published_time'] = date_convert(date, url)

        print(_n)
        to_mongo(_n)

    print("=== Главные новости (news.mail.ru)")
    for n in _top_news:
        _n = {}
        _n['title'] = n.xpath("a[@class='list__text']/text()")[0].replace('\xa0', ' ')
        _n['href'] = n.xpath("a[@class='list__text']/@href")[0]
        _n['source'] = url.split('/')[2]

        _url, news_dom = get_dom(_n['href'])
        if _url != _n['href']:
            _n['href'] = _url
            _n['source'] = _url.split('/')[2]
            _n['published'] = None
        else:
            date = news_dom.xpath(".//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0].strip()
            _n['published_date'], _n['published_time'] = date_convert(date, url)

        print(_n)
        to_mongo(_n)


def yandex_news():
    print('=== Топ новости (yandex.ru/news)')
    url = 'http://yandex.ru/news/'
    _url, dom = get_dom(url)

    #day_news = dom.xpath("//div[contains(@class, 'news-top-flexible-stories news-app__top')]//a[@class='mg-card__link']")
    day_news = dom.xpath("//div[contains(@class, 'news-top-flexible-stories news-app__top')]//div[contains(@class,'mg-grid__col mg-grid__col_xs')]")

    for n in day_news:
        _n = {}
        _n['titel'] = n.xpath(".//h2[@class='mg-card__title']/text()")[0].replace('\xa0', ' ')
        _n['href'] = n.xpath(".//a[@class='mg-card__link']/@href")[0]
        _n['published'] = n.xpath(".//span[@class='mg-card-source__time']/text()")[0]
        news_page = get_dom(_n['href'])[1]
        source = news_page.xpath("//a[@class='mg-story__title-link']/@href")
        _n['source'] = source.split('/')[2]

        print(_n)


def date_convert(date, portal):
    months = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'ноября': '11',
        'декабря': '12',
    }

    for x in months.items():
        date = date.replace(x[0], x[1])

    if portal == 'https://lenta.ru':
        date = datetime.strptime(date, '%H:%M, %d %m %Y')
    if portal == 'https://news.mail.ru':
        date = datetime.fromisoformat(date)
    if portal == 'http://yandex.ru/news/':
        pass

    # '01:10, 23 11 2021'
    date = date.strftime('%d.%m.%Y %H:%M')
    return date.split(" ")


def to_mongo(json):
    '''
    Функция записи данных в БД
    :param json:
    :return:
    '''


    if not mongo_db['hot_news'].count_documents({'href': json['href']}) > 0:
        mongo_db['hot_news'].insert_one(json)
        print("=== Новая новость записана в БД\n")
        stat['saved'] += 1
    else:
        print('=== Новость уже содежиться в БД\n')
        stat['unsaved'] += 1






if __name__ == "__main__":
    lenta_news()
    mail_news()
    try:
        yandex_news()
    except Exception as exc:
        print(exc)
    print(f'Добавлено новых новостей в БД: {stat["saved"]}')