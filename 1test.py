import requests
import json
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor
import ssl
import aiohttp


cookies = {}

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
headers_img = parse_file('./img_info_header.txt')


def fetch(session, url,cookies):
    with session.get(url,cookies=cookies) as response:
        data = response.text
        if response.status_code != 200:
            #print("FAILURE::{0}".format(url))
            req1 = requests.get(url,cookies=cookies)
            print(req1.status_code)
        # Now we will print how long it took to complete the operation from the 
        # `fetch` function itself
        return data
####################################################
def get_info(info_url,cookies):
    cookies['showimage']='0'
    #info_url = 'https://obd-memorial.ru/html/info.htm?id='+str(id)
    res3 = requests.get(info_url,cookies=cookies)
    if(res3.status_code == 503):
        print(res3.status_code)
    return res3.text
####################################################
def make_str_cookie(cookies):
    str_cook = ''
    for key, value in cookies.items():
        str_cook += '{0}={1};'.format(key,value)
    return str_cook
####################################################
def work(image_id):
    global cookies,headers_img
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
    return url_list
####################################################
async def get_data_asynchronous():
    global cookies
    #url_list = work(51480906) # 2
    #url_list = work(89600091) # 4
    url_list = work(85942988)
    with ThreadPoolExecutor(max_workers=1) as executor:
        with requests.Session() as session:
            # Set any session parameters here before calling `fetch`

            # Initialize the event loop        
            loop = asyncio.get_event_loop()
            
            tasks = [
                loop.run_in_executor(
                    executor,
                    get_info,*(url,cookies) # Allows us to pass in multiple arguments to `fetch`
                    #fetch,*(session,url,cookies) # Allows us to pass in multiple arguments to `fetch`
                )
                for url in url_list
            ]
            
            # Initializes the tasks to run and awaits their results
            for response in await asyncio.gather(*tasks):
                pass


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous())
    loop.run_until_complete(future)

main()