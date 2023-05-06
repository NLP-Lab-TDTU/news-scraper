# import pymongo
import os
from scrapy.dupefilters import BaseDupeFilter


class MyDupeFilter(BaseDupeFilter):
    def __init__(self):
        self.visited_urls = set()
        # self.client = pymongo.MongoClient('localhost', 27017)
        # self.db = self.client['corpus']

    def request_seen(self, request):
        # if self.db['news'].find_one({'url': request.url}):
        #     return True

        url = request.url
        item_id = url.split('/')[-1].split('.')[0]
        if os.path.exists(f'/home/hieunguyen/news-scraper/news/data/{item_id}.json'):
            return True

        if request.url in self.visited_urls:
            return True

        self.visited_urls.add(request.url)
        return False

    def close(self, reason=''):
        self.visited_urls.clear()