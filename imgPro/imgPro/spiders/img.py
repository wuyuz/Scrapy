# -*- coding: utf-8 -*-
import scrapy
from imgPro.items import ImgproItem

class ImgSpider(scrapy.Spider):
    name = 'img'
    # allowed_domains = ['www.xxx.com']
    #分析url的页码是有规律的，从81开始
    start_urls = ['http://www.521609.com/daxuemeinv/']

    #url模板
    url = 'http://www.521609.com/daxuemeinv/list8%d.html'
    pageNum = 1
    def parse(self, response):
        li_list = response.xpath('//*[@id="content"]/div[2]/div[2]/ul/li')
        for li in li_list:
            img_src = 'http://www.521609.com'+li.xpath('./a[1]/img/@src').extract_first()
            # scrapy已经为我们建立好了imgpipeline类

            item= ImgproItem()
            item['src'] = img_src
            # 将图片的地址传给管道，当然我们可以自己使用response.body来接受byte类型，然后给item
            yield item

        if self.pageNum <=3:
            self.pageNum += 1
            new_url = self.url%self.pageNum

            yield  scrapy.Request(new_url,callback=self.parse)
