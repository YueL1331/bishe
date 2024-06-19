import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 指定 chromedriver 路径
chromedriver_path = "/Users/a58/Downloads/chromedriver-mac-x64/chromedriver"  # 替换为实际的 chromedriver 路径
service = Service(chromedriver_path)
options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(service=service, options=options)

# 读取 stealth.min.js 内容
with open('/Users/a58/QCC/tzc_paddle_py_script/ssc/stealth.min.js', 'r') as file:
    stealth_js = file.read()

try:
    # 使用带有中文关键词的URL
    search_term = "剑桥科技"
    url = "https://www.sscha.com"
    driver.get(url)

    # 执行 stealth.min.js
    driver.execute_script(stealth_js)

    # 增加等待时间以确保页面加载完成
    time.sleep(15)  # 等待15秒以确保页面完全加载

    # 输出整个页面的HTML内容以调试
    page_source = driver.page_source
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(page_source)
    print("Page source has been saved to 'page_source.html'")

    # 使用id定位搜索框并输入搜索关键词
    wait = WebDriverWait(driver, 30)  # 增加等待时间到30秒

    try:
        search_box = wait.until(EC.presence_of_element_located((By.ID, 'searchInputHomeRef')))
        print("Found search box using ID.")
    except TimeoutException:
        print("Failed to find element using ID.")

    # 等待元素可点击
    search_box = wait.until(EC.element_to_be_clickable((By.ID, 'searchInputHomeRef')))
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)  # 或者使用 search_box.send_keys(Keys.ENTER)

    # 增加等待时间以确保搜索结果加载完成
    time.sleep(10)  # 等待10秒以确保页面完全加载

    # 输出整个页面的HTML内容
    page_source = driver.page_source
    print(page_source)

finally:
    driver.quit()  # 关闭浏览器
