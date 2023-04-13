import pymongo
from scrapy.dupefilters import BaseDupeFilter


class MyDupeFilter(BaseDupeFilter):
    def __init__(self):
        self.visited_urls = set()
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client['corpus']

    def request_seen(self, request):
        if self.db['news'].find_one({'url': request.url}):
            return True

        if request.url in self.visited_urls:
            return True

        self.visited_urls.add(request.url)
        return False

    def close(self, reason=''):
        self.visited_urls.clear()