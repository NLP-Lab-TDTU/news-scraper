import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import NewsItem



class vefpressSpider(CrawlSpider):
    name = 'vfpress'
    allowed_domains = ['vfpress.vn']
    start_urls = ['https://vfpress.vn']

    rules = [
        Rule(LinkExtractor(allow=r'^https:\/\/vfpress\.vn\/.*'), callback='parse_item', follow=True),
    ]

    required_fields = ['title','url','content']
    
    def parse_item(self, response):
        if response.css('h1.entry-title::text').extract_first() is None:
            return

        item = NewsItem()   
        item['title'] = response.css('h1.entry-title::text').extract_first()
        item['url'] = response.url

        # first div tag is the summary  
        try:
            item['summary'] = ''.join(response.css('strong.post-sapo-description')[0].css('::text').extract())
        except IndexError:
            item['summary']  = ''

        content_tag = response.css('div.entry-content')

        p_tags = content_tag.css('p')
        p_texts = [p.css('::text').extract_first() for p in p_tags]
        item['content'] = '\n\n'.join([p.strip() for p in p_texts if p is not None])
        item['content'] = re.sub(r'\n{3,}', '\n\n', item['content'])

        date = response.css('span.posted-on time::text').extract_first()

        item['extra_metadata'] = {'date': date, 'tag': self.get_tags(response)}

        for field in self.required_fields:
            if item[field] is None or item[field] == '':
                return
        return item
            
    def get_tags(self, response):
        tag_elements = response.css('span.category a')
        tags = []
        for tag_element in tag_elements:
            tag = tag_element.css('::text').extract_first()
            if tag is not None:
                tags.append(tag)
        return tags


    