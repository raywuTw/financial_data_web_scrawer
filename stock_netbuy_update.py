
# coding: utf-8

# In[159]:


import pandas as pd
import psycopg2
import time
import datetime
import requests
from bs4 import BeautifulSoup


# In[160]:


def Set():
    global conn,cur,today
    conn = psycopg2.connect(database="equity", user="quant", password="quant", host="localhost", port="5432")
    cur = conn.cursor()
    today=datetime.date.today()


# In[222]:


def get_pandas_(url):
    try:
        data=pd.read_html(url)
        ans=data[0]
    except ValueError:
        ans=[]
    except requests.HTTPError:
        time.sleep(10)
        data=get_pandas_(url)
        ans=data[0]
    except:
        time.sleep(10)
        data=get_pandas_(url)
        ans=data[0]
    return ans


# In[216]:


def get_res_pd(url):
    global ans
    try:
        res=requests.get(url)
        soup=BeautifulSoup(res.text, "lxml")
        table=soup.find('table')
        data=pd.read_html(str(table))
        ans=data[0]
    except requests.HTTPError:
        time.sleep(10)
        ans=get_res_pd(url)
    except ValueError:
        time.sleep(10)
        ans=get_res_pd(url)
    except KeyError:
        time.sleep(10)
        ans=get_res_pd(url)
    return ans


# In[163]:


def insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17):
    insert_str1="INSERT INTO 三大法人交易資訊 (id,日期,股票,外資買進股數,外資賣出股數,外資買賣超股數,投信買進股數,投信賣出股數"
    insert_str2=",投信買賣超股數,自營商買賣超股數,自營商買進股數_自行買賣,自營商賣出股數_自行買賣,自營商買賣超股數_自行買賣,"
    insert_str3="自營商買進股數_避險,自營商賣出股數_避險,自營商買賣超股數_避險,三大法人買賣超股數)"
    value_str1="VALUES('"+str(a1)+"','"+str(a2)+"','"+str(a3)+"',"+str(a4)+','+str(a5)+','+str(a6)+','+str(a7)+','+str(a8)+','+str(a9)+','+str(a10)+','+str(a11)+','+str(a12)+','+str(a13)+','
    value_str2=str(a14)+','+str(a15)+','+str(a16)+','+str(a17)+")"
    #print(insert_str1+insert_str2+insert_str3+value_str1+value_str2)
    #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17)
    try:
        cur.execute(insert_str1+insert_str2+insert_str3+value_str1+value_str2)
    except psycopg2.IntegrityError:
        print(a1,a2,'資料已重複')
    conn.commit()


# In[164]:


#證交所
def tsec_insert_run(day):
    url='http://www.twse.com.tw/fund/T86?response=html&date='+day+'&selectType=ALLBUT0999'
    a=get_pandas_(url)
  #  if a=='無資料':
  #      return a
  #  else:
    for i in range(0,len(a),1):
        a1=a.iloc[i,0] #id
        a2=day #日期
        a3=a.iloc[i,1] #證券名稱
        a4=a.iloc[i,2] #外資買進股數
        a5=a.iloc[i,3] #外資賣出股數
        a6=a.iloc[i,4] #外資買賣超股數
        a7=a.iloc[i,5] #投信買進股數
        a8=a.iloc[i,6] #投信賣出股數
        a9=a.iloc[i,7] #投信買賣超股數
        a10=a.iloc[i,8] #自營商買賣超股數
        a11=a.iloc[i,9] #自營商買進股數(自行買賣)
        a12=a.iloc[i,10]#自營商賣出股數(自行買賣)
        a13=a.iloc[i,11]#自營商買賣超股數(自行買賣)
        a14=a.iloc[i,12]#自營商買進股數(避險)
        a15=a.iloc[i,13]#自營商賣出股數(避險)
        a16=a.iloc[i,14]#自營商買賣超股數(避險)
        a17=a.iloc[i,15]#三大法人買賣超股數
        #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17)
        if len(a1)==4:
            insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17)
    return print(day,'Tsec更新完畢')


# In[212]:


#櫃買中心
def otc_insert_run(day):
    days=str(int(day[0:4])-1911)+"/"+str(day[4:6])+"/"+str(day[6:])
    #print(day)
    url='http://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_print.php?l=zh-tw&se=EW&t=D&d='+days+'&s=0,asc'
    a=get_res_pd(url)
    for i in range(0,len(a),1):
        a1=a.iloc[i,0] #id
        a2=day #日期
        a3=a.iloc[i,1] #證券名稱
        a4=a.iloc[i,2] #外資買進股數
        a5=a.iloc[i,3] #外資賣出股數
        a6=a.iloc[i,4] #外資買賣超股數
        a7=a.iloc[i,5] #投信買進股數
        a8=a.iloc[i,6] #投信賣出股數
        a9=a.iloc[i,7] #投信買賣超股數
        a10=a.iloc[i,8] #自營商買賣超股數
        a11=a.iloc[i,9] #自營商買進股數(自行買賣)
        a12=a.iloc[i,10]#自營商賣出股數(自行買賣)
        a13=a.iloc[i,11]#自營商買賣超股數(自行買賣)
        a14=a.iloc[i,12]#自營商買進股數(避險)
        a15=a.iloc[i,13]#自營商賣出股數(避險)
        a16=a.iloc[i,14]#自營商買賣超股數(避險)
        a17=a.iloc[i,15]#三大法人買賣超股數
        #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17)
        if len(a1)==4:
            insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17)
    return print(day,'otc更新完畢')


# In[166]:


def pastday(n1,n2):
    past=[]
    for i in range(n1,n2,1):
        days=today-datetime.timedelta(days=i)
        temp=days.strftime("%Y%m%d")
        past.append(temp)
    return past
    #print(past)


# In[200]:


Set()


# In[224]:


past=pastday(0,23)


# In[225]:


for i in range(0,len(past),1):
    day=past[i]
    try:
        tsec_insert_run(day)
    except:
        print(day,'更新失敗')
    try:
        otc_insert_run(day)
    except:
        print(day,'更新失敗')

