# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from fbsPro.items import FbsproItem

#继承redis的爬虫类
class FbsSpider(RedisCrawlSpider):
    name = 'fbs'
    # allowed_domains = ['www.xxx.com']

    # start_urls = ['http://www.xxx.com/']
    #不需要start_urls,替换为redis_key,
    #表示的是可被共享调度器中的队列的名称，是用来存储经过调度器中过滤器过滤去重后的数据对象
    redis_key = 'fbsQueue'

    rules = (
        #爬取页码url
        Rule(LinkExtractor(allow=r'type=4&page=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        tr_list = response.xpath('//*[@id="morelist"]/div/table[2]//tr/td/table//tr')
        for tr in tr_list:
            title = tr.xpath('./td[2]/a[2]/@title').extract_first()
            status = tr.xpath('./td[3]/span/text()').extract_first()
            item = FbsproItem()
            item['title'] = title
            item['status'] = status
            yield item
