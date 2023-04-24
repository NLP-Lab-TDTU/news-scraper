from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import VirItem


class vir(CrawlSpider):
    name = "vir"
    allowed_domains = ["vir.com.vn"]
    start_urls = ["https://vir.com.vn/"]

    rules = [

        Rule(
            LinkExtractor(allow=r"https://vir\.com\.vn/.*"),
            callback="parse",
            follow=True,
        )

    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = VirItem()

        url = response.url

        if response.css('h1.title-detail::text').extract_first() is None:
            return
        title = response.css('h1.title-detail::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('div.desc-detail::text').get(default='').strip()
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div#__MB_MASTERCMS_EL_3 p::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('span.date-detail::text').get(default="").strip()
        tag = response.css('div.link-content a::text').get(default="").strip()
        item['extra_metadata'] = {'date': date, 'tag': tag}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
