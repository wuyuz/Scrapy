import requests
import random,re

#UA伪装
from lxml import etree

headers = {
    'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
    'Cookie':'_qddamta_2852155767=4-0; Hm_lpvt_94bfa5b89a33cebfead2f88d38657023=1567769302; Hm_lpvt_63d8823bd78e78665043c516ae5b1514=1567769302; _qddagsx_02095bad0b=5b10f670f189576be11c7a486709ffd468e397833d0587e5c8f4b669a71310df10c8ce832c7d552547e4e5515f88cd44a5791cf82fb5c2da11331b365c1879e5e4c34fa796bdcee6dfe323f46a5b5214688dd78498a8f89a7db8eeeffa7353844e6ce8018e3b8be6363d29621f28273af76d6baaf1f39a8b16c033a82e9c4a5d'
    }

#使用session来保存cooike，注意向同一个网址发送请求时使用session会自动保存cookie，之后发送请求就用session就可以了
# session = requests.Session()

url = 'https://www.fjggfw.gov.cn/Website/AjaxHandler/BuilderHandler.ashx'

def page(num):
    url_data = {
        'OPtype': 'GetListNew',
        'pageNo': num,
        'pageSize': '10',
        'proArea': '-1',
        'category': 'GCJS',
        'announcementType': '5',
        'ProType': '-1',
        'xmlx': '-1',
        'projectName': '',
        'TopTime': '2019-06-07 00:00:00',
        'EndTime': '2019-09-05 23:59:59',
        'rrr': random.random(), #此为随机数，可有可无
    }



    #必须携带cookie，且注意在headers中必须大写，且必须提交数据，否则无法获得数据,获得后反序列化
    page_response = requests.post(url=url,headers=headers,data=url_data).json()
    for item in page_response.get('data'):
        print(item)
        #公告类型
        title = item.get('TITLE')
        if title == '中标结果公告':
            ID = item.get('M_ID')
            GGTYPE = item.get('GGTYPE')

            #调用二级网页
            detial_page(ID,GGTYPE)

def detial_page(ID,GGTYPE):

    params = {
        'OPtype': 'GetGGInfoPC',
        # 传入的还是int类型
        'ID': int(ID),
        'GGTYPE': GGTYPE,
        'url': 'AjaxHandler / BuilderHandler.ashx',
    }

    response = requests.get(url,params=params,headers=headers).json()

    #各种类型
    tender_status = response.get('node')
    for temp in tender_status:
        if temp.get('TITLE') == '中标结果公告':
            time = temp.get('TM')
            num = temp.get('NUM')
            all_html = response.get('data')[int(num)]
            # tree = etree.HTML(all_html)
            # 有问题？？？？？？？？？？？
            # zhongbiao = tree.xpath('.//text()')
            print(all_html)
            ret = re.findall(r'中标供应商为：</span></span><span style=";font-family:宋体;font-size:19px"><span style="font-family:宋体">(?P<company>\w+)</span',all_html,re.S)
            print(ret)



page(2)