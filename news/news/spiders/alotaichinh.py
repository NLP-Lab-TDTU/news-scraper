from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import NewsItem
import requests
import re



class ArticleSpider(CrawlSpider):
    filter_str = ''.join([chr(i) for i in range(1, 32)])
    name = 'alotaichinh'
    allowed_domains = ['alotaichinh.vn']
    start_urls = ['https://alotaichinh.vn/can-tien-gap-phai-lam-sao/']
    
    rules = [
        Rule(LinkExtractor(allow=r'^https:\/\/alotaichinh\.vn\/.*'), callback='parse_item', follow=True),
    ]

    required_fields = ['title','content','url']
    
    def f1(self, texts):
        return ''.join([i.strip() for i in texts])

    def parse_item(self, response):
        try:
            newspaper = NewsItem()
            url = response.url 
            newspaper['title'] = response.css('h1.entry-title::text').get().strip()
            if newspaper['title'] is None:
                return
            newspaper['summary'] = "".join(response.css('div.entry-content>p:first-child').css('*::text').getall())    
            newspaper['content'] = "".join(response.css('div.entry-content>p:not(:first-child)').css('*::text').getall())
            newspaper['url'] = response.url
            newspaper['extra_metadata'] = {'tags':response.css('ul#crumbs>li>a::text')[1:].getall()}
            newspaper['content'] = self.clean(newspaper['content'])
            newspaper['summary'] = self.clean(newspaper['summary'])
            return newspaper
        except Exception as e:
            print(e)
            return
    
    def clean(self,sentence):
        tmp = sentence.translate(str.maketrans('','',ArticleSpider.filter_str))
        sentence = tmp.replace(" +"," ").strip()
        return sentence
