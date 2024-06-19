import json
import random
import time
import urllib3
import requests
import pandas as pd

# 忽略 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cookies = {
    'acw_tc': '0a47309317186134120553889e005d8ee16877d5b4b48ae8eb17485d90ae8c',
    'cna': 'e4d271e1f7564768bf34107701f62c78'
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    # 'Cookie': 'acw_tc=0a47309317186134120553889e005d8ee16877d5b4b48ae8eb17485d90ae8c; cna=e4d271e1f7564768bf34107701f62c78',
    'Origin': 'https://www.sscha.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.sscha.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'userAgent': '5',
}

json_data = {
    'actionType': 1,
    'bizType': 0,
    'companyNameTag': '上海剑桥科技股份有限公司',
    'detail': '{}',
}

response = requests.post('https://api2.sscha.com/center/home/saveCompanySearch', cookies=cookies, headers=headers, json=json_data, verify=False)
print(response.text)