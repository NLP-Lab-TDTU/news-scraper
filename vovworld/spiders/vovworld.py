from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import VovworldItem


class vovworld(CrawlSpider):
    name = "vovworld"
    allowed_domains = ["vovworld.vn"]
    start_urls = ["https://vovworld.vn/"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://vovworld\.vn/en-US/.*"),
            callback="parse",
            follow=True,
        )
    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = VovworldItem()

        url = response.url

        if response.css('header.article__header h1::text').extract_first() is None:
            return
        title = response.css('header.article__header h1::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('div.article__sapo div::text').get(default='').replace('(VOVWORLD)', "").replace(
            '-', "").strip()
        # item['summary'] = ""
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.article__body p::text, div.article__body p strong::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('div.article__meta time::text').get(default="").strip()
        item['extra_metadata'] = {'date': date}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
