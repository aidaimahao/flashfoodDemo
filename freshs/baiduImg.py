#coding:utf-8

import os
import requests
from urllib import request
from time import sleep

def get_img(keyword,page_size = 30):
    """
    :param keyword: 查询关键字
    :param page_size: 单次查询的条数
    """
    dir_path = "baidu_img\\"+keyword
    os.mkdir(dir_path)
    url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E5%93%88%E5%A3%AB%E5%A5%87&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E5%93%88%E5%A3%AB%E5%A5%87&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=30&rn=30&gsm=1e&1535439331790="

    headers = {
        "Referer": "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%93%88%E5%A3%AB%E5%A5%87&oq=%E5%93%88%E5%A3%AB%E5%A5%87&rsp=-1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }

    parameters = {
        "tn": "resultjson_com",
        "ipn": "rj",
        "ct": "201326592",
        "fp": "result",
        "queryWord": keyword,
        "cl": 2,
        "lm": -1,
        "ie": "utf-8",
        "oe": "utf-8",
        "st": -1,
        "ic": 0,
        "word": keyword,
        "face": 0,
        "istype": 2,
        "nc": 1,
        "pn": "",
        "rn": page_size,
        "gsm": "1e"
    }
    for i in range(1,10):
        parameters["pn"] = i*page_size
        response = requests.get(url = url,headers = headers,params = parameters)
        #requests对于json请求是有自己处理方式的
        content = response.json().get("data")
        # print(img_url)
        # 下载图片需要两个参数
        # 下载图片的地址我们这里有
        # 下载图片的路径
        if content:
            for index,data in enumerate(content):
                print("+++++++++++++++++++++++++++++++++++++++++++")
                img_url = data.get("middleURL")
                name = "page_%s_%s.jpg"%(i,index)
                path = "%s\\%s"%(dir_path,name)
                print(path)
                try:
                    request.urlretrieve(url = img_url,filename = path)
                except Exception as e:
                    print(e)
                else:
                    print("%s is donw"%name)
                print("+++++++++++++++++++++++++++++++++++++++++++")
        sleep(1)

if __name__ == "__main__":
    # keyword = input("please enter your keyword: >>> ")
    # get_img(keyword)
    list = [
        "新鲜水果",
        "海鲜水产",
        "猪牛羊肉",
        "禽类蛋品",
        "速冻食品",
    ]
    for key in list:
        get_img(key)



