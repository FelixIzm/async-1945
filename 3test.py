from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import requests
#from requests.exceptions import Timeout, HTTPError
import json
import random
import time
import threading

from lxml.html import fromstring

#####################################
def getStringHash(id):
    h = hashlib.md5(str(id).encode()+b'db76xdlrtxcxcghn7yusxjcdxsbtq1hnicnaspohh5tzbtgqjixzc5nmhybeh')
    p = h.hexdigest()
    return str(p)
#####################################
def parse_file (name_file):
    dict_ = {}
    f = open(name_file, 'r')
    s = f.read()
    dict_={}
    list_ = s.splitlines()
    for item in list_:
        items = item.split(":")
        dict_[items[0]] = items[1].lstrip()
    return dict_
#####################################
headers = parse_file('header.txt')
session = requests.Session()
#session.trust_env = False
cookies = {}

def get_info(info_url):
    global session, cookies
    res3 = requests.get(info_url, cookies=cookies)
    #time.sleep(1)
    threading.Event().wait(1)
    if(res3.status_code == 200):
        print(res3.status_code)
        return res3.text
    elif(res3.status_code == 307):
        res3 = requests.get(info_url,cookies=cookies)
        if(res3.status_code==503):
            res3 = requests.get(info_url,cookies=cookies)
            if('307/503',res3.status_code!=200):
                print(res3.status_code)
    elif(res3.status_code==503):
        res3 = session.get(info_url,cookies=cookies)
        if(res3.status_code!=200):
            print('503',res3.status_code)
    else:
        #print(res3.status_code,len(res3.text))
        if(res3.status_code!=200):
            print('else',res3.status_code)
    pass
def get_path_image():
    print()
def get_path_info(image_id):
    info_url = 'https://obd-memorial.ru/html/info.htm?id={}'.format(image_id)
    res1 = requests.get(info_url)
    if(res1.status_code==307):
        cookies = {}
        cookies['3fbe47cd30daea60fc16041479413da2']=res1.cookies['3fbe47cd30daea60fc16041479413da2']
        cookies['JSESSIONID']=res1.cookies['JSESSIONID']
        cookies['showimage']='0'
        img_info = 'https://obd-memorial.ru/html/getimageinfo?id={}'.format(image_id)
        response = requests.get(img_info)
        response_dict = json.loads(response.text)
        print('response_dict = '+str(len(response_dict)))
        url_list = []
        for item in response_dict:
            for id in item['mapData'].keys():
                info_url = 'https://obd-memorial.ru/html/info.htm?id='+str(id)
                url_list.append(info_url)
    return url_list, cookies


urls, cookies = get_path_info(85942988)
print('urls = ',len(urls))

'''
with PoolExecutor(max_workers=8) as executor:
   for _ in executor.map(get_info, urls):
       pass
'''