# -*- coding: utf-8 -*-
# import requests
import json,time,os,re
from lxml import etree
from selenium import webdriver
class BaidubaikeSpider():
    def __init__(self):
        pass
    def baike_request(self,baike_url):
        baike_html = self.Browser_Rendering(baike_url)
        name = etree.HTML(baike_html).xpath('//h1//text()')[0]
        summary = etree.HTML(baike_html).xpath('//div[@class="lemma-summary J-summary"]//text()')
        summary = ''.join(summary)
        peoplerelationslist = []
        peoplerelations = etree.HTML(baike_html).xpath('//div[@class="lemma-complex-relationship-container"]//div[@class="swiper-wrapper"]/div/a')
        if len(peoplerelations) > 0:
            for number in range(0, len(peoplerelations)):
                peoplerelationsname = peoplerelations[number].xpath('.//div[@class="relationship-name"]/text()')
                peoplerelationspeoplename = peoplerelations[number].xpath('.//div[@class="relationship-lemma-title"]/text()')[0]
                peoplerelationslink = peoplerelations[number].xpath('./@href')
                # peoplerelationsimg = peoplerelations[number].xpath('.//img/@src')
                peoplerelationsname = ''.join(''.join(peoplerelationsname).split())
                peoplerelationslink = 'https://baike.baidu.com' + ''.join(''.join(peoplerelationslink).split())
                # peoplerelationsimg = ''.join(''.join(peoplerelationsimg).split())
                peoplerelation = name + '#' + peoplerelationsname + '#' + peoplerelationspeoplename + '#' + peoplerelationslink
                peoplerelationslist.append(peoplerelation)
        else:
            peoplerelationslist = []
        dictbasic = {}
        basicinfonames = etree.HTML(baike_html).xpath('//div[@class="basic-info J-basic-info cmn-clearfix"]//dt[@class="basicInfo-item name"]')
        basicinfovalues = etree.HTML(baike_html).xpath('//div[@class="basic-info J-basic-info cmn-clearfix"]//dd[@class="basicInfo-item value"]')
        for i in range(0, len(basicinfonames)):
            basicinfoname = basicinfonames[i].xpath('.//text()')
            basicinfovalue = basicinfovalues[i].xpath('.//text()')
            basicinfoname = ''.join(basicinfoname).strip().replace('    ','')
            basicinfovalue = ''.join(basicinfovalue).strip()
            basicinfoname = re.sub(r'\[\d+\]|\(\d+\)', '', basicinfoname)
            basicinfovalue = re.sub(r'\[\d+\]|\(\d+\)', '', basicinfovalue)
            dictbasic[basicinfoname] = basicinfovalue
        baidubaike_data = {}
        baidubaike_data['name'] = name
        baidubaike_data['summary'] = re.sub(r'\[\d+(?:-\d+)?\]', '', summary)
        baidubaike_data['peoplerelations'] = peoplerelationslist
        baidubaike_data['basicinfo'] = dictbasic
        return baidubaike_data
    #浏览器渲染获取百科数据
    def Browser_Rendering(self,url):
        Chrome_options = webdriver.ChromeOptions()
        #根据selenium版本调整参数
        Chrome_options.add_argument('--headless')
        drive = webdriver.Chrome(chrome_options=Chrome_options)
        drive.get(url)
        html = drive.page_source
        drive.quit()
        return html

    # 保存数据到本地
    def write_file(self, text, file_name):
        f = open(file_name + '.txt', mode="a", encoding="UTF-8")
        f.write(text + '\n')
        f.close()
if __name__=="__main__":
    bkid_list = []
    if os.path.exists('baike_data.txt'):
        file = open('./baike_data.txt',encoding='utf-8')
        for line in file:
            bkid = json.loads(line)['bkid']
            bkid_list.append(bkid)
    baidubaikeSpider = BaidubaikeSpider()
    #读取存储百科url数据文件
    file = open('./baike_url_data.txt', encoding='utf-8')
    for line in file:
        baike_data_json = json.loads(line)
        if len(baike_data_json['data'])>0:
            for baike_data in baike_data_json['data']:
                result = baike_data['answer']
                title = baike_data['title']
                for baike_url_data in result:
                    baike_url = baike_url_data['baikeLink']
                    ename = baike_url_data['ename']
                    pic = baike_url_data['img']
                    bkid = baike_url_data['bkid']
                    if bkid not in bkid_list:
                        print(baike_url)
                        try:
                            try:
                                baidubaike_data = baidubaikeSpider.baike_request(baike_url)
                            except:
                                baidubaike_data = baidubaikeSpider.baike_request(baike_url)
                            if baidubaike_data['summary'] == '':
                                time.sleep(3)
                                baidubaike_data = baidubaikeSpider.baike_request(baike_url)
                            baidubaike_data['ename'] = ename
                            baidubaike_data['pic'] = pic
                            baidubaike_data['bkid'] = bkid
                            baidubaike_data['baike_url'] = baike_url
                            print(json.dumps(baidubaike_data,ensure_ascii=False))
                            baidubaikeSpider.write_file(json.dumps(baidubaike_data,ensure_ascii=False),'baike_data')
                        except:
                            pass