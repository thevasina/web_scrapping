# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import os
from urllib.parse import urlparse

import scrapy
from dotenv import dotenv_values
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class LeryaImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["images"]:
            for img_link in item["images"]:
                try:
                    yield scrapy.Request(img_link)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        print("item_completed")
        print()
        if results:
            item["img_info"] = [x[1] for x in results if x[0]]
        if item["images"]:
            del item["images"]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        filename = os.path.basename(urlparse(request.url).path)
        dir_suffix = filename.split('.')[0].split('_')[0]
        return 'files/' + dir_suffix + '/' + filename


class LeryaPipeline:

    def __init__(self):
        self.mongo_client = None
        self.products = None

    def process_item(self, item, spider):
        self.insert_products(item)
        # print("item")
        return item

    def insert_products(self, product):
        doc_id = hashlib.md5(product['url'].encode('utf-8')).hexdigest()
        self.products.replace_one({"_id": doc_id}, product, upsert=True)

    def open_spider(self, spider):
        print("init connect to Db....")
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        CONFIG_PATH = os.path.join(ROOT_DIR, '.env')
        config = dotenv_values(CONFIG_PATH)
        uri = config.get('mongo_uri')
        self.mongo_client = MongoClient(uri)
        self.products = self.mongo_client.get_default_database()['products']

    def close_spider(self, spider):
        self.mongo_client.close()
        print("Db connect close")
