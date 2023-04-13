"""
Author: Duong Trong Chi
"""

import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import NewsItem


class NhanlucnganhluatSpider(CrawlSpider):
    name = "nhanlucnganhluat"
    allowed_domains = ["nhanlucnganhluat.vn"]
    start_urls = ["https://nhanlucnganhluat.vn/tin-tuc.html"]

    rules = [
        Rule(LinkExtractor(allow=r'^https:\/\/nhanlucnganhluat\.vn\/tin-tuc\/.*.html'), callback='parse_item', follow=True),
    ]

    required_fields = ['title', 'url', 'content']

    def parse_item(self, response):
        if response.css('div.col-chi-tiet-tin h1::text').extract_first() is None:
            return

        item = NewsItem()
        item['title'] = response.css('div.col-chi-tiet-tin h1::text').extract_first()
        item['url'] = response.url

        item['summary'] = ''.join(response.css('div.td-tt-noi-dung .font-weight-bold p::text').extract()).strip()

        content_tag = response.css('div.td-tt-noi-dung')

        # remove first p tag
        p_tags = content_tag.css('p')
        p_tags.pop(0)
        p_texts = [p.css('::text').extract_first() for p in p_tags]
        item['content'] = '\n\n'.join([p.strip() for p in p_texts if p is not None])
        item['content'] = re.sub(r'\n{3,}', '\n\n', item['content'])

        date = response.css('div.col-chi-tiet-tin time::text').extract_first().strip()

        item['extra_metadata'] = {'date': date}

        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item