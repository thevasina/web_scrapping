from urllib.parse import quote_plus

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lerya import settings
from lerya.spiders.products import ProductsSpider

if __name__ == "__main__":
    query = input("Введите категорию товара:")
    custom_settings = Settings()
    custom_settings.setmodule(settings)

    process = CrawlerProcess(settings=custom_settings)
    process.crawl(ProductsSpider, query=query)
    process.start()
