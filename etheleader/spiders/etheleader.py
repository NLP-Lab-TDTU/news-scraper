from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import EtheleaderItem


class etheleader(CrawlSpider):
    name = "etheleader"
    allowed_domains = ["e.theleader.vn"]
    start_urls = ["https://e.theleader.vn/"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://e\.theleader\.vn/.*"),
            callback="parse",
            follow=True,
        )
    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = EtheleaderItem()

        url = response.url

        if response.css('h1.news-title::text').extract_first() is None:
            return
        title = response.css('h1.news-title::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('h2.sapo::text').get(default='').strip()
        # item['summary'] = ""
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.news-detail-body-wrapper p::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content
        tag = response.css('div.news-detail-tags a::text').extract_first()
        date = response.css('div.publish-date::text').get(default="").replace('-', '').strip()
        item['extra_metadata'] = {'date': date, 'tag': tag}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
