#!/usr/bin/python3

import requests 
from bs4 import BeautifulSoup 
import re
import pymysql
import sys

# db setting
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
else:
    print('資料庫連線失敗')
    exit(0)

# rebuild database
cursor.execute("drop table if exists jkf;")
cursor.execute("CREATE TABLE jkf ( id int(10) unsigned NOT NULL AUTO_INCREMENT, url varchar(255) DEFAULT NULL, title varchar(255) DEFAULT NULL, content text DEFAULT NULL, avatar varchar(255) DEFAULT NULL, PRIMARY KEY (id), UNIQUE KEY url (url) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")
conn.commit()

# 開始蒐一個月內?頁
if 'main1' in sys.argv or len(sys.argv)==1:
    print('爬網址開始...')
    for i in range(10):
        page = i+1
        url = "https://www.jkforum.net/type-1128-1476.html?forumdisplay&typeid=1476&orderby=dateline&dateline=2592000&filter=dateline&typeid=1476&forumdisplay=&orderby=dateline&dateline=2592000&page=%d" % (page)
        resp = requests.get(url)
        if(resp.status_code == 200):
            resp.encoding = 'utf-8'    #轉換編碼至UTF-8
            soup = BeautifulSoup(resp.content, 'html.parser')
            columns = soup.find_all('a',href=re.compile("thread-"))
            sql = 'INSERT INTO `jkf` (`url`,`avatar`) VALUES (%s,%s) ON DUPLICATE KEY UPDATE url=VALUES(url),avatar=VALUES(avatar)'
            args = []
            for i in columns:
                # href
                href = 'https://www.jkforum.net/'+i['href']
                #avatar
                avatar = i.find('img',recursive=False)['src']
                args.append((href,avatar))
            # 批量插入
            try:
                cursor.executemany(sql,args)
                conn.commit()
            except Exception:
                print('第%d頁存入失敗' % (page))
                continue
            else:
                print('第%d頁存入成功' % (page))
        else:
            print('第%d頁狀態碼錯誤' % (page))
            continue
    print('你這個小淫蟲~~')
    # 重整id
    cursor.execute("SET @newid=0")
    cursor.execute("UPDATE jkf SET id = (SELECT @newid:=@newid+ 1)")
    conn.commit()

# 爬文章
if 'main2' in sys.argv or len(sys.argv)==1:
    print('爬內容開始...')
    cursor.execute("select `url` from jkf  order by id ")
    allRes = cursor.fetchall()
    sql = 'INSERT INTO `jkf` (`url`,`title`,`content`) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE url=VALUES(url),title=VALUES(title),content=VALUES(content)'
    args = []
    # print(allRes)
    # exit(0)
    for i in allRes:
        url = i[0]
        resp = requests.get(url)
        if(resp.status_code == 200):
            soup = BeautifulSoup(resp.content, 'html.parser')
            try:
                # success
                title = soup.find('h1').get_text()
                content = soup.find_all('table',class_="view-data",limit=1)[0].get_text(strip=True)
                args.append((url,title,content))
                print("%s完成..." % (url))
            except Exception:
                # fail
                continue
    cursor.executemany(sql,args)
    conn.commit()
    print('親，跑完了~~...')
    input("隨便按鍵退出")

# sandbox
if 'sandbox' in sys.argv:
    # test something...
    print('測試開始')
    cursor.execute("SET @newid=0")
    cursor.execute("UPDATE jkf SET id = (SELECT @newid:=@newid+ 1)")
    conn.commit()


cursor.close()
conn.close()
