#coding=utf-8
import requests,json
#当前时间抓包第一页测试请求地址：
#https://opendata.baidu.com/api.php?resource_id=28266&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=%E5%90%8D%E4%BA%BA%E5%90%8D%E5%AD%97&sort_key=&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn=0
#url中pn=后面跟的是页数，采集时需要翻页请求
def get_baike_url():
    # for page in range(0,1341*12,12):
    for page in range(0, 101 * 12, 12):
        print(page)
        url = 'https://opendata.baidu.com/api.php?resource_id=28266&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=%E5%90%8D%E4%BA%BA%E5%90%8D%E5%AD%97&sort_key=&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn=' + str(page) + '&rn=12'
        content = requests.get(url).text
        print(content)
        write_file(content)
#保存数据到本地
def write_file(line):
    f = open("baike_url_data.txt", mode="a", encoding="UTF-8")
    f.write(line+'\n')
    f.close()
if __name__=="__main__":
    get_baike_url()