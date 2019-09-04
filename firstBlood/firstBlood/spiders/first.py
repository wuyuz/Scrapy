# -*- coding: utf-8 -*-
import scrapy


class FirstSpider(scrapy.Spider):
    name = 'first'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.baidu.com/','https://www.sogou.com/']

    def parse(self, response):
        print(response.text)
        pass
