#!/usr/bin/python3

import requests 
from bs4 import BeautifulSoup 
import re
import pymysql

db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "db": "jkf",
    "charset": "utf8"
}

def connectDb():
    try:
        mysqldb = pymysql.connect(
                host="127.0.0.1",
                user="root",
                passwd="",
                database='jkf')
        return mysqldb
    except Exception:
        return None
conn = connectDb()

if conn is not None:
    cursor = conn.cursor()
    
# 開始蒐一個月內?頁
# for i in range(10):
#     page = i+1
#     url = "https://www.jkforum.net/type-1128-1948.html?forumdisplay&typeid=1948&orderby=dateline&dateline=2592000&filter=dateline&typeid=1948&forumdisplay=&orderby=dateline&dateline=2592000&page=%d" % (page)

#     resp = requests.get(url)
#     if(resp.status_code == 200):
#         resp.encoding = 'utf-8'    #轉換編碼至UTF-8
#         soup = BeautifulSoup(resp.content, 'html.parser')
#         columns = soup.find_all('a',href=re.compile("thread-"))

#         for i in columns:
#             try:
#                 sql = 'INSERT INTO `jkf` (`url`) VALUES ("%s")' % (i['href'])
#                 cursor.execute(sql)
#                 conn.commit()
#             except Exception as e:
#                 continue


# 爬文章
cursor.execute("select `url` from jkf")
all = cursor.fetchall()
for i in all:
    # print(i[0])
    resp = requests.get(i[0])
    if(resp.status_code == 200):
        soup = BeautifulSoup(resp.content, 'html.parser')
        try:
            # success
            title = soup.find('h1').get_text()
            
        except Exception:
            # fail
            continue


# sandbox

# resp = requests.get('https://www.jkforum.net/thread-12289799-1-1.html')
# if(resp.status_code == 200):
#     soup = BeautifulSoup(resp.content, 'html.parser')
#     try:
#         title = soup.find('h1').get_text()
#         print(title)
#     except Exception:
#         print('aaa')


cursor.close()
conn.close()
