from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re


class vneconomySpider(CrawlSpider):
    name = "vneconomy"
    allowed_domains = ["en.vneconomy.vn"]
    start_urls = ["https://en.vneconomy.vn/"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://en\.vneconomy\.vn/.*.htm"),
            callback="parse",
            follow=True,
        ),
    ]

    def parse(self, response):
        url = response.url
        title = response.css('h1.detail__title::text').get(default='').strip()
        if title is None or len(title) == 0 or title == "RSS":
            raise DropItem('Not A PAGE')

        summary = response.css('h2.detail__summary::text').get(default='').strip()

        content = "\n\n".join([text.strip() for text in response.css('div.detail__content *::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content).strip()
        if content is None or len(content) == 0:
            raise DropItem('Not a page')

        date = response.css('div.detail__meta::text').get(default='').strip()

        yield {
            'title': title,
            'url': url,
            'summary': summary,
            'content': content,
            'extra_metadata': {'date': date}
        }
