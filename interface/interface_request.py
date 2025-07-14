#encoding=utf-8
import json

import requests
if __name__ == "__main__":

    # url = 'http://127.0.0.1:5000/star/attribute'
    # # url = 'http://192.168.1.106:5000/star/attribute'
    # data = {"keyword":"刘德华"}
    # headers = {
    #     'Content-Type': 'application/json;charset=UTF-8'
    # }
    # response = requests.post(url, json=data, headers=headers)
    # print(json.dumps(json.loads(response.text),ensure_ascii=False))

    url = 'http://127.0.0.1:5001/stare/relationship'

    data = {"keyword":"刘德华"}
    headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }
    response = requests.post(url, json=data, headers=headers)
    print(json.dumps(json.loads(response.text),ensure_ascii=False))


    # url = 'http://127.0.0.1:5000/person/刘德华'
    # content = requests.get(url).text
    # print(content)