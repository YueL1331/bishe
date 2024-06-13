import requests
from bs4 import BeautifulSoup
import urllib3
import json

# 忽略 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

# 设置获取到的Cookies
cookies = {
    'QCCSESSID': '988f17dd434c091be146b78d76',
    'qcc_did': 'daf3e340-610c-412d-b313-dee14e652b4c',
    'UM_distinctid': '18ff0b5f620604-0a0a706b91bacd-1b525637-13c680-18ff0b5f6212167',
    'tfstk': 'fTnq6j0VmlcSrugga7ZaTSl_vxZY5kdBbcN_IADghSVcci1izAGtcPAYcclrKXJTfoiXbVrxVqs_GIEZIXZwOBtBAxHYDlABOx7BWYrgIhNMsLd5GlEMOQaqx2p8XXM1HnLZELy_C52isPflq7ecslV0S_buK7VgjlcgqT2gL-jcmiDlEUHjxcCzCrvnpczgjNA3oWD0ixMjqJ5QtxVPjGV43rJrn7SGj0u-Hq48T35uNADKSzowDiZtF2lZSbvGj5uuLXyIG3j4j4crYyDJTiFqrjnacyKNQ8uEEjo4beWYFmkovPovggVqwY0QDDARbXDSdmU-bB5u6qwLq-uyIaV0SgRA68Yi2c3VsNz0e8PBULmlVApL2B8KtNQTkKezOK4cWNU0eG_qvWQOWrpYUW90o',
    'acw_tc': '707c9fce17182588583674650e415548d862f2099ce35fc6adb6d686e7df38',
    'CNZZDATA1254842228': '1490140565-1717730408-%7C1718259007'
}

# 目标页面URL
target_url = "https://www.qcc.com/firm/e55fc46dcafd7c32572901e66ce2b92e.html"

# 创建一个会话
session = requests.Session()

# 设置Cookies
session.cookies.update(cookies)

# 获取目标页面内容
response = session.get(target_url, headers=headers, verify=False)
if response.status_code == 200:
    # 解析HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    data = {}

    # 提取工商信息
    cominfo_section = soup.find('section', {'id': 'cominfo'})
    if cominfo_section:
        rows = cominfo_section.find_all('tr')
        company_info = {}

        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                label_1 = cells[0].get_text(strip=True)
                value_1 = cells[1].get_text(strip=True)
                company_info[label_1] = value_1

                if len(cells) >= 4:
                    label_2 = cells[2].get_text(strip=True)
                    value_2 = cells[3].get_text(strip=True)
                    company_info[label_2] = value_2

                if len(cells) >= 6:
                    label_3 = cells[4].get_text(strip=True)
                    value_3 = cells[5].get_text(strip=True)
                    company_info[label_3] = value_3

        data['工商信息'] = company_info

    # 提取股东信息
    partner_section = soup.find('section', {'id': 'partner'})
    if partner_section:
        rows = partner_section.find_all('tr')
        partner_info = []

        for row in rows[1:]:  # 跳过表头
            cells = row.find_all('td')
            if len(cells) >= 6:
                if not (cells[1].find('span', {'class': 'app-auto-logo'}) or
                        cells[1].find('div', {'class': 'app-tdcoy-tags app-tags margin-type-default'}) or
                        cells[1].find('span', {'class': 'tail-tag'})):
                    partner = {
                        '序号': cells[0].get_text(strip=True),
                        '股东名称': cells[1].get_text(strip=True),
                        '持股比例': cells[2].get_text(strip=True),
                        '认缴出资额': cells[3].get_text(strip=True),
                        '认缴出资日期': cells[4].get_text(strip=True),
                        '首次持股日期': cells[5].get_text(strip=True),
                    }
                    partner_info.append(partner)

        data['股东信息'] = partner_info

    # 提取主要人员信息
    mainmember_section = soup.find('section', {'id': 'mainmember'})
    if mainmember_section:
        rows = mainmember_section.find_all('tr')
        mainmember_info = []

        for row in rows[1:]:  # 跳过表头
            cells = row.find_all('td')
            if len(cells) >= 6:
                if not (cells[1].find('span', {'class': 'app-auto-logo'}) or
                        cells[1].find('div', {'class': 'app-tdcoy-tags app-tags margin-type-default'}) or
                        cells[1].find('span', {'class': 'tail-tag'})):
                    member = {
                        '序号': cells[0].get_text(strip=True),
                        '姓名': cells[1].get_text(strip=True),
                        '职务': cells[2].get_text(strip=True),
                        '持股比例': cells[3].get_text(strip=True),
                        '最终受益股份': cells[4].get_text(strip=True),
                        '个人简介': cells[5].get_text(strip=True),
                    }
                    mainmember_info.append(member)

        data['主要人员信息'] = mainmember_info

    # 提取其他相关信息
    header_info_part = soup.find('div', {'class': 'ui-header-info-part'})
    if header_info_part:
        header_info = {}
        rlines = header_info_part.find_all('div', {'class': 'rline'})

        for rline in rlines:
            label_span = rline.find('span', {'class': 'f'})
            value_span = rline.find('span', {'class': 'val'})
            if label_span and value_span:
                label = label_span.get_text(strip=True)
                value = value_span.get_text(strip=True)
                header_info[label] = value

        # 打印提取的其他信息
        print("\n其他信息：")
        for key, value in header_info.items():
            print(f"{key}: {value}")

    # 提取分支机构信息
    branchelist_section = soup.find('section', {'id': 'branchelist'})
    if branchelist_section:
        rows = branchelist_section.find_all('tr')
        branchelist_info = []

        for row in rows[1:]:  # 跳过表头
            cells = row.find_all('td')
            if len(cells) >= 6:
                if not (cells[1].find('span', {'class': 'app-auto-logo'}) or
                        cells[1].find('div', {'class': 'app-tdcoy-tags app-tags margin-type-default'}) or
                        cells[1].find('span', {'class': 'tail-tag'})):
                    branch = {
                        '序号': cells[0].get_text(strip=True),
                        '企业名称': cells[1].get_text(strip=True),
                        '负责人': cells[2].get_text(strip=True),
                        '地区': cells[3].get_text(strip=True),
                        '成立日期': cells[4].get_text(strip=True),
                        '状态': cells[5].get_text(strip=True),
                    }
                    branchelist_info.append(branch)

        data['分支机构信息'] = branchelist_info

    # 输出为JSON文件
    with open('company_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("数据已保存到 company_data.json 文件。")
else:
    print(f"Failed to retrieve the target page. Status code: {response.status_code}")
