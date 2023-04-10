from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from YHoc.items import YhocItem, YHocItemloader
import newspaper

class SuckhoedoisongSpider(CrawlSpider):
    name = "SucKhoeDoiSong_spider"
    allowed_domains = ["suckhoedoisong.vn"]
    start_urls = ["https://suckhoedoisong.vn/"]

    rules = [
        # đường link thể loại
        Rule(link_extractor=LinkExtractor(allow=r'[a-zA-Z]\.htm'), follow=True, callback=None),
        # Rule(link_extractor=LinkExtractor(allow=r'chu-de'), follow=True, callback=None),
        # đường link bài báo
        Rule(link_extractor=LinkExtractor(allow=r'[0-9]{10,}\.htm'), follow=True, callback='parse')
    ]


    def parse(self, response):

        image_captions = response.css(".PhotoCMS_Caption p::text").getall()

        url = response.url
        article = newspaper.Article(url, language = 'vi')
        article.download()
        article.parse()
        
        Title = article.title
        Content = article.text
        Date = article.publish_date
        Summary = response.css('h2.detail-sapo::text').get() if response.css('h2.detail-sapo::text').get() else 'NaN'
        Tag = response.css('.detail-tag-list a::text').getall()

        loader = YHocItemloader(item=YhocItem())
        loader.add_value('Title', Title)
        loader.add_value('Url', url)
        loader.add_value('Summary', Summary)
        loader.add_value('Content', Content)
        loader.add_value('extra_metadata', {'Tag': Tag, 'Date': Date})
        loader.context['image_captions'] = image_captions
        yield loader.load_item()