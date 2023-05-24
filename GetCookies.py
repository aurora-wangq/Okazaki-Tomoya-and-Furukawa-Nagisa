from selenium import webdriver
import json
import os
input('[INFO] Push any key to start log in...')
browser = webdriver.Edge("")
print('[INFO] WebDriver started successfully!')
print('[INFO] Opening login page.')
browser.get("https://weibo.com/login.php")
print('[INFO] Waiting to log in.')
input('[INFO] Succeed!Push any key to save cookies...')

dictCookies = browser.get_cookies()
jsonCookies = json.dumps(dictCookies)
path = os.getcwd()+r'\cookiess.txt'
with open(path, 'w') as f:
    f.write(jsonCookies)
print(f'[INFO] Cookies had been saved at {path} !')
