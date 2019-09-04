# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class WangyiproSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


from scrapy.http import HtmlResponse
import time
class WangyiproDownloaderMiddleware(object):

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    #进行响应对象进行拦截,这里的spider就是爬虫文件爬虫类实例化的对象，也就是WangyiSpider类的对象，我们
    # 可以通过spider点出类的属性
    def process_response(self, request, response, spider):

        #1、将所有的响应中的那五个不满足要求的response进行截获，先不return它，进行修正后再返回，
        #因为这五个response（模板）是动态加载的，也就是说我们拿到的页面不是先要的
            # 1、每个响应对象对应唯一一个请求对象
            # 2、如果我们可以定位到五个响应对象的请求对象后，就可以通过该请求对象定位到指定的响应对象
            # 3、可以通过五个板块的url定位请求对象
            # 总结： url --> request --> response


        #2、将找到的五个不满足需求的响应对象进行修正
        #spider.five_model_urls : 通过spider点出五个模块对应的url
        bro = spider.bro
        if request.url in spider.five_model_urls:
            # 如果if条件成立则该response就是五个板块对应的响应对象
            # 这里的response就是HtmlResponse类对象
            bro.get(request.url)
            time.sleep(1)
            page_text = bro.page_source # 包含了动态加载
            new_response = HtmlResponse(
                url=request.url,  # 响应对象对应的请求对象
                body=page_text,  #将selenums 获得的页面数据传入
                encoding='utf-8',
                request=request  #五个模板对应的请求对象
            )

            # 返回新的响应对象，包含着动态加载的新闻数据
            return new_response

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

