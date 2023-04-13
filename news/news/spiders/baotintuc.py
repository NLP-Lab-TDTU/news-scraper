import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import NewsItem


class BaotintucSpider(CrawlSpider):
    name = "baotintuc"
    allowed_domains = ["baotintuc.vn"]
    start_urls = ["https://baotintuc.vn/"]

    rules = [
        Rule(LinkExtractor(allow=r"^https:\/\/baotintuc\.vn\/.*"), callback="parse_item", follow=True),
    ]

    def parse_item(self, response):
        if response.css('h1.detail-title::text').extract_first() is None:
            return
        item = NewsItem()
        item['title'] = response.css('h1.detail-title::text').extract_first().strip()
        item['url'] = response.url

        item['summary'] = ''.join(response.css('h2.sapo::text').extract()).strip()

        content_tag = response.css('div.contents')
        p_tags = content_tag.css('p')
        p_texts = [p.css('::text').extract_first() for p in p_tags]
        item['content'] = '\n\n'.join([p.strip() for p in p_texts if p is not None])
        item['content'] = re.sub(r'\n{3,}', '\n\n', item['content'])

        date = response.css('div.date span.txt::text').extract_first().strip()
        tag = response.css('div.date h4.cate a strong::text').extract_first()

        item['extra_metadata'] = {'date': date, 'tag': tag}
        return item