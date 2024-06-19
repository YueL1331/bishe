import json
import math
import random

import openpyxl
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

cookies = {
    'QCCSESSID': '7a7d4c185af89382bc742e5cd0',
    'qcc_did': 'd47b59f4-1d22-4c43-9a10-aff0a97cd5fa',
    'SECKEY_ABVK': 'XQY67zCSwQWsy2FKi566+L21IrepyPA3bu2aOyvzLeQ%3D',
    'UM_distinctid': '1902aa8fa1da7f-0dff9fed09d545-1a525637-13c680-1902aa8fa1eee3',
    'acw_tc': '707c9fd617187097196846917e27a7abeae26dd30110d0b7a1966d2b0626e7',
    'CNZZDATA1254842228': '1268546458-1718694451-https%253A%252F%252Fwww.qcc.com%252F%7C1718709727',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'QCCSESSID=7a7d4c185af89382bc742e5cd0; qcc_did=d47b59f4-1d22-4c43-9a10-aff0a97cd5fa; SECKEY_ABVK=XQY67zCSwQWsy2FKi566+L21IrepyPA3bu2aOyvzLeQ%3D; UM_distinctid=1902aa8fa1da7f-0dff9fed09d545-1a525637-13c680-1902aa8fa1eee3; acw_tc=707c9fd617187097196846917e27a7abeae26dd30110d0b7a1966d2b0626e7; CNZZDATA1254842228=1268546458-1718694451-https%253A%252F%252Fwww.qcc.com%252F%7C1718709727',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

proxies = {
    'http': 'http://t15873905246814:gg6xwmok@u273.kdltps.com:15818',
    'https': 'http://t15873905246814:gg6xwmok@u273.kdltps.com:15818'
}


def qcc_did(now_time):
    e = float(int(now_time * 1000))
    e += random.uniform(10000, 30000)
    e = 1718701069986.5256
    temp = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    r = ''
    for t in temp:
        n = int((e + 16.0 * 0) % 16) | 0
        e = math.floor(e / 16)
        if "x" == t:
            r += str('%x' % n)
        elif "y" == t:
            r += str('%x' % (3 & n | 8))
        else:
            r += str(t)
        # 2a6119a2-0910-4000-8000-000000000000
    return r


def search_info(ind: int, company_name: str, company_id: str):
    now_time = time.time()
    tt = int(now_time)
    cookies['CNZZDATA1254842228'] = '1268546458-1718694451-https%253A%252F%252Fwww.qcc.com%252F%7C' + str(tt)
    cookies['qcc_did'] = qcc_did(now_time)
    response = requests.get('https://www.qcc.com/firm/' + str(company_id) + '.html', cookies=cookies, headers=headers,
                            proxies=proxies)
    data = {}
    if response.status_code == 200:
        data = parse_html(response.text)
        print(f'完成\t{ind}\t{company_id}\t{company_name}\t信息提取')
    else:
        print(f'提取\t{ind}\t{company_id}\t{company_name}\t信息失败')
    return data


def parse_html(content):
    data = {}
    # 解析HTML
    soup = BeautifulSoup(content, 'html.parser')
    # 工商信息提取
    business_info = {}
    base_info = soup.find('section', {'id': 'cominfo'})
    if base_info:
        tr_list = base_info.find_all('tr')
        print(tr_list)
    data['business_info'] = business_info
    # 营业期限信息提取
    business_term_info = {}
    data['business_term_info'] = business_term_info
    # 股东出资信息提取
    shareholder_infos = {}
    holder_info = soup.find('div', {'class': 'app-tree-table'})
    if holder_info:
        tr_list = holder_info.find_all('tr')
        print(tr_list)
    data['shareholder_infos'] = shareholder_infos
    # 主要人员信息提取
    member_infos = []
    staff_info = soup.find('section', {'id': 'mainmember'})
    if staff_info:
        tr_list = staff_info.find_all('tr')
        print(tr_list)
    data['member_infos'] = member_infos
    # 分支机构信息提取
    branch_infos = []
    branch_info = soup.find('section', {'id': 'branchelist'})
    if branch_info:
        tr_list = branch_info.find_all('tr')
        print(tr_list)
    data['branch_infos'] = branch_infos
    # 其他信息提取
    other_info = {}
    data['other_info'] = other_info
    return data


def batch_search_info():
    df = pd.read_excel('../data/qcc_company_id_mapping_no_repeat.xlsx')
    company_ids = df['企业ID']
    names = df['企业名称']
    total = len(company_ids)
    start = 10
    for index in range(total):
        if index < start:
            continue
        key = company_ids[index]
        name = names[index]
        resp = search_info(index + 1, name, key)
        print(resp)


def test_html():
    with open('demo.html', 'r') as file:
        content = file.read()
        parse_html(content)


if __name__ == '__main__':
    # batch_search_info()
    test_html()
