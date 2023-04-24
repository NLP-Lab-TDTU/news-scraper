from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import VietnamlifeItem


class vietnamlife(CrawlSpider):
    name = "vietnamlife"
    allowed_domains = ["vietnamlife.tuoitrenews.vn"]
    start_urls = ["https://vietnamlife.tuoitrenews.vn/"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://vietnamlife\.tuoitrenews\.vn/.*"),
            callback="parse",
            follow=True,
        )
    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = VietnamlifeItem()

        url = response.url

        if response.css('article.art-header h1::text').extract_first() is None:
            return
        title = response.css('article.art-header h1::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('div.content-body p strong::text').get(default='').strip()
        # item['summary'] = ""
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.content-body p::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('div.date::text').get(default="").strip()
        item['extra_metadata'] = {'date': date}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
