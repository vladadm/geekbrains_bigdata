# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Identity, Compose, Join
from lxml import html


def process_price(value):
    try:
        print('Input Value:', value)
        value = value.replace(' ', '')
        value = int(value)
    except Exception as e:
        print(e)
    finally:
        return value


def spec_transform(spec_list):
    specifications = {}
    try:
        for item in spec_list:
            item = html.fromstring(item)
            item = item.xpath('.//text()')
            item = [x for x in [x.strip() for x in item] if x != '']
            specifications[item[0]] = item[1]
    except Exception as e:
        print('Error in spec_transform: ', str(e))

    finally:
        return specifications

class LrmrParserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(process_price))
    specifications = scrapy.Field(input_processor=Compose(spec_transform), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
