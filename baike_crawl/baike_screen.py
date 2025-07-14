#encoding=utf-8
import json

file = open('./baike_append_data.txt',encoding='utf-8')
for line in file:
    summary = json.loads(line)['summary']
    if summary !="":
        filea = open('./baike_append_data_new.txt','a',encoding='utf-8')
        filea.write(line)