import requests

headers = {
    'Host': 'xcx.qcc.com',
    'x-request-device-type': 'Android',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080712) XWEB/1191',
    'content-type': 'application/json',
    'qcc-version': '1.0.0',
    'authmini': 'Bearer d317ba05a53546ec7ea2d10d65ae206f',
    'xweb_xhr': '1',
    'xcx-version': '2024.06.15',
    'qcc-platform': 'mp-weixin',
    'qcc-currentpage': '/company-subpackages/business/index',
    'qcc-timestamp': '1718591432104',
    'qcc-refpage': '/company-subpackages/detail/index',
    'accept': '*/*',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://servicewechat.com/wx395200814fcd7599/353/page-frame.html',
    'accept-language': 'zh-CN,zh;q=0.9',
}

params = {
    'token': 'd317ba05a53546ec7ea2d10d65ae206f',
    't': '1718591432104',
    'unique': 'e55fc46dcafd7c32572901e66ce2b92e',
}

response = requests.get('https://xcx.qcc.com/mp-weixin/forwardApp/v6/base/getEntDetail', params=params, headers=headers)