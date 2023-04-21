from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import BaogiaothongItem


class baogiaothong(CrawlSpider):
    name = "baogiaothong"
    allowed_domains = ["www.baogiaothong.vn"]
    start_urls = ["https://www.baogiaothong.vn/luat-giao-thong-duong-bo-2019-channel362/"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://www\.baogiaothong\.vn/.*"),
            callback="parse",
            follow=True,
        )
    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = BaogiaothongItem()

        url = response.url

        if response.css('div.postTit::text').extract_first() is None:
            return
        title = response.css('div.postTit::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('div.descArt::text').get().strip()
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.bodyArt p::text,div.bodyArt p a::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('div.dateArt::text').get(default='').strip()
        item['extra_metadata'] = {'date': date}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
