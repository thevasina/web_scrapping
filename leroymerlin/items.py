# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Compose, MapCompose


def clean_price(price):
    return float(price)


def prepare_params(params):
    it = map(lambda item: item.strip(),params)
    return dict(zip(it, it))


class LeryaItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    img_info = scrapy.Field()
    params = scrapy.Field(input_processor=Compose(prepare_params))
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clean_price), output_processor=TakeFirst())

