


import pandas as pd
import requests 
from bs4 import BeautifulSoup
import datetime
import numpy as np
import psycopg2
import time
import sys




def get_data(con='australia'):
    url='https://tradingeconomics.com/'+con+'/calendar'
    html=requests.get(url)
    ori=BeautifulSoup(html.text, "lxml")
    global table
    table=ori.findAll('table',{'id':'calendar'})
    rawdata=pd.read_html(str(table[0]).replace('thead','tr'))[0]
    rawdata1=rawdata.dropna(axis=0,how='any',thresh=2)
    rawdata1=rawdata1.drop_duplicates()
    rawdata1=rawdata1.fillna('無數據')
    rawdata1.index=range(0,len(rawdata1),1)
    return rawdata1




def run_insert(rawdata1):
    for i in range(len(rawdata1)):
        if rawdata1.loc[i,1]=='Actual':
            dealtime=rawdata1.loc[i,0].split(' ')
            weekday=dealtime[0]
            tempday=datetime.date(int(dealtime[3]),convertmon(dealtime[1]),int(dealtime[2]))
        else:
            timeinday=convertime(rawdata1.loc[i,0])
            #print(tempday.year,tempday.month,tempday.day,int(timeinday.split(':')[0]),int(timeinday.split(':')[1]))
            if int(timeinday.split(':')[0])==24:
                realtime=datetime.datetime(tempday.year,tempday.month,tempday.day,0,int(timeinday.split(':')[1]))   
            else:
                realtime=datetime.datetime(tempday.year,tempday.month,tempday.day,int(timeinday.split(':')[0]),int(timeinday.split(':')[1]))
            realtime=realtime+datetime.timedelta(hours=8)
            day=realtime.strftime("%Y%m%d")
            taiwantime=realtime.strftime("%H:%M")
            country=rawdata1.loc[i,1]
            dataname=rawdata1.loc[i,4]
            actual=rawdata1.loc[i,5]
            previous=rawdata1.loc[i,6]
            consens=rawdata1.loc[i,7]
            forecast=rawdata1.loc[i,8]
            insert_value(day,weekday,taiwantime,country,dataname,actual,previous,consens,forecast)



def convertmon(month):
    if month=='February':
        number=2
    elif month=='January':
        number=1
    elif month=='March':
        number=3
    elif month=='April':
        number=4
    elif month=='May':
        number=5
    elif month=='June':
        number=6
    elif month=='July':
        number=7
    elif month=='August':
        number=8
    elif month=='September':
        number=9
    elif month=='October':
        number=10
    elif month=='November':
        number=11
    elif month=='December':
        number=12
    return number


def convertime(time):
    #time='12:30 AM'
    #print(time)
    try:
        number=time.split(' ')[0]
        AMPM=time.split(' ')[1]
        if AMPM=='AM':
            number=number.replace('12:','00:')
            hour=number.split(':')[0]
            minute=number.split(':')[1]
        else:
            hour=str(int(number.split(':')[0])+12)
            minute=number.split(':')[1]
        #print(hour+':'+minute)
        return hour+':'+minute
    except IndexError:
        return '00:00'

def insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9):
    conn=psycopg2.connect(database="postgres",user="quant",password="quant",host="172.27.110.104",port="5432")
    cur=conn.cursor()
    insert_str="insert into econ_calendar(日期,weekday,時間,國家,數據名稱,actual,previous,consensus,forecast)"
    #print(a1)
    values_str=" Values('"+str(a1)+"','"+str(a2)+"','"+str(a3)+"','"+str(a4)+"','"+str(a5)+"','"+str(a6)+"','"+str(a7)+"','"+str(a8)+"','"+str(a9)+"')"
    try:
        #print(insert_str+values_str)
        cur.execute(insert_str+values_str)
        conn.commit()
    except psycopg2.IntegrityError:
        update_value(a1,a2,a3,a4,a5,a6,a7,a8,a9)


def update_value(a1,a2,a3,a4,a5,a6,a7,a8,a9):
    conn=psycopg2.connect(database="postgres",user="quant",password="quant",host="172.27.110.104",port="5432")
    cur = conn.cursor()
    str1="UPDATE econ_calendar SET "
    str2="weekday='"+str(a2)+"',時間='"+str(a3)+"',actual='"+str(a6)+"',previous='"+str(a7)+"',consensus='"+str(a8)+"',forecast='"+str(a9)+"'"
    str3=" where 日期='"+str(a1)+"' AND 國家='"+str(a4)+"' AND 數據名稱='"+str(a5)+"'"
    cur.execute(str1+str2+str3);
    conn.commit()




def update_import(a1,a2,a3,a4,a5,a6,a7):
    conn=psycopg2.connect(database="postgres",user="quant",password="quant",host="172.27.110.104",port="5432")
    cur = conn.cursor()
    if a4=='':
        a4='無數據'
    if a5=='':
        a5='無數據'
    if a6=='':
        a6='無數據'
    if a7=='':
        a7='無數據'
    str1="UPDATE econ_calendar SET "
    str2="重要度='"+str(a1)+"'"
    #"' AND 數據名稱='"+str(a3)+
    str3=" where 國家='"+str(a2)+"' AND actual='"+str(a4)+"'"
    str4=" AND  previous='"+str(a5)+"' AND consensus='"+str(a6)+"' AND forecast='"+str(a7)+"'"
    #print(str1+str2+str3+str4)
    cur.execute(str1+str2+str3+str4)
    conn.commit()


def deal_important():
    a=table[0]
    first=a.findAll('tr',{'data-id':True})
    for i in range(len(first)):
        if first[i].find('span')['class'][0]=='calendar-date-3':
            important='3'
        elif first[i].find('span')['class'][0]=='calendar-date-2':
            important='2'
        elif first[i].find('span')['class'][0]=='calendar-date-1':
            important='1'    
        #print(important)
        country=(first[i].find('td',{'class':'calendar-iso'})).text
        dataname=(first[i].find('a',{'class':'calendar-event'})).text
        actual=(first[i].find('span',{'id':'actual'})).text
        previous=(first[i].find('span',{'id':'previous'})).text
        consensus=(first[i].find('span',{'id':'consensus'})).text
        forecast=(first[i].find('span',{'id':'forecast'})).text
        update_import(important,country,dataname,actual,previous,consensus,forecast)
        #print(important,country,dataname)



country=['united-states','australia','canada','new-zealand']
#if (len(sys.argv)==2):
#    if sys.argv[1]=='AUD':
#        data=get_data('australia')
#    elif sys.argv[1]=='USD':
#        data=get_data('united-states')
#    elif sys.argv[1]=='CAD':
#        data=get_data('canada')
#    elif sys.argv[1]=='NZD':
#        data=get_data('new-zealand')		
#    run_insert(data)
#    deal_important()
#    print(sys.argv[1]+" 數據下載成功")
#else:
#    print("Errors, please infor Quant team")
for co in country:
    try:
        data=get_data(co)
        run_insert(data)
        deal_important()
        print(co+" 數據下載成功")
    except:
        print(co+" 數據下載失敗")
