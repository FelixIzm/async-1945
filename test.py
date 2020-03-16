import requests
import json
import aiohttp
import asyncio
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

async def get(url, cookies, headers):
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        async with session.get(url) as resp:
            #assert resp.status == 200
            return resp

async def fetch(client):
    async with client.get('http://python.org') as resp:
        assert resp.status == 200
        return await resp.text()
#####################################
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
        print(res1.status_code)
        print('*****************')
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
                #print('\t',info_url)
                url_list.append(info_url)
    return url_list
####################################################


url_list = work(84042290)
loop = asyncio.get_event_loop()
headers_img['cookies'] = make_str_cookie(cookies)
coroutines = [get(url, cookies, headers_img) for url in url_list]

results = loop.run_until_complete(asyncio.gather(*coroutines))

for res in results:
    print(res.status)

#print(results.status)
