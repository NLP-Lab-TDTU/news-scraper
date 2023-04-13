import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import NewsItem


class TuoitreSpider(CrawlSpider):
    name = "tuoitre"
    allowed_domains = ["tuoitre.vn"]
    start_urls = ['https://tuoitre.vn']

    rules = [
        Rule(LinkExtractor(allow=r'^https:\/\/tuoitre\.vn\/.*.htm'), callback='parse_item', follow=True),
    ]

    def parse_item(self, response):
        if response.css('h1.detail-title.article-title::text').extract_first() is None:
            return
        item = NewsItem()
        item['title'] = response.css('h1.detail-title.article-title[data-role="title"]::text').extract_first()
        item['url'] = response.url

        item['summary'] = ''.join(response.css('h2.detail-sapo[data-role="sapo"]::text').extract()).strip()

        content_tag = response.css('div.detail-content.afcbc-body[data-role="content"]')
        p_tags = content_tag.css('p:not(.VCObjectBoxRelatedNewsItemSapo)')
        p_texts = [p.css('::text').extract_first() for p in p_tags]
        item['content'] = '\n\n'.join([p.strip() for p in p_texts if p is not None])
        item['content'] = re.sub(r'\n{3,}', '\n\n', item['content'])

        date = response.css('div.detail-time div[data-role="publishdate"]::text').extract_first().strip()
        item['extra_metadata'] = {'date': date}
        return item