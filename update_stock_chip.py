

import requests
from bs4 import BeautifulSoup
import psycopg2
import time
from get_stockid import *
from requests.auth import HTTPProxyAuth



def insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15):
    if(a15==""):
        a15="-1" 
    conn = psycopg2.connect(database="equity", user="quant", password="quant", host="172.27.110.104", port="5432")
    cur = conn.cursor()      
    try:
        insert_str="INSERT INTO stck_week_chip (id,name,資料日期,集保總張數,總股東人數,每人平均張數,大於400張大股東持有張數,大於400張大股東持有百分比,大於400張大股東人數,介於400到600張人數,介於600到800張人數,介於800到1000張人數,大於1000張股東人數,大於1000張大股東持有百分比,收盤價) "
        value_str="VALUES ('" + a1 + "','" + a2 + "','" + a3 + "'," + a4 +"," + a5 +"," + a6 +"," + a7 +"," + a8 +"," + a9 +"," + a10 +"," + a11 +"," + a12 +"," + a13 +"," + a14 +"," + a15 +")"
        print(value_str)
        cur.execute(insert_str + value_str);
        conn.commit()
    except psycopg2.IntegrityError:
        print('資料已存在')

def get_soup(id_s):
    time.sleep(5)
	#stockid[j]=3260
    url='http://norway.twsthr.info/StockHolders.aspx'
    payload={'stock':id_s}
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    proxies = {"http":"c700wcg.esunbank.com.tw:8080"}
    auth = HTTPProxyAuth("sjoejoejoejoes-15923","O100221816")
    ori=requests.post(url,data=payload,headers=header,proxies=proxies,auth=auth)
    content=BeautifulSoup(ori.text,"html5lib")
    title=content.find('title').text
    if(title =='Proxy Authorization Required'):
        print('407發生了!!!')
        time.sleep(20)
        ori=get_soup(id_s)
    return ori


def run_insert(ori,n):
    n2=1+n*2
    try:
        stockname=ori.findAll('p')[0].text.split()[1]
        table=ori.findAll('table',{'cellpadding':'2'},{'cellspacing':'0'})[0]
        if stockname=='"趨吉避凶"，整理股權資料的最佳工具！':
            print('神秘金字塔沒資料')
        for i in range(1,n2,2):    
            tr = table.findAll('tr')[i]
            a=[]
            for td in tr.findAll('td')[2:-1]:
                a.append(td.text.replace(',','').replace('\xa0',''))
            if a==[]:
                break
            elif len(a[0])==8:
                insert_value(stockid[j],stockname,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11],a[12])
                print(stockid[j],stockname,a)
            else:
                print("資料已充分")            
    except IndexError:
        print('神秘金字塔沒資料')

    
    



stockid=get_stockid()


for j in range(0,len(stockid),1):
    print(j,len(stockid),stockid[j])
    content=get_soup(stockid[j])
    ori=BeautifulSoup(content.text, "html5lib")
    run_insert(ori,2)



