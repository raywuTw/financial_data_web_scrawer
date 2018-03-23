
# coding: utf-8

# In[1]:


import pandas as pd 
import datetime
import time
import psycopg2
import requests
from bs4 import BeautifulSoup


# In[2]:


def tsec_get_data(days):
    #days=datetime.date.today().strftime("%Y%m%d")
    url='http://www.tse.com.tw/exchangeReport/BWIBBU_d?response=html&date='+days+"'&selectType=ALL"
    a=pd.read_html(url)
    data=a[0]
    if len(data.columns)==7:
        data.columns=['證券代號','證券名稱','殖利率','股利年度','本益比','股價淨值比','財報年_季']
    else:
        data.columns=['證券代號','證券名稱','本益比','殖利率','股價淨值比']
    return data


# In[3]:


def otc_get_data(days):
    #days=datetime.date.today().strftime("%Y%m%d")
    day=str(int(days[0:4])-1911)+'/'+days[4:6]+'/'+days[6:]
    url="http://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/pera_result.php?l=zh-tw&o=htm&d="+day+"&c=&s=0,asc"
    res=requests.get(url)
    soup=BeautifulSoup(res.text, "lxml")
    a=pd.read_html(str(soup.find('table')))
    data=a[0]
    data=data.dropna(axis=0,thresh=3)
    data.index=range(len(data))
    data.columns=['證券代號','證券名稱','本益比','每股股利','殖利率','股價淨值比']
    return data


# In[4]:


def tsec_insert_value(a1,a2,a3,a4,a5,a6,a7,a8):
    conn = psycopg2.connect(database="equity", user="quant", password="quant", host="localhost", port="5432")
    cur = conn.cursor()
    insert_str="INSERT INTO 個股殖利率與本益比 (日期,證券代號,證券名稱,殖利率,股利年度,本益比,股價淨值比,財報年_季)"
    value_str=" VALUES ('"+str(a1) +"','" + str(a2) + "', '" + str(a3) +"'," + str(a4)+", " + str(a5) +"," + str(a6) + "," + str(a7) +",'" + str(a8)+ "')"
    #print(insert_str+value_str)
    try :
        cur.execute(insert_str+value_str)
    except psycopg2.IntegrityError:
        pass
    conn.commit()


# In[5]:


def otc_insert_value(a1,a2,a3,a4,a5,a6,a7):
    conn = psycopg2.connect(database="equity", user="quant", password="quant", host="localhost", port="5432")
    cur = conn.cursor()
    insert_str="INSERT INTO 個股殖利率與本益比 (日期,證券代號,證券名稱,本益比,每股股利,殖利率,股價淨值比)"
    value_str=" VALUES ('"+a1 +"','" + a2 + "', '" + str(a3) +"'," + str(a4)+", " + str(a5) +"," + str(a6) + "," + str(a7) + ")"
    try :
        cur.execute(insert_str+value_str)
    except psycopg2.IntegrityError:
        pass
    conn.commit()


# In[6]:


def run_tsec(day):
    a1=day       
    data=tsec_get_data(day)
    for i in range(len(data)):
        a2=data.loc[i,'證券代號']
        a3=data.loc[i,'證券名稱']
        a4=data.loc[i,'殖利率']
        try:
            a5=data.loc[i,'股利年度']
        except:
            a5=int(day[0:4])-1912
        a6=data.loc[i,'本益比']
        if a6=='-':
            a6=-1
        a7=data.loc[i,'股價淨值比']
        if str(a7)=='-':
            a7=-1
        try:
            a8=data.loc[i,'財報年_季']
        except:
            a8='---'
        #print(a1,a2,a3,a4,a5,a6,a7,a8) 
        tsec_insert_value(a1,a2,a3,a4,a5,a6,a7,a8)
    #print(a1,a2,a3,a4,a5,a6,a7,a8)


# In[7]:


def run_otc(day):
    a1=day
    data=otc_get_data(day)
    for i in range(len(data)):
        a2=data.loc[i,'證券代號']
        a3=data.loc[i,'證券名稱']
        a4=data.loc[i,'本益比']
        if str(a4)=='nan':
            a4=-1
        a5=data.loc[i,'每股股利']
        if str(a5)=='nan':
            a5=-1
        a6=data.loc[i,'殖利率']
        a7=data.loc[i,'股價淨值比']
        if str(a7)=='nan':
            a7=-1
        otc_insert_value(a1,a2,a3,a4,a5,a6,a7)
    #print(a1,a2,a3,a4,a5,a6,a7)


# In[8]:


today=datetime.date.today().strftime("%Y%m%d")
begindate=datetime.date(2016,1,4)


# In[ ]:


day=begindate.strftime("%Y%m%d")
while day!=today:
    day=begindate.strftime("%Y%m%d")
    try:
        run_tsec(day)
    except ValueError:
        pass
    try:
        run_otc(day)
    except ValueError:
        pass    
    begindate=begindate+datetime.timedelta(days=1)
    print(day)
    time.sleep(8)

