from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import EvnexpressItem


class evnexpress(CrawlSpider):
    name = "evnexpress"
    allowed_domains = ["e.vnexpress.net"]
    start_urls = ["https://e.vnexpress.net/"]

    rules = [

        Rule(
            LinkExtractor(allow=r"https://e\.vnexpress\.net/.*"),
            callback="parse",
            follow=True,
        )

    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = EvnexpressItem()

        url = response.url

        if response.css('h1.title_post::text').extract_first() is None:
            return
        title = response.css('h1.title_post::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('span.lead_post_detail::text').get(default='').strip()
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.fck_detail p::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('div.author::text').getall()[-1].strip()
        tag = response.css('h5.tag_item a::text').get(default='').strip()
        item['extra_metadata'] = {'date': date, 'tag':tag}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
