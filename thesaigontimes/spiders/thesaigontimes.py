from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re
from ..items import ThesaigontimesItem


class thesaigontimes(CrawlSpider):
    name = "thesaigontimes"
    allowed_domains = ["english.thesaigontimes.vn"]
    start_urls = ["https://english.thesaigontimes.vn/hcmc-updates-first-metro-lines-construction-plan/"]

    rules = [

        Rule(
            LinkExtractor(allow=r"https://english\.thesaigontimes\.vn/.*"),
            callback="parse",
            follow=True,
        )

    ]

    required_fields = ['title', 'url', 'content']

    def parse(self, response):
        item = ThesaigontimesItem()

        url = response.url

        if response.css('h1.tdb-title-text::text').extract_first() is None:
            return
        title = response.css('h1.tdb-title-text::text').get(default='').strip()
        item['title'] = title
        item['url'] = url
        item['summary'] = response.css('div.tdb_single_content h6::text').get(default='').strip()
        # content = response.css('div#content_body p::text').getall()
        content = "\n\n".join([text.strip() for text in response.css(
            'div.tdb_single_content p::text').getall()])
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r'[\xa0\u200b]+', " ", content)
        item['content'] = content

        date = response.css('time.entry-date::text').get(default="").strip()
        tag = response.css('ul.tdb-tags li a::text').get(default="").strip()
        item['extra_metadata'] = {'date': date, 'tag': tag}
        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
