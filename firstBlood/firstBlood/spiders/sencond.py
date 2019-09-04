# -*- coding: utf-8 -*-
import scrapy
from firstBlood.items import FirstbloodItem


# class SencondSpider(scrapy.Spider):
#     name = 'sencond'
#     # allowed_domains = ['www.xxx.com']
#     start_urls = ['https://www.qiushibaike.com/text/']
#
#     # 将多个页码对应的数据进行爬取和解析的操作
#     url = 'https://www.qiushibaike.com/text/page/%d/'   #先制定一个通用的url模板
#     #page 第一次调用表示的是用来解析第一页对应页面中的段子内容和作者
#     pageNum = 1
#     def parse(self, response):
#         div_list = response.xpath('//*[@id="content-left"]/div')
#         for div in div_list:
#             author = div.xpath('./div[1]/a[2]/h2/text()').extract_first()
#             content = div.xpath('./a/div/span//text()').extract()
#
#             # 每次循环的数据都要实例化一个item类
#             item = FirstbloodItem()
#             # 类似于字典，item已经封装好了，将各字段封装成字典
#             item['author'] = author
#             item['content'] = ''.join(content)
#
#             #将item提交给管道
#             yield item #item一定是提交给了优先级最高的管道类
#
#         # 递归条件
#         if self.pageNum <= 5:
#             self.pageNum += 1
#             new_url = self.url%self.pageNum
#             #手动请求发送,发起get请求, 使整个函数进行递归，必须要yield，否则响应发送不成功
#             yield scrapy.Request(new_url,callback=self.parse)
#




class SencondSpider(scrapy.Spider):
    name = 'sencond'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.qiushibaike.com/text/','https://www.qiushibaike.com/text/page/2/','https://www.qiushibaike.com/text/page/3/']

    #重写start_requests方法循环自动爬取页面
    def start_requests(self):
        for url in self.start_urls:
            yield  scrapy.Request(url,callback=self.parse)

    pageNum = 1
    def parse(self, response):
        div_list = response.xpath('//*[@id="content-left"]/div')
        for div in div_list:
            author = div.xpath('./div[1]/a[2]/h2/text()').extract_first()
            content = div.xpath('./a/div/span//text()').extract()

            # 每次循环的数据都要实例化一个item类
            item = FirstbloodItem()
            # 类似于字典，item已经封装好了，将各字段封装成字典
            item['author'] = author
            item['content'] = ''.join(content)

            #将item提交给管道
            yield item #item一定是提交给了优先级最高的管道类



