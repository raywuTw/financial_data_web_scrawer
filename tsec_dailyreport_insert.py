

import pymongo
import requests
import time
import psycopg2
from bs4 import BeautifulSoup
import pandas as pd



def run_insert_tsec(YYYYMMDD,id,name):
    try:
        file = open('D:\\daily_report\\'+YYYYMMDD+'_'+id+name+'.txt' , 'r',encoding='UTF-8')
        res=file.read()
        soup2=BeautifulSoup(res, "html5lib")
        a=pd.read_html(res)
    except FileNotFoundError:
        name=name.replace('-','')
        file = open('D:\\daily_report\\'+YYYYMMDD+'_'+id+name+'.txt' , 'r',encoding='UTF-8')
        res=file.read()
        soup2=BeautifulSoup(res, "html5lib")
        a=pd.read_html(res)
    except ValueError:
        return print('無資料')
    file.close
    a1=a[2].iloc[0,1]
    a2=a[2].iloc[0,3].split('\xa0')[1]
    a3=a[2].iloc[0,3].split('\xa0')[0]
    for i in range(4,len(a),6):
        for j in range(1,len(a[i]),1):
            a4=str(a[i].iloc[j,1]).replace(' ','')
            if len(a4)!=4:
                a5=a4[4:]
                a4=a4[0:4]
            else:
                a5=branchname(a4)
            a6=str(a[i].iloc[j,2]).replace(' ','')
            a7=str(a[i].iloc[j,3]).replace(' ','')
            a8=str(a[i].iloc[j,4]).replace(' ','')
            a9=str(a[i+1].iloc[j,1]).replace(' ','')
            if len(a9)!=4:
                a10=a9[4:]
                a9=a9[0:4]
            else:
                a10=branchname(a9)
            a11=str(a[i+1].iloc[j,2]).replace(' ','')
            a12=str(a[i+1].iloc[j,3]).replace(' ','')
            a13=str(a[i+1].iloc[j,4]).replace(' ','')           
            branchdeal(a1,a2,a3,a4,a5,a6,a7,a8)
            branchdeal(a1,a2,a3,a9,a10,a11,a12,a13)
    print(a1,a2,a3,a4,a5,a6,a7,a8)

            



from pymongo  import MongoClient


def branchdeal(a1,a2,a3,a4,a5,a6,a7,a8):
    post={"日期":a1,
          "股票":a2,
          "id":a3,
          "劵商分支":a4,
          "劵商分支名稱":a5,
          "成交單價":a6,
          "買進股數":a7,
          "賣出股數":a8
            }
    try:
        post_id=db.daily_report.insert_one(post)
    except pymongo.errors.DuplicateKeyError:
        pass



def branchname(a1):
    select_str="select 劵商分支 from 劵商分支代碼 where 代碼='"+a1+"'"
    a=pd.read_sql(select_str,conn)
    return a.loc[0,'劵商分支']




def Mongoset():
    global client,db,collection
    client=MongoClient('172.27.110.106',27017)
    db=client.jackdb
    collection=db.daily_report
    x= [
        ("劵商分支",1),
        ("日期",1),
        ("id",1),
        ("成交單價",1),
        ("買進股數",1),
        ("賣出股數",1),
   ]

    collection.create_index(
    x,
    unique=True
    )

def stockname(a1,otc):
  #  conn = psycopg2.connect(database='equity', user='quant', password='quant', host='localhost', port='5432')
  #  cur = conn.cursor()
    if otc==False:
        select_str="select name from 上市股票代碼 where id='"+a1+"'"
    else:
        select_str="select name from 上櫃股票代碼 where id='"+a1+"'"
    a=pd.read_sql(select_str,conn)
    return a.loc[0,'name']



global conn,cur
conn = psycopg2.connect(database='equity', user='quant', password='quant', host='localhost', port='5432')
cur = conn.cursor()



string='select A1.id,A1.name from 上市股票代碼 A1,stock_desk_id A2 where A1.id=A2.id'
stockid=pd.read_sql(string,conn)
stockid1=stockid['id'].values.tolist()
stockname=stockid['name'].values.tolist()


date=time.strftime("%Y%m%d")



Mongoset()
for j in range(0,len(date),1):
    for i in range(0,len(stockid1),1):
        run_insert_tsec(date[j],stockid1[i],stockname[i])

