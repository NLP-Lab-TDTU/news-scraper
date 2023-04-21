from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re


class atgt(CrawlSpider):
    name = "antoangiaothong"
    allowed_domains = ["antoangiaothong.gov.vn"]
    start_urls = ["http://antoangiaothong.gov.vn/"]

    rules = [
        Rule(
            LinkExtractor(allow=[r"/.*"]),
            callback="parse",
            follow=True,
        )

    ]
    custom_settings = {
        'DEPTH_LIMIT': 10
    }

    def parse(self, response):
        url = response.url
        title = response.css('h1.heading_td::text').get(default='').strip()
        if title is None or len(title) == 0 or title == "RSS":
            raise DropItem('Not A PAGE')

        summary = ""
        content = "\n\n".join([text.strip() for text in response.css('div.box__nth_2 p::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        if content is None or len(content) == 0:
            raise DropItem('Not a page')

        date = response.css('span.posted span::text').get(default='').strip()

        yield {
            'title': title,
            'url': url,
            'summary': summary,
            'content': content,
            'extra_metadata': {'date': date}
        }
