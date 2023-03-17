from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tuoitre.items import NewspaperspiderItem
import requests
from bs4 import BeautifulSoup
import re


def getPage(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, 'html.parser')


def get_content(url):
    bs = getPage(url)
    div_normal = bs.find('div', {'class': 'detail-content afcbc-body'})
    p_tags = div_normal.find_all('p', class_=lambda x: x != 'VCObjectBoxRelatedNewsItemSapo')
    content = '\n\n'.join([p.text for p in p_tags if p.text.strip() != ''])
    return content


def get_summary(url):
    bs = getPage(url)
    summary = bs.find('h2', {'class': 'detail-sapo'})
    return summary


class ArticleSpider(CrawlSpider):
    name = 'articleItems'
    allowed_domains = ['tuoitre.vn']
    start_urls = ['https://tuoitre.vn/mua-tiem-rua-xe-khi-22-tuoi-co-gai-kiem-duoc-hang-ti-moi-nam-ma-khong-can-lam-viec-20230316102945773.htm']
    rules = [
        Rule(LinkExtractor(allow=r'^https:\/\/tuoitre\.vn\/.*'), callback='parse_item', follow=True),
    ]
    
    def f1(self, texts):
        return ''.join([i.strip() for i in texts])

    def parse_item(self, response):
        try:
            newspaper = NewspaperspiderItem()
            newspaper['title'] = response.css('h1::text').extract_first()
            newspaper['url'] = response.url
            newspaper['summary'] = self.f1(response.xpath('//h2[@class="detail-sapo"]/text()').extract())
            text = get_content(response.url)
            newspaper['content'] = re.sub(r'\n{3,}', '\n\n', text)
            date = str(response.xpath('//div[@class="detail-time"]//div[@data-role="publishdate"]/text()').get()).strip()
            newspaper['extra_metadata'] = {'date': date}
            return newspaper
        except:
            pass

    



    

        