# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonseleniumItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Mongdb与mysql的表名
    collection = table = 'amazon'
    images = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    star = scrapy.Field()