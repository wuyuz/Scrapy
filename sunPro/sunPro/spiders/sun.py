# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from sunPro.items import SunproItem,SunproItem_second

#实现深度爬取
class SunSpider(CrawlSpider):
    name = 'sun'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=']

    #连接提取器：http://wz.sun0769.com/index.php/question/report?page=，但是这个规则写的时候太多符号需要转义，所以我们想简化哈
    #简化版本：r'report\?page=\d+', 即提取规则
    link = LinkExtractor(allow=r'type=4&page=\d+')   # 提取页码连接

    #详情页：http://wz.sun0769.com/html/question/201909/427019.shtml
    #简化版本：r'question/\d+/\d+\.shtml'
    link_detail = LinkExtractor(allow=r'question/\d+/\d+\.shtml')  #提取详情页url

    #规则解析器
    #作用：获取连接提取器取到的连接，然后对其进行请求发送，根据指定规则对请求到的页面源码数据进行数据解析
    rules = (
        #实例化一个Rule对象, 这里的follow如果是False，那么只加载起始页的下方的页码连接，如果是True则可以获取每一页的下方的页码url
        #且可自动去重，也就是说所有的页码都会获取到
        Rule(link, callback='parse_item', follow=True),  # 匹配到每一页url并获得response后，调用parse_item解析函数，获得每个tr

        #匹配每一tr对应的response，然后调用回调函数解析正文内容
        Rule(link_detail,callback='parse_detail',follow=False)  # 不需要检测每个详情页的页码，但是一般页匹配不到提取规则
    )

    def parse_item(self, response):
        tr_list = response.xpath('//*[@id="morelist"]/div/table[2]//tr/td/table//tr')
        for tr in tr_list:
            title = tr.xpath('./td[2]/a[2]/@title').extract_first()
            status = tr.xpath('./td[3]/span/text()').extract_first()
            num = tr.xpath('./td[1]/text()').extract_first()

            # 使用item 记录每个二级页面的新闻标签
            item = SunproItem_second()
            item['title'] = title
            item['status'] = status
            item['num'] = num
            yield  item



    # 注意：之前我们做深度爬取的时候，通过meta传递item，可以使每条跨页面数据共用一个item，但是现在由于Rule规则
    #作用，是我们不能使用meta传递参数，因为之前使scrap.Request类中的回调和meta元数据，但这里的Rule显然没有那种功能，

    #解决办法：各自存储一个item，同过唯一键进行连接绑定存储
    def parse_detail(self,response):
        # 不能出现tbody，不然匹配不到content数据
        content = response.xpath('/html/body/div[9]/table[2]//tr[1]//text()').extract()
        content = ''.join(content)
        num = response.xpath('/html/body/div[9]/table[1]//tr/td[2]/span[2]/text()').extract_first()
        if num:
            num = num.split(':')[-1]
            # 使用item，记录正文
            item = SunproItem()
            item['num'] = num
            item['content'] = content
            yield  item






