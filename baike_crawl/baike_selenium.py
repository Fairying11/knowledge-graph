#coding=utf-8
from lxml import etree
from selenium import webdriver
Chrome_options = webdriver.ChromeOptions()
Chrome_options.add_argument('--headless')
drive = webdriver.Chrome(chrome_options=Chrome_options)
drive.get('https://baike.baidu.com/item/%E7%A7%A6%E5%A7%8B%E7%9A%87/6164')
html = drive.page_source
h1 = etree.HTML(html).xpath('//h1//text()')[0]
#打印标题
print(h1)
drive.quit()



