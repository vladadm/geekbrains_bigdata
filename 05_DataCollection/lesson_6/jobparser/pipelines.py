# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('mongodb://%s:%s@127.0.0.1' % ('admin', 'admin'))
        self.mongo_base = client.vacancy2611

    def process_item(self, item, spider):
        if spider.name == 'hhru' or 'sjru':
            final_salary = self.process_salary(item['salary'])

            item['min_salary'] = final_salary[0]
            item['max_salary'] = final_salary[1]
            item['currency'] = final_salary[2]
            del item['salary']
        else:
            pass

        self.to_mongo(item, spider.name)

        return

    def process_salary(self, salary):
        vvvv = {
            'min': None,
            'max': None,
            'currency': None,
        }
        print('Sall:', salary)
        if len(salary) > 1:
            salary = self.salary_transform(salary)

            # Определяем валюту
            if len([x for x in salary if 'руб' in x]) > 0:

                if salary[-1] == 'руб.' or 'месяц':
                    salary[-1] = 'RUB'

                salary = [x.replace('руб.', '') for x in salary]

                try:
                    salary.remove('')
                except ValueError:
                    pass
                vvvv['currency'] = 'RUB'

            print('Salll:', salary)

            if len(salary) == 2:
                vvvv['min'] = None
                vvvv['max'] = int(salary[0])

            if 'от' in salary[0] and len(salary) == 3:
                vvvv['min'] = int(salary[1])
                vvvv['max'] = None
                vvvv['currency'] = salary[-1]
                salary.pop(0)

            if 'до' in salary[0] and len(salary) == 3:
                vvvv['min'] = None
                vvvv['max'] = int(salary[1])
                vvvv['currency'] = salary[-1]
                salary.pop(0)

            if 'от' and 'до' in salary:
                salary.remove('от')
                salary.remove('до')

            if len(salary) == 3:
                vvvv['min'] = int(salary[0])
                vvvv['max'] = int(salary[1])
                vvvv['currency'] = salary[-1]

            salary = list(vvvv.values())
            print(f'=== salary final:\n', salary)
        else:
            salary = [None, None, None]
            print("=== salary empty:\n", salary)

        return salary

    def salary_transform(self, _list):
        _list = [x.replace('\xa0', '') for x in _list]

        for item in ['/', '.', '—',  ' на руки', ]:
            try:
                _list.remove(item)
            except ValueError as valerr:
                #print(valerr)
                pass

        _list = ' '.join(_list).split()

        print("Transform_sel:", _list)
        return _list

    def to_mongo(self, item, spider_name):
        collection = self.mongo_base[spider_name]
        if not collection.count_documents({'url': item['url']}) > 0:
            collection.insert_one(item)
            print("=== Новая вакансия: сохранено\n")
        else:
            print('=== Вакансия уже содежиться в БД\n')

        return