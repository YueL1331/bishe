import json
import random
import time
import urllib3
import requests
import pandas as pd

# 忽略 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cookies = {
    'HWWAFSESID': 'e2bcaf1852238ef606',
    'HWWAFSESTIME': '1718691461689',
    'csrfToken': 'ttM8SueaOZfFBG7r3iRwiDs8',
    'TYCID': '78e102a02d3a11ef868013133f6b1117',
    'CUID': '5f90b4ffda502ed3260b8340b31a94eb',
    'sajssdk_2015_cross_new_user': '1',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2219029fe85971f31-00285058c656aaf2-1a525637-1296000-19029fe8598212b%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMjlmZTg1OTcxZjMxLTAwMjg1MDU4YzY1NmFhZjItMWE1MjU2MzctMTI5NjAwMC0xOTAyOWZlODU5ODIxMmIifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219029fe85971f31-00285058c656aaf2-1a525637-1296000-19029fe8598212b%22%7D',
    'Hm_lvt_e92c8d65d92d534b0fc290df538b4758': '1718267992,1718594885,1718677622',
    'bannerFlag': 'true',
    'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758': '1718693212',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'HWWAFSESID=e2bcaf1852238ef606; HWWAFSESTIME=1718691461689; csrfToken=ttM8SueaOZfFBG7r3iRwiDs8; TYCID=78e102a02d3a11ef868013133f6b1117; CUID=5f90b4ffda502ed3260b8340b31a94eb; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219029fe85971f31-00285058c656aaf2-1a525637-1296000-19029fe8598212b%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMjlmZTg1OTcxZjMxLTAwMjg1MDU4YzY1NmFhZjItMWE1MjU2MzctMTI5NjAwMC0xOTAyOWZlODU5ODIxMmIifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219029fe85971f31-00285058c656aaf2-1a525637-1296000-19029fe8598212b%22%7D; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1718267992,1718594885,1718677622; bannerFlag=true; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1718693212',
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

# 设置代理
proxies = {
    'http': 'http://t15873905246814:gg6xwmok@u273.kdltps.com:15818',
    'https': 'http://t15873905246814:gg6xwmok@u273.kdltps.com:15818'
}

response = requests.get('https://www.tianyancha.com/company/3048233042', cookies=cookies, headers=headers, proxies=proxies,verify=False)
print(response.text)

