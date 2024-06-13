from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import browser_cookie3
import pandas as pd
import os

# 指定 chromedriver 路径
chromedriver_path = "/Users/a58/Downloads/chromedriver-mac-x64/chromedriver"  # 替换为实际的 chromedriver 路径

# 设置 ChromeDriver 服务
service = Service(chromedriver_path)

# 初始化 Chrome 浏览器
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# 打开目标网页
url = 'https://www.qcc.com/firm/e55fc46dcafd7c32572901e66ce2b92e.html'
print(f"打开页面: {url}...")
driver.get(url)
driver.implicitly_wait(10)  # 等待页面加载

# 从本地浏览器获取Cookies
cookies = browser_cookie3.chrome(domain_name='qcc.com')

# 添加Cookies到Selenium浏览器
for cookie in cookies:
    cookie_dict = {
        'name': cookie.name,
        'value': cookie.value,
        'domain': '.qcc.com',
        'path': cookie.path,
        'expiry': cookie.expires,
        'secure': bool(cookie.secure)
    }
    driver.add_cookie(cookie_dict)

# 刷新页面以应用Cookies
driver.refresh()
driver.implicitly_wait(10)  # 等待页面刷新

# 搜索目标公司
search_keyword = "五八同城信息技术有限公司"
search_box = driver.find_element(By.ID, 'searchKey')
search_box.clear()
search_box.send_keys(search_keyword)
search_box.send_keys(Keys.RETURN)
driver.implicitly_wait(10)  # 等待搜索结果加载

# 点击第一个搜索结果
first_result = driver.find_element(By.XPATH, f"//span[@class='copy-title']//em[contains(text(), '{search_keyword}')]")
first_result.click()
driver.implicitly_wait(10)  # 确保页面完全加载


# 提取表格中的信息
def extract_table_data(table):
    rows = table.find_elements(By.TAG_NAME, 'tr')
    data = []
    headers = [header.text.strip() for header in rows[0].find_elements(By.TAG_NAME, 'th')]
    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, 'td')
        row_data = [col.text.strip().replace('\n', ' ') for col in cols]
        data.append(row_data)
    return headers, data


# 初始化一个空的字典来保存所有表格数据
all_data = {}

# 获取包含表格的div块
data_base_div = driver.find_element(By.CLASS_NAME, 'data-base')
company_data_div = driver.find_element(By.CLASS_NAME, 'company-data')

# 在这些div块中查找并提取表格数据
sections = company_data_div.find_elements(By.TAG_NAME, 'section')

for section in sections:
    section_id = section.get_attribute('id')
    try:
        table = section.find_element(By.TAG_NAME, 'table')
        headers, data = extract_table_data(table)
        all_data[section_id] = pd.DataFrame(data, columns=headers)
    except Exception as e:
        print(f"未找到表格或提取数据失败: {e}")

# 关闭浏览器
driver.quit()

# 确保至少有一个表格成功提取
if not all_data:
    print("未能提取任何表格数据")
    exit()

# 将所有数据保存到一个Excel文件中
with pd.ExcelWriter('公司信息.xlsx') as writer:
    for sheet_name, df in all_data.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print("数据已保存到公司信息.xlsx")
