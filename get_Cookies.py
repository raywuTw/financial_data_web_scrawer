from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys

def get_Cookies(password):
    driver = 'D:\VolSurface\IEDriverServer'
    browser = webdriver.Ie(driver)
#     browser.get('https://clientlogin.ibb.ubs.com/login')
    browser.get('https://clientportal.ibb.ubs.com/portal/index.htm?page=foreignexchange')
    user = browser.find_element_by_css_selector('input.submit-password-input.input-field')
    user.send_keys(password)
    submit = browser.find_element_by_css_selector('button.submit-password-button.btn.btn-primary')
    submit.click()
    timeout = 20
# 等網頁全部Load出來在做下一個動作, 最多等20秒
    try:
        element_present = EC.presence_of_element_located((By.ID, 'element_id'))
        WebDriverWait(browser, timeout).until(element_present)
    except TimeoutException:
        print( "Timed out waiting for page to load")
    cookies_list = browser.get_cookies()
    cookies_dict = {}
    for cookie in cookies_list:
        cookies_dict[cookie['name']] = cookie['value']
    f = open("D:\VolSurface\\volcast_cookies.txt","w")
    f.write(str(cookies_dict))
    f.close()
    browser.close()
if (len(sys.argv)==2):
    password = sys.argv[1]
    get_Cookies(password)
    print(" Cookies got! Please close this command window ")
else:
    print("Errors, please infor Quant team")