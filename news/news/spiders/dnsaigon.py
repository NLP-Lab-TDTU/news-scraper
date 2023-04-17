from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import NewsItem
import requests
import re


class ArticleSpider(CrawlSpider):
    name = 'doanhnhansaigon'
    filter_str = ''.join([chr(i) for i in range(1, 32)])
    allowed_domains = ['doanhnhansaigon.vn']
    start_urls = ['https://doanhnhansaigon.vn/goc-nha-quan-tri/doanh-nghiep-tang-luong-cap-xe-de-giu-nguoi-lam-1116705.html']
    
    rules = [
        Rule(LinkExtractor(allow=r'^https:\/\/doanhnhansaigon\.vn\/.*'), callback='parse_item', follow=True),
    ]
    
    required_fields = ['title','url','content']

    def f1(self, texts):
        return ''.join([i.strip() for i in texts])

    def clean(self, txt):
        #tmp = txt.translate(str.maketrans('','',ArticleSpider.filter_str))
        txt = txt.replace(" +"," ").strip()
        return txt

    def parse_item(self, response):
        try:
            newspaper = NewsItem()
            url = response.url
            newspaper['title'] = response.css("h1::text").extract_first().strip()
            if newspaper['title'] is None:
              return
            newspaper['url'] = url
            newspaper['summary'] = response.css('h2.description::text').get().strip()
            newspaper['content'] = ' '.join(\
                    response.css('article.fck_detail>*:not(.box_see_more)::text').getall())
            newspaper['extra_metadata'] = \
                    {'tags': response.css('div.inner-tags').css("a::text").getall()\
                    ,'date': response.css('span.time::text').get()}
            newspaper['content'] = self.clean(newspaper['content'])
            return newspaper
        except Exception as e:
            print(e)
    
