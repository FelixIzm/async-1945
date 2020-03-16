from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import requests
#from requests.exceptions import Timeout, HTTPError
import json
import random
import time
import threading
from lxml.html import fromstring

image_id=85942988

img_info = 'https://obd-memorial.ru/html/getimageinfo?id={}'.format(image_id)
res1 = requests.get(img_info)
print(res1.status_code)
if(res1.status_code==307):
    cookies = {}
    cookies['3fbe47cd30daea60fc16041479413da2']=res1.cookies['3fbe47cd30daea60fc16041479413da2']
    cookies['JSESSIONID']=res1.cookies['JSESSIONID']
    cookies['showimage']='0'
    img_info = 'https://obd-memorial.ru/html/getimageinfo?id={}'.format(image_id)
    response = requests.get(img_info)
    response_dict = json.loads(response.text)
    print('response_dict = '+str(len(response_dict)))

