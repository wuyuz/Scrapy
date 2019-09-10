# -*- coding: utf-8 -*-
import scrapy
import re,jsonpath,json
from kuaixun.items import KuaixunItem


class SpidersSpider(scrapy.Spider):
    name = 'spiders'
    # allowed_domains = ['www.xx.com']
    start_urls = ['http://newsapi.eastmoney.com/kuaixun/v1/getlist_103_ajaxResult_50_1_.html']

    #制作通用模板
    url = 'http://newsapi.eastmoney.com/kuaixun/v1/getlist_103_ajaxResult_50_%d_.html'

    # 页码数
    pageNum = 1
    def parse(self, response):
        data_str = response.body.decode('utf-8')
        data = json.loads((data_str[15:]))
        for one in data['LivesList']:
            title = one['title']
            content = re.findall('【(.*?)】(.*)',one['digest'])[-1]
            # print(content)
            item = KuaixunItem()
            item['title'] = title
            item['content'] = content
            # print(title, content)

            yield item










