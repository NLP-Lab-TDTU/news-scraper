from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
import re

class YHocVietNamSpider(CrawlSpider):
    name = "YHocVietNam_spider"
    allowed_domains = ["yhocvietnam.com.vn"]
    start_urls = ["https://yhocvietnam.com.vn/"]

    rules = [
        Rule(LinkExtractor(allow=r'.*', deny=r'author'), follow=True, callback='parse'),
        # Rule(LinkExtractor(deny=r'.*\/author\/.*'))
    ]

    def parse(self, response):

        Title = response.css('.post-title::text').get()
        Url = response.url
        Summary = response.css('.main-content p').getall()[0]
        Content = response.css('.main-content p').getall()[1:-2]
        Tag = response.css('.cats a::text').getall()

        if Content is None or len(Content) == 0 or Title is None:
            raise DropItem('Not a page')

        # lam sach data
        Content = re.sub('<[^>]*>', '', '\n\n'.join(Content)) # Remove all tags
        Content = Content.strip(' ')
        Content = re.sub(r'[ \t]{2,}', '', Content) # Remove all tags
        Content = re.sub(r'\n{3,}', '\n\n', Content) # replace redudance \n\n
        if Title is not None:  
            Title = Title.strip('\n\t\t ')

        if Summary is not None:        
            Summary = Summary.strip('\n\t\r ')
            Summary = re.sub('<[^>]*>', '',Summary) # Remove all tags
            Summary = re.sub(r'\n{3,}', '\n\n', Summary) # replace redudance \n\n
            
        yield {
            'Title': Title,
            'Url': Url,
            'Summary': Summary,
            'Content': Content,
            'extra_metadata':{'Tag': Tag}
        } 



