# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


#原有的，不用
# class ImgproPipeline(object):
#     def process_item(self, item, spider):
#         return item

from scrapy.pipelines.images import ImagesPipeline
import scrapy

#注意这个类名如果更改，用自己的mingz，相应的配置文件也要改变，所以这里我直接使用它原名
class ImgproPipeline(ImagesPipeline):

    #重写继承类的方法,对某一个媒体资源进行请求发送
    #item就是接受到的spider提交过来的item
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['src'])


     # 制定媒体数据存储的名称，在settings.py中配置IMAGEs_STORE
    def file_path(self, request, response=None, info=None):
        name = request.url.split('/')[-1]
        print(name)
        return name

    # 在图片储存好后，交给下一个待执行的管道了，return item
    def item_completed(self, results, item, info):
        return item