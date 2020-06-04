"""
When the window shows up follow the standard log in procedure promptly
Requires a UCSD SSO account
"""
import requests, pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

#May need to change where the path is
CHROME_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.binary_location = CHROME_PATH

#Change FilePath to be the path to chromedriver.exe which you can download https://chromedriver.chromium.org/ make sure it matches your installed version of google chrome
driver = webdriver.Chrome("FilePath", options=chrome_options)
wait = WebDriverWait(driver, 100)

headers = {"User-Agent":
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
}


url = "https://cape.ucsd.edu/responses/Results.aspx?"
driver.get(url)


#print(driver.page_source.encode("utf-8"))
wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="aspnetForm"]/div[3]/div[1]/h1')))
print("hi")

#Update cookies
browser_cookies = driver.get_cookies()
session = requests.session()
session.headers.update(headers)
for c in browser_cookies:
    cookies = {c['name']: c['value']}
    session.cookies.update(cookies)

#Make sure to move CapeCookies.txt to the same directory as cape_html.py
with open('CapeCookies.txt', 'wb') as f:
    pickle.dump(session.cookies, f)
print("done")