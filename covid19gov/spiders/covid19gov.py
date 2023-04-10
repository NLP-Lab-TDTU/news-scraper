from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem, IgnoreRequest
import re
import scrapy

class covid19gov(CrawlSpider):
    name = "covid19gov_spider"
    allowed_domains = ["covid19.gov.vn"]
    start_urls = ["https://covid19.gov.vn/timelinelist/1711565/1.htm",
                  "https://covid19.gov.vn/timelinelist/1711566/1.htm",
                  "https://covid19.gov.vn/timelinelist/1711567/1.htm",
                  "https://covid19.gov.vn/timelinelist/1711568/1.htm",
                  "https://covid19.gov.vn/timelinelist/1711569/1.htm",
                  "https://covid19.gov.vn/timelinelist/1711570/1.htm",
                  "https://covid19.gov.vn/timelinelist/1711571/1.htm",
                  "https://covid19.gov.vn/timelinelist/1711572/1.htm",
                  "https://covid19.gov.vn/big-story/cap-nhat-dien-bien-dich-covid-19-moi-nhat-hom-nay-171210901111435028.htm"  
                ]

    rules = [
        # Rule(link_extractor=LinkExtractor(allow=r'[a-zA-Z]\.htm'), follow=True, callback=None),
        Rule(link_extractor=LinkExtractor(allow=r'[0-9]{10,}\.htm', deny=r'big-story'), follow=False, callback='parse'),
        # Rule(link_extractor=LinkExtractor(allow=r'[0-9]+\/[0-9]+\.htm'), follow=True, callback='parse_request'),
        # Rule(LinkExtractor(allow=r'https://covid19.gov.vn/big-story/cap-nhat-dien-bien-dich-covid-19-moi-nhat-hom-nay-171210901111435028.htm'), follow=False, callback='parse_special')
    ]

    def parse(self, response):
        Title = response.css('.detail-title::text').get().strip('\n\t\r ')
        Url = response.url
        Summary = response.css('.detail-sapo::text').get().strip('\n\t\r ')
        Content = response.css('.afcbc-body h3, .afcbc-body h2 , .afcbc-body p, .afcbc-body h4, .afcbc-body li').getall()

        if Content is None or len(Content) == 0:
            raise DropItem('Not a page')

        # lam sach data
        Content = re.sub('<[^>]*>', '', '\n\n'.join(Content)) # Remove all tags
        Content = Content.strip(' ')
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
            # 'extra_metadata':{'Tag': Tag}
        }
        # if not Content:
        next = self.generate_request(response.request.headers.get('Referer'))
        yield scrapy.Request(
            url=next,
            callback=self.access_all_link
        )

    def generate_request(self,response):
        response = response.decode("utf-8")
        x = int(re.findall(r'[0-9]+\.htm$', response)[0].split('.')[0])
        next = re.sub(r'[0-9]+\.htm$','{}.htm'.format(x+1),response)
        return next

    def access_all_link(self,response):
        next_page = response.css('a::attr(href)').getall()
        if next_page:
            yield from response.follow_all(next_page, callback=self.parse)
