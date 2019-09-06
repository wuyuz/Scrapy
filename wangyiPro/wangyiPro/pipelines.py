# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from aip import AipNlp
#pip install baidu-aip
import pymysql
import time

APP_ID = '17170467'
API_KEY = 'I9gTHCwucpgxwPUjepnLrpsG'
SECRET_KEY = '7BouOaHfzde2rv7XD7QPWl40gRB0j7GE'



class MysqlPL(object):
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    conn = None
    cursor = None

    def open_spider(self, spider):
        # 提前在数据库中创建news数据库和new表，包含四个字段
        self.conn = pymysql.Connect(host='127.0.0.1', port=3306, user="root", password='123', db='news',)

    def process_item(self, item, spider):
        title = item["title"]
        content = item['content']
        tag = self.client.keyword(title,content)  # 标签
        first_tag = tag.get('items')[0].get('tag')

        time.sleep(1)
        types = self.client.topic(title,content)  # 类型
        content_type = types.get('item').get('lv1_tag_list')[0].get('tag')
        sql = 'insert into new values ("%s","%s","%s","%s")' % (title, content, content_type, first_tag)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)

        except Exception as e:
            self.conn.rollback()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()