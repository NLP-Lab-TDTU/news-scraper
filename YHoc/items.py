# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, TakeFirst, Identity
import re

class YhocItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = scrapy.Field()
    Url = scrapy.Field()
    Summary = scrapy.Field()
    Content = scrapy.Field()
    extra_metadata = scrapy.Field()

def filter_Content(Content, loader_context):
    try:
        image_cap = loader_context.get('image_captions',[])
        for i in image_cap:
            Content = Content.replace(i, '')
    except:
        return Content
    else:
        return Content

def replace_newlines(Text):
    return re.sub(r'\n{3,}', '\n\n', Text)

def Extrametadata_date_format(Data):
    Data['Date'] = Data['Date'].strftime('%Y-%m-%d %H:%M:%S')
    return Data

def clease_Summary(Summary):
    if Summary[0] is None:
        return None
    return Summary[0].strip(' \n\r')

class YHocItemloader(ItemLoader):
    default_input_processor = Identity()
    default_output_processor = TakeFirst()
    Summary_in = Compose(clease_Summary)
    Content_in = Compose(TakeFirst(),filter_Content, replace_newlines)
    extra_metadata_in = TakeFirst()
    extra_metadata_out = Compose(TakeFirst(),Extrametadata_date_format)
    
    

    