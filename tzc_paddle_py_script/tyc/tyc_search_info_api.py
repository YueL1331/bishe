import hashlib
import math
import os
import time

import requests
import json
import pandas as pd
import urllib3
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook

# 忽略 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cookies = {

}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'HWWAFSESID=e2bcaf1852238ef606; HWWAFSESTIME=1718691461689; csrfToken=ttM8SueaOZfFBG7r3iRwiDs8; TYCID=78e102a02d3a11ef868013133f6b1117; CUID=5f90b4ffda502ed3260b8340b31a94eb',
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
    'https': 'http://t15873905246814:gg6xwmok@u273.kdltps.com:15818',
}


def search_info(ind: int, company_name: str, company_id: int):
    response = requests.get(f'https://www.tianyancha.com/company/{company_id}', headers=headers,
                            cookies=cookies, proxies=proxies, verify=False)
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
    base_info = soup.find("div", {'data-dim': 'baseInfo'})
    if base_info:
        tr_list = base_info.find_all('tr')
        print(tr_list)
    data['business_info'] = business_info
    # 营业期限信息提取
    business_term_info = {}
    data['business_term_info'] = business_term_info
    # 股东出资信息提取
    shareholder_infos = {}
    holder_info = soup.find("div", {'data-dim': 'holder'})
    if holder_info:
        tr_list = holder_info.find_all('tr')
        print(tr_list)
    data['shareholder_infos'] = shareholder_infos
    # 主要人员信息提取
    member_infos = []
    staff_info = soup.find("div", {'data-dim': 'staff'})
    if staff_info:
        tr_list = staff_info.find_all('tr')
        print(tr_list)
    data['member_infos'] = member_infos
    # 分支机构信息提取
    branch_infos = []
    branch_info = soup.find("div", {'data-dim': 'branch'})
    if branch_info:
        tr_list = branch_info.find_all('tr')
        print(tr_list)
    data['branch_infos'] = branch_infos
    # 其他信息提取
    other_info = {}
    data['other_info'] = other_info
    return data


def batch_search_info():
    df = pd.read_excel('../data/tyc_company_id_mapping.xlsx')
    company_ids = df['企业ID']
    names = df['企业名称']
    total = len(company_ids)
    start = 10
    for index in range(total):
        if index < start:
            continue
        key = company_ids[index]
        name = names[index]
        if not math.isnan(key):
            resp = search_info(index + 1, name, int(key))
        else:
            print(f'数据\t{index}\t{key}\t{name}\t信息缺失')


def test_html():
    with open('info_demo.html', 'r') as file:
        content = file.read()
        parse_html(content)


if __name__ == '__main__':
    batch_search_info()
    # test_html()
