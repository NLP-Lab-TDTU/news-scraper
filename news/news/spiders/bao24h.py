"""
Author: Duong Trong Chi
"""

import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import NewsItem


class Bao24hSpider(CrawlSpider):
    name = "bao24h"
    allowed_domains = ["www.24h.com.vn"]
    start_urls = ["https://www.24h.com.vn/"]

    rules = [
        Rule(LinkExtractor(allow=r"https://www\.24h\.com\.vn/.*.html"), callback='parse_item', follow=True),
    ]

    required_fields = ['title', 'url', 'content']

    def parse_item(self, response):
        if response.css('h1#article_title::text').extract_first() is None:
            return

        item = NewsItem()
        item['title'] = response.css('h1#article_title::text').extract_first().strip()
        item['url'] = response.url

        item['summary'] = ''.join(response.css('h2#article_sapo strong::text').extract()).strip()

        content_tag = response.css('article.cate-24h-foot-arti-deta-info')
        p_tags = content_tag.css('p')
        p_texts = [p.css('::text').extract_first() for p in p_tags]
        item['content'] = '\n\n'.join([p.strip() for p in p_texts if p is not None])
        item['content'] = re.sub(r'\n{3,}', '\n\n', item['content'])

        date = response.css('time.cate-24h-foot-arti-deta-cre-post::text').extract_first().strip()

        item['extra_metadata'] = {'date': date}

        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item