"""
Author: Duong Trong Chi
"""

import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import NewsItem


class LuatvietnamSpider(CrawlSpider):
    name = "luatvietnam"
    allowed_domains = ["luatvietnam.vn"]
    start_urls = ["https://luatvietnam.vn"]

    rules = [
        Rule(LinkExtractor(allow=r'https:\/\/luatvietnam\.vn\/.*\.html'), callback='parse_item', follow=True),
    ]

    required_fields = ['title', 'url', 'content']

    def parse_item(self, response):
        if response.css('h1.the-article-title::text').extract_first() is None:
            return

        item = NewsItem()
        item['title'] = response.css('h1.the-article-title::text').extract_first()
        item['url'] = response.url

        # first div tag is the summary
        try:
            item['summary'] = ''.join(response.css('div#article-content div')[0].css('::text').extract()).strip()
        except IndexError:
            return

        content_tag = response.css('div#newsIndex')

        p_tags = content_tag.css('p')
        p_texts = [p.css('::text').extract_first() for p in p_tags]
        item['content'] = '\n\n'.join([p.strip() for p in p_texts if p is not None])
        item['content'] = re.sub(r'\n{3,}', '\n\n', item['content'])

        date = response.css('div.date-publish span::text').extract_first().strip()

        item['extra_metadata'] = {'date': date}

        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item