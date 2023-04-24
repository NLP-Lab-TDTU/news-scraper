from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import CucduongbovietnamItem


class vneconomySpider(CrawlSpider):
    name = "cucduongbovietnam"
    allowed_domains = ["drvn.gov.vn"]
    start_urls = ["https://drvn.gov.vn/"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://drvn\.gov\.vn/.*"),
            callback="parse",
            follow=True,
        )

    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = CucduongbovietnamItem()

        url = response.url

        if response.css('header.entry-header h1.entry-title::text').extract_first() is None:
            return
        title = response.css('header.entry-header h1.entry-title::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = ""
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.entry-content p::text,div.entry-content p a::text,div.entry-content li::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('span.entry-time::text').get(default='').strip()
        item['extra_metadata'] = {'date': date}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
