# -*- coding: utf-8 -*-
# import requests
import json,time,os
from lxml import etree
from selenium import webdriver
from baike_spdier import BaidubaikeSpider

if __name__=="__main__":
    bkid_list = []
    people_relations_list = []
    if not os.path.exists('baike_append_data.txt'):
        file = open('./baike_data.txt',encoding='utf-8')
        for line in file:
            bkid = json.loads(line)['bkid']
            peopleRelations = json.loads(line)['peoplerelations']
            if len(peopleRelations)>0:
                people_relations_list.append(peopleRelations)
            bkid_list.append(bkid)
    else:
        file = open('./baike_data.txt',encoding='utf-8')
        for line in file:
            bkid = json.loads(line)['bkid']
            peopleRelations = json.loads(line)['peoplerelations']
            if len(peopleRelations)>0:
                people_relations_list.append(peopleRelations)
            bkid_list.append(bkid)
        file = open('./baike_append_data.txt',encoding='utf-8')
        for line in file:
            bkid = json.loads(line)['bkid']
            # 进一步深度采集人物实体关系
            # peopleRelations = json.loads(line)['peoplerelations']
            # if len(peopleRelations)>0:
            #     people_relations_list.append(peopleRelations)
            bkid_list.append(bkid)
    print(len(bkid_list))
    baidubaikeSpider = BaidubaikeSpider()
    for people_relations in people_relations_list:
        for people_relation in people_relations:
            ename = people_relation.split('#')[2]
            baike_url = people_relation.split('#')[3]
            target_bkid = people_relation.split('#')[3].split('?')[0].split('/')[-1]
            if target_bkid not in bkid_list:
                try:
                    baidubaike_data = baidubaikeSpider.baike_request(baike_url)
                    baidubaike_data['baike_url'] = baike_url
                    baidubaike_data['ename'] = ename
                    baidubaike_data['bkid'] = target_bkid
                    # print(json.dumps(baidubaike_data,ensure_ascii=False))
                    baidubaikeSpider.write_file(json.dumps(baidubaike_data,ensure_ascii=False),'baike_append_data')
                except:
                    pass