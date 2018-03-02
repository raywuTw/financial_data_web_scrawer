#!/usr/bin/python3
# coding: utf-8
import requests
from bs4 import BeautifulSoup
import psycopg2
import time
import sys

def count_it():
    cursor = conn.cursor()
    cursor.execute("select count(id) from 上櫃股票代碼")
    arr=cursor.fetchall()
    conn.commit()
    return str(arr[0][0])

def insertdb(a,b,c):
    cursor = conn.cursor()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("insert into 上櫃股票代碼(id, name, insert_dt, note) values ('" + a + "','" + b + "','" + timestamp + "','" + c + "')")
    conn.commit()

def trancated():
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE 上櫃股票代碼")
    conn.commit()

def get_soup(types):
    url="http://www.tpex.org.tw/web/regular_emerging/corporateInfo/regular/regular_stock.php"
    payload={
        'stk_code':'',
        'stk_category':'02',
        'choice_type':'stk_type',
        'stk_type':types
    }
    res=requests.post(url,data=payload)
    res.encoding='big-5'
    if(sys.platform=='linux'):
        soup=BeautifulSoup(res.text, "lxml")
    else:
        soup=BeautifulSoup(res.text, "html5lib")
    return soup	
	
def parser(local_soup):
    tbody=local_soup.findAll('table')[0].findAll('tbody')[0]
    for tr in tbody.findAll('tr'):
        a1=tr.findAll('td')[0].text                    #id
        a2=tr.findAll('td')[1].text.replace('*','')    #name
        a3=tr.findAll('td')[3].text                    #產業別
        if(a1=='6506'):
            a2='雙邦'
        #print(a1 + ',' + a2 + ',' +a3)
        try:
            insertdb(a1,a2,a3)
        except:
            print("insert 上櫃股票代碼 occurs problem! pls check: " + a1)

stk_types=['','RR']
conn = psycopg2.connect(host='localhost',port='5432', database='equity', user='quant', password='quant')
trancated()
for stk_type in stk_types:
    soup=get_soup(stk_type)
    parser(soup)
print("exists " + count_it() + " records right now")
conn.close()
