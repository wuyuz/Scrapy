# -*- coding: utf-8 -*-
import scrapy
from HeBei.items import HebeiItem

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    # allowed_domains = ['www.xx.com']
    # 起始网址
    start_urls = ['http://www.hebpr.gov.cn/hbjyzx/jydt/001002/001002002/001002002003/jyxxList.html']

    #模板url
    url = 'http://www.hebpr.gov.cn/hbjyzx/jydt/001002/001002002/001002002003/%d.html'
    pageNum = 1

    # 解析函数，用于解析本网页li标签
    def parse(self, response):
        li_list = response.xpath('//*[@id="content_001002002003"]/li')
        for li in li_list:
            title = li.xpath('./div/a/text()').extract_first()
            # 解析出二级页面的url
            detail_url = 'http://www.hebpr.gov.cn/'+li.xpath('./div/a/@href').extract_first()
            item = HebeiItem()
            item['title'] = title
            yield scrapy.Request(detail_url,callback=self.parse_detail,meta={'item':item})

        if self.pageNum<20:
            self.pageNum += 1
            new_url = self.url%self.pageNum

            yield scrapy.Request(new_url,callback=self.parse)

    def parse_detail(self,response):
        item = response.meta['item']
        name = response.xpath('/html/body/div[3]/div[2]/div/div[2]/div/table//tr[3]/td[2]/p//text() | /html/body/div[3]/div[2]/div/div[2]/div/table/tbody/tr[6]/td[2]/p/span[1]//text() | /html/body/div[3]/div[2]/div/div[2]/div/table/tbody/tr[3]/td/table//tr[3]/td[3]/div//text() | /html/body/div[3]/div[2]/div/div[2]/div/table[1]//tr[3]/td[3]/text()').extract()
        time = response.xpath('/html/body/div[3]/div[2]/div/div[2]/div/table//tr[11]/td[2]/p//text() | /html/body/div[3]/div[2]/div/div[2]/div/table/tbody/tr[10]/td[2]/p/span[1]//text() | /html/body/div[3]/div[2]/div/div[2]/div/table/tbody/tr[2]/td/table//tr[5]/td[1]//text() | /html/body/div[3]/div[2]/div/div[1]/div[1]/text()').extract()
        name = ''.join(name)
        item['name'] = name
        time = ''.join(time)
        item['time'] = time


        yield item



