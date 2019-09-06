import time
import json
import redis
from selenium import webdriver

# 获取redis连接对象
client = redis.StrictRedis()


driver = webdriver.Chrome(executable_path=r'D:\21期\爬虫 + 数据分析\tools\chromedriver.exe')
driver.get('http://exercise.kingname.info/exercise_login_success')

user = driver.find_element_by_xpath('//input[@name="username"]')
user.clear()
user.send_keys('kingname')

user = driver.find_element_by_xpath('//input[@name="password"]')
user.clear()
user.send_keys('genius')

rember = driver.find_element_by_xpath('//input[@name="rememberme"]')
rember.click()

login = driver.find_element_by_xpath('//button[@class="login"]')
login.click()

time.sleep(2)
cookies = driver.get_cookies()
client.lpush('cookies',json.dumps(cookies))
driver.quit()