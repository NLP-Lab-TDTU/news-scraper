# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity

class YhocvietnamItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = scrapy.Field()
    Url = scrapy.Field()
    Summary = scrapy.Field()
    Content = scrapy.Field()
    extra_metadata = scrapy.Field()

class YHocItemloader(ItemLoader):
    default_input_processor = Identity()
    default_output_processor = TakeFirst()

