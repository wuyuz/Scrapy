# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from redis import Redis

class FirstbloodPipeline(object):
    #设置全局变量，否则无效
    fp = None

    #重写父类的方法
    def open_spider(self,spider):
        print('开始爬虫')
        # 只打开一次文件就行了，不用反复打开，开始爬虫时就会执行
        self.fp = open('qiushibaike.txt','w',encoding='utf-8')

    # 用于接收爬虫文件提交过来的item，然后将其进行任意形式的持久化存储，
    #参数item：就是接收到的item对象,一次接受一个item
    #该方法每接受一个item就会调用一次
    def process_item(self, item, spider):
        author = item['author']
        content = item['content']
        if not author: author = '无'
        self.fp.write(author+":"+content+'\n')

        # 注意pipeline类中写了return item，表示会交给紧接这该类的优先级的管道类处理
        return item

    # 重写父类方法，当爬虫结束后执行
    def close_spider(self,spider):
        print('爬虫结束')
        self.fp.close()


# 自定义存储类，用于数据存储到mysql中
class MysqlPL(object):
    conn = None   #数据库连接
    cursor = None  # 执行sql语句
    def open_spider(self,spider):
        self.conn = pymysql.Connect(host='127.0.0.1',port=3306,user='root',password='123',db='s1',charset='utf8')

    def process_item(self,item,spider):
        author = item['author']
        content = item['content']

        sql = "insert into qiubai values ('%s','%s')"%(author,content)
        self.cursor = self.conn.cursor()  #创建游标

        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()  #回滚

        #仍然返回给下一个管道，当然可以不写
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()

#重点:首先如果你的settings中的ITEM_PIPELINE写了第一种类的优先级最高，但是你在这把那个类删除了，意味着后面的类都拿不到
#item了

class RedisPL(object):
    conn = None

    def open_spider(self,spider):
        self.conn = Redis(host='127.0.0.1',port=6379)
        print(self.conn)

    def process_item(self,item,spider):
        # 注意我们之前说的item是一个类似与字典的数据结构，相对有序字典
        self.conn.lpush('all_data',item)  #每次将item添加到 all_data的列表中



