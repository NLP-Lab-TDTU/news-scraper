from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import NewsItem
import requests
import re


class ArticleSpider(CrawlSpider):
    name = 'forbesvn'
    #filter_str = ''.join([chr(i) for i in range(1, 32)])
    allowed_domains = ['forbes.vn']
    start_urls = ['https://forbes.vn/tesla-ghi-nhan-so-luong-xe-ban-giao-cho-khach-trong-quy-1-tang-36']
    
    rules = [
        Rule(LinkExtractor(allow=r'^https:\/\/forbes\.vn\/.*'), callback='parse_item', follow=True),
    ]   
    required_fields = ['title','url','content']

    def f1(self, texts):
        return ''.join([i.strip() for i in texts])

    def clean(self, txt):
        #tmp = txt.translate(str.maketrans('','',ArticleSpider.filter_str))
        txt = re.sub(" +"," ",txt)
        txt = re.sub("\n+",'\n',txt).strip()
        return txt

    def parse_item(self, response):
        try:
            newspaper = NewsItem()
            url = response.url
            newspaper['title'] = response.css("h1.forbes-single__heading-title::text").get().strip()
            if newspaper['title'] is None:
              return
            newspaper['url'] = url
            newspaper['summary'] = response.css('div.forbes-short-description__container>p::text').get().strip()

            body = response.css('div.forbes-single__content>*')
            test = body[-2].css("*::text").get()
            limit = -1
            if re.match(r"^Biên dịch:",test) is not None:
                limit = -2
            newspaper['content'] = " ".join(body[:limit].css("*:not(.wp-element-caption)::text").getall())

            newspaper['extra_metadata'] = \
                    {'tags': response.css('div.forbes-single__tags').css("a::text").getall()}
            newspaper['content'] = self.clean(newspaper['content'])
            return newspaper
        except Exception as e:
            print(e)
    
