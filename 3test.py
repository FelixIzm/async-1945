from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import requests
from requests.exceptions import Timeout, HTTPError
import json
import random
import time
import threading

from lxml.html import fromstring
user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

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
    #cookies['showimage']='0'
    #info_url = 'https://obd-memorial.ru/html/info.htm?id='+str(id)
    res3 = requests.get(info_url, cookies=cookies)
    #time.sleep(1)
    threading.Event().wait(1)
    print(res3.status_code)
    if(res3.status_code == 307):
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

def work(image_id):
    #image_id = 84042290
    info_url = 'https://obd-memorial.ru/html/info.htm?id={}'.format(image_id)
    #print(info_url)
    res1 = requests.get(info_url)

    if(res1.status_code==307):
        cookies = {}
        cookies['3fbe47cd30daea60fc16041479413da2']=res1.cookies['3fbe47cd30daea60fc16041479413da2']
        cookies['JSESSIONID']=res1.cookies['JSESSIONID']
        cookies['showimage']='0'

        #print(cookies)

        img_info = 'https://obd-memorial.ru/html/getimageinfo?id={}'.format(image_id)
        response = requests.get(img_info)
        response_dict = json.loads(response.text)
        print('response_dict = '+str(len(response_dict)))
        url_list = []
        for item in response_dict:
            #print(i, item['id'])
            for id in item['mapData'].keys():
                info_url = 'https://obd-memorial.ru/html/info.htm?id='+str(id)
                #info_url = str(id)
                #print('\t',info_url)
                url_list.append(info_url)
    return url_list, cookies



#file = open('urls.txt','r')
#urls = file.readlines()

urls, cookies = work(85942988)
print('urls = ',len(urls))

with PoolExecutor(max_workers=6) as executor:
   for _ in executor.map(get_info, urls):
       pass