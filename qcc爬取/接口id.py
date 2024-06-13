import hashlib
import requests
from urllib import parse
import json
import hmac
import pandas as pd


# 读取Excel文件
def read_excel(file_path):
    df = pd.read_excel(file_path, usecols=[0])  # 只读取第一列
    df.columns = ['Keyword']  # 重命名列为'Keyword'
    return df


# 处理搜索请求
def search_mind(keyword: str):
    cookies = {
        'QCCSESSID': 'c6f68701cd4246adc2a500b650',
        'qcc_did': 'bf37a478-7d83-4e54-b0e2-c845d2c4e57b',
        'UM_distinctid': '1900a8306fb7b0-0ecc7ea4c8cc72-1a525637-13c680-1900a8306fc8fc',
        'tfstk': 'fups1vZDrEpF8LKCo1nFFFazXeXXhFMzlosvqneaDOBTkrKR8GJZSnQXle737ClDuEaX7e8ficbVkZT2DCoEUY-MjtXvl4krUAfgtxv1krWAx5OOZ4urUvWaVJ9KzIRw0oWCmwIOX5FtA6I5XtUOXEQd9gIzWtBvkHnCbgyYBtQYJwIJPNe1Yc_HfDwG9cR7xMxOR8tHdGI_shQQH-pB41_-hwwYHps6xLWf7RH5JCRvQ9ptJzXpqB8OATMbcMOWvOI6oY2GB3KpM19jgubDOHdPOBqZjM96VKs59yn1od86h1v-zJb9OpvfQBu_UZfvTdfkQ2e1eQxNQILKD-QX9iIyn875MhNbA_2fAaoIASV2EFvGlCxYuIfOxMuqADNym1IhAMmIASVc6MjedDiQanf..',
        'CNZZDATA1254842228': '992078368-1718163278-https%253A%252F%252Fwww.qcc.com%252F%7C1718185629',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.qcc.com/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'x-pid': '83501dfb338244157a6af1e1380ff0dd',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'mindKeyWords': 'true',
        'mindType': '9',  # 假设9为精确搜索，根据实际情况调整
        'pageSize': '5',
        'person': 'true',
        'searchKey': keyword,
        'suggest': 'true',
    }

    header = dynamic_header(params)
    headers[header[0]] = header[1]
    response = requests.get('https://www.qcc.com/api/search/searchMind', params=params, cookies=cookies,
                            headers=headers, verify=False)

    if response.status_code == 200:
        data = response.json()
        if 'list' in data and data['list']:
            return data['list'][0].get('KeyNo', 'No KeyNo found')
    return 'Request failed'


def dynamic_header(params: dict):
    e = {
        "url": "/api/search/searchMind",
        "baseURL": "https://www.qcc.com",
        "params": params,
        "data": {}
    }
    t = e['url'].replace(e['baseURL'], "")
    n = None
    if e['params']:
        n = parse.urlencode(e['params'])
    else:
        n = parse.urlencode({})
    if n:
        if t.find('?') == -1:
            t += ('?' + n)
        else:
            t += ('&' + n)
    t = t.lower()
    name = gen_name(t, e['data'])
    windowTid = 'c400b081f47505d5f59e7f2b09813034'
    val = gen_val(t, e['data'], windowTid)
    return name, val


def gen_name(t: str, e: dict):
    if t == '' or t is None:
        t = '/'
    t = t.lower()
    if e is None:
        e = {}
    n = json.dumps(e).lower()
    url = encode_url(t)
    n_ = (t + n)
    hmac_md5 = hmac.new(url.encode('utf-8'), n_.encode('utf-8'), hashlib.sha512)
    digest = hmac_md5.hexdigest()
    return digest.lower()[8:28]


def gen_val(n: str, e: dict, t: str):
    if n == '' or n is None:
        n = '/'
    n = n.lower()
    if e is None:
        e = {}
    if t is None:
        t = ''
    i = json.dumps(e).lower()
    hmac_md5 = hmac.new(encode_url(n).encode('utf-8'), (n + "pathString" + i + t).encode('utf-8'), hashlib.sha512)
    return hmac_md5.hexdigest()


codes = {0: 'W', 1: 'l', 2: 'k', 3: 'B', 4: 'Q', 5: 'g', 6: 'f', 7: 'i', 8: 'i', 9: 'r', 10: 'v', 11: '6', 12: 'A',
         13: 'K', 14: 'N', 15: 'k', 16: '4', 17: 'L', 18: '1', 19: '8'}
le = len(codes)


def encode_url(e: str):
    t = e + e
    n = ''
    for i in range(len(t)):
        a = ord(t[i]) % le
        n += codes[a]
    return n


if __name__ == '__main__':
    file_path = 'qcc查询query.xlsx'  # Excel文件名
    df = read_excel(file_path)

    # 打印列名称以确认
    print("Excel columns:", df.columns)

    results = []
    for index, row in df.iterrows():
        keyword = row['Keyword']
        keyno = search_mind(keyword)
        results.append({'Keyword': keyword, 'KeyNo': keyno})

    # 保存结果到新的Excel文件
    result_df = pd.DataFrame(results)
    result_df.to_excel('search_results.xlsx', index=False)
    print('Results saved to search_results.xlsx')
