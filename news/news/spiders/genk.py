"""
Author: Duong Trong Chi
"""

import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import NewsItem

class GenkSpider(CrawlSpider):
    name = "genk"
    allowed_domains = ["genk.vn"]
    start_urls = ["https://genk.vn/"]

    rules = [
        Rule(LinkExtractor(allow=r"https://genk\.vn/.*\.chn"), callback='parse_item', follow=True),
    ]

    required_fields = ['title', 'url', 'content']

    def parse_item(self, response):
        if response.css('h1.kbwc-title span::text').extract_first() is None:
            return

        item = NewsItem()
        item['title'] = response.css('h1.kbwc-title span::text').extract_first()
        item['url'] = response.url

        item['summary'] = ''.join(response.css('h2.knc-sapo::text').extract()).strip()

        content_tag = response.css('div#ContentDetail')
        p_tags = content_tag.css('p:not(.VCObjectBoxRelatedNewsItemSapo)')
        p_texts = [p.css('::text').extract_first() for p in p_tags]
        item['content'] = '\n\n'.join([p.strip() for p in p_texts if p is not None])
        item['content'] = re.sub(r'\n{3,}', '\n\n', item['content'])

        date = response.css('meta[property="og:title"]::attr(content)').extract_first().strip()
        tag = response.css('meta[name="keywords"]::attr(content)').extract_first().strip()

        item['extra_metadata'] = {'date': date, 'tag': tag}

        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item