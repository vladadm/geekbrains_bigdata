from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lrmr_parser.spiders.lrmr import LrmrSpider
from lrmr_parser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    query = 'dekorativnye-oboi'

    process.crawl(LrmrSpider, query=query)
    process.start()
