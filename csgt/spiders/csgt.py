from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import CsgtItem


class csgt(CrawlSpider):
    name = "csgt"
    allowed_domains = ["www.csgt.vn"]
    start_urls = ["https://www.csgt.vn/"]

    rules = [
        Rule(
            LinkExtractor(allow=r"https://www\.csgt\.vn/.*"),
            callback="parse",
            follow=True,
        )

    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = CsgtItem()

        url = response.url

        if response.css('div.detail_name::text').extract_first() is None:
            return
        title = response.css('div.detail_name::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('div.detail_summarise::text').get(default='').strip()
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.detail_content p::text,div.detail_content p span span::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        if content == '\n\n':
            content = ""
        item['content'] = content

        date = response.css('div.detail_date i::text').get(default='').strip()
        date = "".join(re.findall(r'\d+/\d+/\d+', date))
        item['extra_metadata'] = {'date': date}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
