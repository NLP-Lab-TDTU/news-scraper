from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import DtinewsItem


class dtinews(CrawlSpider):
    name = "dtinews"
    # allowed_domains = ["dtinews.vn/en/"]
    start_urls = ["http://dtinews.vn/en/index.html"]

    rules = [
        Rule(
            LinkExtractor(allow=r"http://dtinews\.vn/en/.*"),
            callback="parse",
            follow=True,
        )
    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = DtinewsItem()

        url = response.url

        if response.css('div.name_article::text').extract_first() is None:
            return
        title = response.css('div.name_article::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        # item['summary'] = response.css('div.desc-detail::text').get(default='').strip()
        item['summary'] = ""
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.content_article span span::text, div.content_article div span::text, div.content_article p span::text, div.content_article span::text, div.content_article p::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('span#__MB_ARTICLE_TIME::text').get(default="").strip()
        item['extra_metadata'] = {'date': date}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
