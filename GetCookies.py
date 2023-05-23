from selenium import webdriver
import json
import os
input('[INFO] Push any key to start log in and then push any key to get cookies if you have finshed...')
browser = webdriver.Edge("")
print('[INFO] WebDriver started successfully!')
print('[INFO] Opening login page.')
browser.get("https://weibo.com/login.php")
input('[INFO] Waiting to log in...')
print('[INFO] Succeed!Please log in now...')

dictCookies = browser.get_cookies()
jsonCookies = json.dumps(dictCookies)
path = os.getcwd()+r'\cookiess.txt'
with open(path, 'w') as f:
    f.write(jsonCookies)
print(f'[INFO] Cookies had been saved at {path} !')
