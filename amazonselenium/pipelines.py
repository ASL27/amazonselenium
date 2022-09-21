# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class MongoPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # scrapy通过itemadapter库支持以下类型的item：dictionaries、item object、dataclass object和attrs object
        # self.db[item.collection].insert_one(ItemAdapter(item).asdict())
        # 存在则更新，不存在则新建，
        self.db[item.collection].update_one({
            # 保证 数据 是唯一的
            'images': ItemAdapter(item).get('images')
        }, {
            '$set': ItemAdapter(item)
        }, upsert=True)
        return item



class AmazonseleniumPipeline:
    def process_item(self, item, spider):
        return item
