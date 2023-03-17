# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewspaperspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    summary = scrapy.Field()
    content = scrapy.Field()
    extra_metadata = scrapy.Field()
