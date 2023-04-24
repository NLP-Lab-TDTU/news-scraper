from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import DangcongsanItem


class dangcongsan(CrawlSpider):
    name = "dangcongsan"
    allowed_domains = ["dangcongsan.vn"]
    start_urls = ["https://dangcongsan.vn/"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://dangcongsan\.vn/.*"),
            callback="parse",
            follow=True,
        )
    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = DangcongsanItem()

        url = response.url

        if response.css('h1.post-title::text').extract_first() is None:
            return
        title = response.css('h1.post-title::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('div.post-summary::text').get(default='').replace("(ĐCSVN)", "").replace('-',
                                                                                                                '').replace(
            "\n", "").strip()
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.post-content div p::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('div.lbPublishedDate::text').get(default='').strip()
        item['extra_metadata'] = {'date': date}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
