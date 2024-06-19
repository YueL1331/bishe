import json
import random
import time
import urllib3
import requests
import pandas as pd

# 忽略 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cookies = {
    'acw_tc': '1a0c399b17186821742333522e005e09545bc20c48ceeb6687b2c3fb413f82',
    'sajssdk_2015_cross_new_user': '1',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%221902970c4536e3-032e12ae99879ec-1a525637-1296000-1902970c4541171%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMjk3MGM0NTM2ZTMtMDMyZTEyYWU5OTg3OWVjLTFhNTI1NjM3LTEyOTYwMDAtMTkwMjk3MGM0NTQxMTcxIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%221902970c4536e3-032e12ae99879ec-1a525637-1296000-1902970c4541171%22%7D',
    'Hm_lvt_6b63cf9e50e2bd684eba62e24995ba09': '1718604144,1718612767,1718682125',
    'Hm_lpvt_6b63cf9e50e2bd684eba62e24995ba09': '1718682175',
    'Hm_lvt_78d5885b19eecf93e59673b4b37c8530': '1718604144,1718612767,1718682125',
    'Hm_lpvt_78d5885b19eecf93e59673b4b37c8530': '1718682175',
    'UM_distinctid': '1902970c4cae73-0f414d6df7036f-1a525637-13c680-1902970c4cb1a6e',
    'CNZZDATA1281275881': '2038667153-1718682175-%7C1718682175',
    'cna': '1917ec4c7d0f46cbbf683f1e6187fd8d',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'acw_tc=1a0c399b17186821742333522e005e09545bc20c48ceeb6687b2c3fb413f82; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221902970c4536e3-032e12ae99879ec-1a525637-1296000-1902970c4541171%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMjk3MGM0NTM2ZTMtMDMyZTEyYWU5OTg3OWVjLTFhNTI1NjM3LTEyOTYwMDAtMTkwMjk3MGM0NTQxMTcxIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%221902970c4536e3-032e12ae99879ec-1a525637-1296000-1902970c4541171%22%7D; Hm_lvt_6b63cf9e50e2bd684eba62e24995ba09=1718604144,1718612767,1718682125; Hm_lpvt_6b63cf9e50e2bd684eba62e24995ba09=1718682175; Hm_lvt_78d5885b19eecf93e59673b4b37c8530=1718604144,1718612767,1718682125; Hm_lpvt_78d5885b19eecf93e59673b4b37c8530=1718682175; UM_distinctid=1902970c4cae73-0f414d6df7036f-1a525637-13c680-1902970c4cb1a6e; CNZZDATA1281275881=2038667153-1718682175-%7C1718682175; cna=1917ec4c7d0f46cbbf683f1e6187fd8d',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

params = {
    'keyword': '厦门市巨龙信息科技有限公司',
    'type': '1',
    'keywordType': '输入词',
}

response = requests.get('https://www.sscha.com/search-list', params=params,
                        cookies=cookies, headers=headers, verify=False)
print(response.text)

