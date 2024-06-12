import browser_cookie3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from PIL import Image
import io

# 创建保存截图的目录
output_dir = "/Users/a58/bishe/截图爬取/pictures"
os.makedirs(output_dir, exist_ok=True)

# 指定 chromedriver 路径
chromedriver_path = "/Users/a58/Downloads/chromedriver-mac-x64/chromedriver"  # 替换为实际的 chromedriver 路径

# 设置 ChromeDriver 服务
service = Service(chromedriver_path)

# 初始化 Chrome 浏览器
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# 打开目标网页
url = 'https://www.qcc.com'
print(f"打开页面: {url}...")
driver.get(url)
print("页面加载完成")

# 从本地浏览器获取Cookies
cookies = browser_cookie3.chrome(domain_name='qcc.com')

# 添加Cookies到Selenium浏览器
print("开始添加Cookies...")
for cookie in cookies:
    cookie_dict = {
        'name': cookie.name,
        'value': cookie.value,
        'domain': '.qcc.com',  # 强制设置为当前域名
        'path': cookie.path,
        'expiry': cookie.expires,
        'secure': bool(cookie.secure)  # 确保 secure 是布尔值
    }
    driver.add_cookie(cookie_dict)
    print(f"添加 Cookie: {cookie_dict}")

print("Cookies添加完成")

# 刷新页面以应用Cookies
print("刷新页面...")
driver.refresh()
time.sleep(5)  # 等待页面刷新

# 搜索关键词
search_keyword = "五八同城信息技术有限公司"
print(f"搜索关键词: {search_keyword}...")
search_box = driver.find_element(By.ID, 'searchKey')  # 替换为实际的搜索框元素ID或其他选择器
search_box.send_keys(search_keyword)
search_box.send_keys(Keys.RETURN)

# 等待搜索结果加载
print("等待搜索结果加载...")
try:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//table[@id="search-result"]/tbody/tr[1]/td[3]/a')))
except Exception as e:
    print(f"搜索结果加载失败: {e}")
    driver.quit()
    exit()

# 点击第一个搜索结果
print("点击第一个搜索结果...")
try:
    first_result = driver.find_element(By.XPATH, '//table[@id="search-result"]/tbody/tr[1]/td[3]/a')  # 替换为第一个结果的实际XPath
    first_result.click()
    time.sleep(5)  # 等待目标页面加载
except Exception as e:
    print(f"未找到元素: {e}")
    driver.quit()
    exit()

# 获取网页高度以准备滚动截屏
total_height = driver.execute_script("return document.body.scrollHeight")
print(f"网页总高度: {total_height}px")

# 设置窗口大小（宽度可以根据需要调整）
driver.set_window_size(1920, 1080)
print("窗口大小设置完成")

# 滚动截屏
print("开始滚动截屏...")
screenshots = []
scroll_height = 1080
for i in range(0, total_height, scroll_height):
    driver.execute_script(f"window.scrollTo(0, {i});")
    time.sleep(2)  # 等待页面加载
    screenshot = driver.get_screenshot_as_png()
    screenshots.append(Image.open(io.BytesIO(screenshot)))

# 拼接截图
full_image = Image.new('RGB', (1920, total_height))
offset = 0
for screenshot in screenshots:
    full_image.paste(screenshot, (0, offset))
    offset += screenshot.height

# 保存拼接后的截图
screenshot_path = os.path.join(output_dir, "full_screenshot.png")
full_image.save(screenshot_path)
print(f"截图保存到 {screenshot_path}")

# 关闭浏览器
driver.quit()
print("浏览器关闭")
