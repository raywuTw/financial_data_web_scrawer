

import requests
from bs4 import BeautifulSoup
import psycopg2
import time
import json
import datetime
from get_stockid import *
from requests.auth import HTTPProxyAuth



def get_soup(date,id):
    payload={
        'response':json,
        'date':date,
        'stockNo':id
    }
    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    proxies = {"http":"c700wcg.esunbank.com.tw:8080"}
    auth = HTTPProxyAuth("sjoejoejoejoes-15923","O100221816")
    ori=requests.post(url,data=payload,headers=header,proxies=proxies,auth=auth)
    time.sleep(2)
    content=ori.text
    content1=BeautifulSoup(ori.text,"html5lib")
    title=content.find('TITLE')
    if(title==7 or str(title)=='<TITLE>internal error - server connection terminated</TITLE>'):
        time.sleep(30)
        print('407發生了')
        #print(content1)
        #print(title)
        content=get_soup(date,id)
    return content



def insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11):
    conn = psycopg2.connect(database='equity', user='quant', password='quant', host='localhost', port="5432")
    cur = conn.cursor()
    insert_str="INSERT INTO stock_price (id,股票,日期,成交股數,成交金額,開盤價,最高價,最低價,收盤價,漲跌價差,成交筆數)"
    #value_str="VALUES ('"a1 +"','"+a2 +"','" + a3 +"',"+ a4 + ','+ a5 +',' + a6 + ',' + a7 +',' + a8+',' + a9+','+ a10 +','+a11 +')'
    value_str="VALUES('"+a1+"','"+a2+"','"+a3+"',"+a4+","+a5+","+a6+","+a7+","+a8+","+a9+","+a10+","+a11+")"
    cur.execute(insert_str+value_str);
    conn.commit()




def autorun(date,id):
    a=get_soup(date,id)
    try:
        jsonobj=json.loads(a)
        if (jsonobj.get('stat')=='很抱歉，沒有符合條件的資料!'):
            print('很抱歉，沒有符合條件的資料!')
        else:
            id=str(jsonobj.get('title')).split(' ')[1]
            name=str(jsonobj.get('title')).split(' ')[2]
            number=jsonobj.get('data')
            for i in range(0,len(number),1):
                a=number[i]
            #    print(a)
                if a[6]=='--':
                    continue
                for d in range(0,len(a),1):
                    a[d]=a[d].replace(',','').replace('106/','2017/').replace('105/','2016/').replace('104/','2015/').replace('X','')
                try:
                    insert_value(id,name,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8])
                    print(id,name,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8])
                except psycopg2.IntegrityError:
                    print('資料已重複')
    except:
        #print(a)
        autorun(date,id)


url='http://www.tse.com.tw/exchangeReport/STOCK_DAY'
stockid=get_stockid_tsec()

	
today=datetime.date.today()
first=today.replace(day=1)
year=time.strftime("%Y")
month=time.strftime("%m")
day=time.strftime("%d")
datatime=[]
today=str(int(year))+str(month)+str(day)
a=first-datetime.timedelta(days=1)
lastmonth=a.strftime("%Y""%m""%d")
datatime=[today]		
datatime.append(lastmonth)	
	
	


for j in range(0,len(stockid),1):
    id_stock= stockid[j]
    for i in range(0,len(datatime),1):
        autorun(datatime[i],id_stock)
        print(j,len(stockid))




