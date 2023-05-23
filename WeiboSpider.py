from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import json
import os
try:
    like_sum = 0
    comment_sum = 0
    share_sum = 0
    post_sum = 0

    retwee_sum = 0

    useless_like_sum = 0
    useless_comment_sum = 0
    useless_share_sum = 0
    
    url_ = input("[INFO] Input url:")
    browser = webdriver.Edge()
    browser.minimize_window()
    print("[INFO] WebDriver started successfully!")
    browser.get(f'{url_}&nodup=1&page=1')#&nodup=1是微博搜索的“显示所有结果”值
    time.sleep(5)#不睡几秒cookies来不及加载

    #暴风吸入cookies
    path = os.getcwd()+r'\cookiess.txt'
    with open(path, 'r', encoding='utf8') as f:
          listCookies = json.loads(f.read())

    #cookies植入浏览器
    for cookie in listCookies:
     cookie_dict = {
        'domain': "weibo.com",
        'name': cookie.get('name'),
        'value': cookie.get('value'),
        "expires": '',
        'path': '/',
        'httpOnly': False,
        'HostOnly': False,
        'Secure': False
        }
     browser.add_cookie(cookie_dict)
    browser.refresh()#刷新
    
    print("[INFO] Cookies had been read in!\n[INFO] Retrieving page!")
    #爬
    browser.get(f'{url_}&nodup=1&page=1')#必须要在获取一遍因为第一遍获取被登录阻拦了
    print('[INFO] Succeed!')

    max_page = 50#最大页数,貌似在“显示所有结果的情况下”固定是50页
    print(f'[INFO] MAX_PAGE default to {max_page}')
    print("[INFO] Starting crawling!")
    for page in range(1,max_page+1):
          browser.get(f'{url_}&nodup=1&page={page}')

          result_t_or_f = re.findall('抱歉，未找到相关结果。',browser.page_source)

          if len(result_t_or_f) == 0:
               like_count = re.findall(r'class="woo-like-count">(\d+)</span',browser.page_source)
               comment_count =re.findall(r'<i class="woo-font woo-font--comment toolbar_icon"></i></span>\s*(\d+)</a></li>',browser.page_source)
               share_count = re.findall(r'<i class="woo-font woo-font--retweet toolbar_icon"></i></span>\s*(\d+)</a></li>',browser.page_source)
               post_each_page = len(re.findall(r'class="woo-like-count">',browser.page_source))

               retwee_each_page = len(re.findall('node-type="feed_list_forwardContent"',browser.page_source))

               useless_like_count = re.findall(r'node-type="feed_list_forwardContent".*?woo-like-count">(.*?)</span>.*?woo-like-count">(.*?)</span>',browser.page_source)
               useless_comment_count = re.findall(r'node-type="feed_list_forwardContent".*?<i class="woo-font woo-font--comment toolbar_icon"></i></span>\s*(.*?)</a></li>.*?<i class="woo-font woo-font--comment toolbar_icon"></i></span>\s*(.*?)</a></li>',browser.page_source)
               useless_share_count = re.findall(r'node-type="feed_list_forwardContent".*?<i class="woo-font woo-font--retweet toolbar_icon"></i></span>\s*(.*?)</a></li>.*?<i class="woo-font woo-font--retweet toolbar_icon"></i></span>\s*(.*?)</a></li>',browser.page_source)

               #点赞、评论、分享、帖子总数(含转发即useless)
               for i in like_count:
                    like_sum += int(i)
               for i in comment_count:
                    comment_sum += int(i)
               for i in share_count:
                    share_sum += int(i)
               post_sum += post_each_page

               #useless帖子条数
               retwee_sum += retwee_each_page
          

               #计算useless的点赞、评论、分享数
               for i in useless_like_count:
                    for j in i:
                         if j != '赞':
                              useless_like_sum += int(j)
               for i in useless_comment_count:
                    for j in i:
                         if j != '评论':
                              useless_comment_sum += int(j)
               for i in useless_share_count:
                    for j in i:
                         if j != '转发':
                              useless_share_sum += int(j)
          print(f"[INFO] Page {page} crawling completed!")

    print(f"[INFO] Retweet: {share_sum-useless_share_sum} Comment: {comment_sum-useless_comment_sum} Like: {like_sum-useless_like_sum} Post: {post_sum-retwee_sum*2}")
    input("[INFO] Push any key to shutdown...")
finally:#结束
    browser.close()