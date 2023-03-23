# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class YhocPipeline(object):
    def process_item(self, item, spider):
        # # dump to JSONL file
        if "Content" not in item:
            raise DropItem(f"Item {item} missing required field")
        # line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # self.file.write(line)
        return item
    def close_spider(self, spider):
        # self.file.close()
        pass
    def open_spider(self, spider):
        # self.file = open("data.jsonl", 'a', encoding='utf-8')
        pass