from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re


class vneconomySpider(CrawlSpider):
    name = "tuoitrenews"
    allowed_domains = ["tuoitrenews.vn"]
    start_urls = ["https://tuoitrenews.vn/"]

    rules = [
        Rule(
            LinkExtractor(allow=[r"/news/.*"], deny=[r"/news/video/.*"]),
            callback="parse",
            follow=True,
        )

    ]
    custom_settings = {
        'DEPTH_LIMIT': 10
    }

    def parse(self, response):
        url = response.url
        title = response.css('article.art-header h1::text').get(default='').strip()
        if title is None or len(title) == 0 or title == "RSS":
            raise DropItem('Not A PAGE')

        summary = response.css('div#content-body p strong::text').get(default='').strip()
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css('div#content-body p::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        if content is None or len(content) == 0:
            raise DropItem('Not a page')

        date = response.css('article.art-header div.date::text').get(default='').strip()

        yield {
            'title': title,
            'url': url,
            'summary': summary,
            'content': content,
            'extra_metadata': {'date': date}
        }
