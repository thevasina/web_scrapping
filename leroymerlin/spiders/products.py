import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from lerya.items import LeryaItem


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://leroymerlin.ru/search/?q={query}"]

    def parse(self, response, **kwargs):
        links = response.xpath('''//div[contains(@class,"phytpj4_plp largeCard")]/a/@href''').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_item)

        next_page = response.xpath('''//a[contains(@data-qa-pagination-item,"right")]/@href''').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=LeryaItem(), response=response)
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('images', '//div[contains(@class, "detailed-view-inner")]//img/@src') #picturesWrapper
        loader.add_xpath('params',
                         '//div[contains(@class, "def-list__group")]/dt/text() | '
                         '//div[contains(@class, "def-list__group")]/dd/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('price', '(//meta[@itemprop="price"]/@content)[1]')

        yield loader.load_item()
