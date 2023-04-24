from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import HanoitimesItem


class hanoitimes(CrawlSpider):
    name = "hanoitimes"
    allowed_domains = ["hanoitimes.vn"]
    start_urls = ["https://hanoitimes.vn/"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://hanoitimes\.vn/.*"),
            callback="parse",
            follow=True,
        )
    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = HanoitimesItem()

        url = response.url

        if response.css('h1.ArticleHeader_headline::text').extract_first() is None:
            return
        title = response.css('h1.ArticleHeader_headline::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('div.StandardArticleBody_body p::text').get(default='').strip()
        # item['summary'] = ""
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.art_content p::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('div.ArticleHeader_date::text').get(default="").strip()
        tag = response.css('div.tag_detail a::text').get(default="").strip()

        item['extra_metadata'] = {'date': date}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
