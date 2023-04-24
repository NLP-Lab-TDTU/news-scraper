from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import VietnambreakingnewsItem


class vietnambreakingnews(CrawlSpider):
    name = "vietnambreakingnews"
    allowed_domains = ["www.vietnambreakingnews.com"]
    start_urls = ["https://www.vietnambreakingnews.com"]

    rules = [

        Rule(
            LinkExtractor(allow=r"https://www\.vietnambreakingnews\.com/.*/.*"),
            callback="parse",
            follow=True,
        )

    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = VietnambreakingnewsItem()

        url = response.url

        if response.css('h1.jeg_post_title::text').extract_first() is None:
            return
        title = response.css('h1.jeg_post_title::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        # item['summary'] = response.css('div.desc-detail::text').get(default='').strip()
        item['summary'] = ""
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.entry-content p::text,div.entry-content h2::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('div.jeg_meta_date a::text').get(default="").strip()
        tag = response.css('div.jeg_post_tags a::text').get(default="").strip()
        item['extra_metadata'] = {'date': date, 'tag': tag}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
