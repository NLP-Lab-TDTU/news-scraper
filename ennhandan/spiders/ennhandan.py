from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import EnnhandanItem


class ennhandan(CrawlSpider):
    name = "ennhandan"
    allowed_domains = ["en.nhandan.vn"]
    start_urls = ["https://en.nhandan.vn/"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://en\.nhandan\.vn/.*"),
            callback="parse",
            follow=True,
        )
    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = EnnhandanItem()

        url = response.url

        if response.css('h1.article__title::text').extract_first() is None:
            return
        title = response.css('h1.article__title::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('div.article__sapo::text').get(default='').strip()
        # item['summary'] = ""
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.article__body p::text, div.article__body p strong::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('div.article__meta time.time::text').get(default="").strip()
        item['extra_metadata'] = {'date': date}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
