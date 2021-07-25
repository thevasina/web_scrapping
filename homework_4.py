from pymongo import MongoClient
import requests
from lxml.html import fromstring

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'news'
MONGO_COLLECTION = 'news_collection'


def upsert_news(info):
    title_get = info.get('title')
    link_get = info.get('link')
    datetime_get = info.get('datetime')
    source_get = info.get('source')

    key = {'title': title_get}
    data = {'$set':
                {'link': link_get,
                 'datetime': datetime_get,
                 'source': source_get}
            }

    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        vacancies = db[MONGO_COLLECTION]
        vacancies.update_one(key, data, upsert=True)


def get_info_from_lenta():

    url = "https://lenta.ru/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    dom = fromstring(response.text)

    items_xpath = '//div[contains(@class, "main__content")]//div[contains(@class, "item")]' \
                  '//time[contains(@class, "g-time")]/..'

    title_xpath = './text()'
    link_xpath = './@href'
    datetime_xpath = './/@datetime'
    source = url.split('/')[2]

    news = dom.xpath(items_xpath)

    for new in news:
        info = {}
        info['title'] = new.xpath(title_xpath)[0].replace('\xa0', ' ')
        info['link'] = url + new.xpath(link_xpath)[0]
        info['datetime'] = new.xpath(datetime_xpath)
        info['source'] = source

        upsert_news(info)


def get_info_from_yandex():

    url = "https://yandex.ru/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    dom = fromstring(response.text)

    items_xpath = '//div[contains(@class, "mg-grid__col")]/article[contains(@class, "mg-card")]'

    title_xpath = './/h2/text()'
    link_xpath = './/a//@href'
    datetime_xpath = './/span[contains(@class, "mg-card-source__time")]/text()'
    source = './/span[contains(@class, "mg-card-source__source")]//a/text()'

    news = dom.xpath(items_xpath)

    for new in news:
        info = {}
        info['title'] = new.xpath(title_xpath)[0].replace('\xa0', ' ')
        info['link'] = new.xpath(link_xpath)[0]
        info['datetime'] = new.xpath(datetime_xpath)
        info['source'] = new.xpath(source)[0]

        upsert_news(info)


def get_info_from_mail():

    url = "https://news.mail.ru/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    dom = fromstring(response.text)

    base_items_xpath = '//ul[contains(@class, "list list_type_square list_half js-module")]/li'
    new_items_xpath = '//div[contains(@class, "article js-article")]'

    title_xpath = './a//text()'
    link_xpath = './a/@href'
    datetime_xpath = './/span[contains(@class, "note__text")]//@datetime'
    source = './/span[contains(@class, "link__text")]/text()'

    news = dom.xpath(base_items_xpath)

    for new in news:
        info = {}
        info['title'] = new.xpath(title_xpath)[0].replace('\xa0', ' ')
        info['link'] = new.xpath(link_xpath)[0]
        new_url = new.xpath(link_xpath)[0]
        new_response = requests.get(new_url, headers=headers)
        new_dom = fromstring(new_response.text)
        info_for_news = new_dom.xpath(new_items_xpath)
        info['datetime'] = info_for_news[0].xpath(datetime_xpath)[0]
        info['source'] = info_for_news[0].xpath(source)[0]

        upsert_news(info)
