from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import NewsItem
import requests
import re


class ArticleSpider(CrawlSpider):
    name = 'nhipcaudautu'
    #filter_str = ''.join([chr(i) for i in range(1, 32)])
    allowed_domains = ['nhipcaudautu.vn']
    start_urls = ['https://nhipcaudautu.vn/kinh-doanh/ngay-174-gia-vang-the-gioi-van-tru-vung-muc-2000-usdoune-3351987/']
    
    rules = [
        Rule(LinkExtractor(allow=r'^https:\/\/nhipcaudautu\.vn\/.*'), callback='parse_item', follow=True),
    ]   
    required_fields = ['title','url','content']

    def f1(self, texts):
        return ''.join([i.strip() for i in texts])

    def clean(self, txt):
        #tmp = txt.translate(str.maketrans('','',ArticleSpider.filter_str))
        txt = re.sub(" +"," ",txt)
        txt = re.sub("\n+",'\n',txt).strip()
        return txt

    def check_get(self, newspaper, required_fields):
        for field in required_fields:
            if newspaper[field] is None or len(newspaper[field]) < 1:
                return False
        return True

    def parse_item(self, response):
        try:
            newspaper = NewsItem()
            newspaper['title'] = response.css('h1.post-detail-title::text')\
                    .get().strip()
            if newspaper['title'] is None:
              return
            newspaper['url'] = response.url
            newspaper['summary'] = response.css('div.post-container')\
                    .css('div.des-small::text').get().strip()
            content = response\
                    .css('div.tdInfo').css("*:not(script)::text").getall()
            newspaper['content'] = " ".join([i.strip() for i in content])
            #newspaper['content'] = self.clean(newspaper['content'])
            newspaper['extra_metadata'] = \
                    {'tags': response.css('div.post-tags>a')\
                    .css('*::text').getall(),\
                    'date': response.css('span.date-post::text')[-1].get().strip()}
            test = self.check_get(newspaper, self.required_fields)
            if test == False:
                return
            return newspaper
        except Exception as e:
            print(e)
            return
    
