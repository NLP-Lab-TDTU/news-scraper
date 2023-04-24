from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import KinhtenongthonItem


class baogiaothong(CrawlSpider):
    name = "kinhtenongthon"
    allowed_domains = ["kinhtenongthon.vn"]
    start_urls = ["https://kinhtenongthon.vn/Tranh-so-trach-nhiem-va-tieu-cuc-trong-mua-sam-thuoc-vat-tu-y-te-post55930.html"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://kinhtenongthon\.vn/.*"),
            callback="parse",
            follow=True,
        )
    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = KinhtenongthonItem()

        url = response.url

        if response.css('div.title_news h1::text').extract_first() is None:
            return
        title = response.css('div.title_news h1::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('div.box_details_news h3.sapo p::text').get(default='').strip()
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.detainew p::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('div.block_timer::text').get(default='').replace("\r", "").replace("\n", "").strip()
        tag = response.css('a.tag_item::text').get(default='').strip()
        item['extra_metadata'] = {'date': date, 'tag': tag}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
