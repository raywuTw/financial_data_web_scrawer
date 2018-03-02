

import requests
from bs4 import BeautifulSoup
import psycopg2
import time
from get_stockid import *
from requests.auth import HTTPProxyAuth
import pandas as pd
import numpy
import datetime



def insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11):
    conn = psycopg2.connect(database="equity", user="quant", password="quant", host="localhost", port="5432")
    cur = conn.cursor()
    insert_str="INSERT INTO stock_price (id,股票,日期,成交股數,成交金額,開盤價,最高價,最低價,收盤價,漲跌價差,成交筆數"
    value_str=")VALUES ('"+a1 +"','" + a2 + "', '" + a3 + "', " + a4 + ", " + a5 +"," + a6 + "," + a7 +"," + a8+"," + a9+","+ a10 +","+ a11 + ")"
    if a6=='----':
        a6=str(0);a7=str(0);a8=str(0);a9=str(0);a10=str(0);
        insert_str=insert_str+',備註'
        value_str=")VALUES ('"+a1 +"','" + a2 + "', '" + a3 + "', " + a4 + ", " + a5 +"," + a6 + "," + a7 +"," + a8+"," + a9+","+ a10 +","+ a11 +",'"+"今天無交易"+"')"
    if a10=='除息'or a10=='除權'or a10=='除權息':
        a10=str(0);
        insert_str=insert_str+',備註'
        value_str=")VALUES ('"+a1 +"','" + a2 + "', '" + a3 + "', " + a4 + ", " + a5 +"," + a6 + "," + a7 +"," + a8+"," + a9+","+ a10 +","+ a11 +",'"+"除權息"+"')"
    #print(insert_str+value_str)
    cur.execute(insert_str+value_str);
    conn.commit()



def update_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11):
    conn = psycopg2.connect(database="equity", user="quant", password="quant", host="localhost", port="5432")
    cur = conn.cursor()
    #insert_str="UPDATE stock_price set(id,股票,日期,成交股數,成交金額,開盤價,最高價,最低價,收盤價,漲跌價差,成交筆數"
    #value_str=")VALUES ('"+a1 +"','" + a2 + "', '" + a3 + "', " + a4 + ", " + a5 +"," + a6 + "," + a7 +"," + a8+"," + a9+","+ a10 +","+ a11 + ")"
    str1="UPDATE stock_price SET "
    str2="股票='"+a2+"',成交股數="+a4+",成交金額="+a5+",開盤價="+a6+",最高價="+a7+",最低價="+a8+",收盤價="+a9+",漲跌價差="+a10+",成交筆數="+a11
    str3=" where id='"+a1+"' AND 日期='"+a3+"'"
    if a6=='----':
        a6=str(0);a7=str(0);a8=str(0);a9=str(0);a10=str(0);
        str2="股票='"+a2+"',成交股數="+a4+",成交金額="+a5+",開盤價="+a6+",最高價="+a7+",最低價="+a8+",收盤價="+a9+",漲跌價差="+a10+",成交筆數="+a11
        str2=str2+",備註='今天無交易'"
    if a10=='除息'or a10=='除權'or a10=='除權息':
        demo=a10
        a10='0';
        str2="股票='"+a2+"',成交股數="+a4+",成交金額="+a5+",開盤價="+a6+",最高價="+a7+",最低價="+a8+",收盤價="+a9+",漲跌價差="+a10+",成交筆數="+a11
        str2=str2+",備註='"+demo+"'"
    #print(str1+str2+str3)
    cur.execute(str1+str2+str3);
    conn.commit()



def get_content(date):
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    ur1='http://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_print.php?l=zh-tw&d='
    #d=106/02/30
    ur2='&se=EW&s=0,asc,0'
    abc=date[0:3]+'/'+date[3:5]+'/'+date[5:7]
    url=ur1+abc+ur2
    proxies = {"http":"c700wcg.esunbank.com.tw:8080"}
    auth = HTTPProxyAuth("sjoejoejoejoes-15923","O100221816")
    print(url)
    ori=requests.get(url,headers=header,proxies=proxies,auth=auth)
    time.sleep(5)
    soup=BeautifulSoup(ori.text, "html5lib")
    title=soup.find('title')
    if(str(title)=='<title>Proxy Authorization Required</title>'or str(title)=='<title>internal error - server connection terminated</title>'):
        time.sleep(30)
        print('407發生了')
        soup=get_content(date)
    return soup


def get_date():
    conn = psycopg2.connect(database="equity", user="quant", password="quant", host="localhost", port="5432")
    time=pd.read_sql("select DISTINCT 日期 from stock_price order by 日期",conn)
    timeu=[]
    for i in range(0,len(time),1):
        number=str(time.ix[i,'日期'])
        number=int(number.replace('-',''))-19110000
        tim=str(number)
        timeu.append(tim)
    return timeu    


datetime=get_date()
datetime=datetime[-30:]
for i in range(0,len(datetime),1):
    time.sleep(3)
    #a=[]
    #a.append(l)
    soup=get_content(datetime[i])
    a=datetime[i][3:7]
    b=datetime[i][0:3]
    b=b.replace('104','2015').replace('105','2016').replace('106','2017')
    datetime[i]=b+a
    for tr in soup.find_all('tr')[2:-1]:
        td=tr.find_all('td')[0:10]
        l=[td[0].text,td[1].text,datetime[i],td[7].text,td[8].text,td[4].text,td[5].text,td[6].text,td[2].text,td[3].text,td[9].text]
        for h in range(0,len(l),1):
             l[h]=l[h].replace(' ','').replace(',','').replace('+','')
        if len(l[0])==4:
            try:
                insert_value(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10])
                #print(l)
            except psycopg2.IntegrityError:
                update_value(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10])
                print(l,'資料更新')






