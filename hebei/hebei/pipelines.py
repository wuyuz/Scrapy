# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class HebeiPipeline(object):
    def open_spider(self,spider):

        self.client = pymysql.Connect(host='127.0.0.1', port=3306, user="root", password='123', db='news')

    def process_item(self, item, spider):
        title = item['title']
        name = item['name']
        time = item['time']
        # print(name,title,time)
        sql = 'insert into data values ("%s","%s","%s")'%(name,title,time)
        self.cusor = self.client.cursor()
        try:
            self.cusor.execute(sql)
            self.client.commit()
        except Exception as e:
            print(e)
            self.cusor.rollback()



    def close_spider(self, spider):
        self.cusor.close()
        self.client.close()