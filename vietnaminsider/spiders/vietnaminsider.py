from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import VietnaminsiderItem


class vietnaminsider(CrawlSpider):
    name = "vietnaminsider"
    allowed_domains = ["vietnaminsider.vn"]
    start_urls = ["https://vietnaminsider.vn/"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://vietnaminsider\.vn/.*"),
            callback="parse",
            follow=True,
        )
    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = VietnaminsiderItem()

        url = response.url

        if response.css('h1.post-title::text').extract_first() is None:
            return
        title = response.css('h1.post-title::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('h2.penci-psub-title::text').get(default='').strip()
        # item['summary'] = ""
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.inner-post-entry p::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('time.entry-date::text').get(default="").strip()
        item['extra_metadata'] = {'date': date}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
