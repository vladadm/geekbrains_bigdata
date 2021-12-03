import scrapy
from scrapy.http import HtmlResponse
from lrmr_parser.items import LrmrParserItem
from scrapy.loader import ItemLoader


class LrmrSpider(scrapy.Spider):
    name = 'lrmr'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/catalogue/{query}/?page=1']

    def parse(self, response: HtmlResponse):
        pagination = response.xpath('//div[@data-qa-pagination]//a/@href')
        #
        last_page = pagination[-2]
        print("Last_page:", last_page.extract())
        #
        # next_page = pagination[-1]
        # print("Next_page:", next_page.extract())
        # #
        # if next_page != last_page:
        #     yield response.follow(next_page, callback=self.parse)

        # count_pages =  #int(last_page.extract().split('=')[-1])
        #
        # print("Count pages:", count_pages)
        #
        # for page_number in range(2, count_pages, 1):
        #     print('Parce page:', page_number)
        #     yield response.follow(
        #         f'https://leroymerlin.ru/catalogue/dekorativnye-oboi/?page={page_number}',
        #         callback=self.parse
        #     )

        links = response.xpath('//div[@data-qa-product]/a/@href')
        print(links)
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LrmrParserItem(), response=response)

        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', '//meta[@itemprop="priceCurrency"]/../span/text()')
        loader.add_xpath('specifications', '//div[@class="def-list__group"]')
        loader.add_xpath('photos', "//img[@slot='thumbs']/@src")
        loader.add_value('url', response.url)

        yield loader.load_item()
