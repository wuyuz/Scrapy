# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://exercise.kingname.info/exercise_login_success']

    link = LinkExtractor(allow=r'type=4&page=\d+')

    link_detail = LinkExtractor(allow=r'question/\d+/\d+\.shtml')

    rules = (
        Rule(link, callback='parse_item', follow=True),

        Rule(link_detail, callback='parse_detail', follow=False)
    )

    def parse(self, response):
        print(response.body.decode())
