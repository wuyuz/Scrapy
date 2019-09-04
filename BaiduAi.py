from aip import AipNlp
#pip install baidu-aip

""" 你的 APPID AK SK """
APP_ID = '17170467'
API_KEY = 'I9gTHCwucpgxwPUjepnLrpsG'
SECRET_KEY = '7BouOaHfzde2rv7XD7QPWl40gRB0j7GE'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


title = "iphone手机出现“白苹果”原因及解决办法，用苹果手机的可以看下"

content = "如果下面的方法还是没有解决你的问题建议来我们门店看下成都市锦江区红星路三段99号银石广场24层01室。"

""" 调用文章标签 """
w_dic = client.keyword(title, content)
print(w_dic)

tage = client.topic(title, content);
print(tage)