from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import GiaothongvietnamItem


class giaothongvietnam(CrawlSpider):
    name = "giaothongvietnam"
    allowed_domains = ["giaothongvietnam.vn"]
    start_urls = [
        "https://giaothongvietnam.vn/ca%cc%89nh-bao-chieu-hack-chia-khoa-thong-minh-o-to-bang-email-gui-qua-dien-thoai/"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://giaothongvietnam\.vn/.*"),
            callback="parse",
            follow=True,
        )

    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = GiaothongvietnamItem()

        url = response.url

        if response.css('h1.entry-title::text').extract_first() is None:
            return
        title = response.css('h1.entry-title::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        # item['summary'] = response.css('div.detail_summarise::text').get(default='').strip()
        item['summary'] = ""
        # content = response.css('div#content_body p::text').getall()
        content = response.css(
            'div.td-post-content p::text,div.td-post-content p strong::text,div.td-post-content p a::text, div.td-post-content h2::text').getall()
        stop = -1
        for i in range(len(content)):
            if "Tin cùng chuyên mục" in content[i]:
                stop = i
                break
        content = content[:stop]
        content = '\n\n'.join([text.strip() for text in content])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        if content == '\n\n':
            content = ""
        item['content'] = content

        date = response.css('span.td-post-date time::text').get(default='').strip()
        tag = response.css('ul.td-tags li a::text').get(default='').strip()
        item['extra_metadata'] = {'date': date, 'tag': tag}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
