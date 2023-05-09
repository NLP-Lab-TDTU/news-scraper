# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json

import pymongo
from itemadapter import ItemAdapter


class NewsPipeline:
    def process_item(self, item, spider):
        return item

class MongoPipeline:
    collection_name = 'news'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client['corpus']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item

class WriteFilePipeline:
    def process_item(self, item, spider):
        item_id = item['extra_metadata']['id']
        open(f'/home/cuong/projects/VietGPT/data/{item_id}.json', 'w').write(json.dumps(dict(item), ensure_ascii=False))
        return item