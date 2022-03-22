# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


import scrapy
import hashlib
from scrapy.utils.python import to_bytes
from scrapy.pipelines.images import ImagesPipeline


class LrmrParserPipeline:
    def process_item(self, item, spider):
        return item


class LrmrPhotosPipeline(ImagesPipeline):

    # def __init__(self):
    #     self.img_size = 'w_1000,h_1000'

    def get_media_requests(self, item, info):
        img_size = 'w_1000,h_1000'
        if item['photos']:
            for img in item['photos']:
                try:
                    img = img.replace('w_82,h_82', img_size)
                    yield scrapy.Request(img)
                except Exception as e:
                    print('Error in LrmrPhotosPipeline:', e)

    def item_completed(self, results, item, info):
        item['photos'] = [x[1] for x in results if x[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):

        try:
            country = item['specifications']['Страна производства']
            collection = item['specifications']['Коллекция']
            color = item['specifications']['Цвет']
            img_path = f'{country}/{collection}/{color}'
        except Exception:
            img_path = 'undefined'

        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()

        return f'{img_path}/{image_guid}.jpg'
