import json
import random
import time
import urllib3
import requests
import pandas as pd

# 忽略 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

token = '531239ad5753e33b32cb8ecae40f49b5'

headers = {
    'Host': 'xcx.qcc.com',
    'x-request-device-type': 'Android',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.8(0x1308080a) XWEB/1216',
    'content-type': 'application/json',
    'qcc-version': '1.0.0',
    'authmini': 'Bearer ' + token,
    'xweb_xhr': '1',
    'xcx-version': '2024.06.15',
    'qcc-platform': 'mp-weixin',
    'qcc-currentpage': '/company-subpackages/detail/index',
    'qcc-timestamp': '1718598895351',
    'qcc-refpage': '/pages/search/index/index',
    'accept': '*/*',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://servicewechat.com/wx395200814fcd7599/353/page-frame.html',
    'accept-language': 'zh-CN,zh;q=0.9',
}

params = {
    'token': token,
    't': '1718598895351',
    'unique': '8361643db2bf20a5c5f9816d4922b8d8',
}

# 设置代理
proxies = {
    'http': 'http://t15873905246814:gg6xwmok@u273.kdltps.com:15818',
    'https': 'http://t15873905246814:gg6xwmok@u273.kdltps.com:15818',
}


def get_ent_detail(ind: int, name: str, key_no: str):
    millis = str(int(round(time.time() * 1000)))
    headers['qcc-timestamp'] = millis
    headers['authmini'] = millis
    params['t'] = millis
    params['unique'] = key_no
    try:
        response = requests.get('https://xcx.qcc.com/mp-weixin/forwardApp/v1/ent/detail', params=params,
                                headers=headers, proxies=proxies, verify=False)
        data = {}
        if response.status_code == 200:
            resp = json.loads(response.text)
            data['status'] = resp['status']
            if data['status'] == 200:
                data['name'] = resp['result']['Company']['Name']
                data['shortStatus'] = resp['result']['Company']['ShortStatus']
            else:
                data['message'] = resp['message']
        print(ind, '\t', name, '\t', key_no, '\t', data)
    except Exception as e:
        print(ind, '\t', name, '\t', key_no, '\t', '异常')
        print(e)


if __name__ == '__main__':
    df = pd.read_excel('company_id_mapping_no_repeat.xlsx')
    keyNos = df['企业ID']
    names = df['企业名称']
    total = len(keyNos)
    for index in range(total):
        get_ent_detail(index, names[index], keyNos[index])
        if index >= 100:
            break
        time.sleep(30)
