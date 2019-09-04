# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#创建两个item类
class SunproItem(scrapy.Item):
    content = scrapy.Field()
    num = scrapy.Field()


class SunproItem_second(scrapy.Item):
    title = scrapy.Field()
    status = scrapy.Field()
    num = scrapy.Field()
