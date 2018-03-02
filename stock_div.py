import requests
from bs4 import BeautifulSoup
import psycopg2
import time
from requests.auth import HTTPProxyAuth
from get_stockid import *

def get_soup(id):
    time.sleep(10)
    url='http://goodinfo.tw/StockInfo/StockDividendSchedule.asp'
    payload={
        'STOCK_ID':id}
    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    proxies={"http":"c700wcg.esunbank.com.tw:8080"}
    auth=HTTPProxyAuth("sjoejoejoejoes-15923","O100221816")
    ori=requests.post(url,data=payload,headers=header)
    ori.encoding='Big-5'
    content=BeautifulSoup(ori.text, "html5lib")
    title=content.find('title')
    body=content.find('body')
    if (str(title)=='<title>Proxy Authorization Required</title>'):
        print('407發生了')
        time.sleep(40)
        content=get_soup(id)
    if (str(body)=='<body>您的瀏覽量異常, 已影響網站速度, 目前暫時關閉服務, 請稍後再重新使用<br/>若您是使用程式大量下載本網站資料, 請適當調降程式查詢頻率, 以維護一般使用者的權益</body>'):
        print('網站檔我')
        time.sleep(800)
        content=get_soup(id)
    return content

def insert_value2(str1):
    conn=psycopg2.connect(database="equity",user="quant",password="quant",host="172.27.110.104",port="5432")
    cur=conn.cursor()
    try:
        cur.execute(str1)
        #print(str1)
    except psycopg2.IntegrityError:
        print('資料已存在')
    conn.commit()

def insert_str_com(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18):
    a3=a3[0:10]
    a4=a4[0:10]
    a6=a6[0:10]
    a8=a8[0:10]
    n=(a3!='')+(a4!='')+(a6!='')+(a8!='')-1
    a=[a3,a4,a6,a8,a1,a2,a5,a7,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18]
    b=['股東會日期','除息交易日','除權交易日','現金股利發放日','盈餘所屬年度','股利發放年度','除息參考價','除權參考價','現金股利盈餘','現金股利公積','現金股利合計','股票股利盈餘','股票股利公積','股票股利合計','股利合計','發放年度平均股價','年均殖利率','id']
    str_head="insert into 台股除權息日程表("
    str_tail=")values('"
    #+a1+"','"+a2+"','"+a3+"','"+a4+"','"+a5+"','"+a6+"','"+a7+"')"
    j=0
    for i in range(0,len(a),1):
        if(n==-1 and j==0):
            str_tail=str_tail[0:8]
            j=j+1
        elif(a[i]!='' and j<n):
            str_head=str_head+b[i]+","
            str_tail=str_tail+a[i]+"','"
            j=j+1
            #print(str_head+str_tail)
        elif(a[i]!='' and j==n):
            str_head=str_head+b[i]+","
            str_tail=str_tail+a[i]+"',"
            j=j+1
            #print(str_head+str_tail)
        elif(a[i]!=''and i!=(len(a)-1) and j>n):
            str_head=str_head+b[i]+","
            str_tail=str_tail+a[i]+","
            j=j+1
            #print(str_head+str_tail)
        elif(i==(len(a)-1)):
            str_head=str_head+b[i]
            str_tail=str_tail+a[i]+")"
            #print(str_head+str_tail)
    total_str=str_head+str_tail
    return total_str

stockid=get_stockid()

for i in range(0,len(stockid),1):
    content=get_soup(stockid[i])
    table =content.find('table',{'class':'solid_1_padding_3_3_tbl'})
    for row in range(0,5,1):
        row='row'+str(row)
        for tr in table.find_all('tr',{'id':row}):
            a=[]
            for td in tr.find_all('td'):
                a.append(td.text)
        exestr=insert_str_com(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11],a[12],a[13],a[14],a[15],a[16],stockid[i])
        print(exestr)
        insert_value2(exestr)