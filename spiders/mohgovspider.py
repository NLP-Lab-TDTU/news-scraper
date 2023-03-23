from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re

class MohgovspiderSpider(CrawlSpider):
    name = "mohgov"
    allowed_domains = ["moh.gov.vn"]
    start_urls = ["https://moh.gov.vn/so-o-trang"]

    rules = [
        Rule(LinkExtractor(allow=r'\/asset_publisher\/'), follow=True, callback='parse'),
        Rule(LinkExtractor(allow=(), deny=r'\/tin-noi-bat\/'), follow=True)
        # Rule()
    ]

    def parse(self, response):

        Title = response.css('h3::text').get()
        Url = response.url
        Summary = response.css('.contentDetail strong::text').get()
        Content = response.css('.journal-content-article h3, .journal-content-article h2 , .journal-content-article p,.journal-content-article h4, .journal-content-article li, .journal-content-article').getall()
        Date =  response.css('.time-post::text').get()
        if Content is None or len(Content) == 0:
            raise DropItem('Not a page')

        # lam sach data
        Content = re.sub('<[^>]*>', '', '\n\n'.join(Content)) # Remove all tags
        Content = Content.strip(' ') # Remove all tags
        Content = re.sub(r'[ \t]{2,}', '', Content) # Remove all tags
        Content = re.sub(r'\n{3,}', '\n\n', Content) # replace redudance \n\n
        if Summary is not None:
            Summary = Summary.strip('\n\t\r ')
            Summary = re.sub('<[^>]*>', '',Summary) # Remove all tags
            Summary = re.sub(r'\n{3,}', '\n\n', Summary) # replace redudance \n\n

        yield {
            'Title': Title,
            'Url': Url,
            'Summary': Summary,
            'Content': Content,
            'extra_metadata':{'Date': Date}
            # 'extra_metadata':{'Tag': Tag}
        }
