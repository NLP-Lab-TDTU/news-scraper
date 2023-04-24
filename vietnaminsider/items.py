# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VietnaminsiderItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    summary = scrapy.Field()
    content = scrapy.Field()
    extra_metadata = scrapy.Field()
    pass
