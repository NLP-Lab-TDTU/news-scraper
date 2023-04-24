from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import MoitruongItem


class moitruong(CrawlSpider):
    name = "moitruong"
    allowed_domains = ["moitruong.net.vn"]
    start_urls = ["https://moitruong.net.vn/"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://moitruong\.net\.vn/.*"),
            callback="parse",
            follow=True,
        )
    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = MoitruongItem()

        url = response.url

        if response.css('h1.c-detail-head__title::text').extract_first() is None:
            return
        title = response.css('h1.c-detail-head__title::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('p.desc::text').get(default='').strip()
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.content-main-normal p::text,div.content-main-normal p a::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('span.c-detail-head__time::text').get(default='').strip()
        item['extra_metadata'] = {'date': date}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
