# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class KuaixunPipeline(object):
    def open_spider(self,spider):
        self.client = pymysql.Connect(host='127.0.0.1', port=3306, user="root", password='123', db='news')


    def process_item(self, item, spider):

        title  = item['title']
        content  = item['content']
        sql = 'insert into data values ("%s","%s")'

        self.course = self.client.cursor()

        try:
            self.course.execute(sql,(title,content))
            self.client.commit()
        except:
            self.client.rollback()


    def close_spider(self,spider):
        self.course.close()
        self.client.close()




