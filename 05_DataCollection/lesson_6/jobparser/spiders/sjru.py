import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = [
        'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4'
    ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class, 'f-test-link-Dalshe')]/@href").get()
        print('Next_page:', next_page)

        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[contains(@class, 'f-test-vacancy-item')]//a[@target='_blank'][1]/@href").getall()

        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        print('Name:', name)

        salary = response.xpath("//h1/../span//text()").getall()
        print('Sal:', salary)
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
