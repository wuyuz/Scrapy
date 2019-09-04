# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from wangyiPro.items import WangyiproItem

class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    # allowed_domains = ['wwww.xxx.com']
    start_urls = ['https://news.163.com/']
    five_model_urls = []
    # 创建浏览器对象
    bro = webdriver.Chrome(executable_path=r'D:\21期\爬虫 + 数据分析\tools\chromedriver.exe')


    # 用来解析五个板块对应的url，然后对其进行手动发送发送
    def parse(self, response):
        # 找出所需模块对应的li标签索引
        model_index = [3,4,6,7,8]
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        for index in model_index:
            # 五个板块的li标签,取出url
            li = li_list[index]
            model_url = li.xpath('./a/@href').extract_first()

            self.five_model_urls.append(model_url)
            # 对每一个板块的url进行手动请求发送
            yield scrapy.Request(model_url,callback=self.parse_model)


    # 解析每个板块页面中的新闻标题和新闻详情页的url
    # 问题：response中并没有包含每个板块中动态加载出的新闻数据，也就是说这个response是不满足需求的响应
    # 解决： 在中间件中，对不满足要求的response进行重新修正或重新加载
    def parse_model(self,response):
        # 通过中间件中使用selenium处理后每个板块已经获得了动态加载的页面数据后
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div/div/ul/li/div/div')
        for div in div_list:
            title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()
            if detail_url:
                item = WangyiproItem()
                item['title'] = title

                # 对详情页发起请求解析出新闻内容,再定义一个回调函数提取新闻内容,将item传递给下一个需要的解析函数
                yield scrapy.Request(detail_url,callback=self.parse_new_content,meta={'item':item})


    #解析新闻内容
    def parse_new_content(self,response):
        content = response.xpath('//*[@id="endText"]//text()').extract()
        content = ''.join(content)

        item = response.meta['item']
        item['content'] = content

        yield item


    #重写父类的关闭函数，所有操作的最后执行
    def closed(self,spider):
        self.bro.quit()


