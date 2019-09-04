# -*- coding: utf-8 -*-
import scrapy
from movie.items import MovieItem

# 单页爬取
# class MoviesSpider(scrapy.Spider):
#     name = 'movies'
#     # allowed_domains = ['www.xxx.com']
#     start_urls = ['https://www.4567tv.tv/frim/index1.html']
#
#     def parse(self, response):
#         li_list = response.xpath('/html/body/div[1]/div/div/div/div[2]/ul/li')
#         for li in li_list:
#             title = li.xpath('./div[1]/a/@title').extract_first()
#             detail_url ='https://www.4567tv.tv' + li.xpath('./div[1]/a/@href').extract_first()
#
#             # 此时我们可以拿到item了，但是我们不能在这就直接item赋值了额，因为我们还要获取详情页的数据
#             item = MovieItem()
#             item['title'] = title
#
#             #进行请求传参，将item进行传递,因为是将item放在请求中传递，所以叫请求传参,meta参数是一个字典，该字典
#             #可以传递给callback指定的回调函数
#             yield scrapy.Request(detail_url,callback=self.parse_detail,meta={'item':item})
#
#
#
#     def parse_detail(self,response):
#         # item接受的就是我们传递过来的item
#         item = response.meta['item']
#         desc = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[5]/span[2]/text()').extract_first()
#         item['desc'] = desc

        # yield item


#多页爬取,之后我们会学习CrawlSpider可以全栈爬取
class MoviesSpider(scrapy.Spider):
    name = 'movies'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.4567tv.tv/frim/index1.html']
    url = 'https://www.4567tv.tv/frim/index1-%d.html'
    pageNum = 1

    def parse(self, response):
        li_list = response.xpath('/html/body/div[1]/div/div/div/div[2]/ul/li')
        for li in li_list:
            title = li.xpath('./div[1]/a/@title').extract_first()
            detail_url ='https://www.4567tv.tv' + li.xpath('./div[1]/a/@href').extract_first()

            # 此时我们可以拿到item了，但是我们不能在这就直接item赋值了额，因为我们还要获取详情页的数据
            item = MovieItem()
            item['title'] = title

            #进行请求传参，将item进行传递,因为是将item放在请求中传递，所以叫请求传参,meta参数是一个字典，该字典
            #可以传递给callback指定的回调函数
            yield scrapy.Request(detail_url,callback=self.parse_detail,meta={'item':item})

        if self.pageNum < 5:
            self.pageNum += 1
            new_url = self.url % self.pageNum

            # 递归，对其他页面进行爬取
            yield  scrapy.Request(new_url, callback=self.parse)



    def parse_detail(self,response):
        # item接受的就是我们传递过来的item
        item = response.meta['item']
        desc = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[5]/span[2]/text()').extract_first()
        item['desc'] = desc
        yield item