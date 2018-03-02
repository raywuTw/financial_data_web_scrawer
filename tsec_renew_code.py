#!/usr/bin/python3
# coding: utf-8
import requests
from bs4 import BeautifulSoup
import psycopg2
import time
import datetime
import sys

def count_it():
    cursor = conn.cursor()
    cursor.execute("select count(id) from 上市股票代碼")
    arr=cursor.fetchall()
    conn.commit()
    return str(arr[0][0])

def insertdb(a,b):
    cursor = conn.cursor()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("insert into 上市股票代碼(id, name, insert_dt) values ('" + a + "','" + b + "','" + timestamp + "')")
    conn.commit()

def trancated():
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE 上市股票代碼")
    conn.commit()

def get_soup(catogory):
    payload={
    'tse':'1',
    'cat':catogory,
    'form':'menu',
    'form_id':'stock_id',
    'form_name':'stock_name',
    'domain':'0'
    }
    res1=requests.post(url,headers=head,data=payload)
    if(sys.platform=='linux'):
        soup1=BeautifulSoup(res1.text, "lxml")
    else:
        soup1=BeautifulSoup(res1.text, "html5lib")
    return soup1
	
def parser(sp):
    table1=sp.findAll('table')[5]
    dd=[]
    for a in table1.findAll('a',{'class':'none'}):
        dd=a.text.replace('\n','').split(' ')
        if(dd[0]=='6285'):
            dd[1]='啟碁'
        #print(dd[0] + ',' + dd[1])
        try:
            if(len(str(dd[0]))==4):
                insertdb(str(dd[0]),str(dd[1]))
        except:
            print("insert 上市股票代碼 occurs problem! pls check: " + dd[0])

def get_all_catogories():
    global url,head
    url="https://tw.stock.yahoo.com/h/kimosel.php"
    head={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}			
    
    res=requests.get(url,headers=head)
    if(sys.platform=='linux'):
        soup=BeautifulSoup(res.text, "lxml")
    else:
        soup=BeautifulSoup(res.text, "html5lib")
    classify=[]
    table=soup.findAll('table')[4]
    for td in table.findAll('td'):
        if(td.text!='上市' and td.text!='上櫃' and td.text!='存託憑證' and td.text!='ETF' and td.text!='受益證券' and td.text!='市認購' and td.text!='市認售' and td.text!='指數類' and td.text!='市牛證' and td.text!='市熊證'):
            classify.append(td.text)
            #print(td.text)
	
    return classify
	
conn = psycopg2.connect(host='localhost',port='5432', database='equity', user='quant', password='quant')
isSucceed=False
while(isSucceed==False):
    trancated()
    try:
        all_catogory=get_all_catogories()
        for ct in all_catogory:
            #time.sleep(5)
            sub_soup=get_soup(ct)
            parser(sub_soup)
        print("exists " + count_it() + " records right now")
        isSucceed=True
    except:
        print("Something wrong!!!")
conn.close()
