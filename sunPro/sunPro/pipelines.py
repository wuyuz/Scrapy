# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SunproPipeline(object):
    def process_item(self, item, spider):
        if item.__class__.__name__ == 'SunproItem':
            content = item['content']
            # 执行sql语句，但是发现不能同时存入content以及对应的title、status，我们可以用num标识
            #我们通过编号进行唯一码标识
            num = item['num']
            print(content,num)

        else:
            title = item['title']
            status = item['status']
            num = item['num']
            print(num,title)

        return item
