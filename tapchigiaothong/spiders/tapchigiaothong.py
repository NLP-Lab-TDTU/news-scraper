from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import TapchigiaothongItem


class vneconomySpider(CrawlSpider):
    name = "tapchigiaothong"
    allowed_domains = ["tapchigiaothong.vn"]
    start_urls = ["https://tapchigiaothong.vn/"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://tapchigiaothong\.vn/.*"),
            callback="parse",
            follow=True,
        )

    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = TapchigiaothongItem()

        url = response.url

        if response.css('h1.detail-title::text').extract_first() is None:
            return
        title = response.css('h1.detail-title::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('h2.detail-sapo::text').get().strip()
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.detail-content p::text,div.detail-content p span::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('div.detail-time div.left span::text').get(default='').strip()
        item['extra_metadata'] = {'date': date}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
