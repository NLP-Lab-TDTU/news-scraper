# import pymongo
import hashlib
import os

from scrapy.dupefilters import BaseDupeFilter


class MyDupeFilter(BaseDupeFilter):
    def __init__(self):
        self.visited_urls = set()

    def request_seen(self, request):
        item_id = hashlib.md5(request.url.encode('utf-8')).hexdigest()
        folder = os.getenv('FOLDER')
        my_path = f'./{folder}/{item_id}.json'
        master_path = f'/home/cuong/projects/VietGPT/data/{item_id}.json'
        if os.path.exists(my_path):
            return True

        if request.url in self.visited_urls:
            return True

        self.visited_urls.add(request.url)
        return False

    def close(self, reason=''):
        self.visited_urls.clear()
