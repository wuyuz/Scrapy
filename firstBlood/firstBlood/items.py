# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FirstbloodItem(scrapy.Item):
    #Field可以将其理解成一个万能的数据类型，可以存任意数据类型，Field不能写死，只能用万能的
    author = scrapy.Field()
    content = scrapy.Field()

