
# coding: utf-8

# In[236]:


import requests
import pandas as pd
from bs4 import BeautifulSoup
import psycopg2
import time
import datetime
import json
import warnings


# In[3]:


def insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13):
    conn=psycopg2.connect(database="postgres",user="quant",password="quant",host="localhost",port="5432")
    cur=conn.cursor()
    a14=time.strftime("%x %X" )
    insert_str="insert into funding_rate(bank,ccys,date,活期,一週,兩週,三週,一月,三月,六月,九月,一年,放款利率,更新時間)"
    values_str1="VALUES('"+a1+"','"+a2+"','"+a3+"','"+a4+"','"+a5+"','"+a6+"','"+a7+"','"+a8+"',"
    values_str2="'"+a9+"','"+a10+"','"+a11+"','"+a12+"','"+a13+"','"+a14+"')"
    str1=insert_str+values_str1+values_str2
    try:
        cur.execute(insert_str+values_str1+values_str2)
        conn.commit()
    except psycopg2.IntegrityError:
        update_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
        #conn.commit()


# In[204]:


def update_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13):
    conn=psycopg2.connect(database="postgres",user="quant",password="quant",host="localhost",port="5432")
    cur=conn.cursor()
    a14=time.strftime("%x %X" )
    update_str="UPDATE funding_rate SET "
    set_str1="活期='"+a4+"',"+"一週='"+a5+"',"+"兩週='"+a6+"',"+"三週='"+a7+"',"+"一月='"+a8+"',"+"三月='"+a9+"',"+"六月='"+a10+"',"
    set_str2="九月='"+a11+"',"+"一年='"+a12+"',"+"放款利率='"+a13+"',"+"更新時間='"+a14+"'"
    where_str="WHERE bank ='"+a1+"' AND ccys='"+a2+"'AND date='"+a3+"'"
    cur.execute(update_str+set_str1+set_str2+where_str)
    conn.commit()


# In[205]:


def get_pd_html(url):
    try:
        a=pd.read_html(url)
    except requests.ConnectionError:
        time.sleep(10)
        print('407發生')        
        a=get_pd_html(url)
    except URLError:
        time.sleep(10)
        print('407發生')
        res=get_requests(url)
    return a


# In[206]:


def get_requests(url):
    header={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}
    try:
        res=requests.get(url,headers=header,verify=False)
    except requests.ConnectionError:
        time.sleep(10)
        print('407發生')
        res=get_requests(url)
    return res
    


# In[238]:


#台灣銀行存款
def get_twbank_deposit_rate():
    url="http://rate.bot.com.tw/ir?Lang=zh-TW"
    a=get_pd_html(url)
    for i in range(0,len(a[0]),1):
        a1='台灣銀行'
        a2=str(a[0].ix[i,0])
        a3=time.strftime("%F")
        a4=str(a[0].ix[i,1])
        a5=str(a[0].ix[i,2])
        a6=str(a[0].ix[i,3])
        a7=str(a[0].ix[i,4])
        a8=str(a[0].ix[i,5])
        a9=str(a[0].ix[i,6])
        a10=str(a[0].ix[i,7])
        a11=str(a[0].ix[i,8])
        a12=str(a[0].ix[i,9])
        a13="---"
        insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
    twbank_lendrate()
    print(a1+a3+'更新成功')
        #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)


# In[239]:


def update_value_lendrate(a1,a2,a3,a4):
    conn=psycopg2.connect(database="postgres",user="quant",password="quant",host="localhost",port="5432")
    cur=conn.cursor()
    a5=time.strftime("%x %X" )
    update_str="UPDATE funding_rate SET "
    set_str="放款利率='"+a4+"',"+"更新時間='"+a5+"'"
    where_str="WHERE bank ='"+a1+"' AND ccys='"+a2+"'AND date='"+a3+"'"
    cur.execute(update_str+set_str+where_str)
    conn.commit()


# In[240]:


def twbank_lendrate():
    url="http://rate.bot.com.tw/use/obu?Lang=zh-TW"
    a=get_pd_html(url)
    for i in range(0,len(a[0]),1):
        a1='台灣銀行'
        a2=str(a[0].ix[i,0])
        a3=time.strftime("%F")
        a4=str(a[0].ix[i,1])
        a5=str(a[0].ix[i,2])
        a6=str(a[0].ix[i,3])
        if a4!='-'and a4!='nan':
        #print(a1,a2,a3,a4)
            update_value_lendrate(a1,a2,a3,a4)
        if a6!="-"and a6!='nan':
        #print(a1,a5,a3,a6)
            update_value_lendrate(a1,a5,a3,a6)


# In[241]:


#第一銀行匯率
def get_firstbank_deposit_rate():   
    ccysname=["美金 (USD)","英鎊 (GBP)","港幣 (HKD)","澳幣 (AUD)","新加坡幣 (SGD)","瑞士法郎 (CHF)","加拿大幣 (CAD)","日圓 (JPY)","南非幣 (ZAR)"
          ,"瑞典幣 (SEK)","泰銖 (THB)","紐元 (NZD)","歐元 (EUR)","人民幣 (CNY)","土耳其幣(TRY)"]
    url="https://ibank.firstbank.com.tw/NetBank/7/0103.html?sh=none"
    a=get_pd_html(url)
    for i in range(0,len(a[4])-2,1):
        a1='第一銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(a[4].ix[i+2,1])
        a5=str(a[4].ix[i+2,2])
        a6=str(a[4].ix[i+2,3])
        a7=str(a[4].ix[i+2,4])
        a8=str(a[4].ix[i+2,5])
        a9=str(a[4].ix[i+2,6])
        a10=str(a[4].ix[i+2,7])
        a11=str(a[4].ix[i+2,8])
        a12=str(a[4].ix[i+2,9])
        a13="---"
        #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
        insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
    firstbank_lendrate()
    print(a1+a3+'更新成功')


# In[242]:


def firstbank_lendrate():    
    ccysname=["美金 (USD)","英鎊 (GBP)","港幣 (HKD)","澳幣 (AUD)","新加坡幣 (SGD)","瑞士法郎 (CHF)","加拿大幣 (CAD)","日圓 (JPY)","南非幣 (ZAR)"
      ,"瑞典幣 (SEK)","泰銖 (THB)","紐元 (NZD)","歐元 (EUR)","人民幣 (CNY)","土耳其幣(TRY)"]
    url="https://ibank.firstbank.com.tw/NetBank/7/0205.html?sh=none"
    a=get_pd_html(url)
    for i in range(0,len(a[4])-6,1):
        a1='第一銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        if i==0:
            a4=str(a[4].ix[i+1,2])
        else:
            a4=str(a[4].ix[i+6,2])
        if a4!='-'and a4!='nan':
            #print(a1,a2,a3,a4)
            update_value_lendrate(a1,a2,a3,a4)


# In[243]:


#富邦銀行
def get_fubon_deposit_rate():   
    ccysname=["美金 (USD)","澳幣 (AUD)","南非幣 (ZAR)","人民幣 (CNY)","日圓 (JPY)","歐元 (EUR)","紐元 (NZD)",
              "英鎊 (GBP)","加拿大幣 (CAD)","港幣 (HKD)","新加坡幣 (SGD)","瑞典幣 (SEK)","泰銖 (THB)","瑞士法郎 (CHF)"]   
    url="https://ebank.taipeifubon.com.tw/B2C/cfhqu/cfhqu013/CFHQU013_Home.faces?menuId=CFH0302&menuId=CFH0302&showLogin=true&popupMode=true&popupMode=true&frameMode=false&frameMode=false#"
    a=get_pd_html(url)
    for i in range(0,len(a[0])-3,1):
        a1='台北富邦銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(a[0].ix[i+3,1])
        a5=str(a[0].ix[i+3,2])
        a6=str(a[0].ix[i+3,3])
        a7=str(a[0].ix[i+3,4])
        a8=str(a[0].ix[i+3,5])
        a9=str(a[0].ix[i+3,6])
        a10=str(a[0].ix[i+3,7])
        a11=str(a[0].ix[i+3,8])
        a12=str(a[0].ix[i+3,9])
        a13="---"
        #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
        insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
    print(a1+a3+'更新成功')


# In[244]:


#玉山銀行
def get_esun_deposit_rate():   
    ccysname=["美金 (USD)","人民幣 (CNY)", "澳幣 (AUD)","南非幣 (ZAR)","紐元 (NZD)","歐元 (EUR)","港幣 (HKD)","日圓 (JPY)",
              "墨西哥披索 (MXN)","加拿大幣 (CAD)","瑞士法郎 (CHF)","英鎊 (GBP)","瑞典幣 (SEK)","新加坡幣 (SGD)","泰銖 (THB)"]   
    url="https://www.esunbank.com.tw/bank/personal/deposit/rate/foreign/deposit-rate"
    a=get_pd_html(url)
    for i in range(0,len(a[0])-2,1):
        a1='玉山銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(a[0].ix[i+2,1]).replace('nan','-')
        a5=str(a[0].ix[i+2,2]).replace('nan','-')
        a6=str(a[0].ix[i+2,3]).replace('nan','-')
        a7=str(a[0].ix[i+2,4]).replace('nan','-')
        a8=str(a[0].ix[i+2,5]).replace('nan','-')
        a9=str(a[0].ix[i+2,6]).replace('nan','-')
        a10=str(a[0].ix[i+2,7]).replace('nan','-')
        a11=str(a[0].ix[i+2,8]).replace('nan','-')
        a12=str(a[0].ix[i+2,9]).replace('nan','-')
        a13="---"
        
        #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
        insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
    esunbank_lendrate()
    print(a1+a3+'更新成功')


# In[245]:


def esunbank_lendrate():    
    ccysname=["美金 (USD)", "澳幣 (AUD)","歐元 (EUR)","日圓 (JPY)","瑞士法郎 (CHF)","瑞典幣 (SEK)","泰銖 (THB)"]    
    ccysnames=["人民幣 (CNY)","南非幣 (ZAR)","港幣 (HKD)","加拿大幣 (CAD)","英鎊 (GBP)","新加坡幣 (SGD)"]
    url="https://www.esunbank.com.tw/bank/personal/deposit/rate/foreign/loan-rate"
    a=get_pd_html(url)
    for i in range(0,len(a[0])-1,1):
        a1='玉山銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        if i==0:
            a4=str(a[0].ix[i+1,1])
        else:
            a4=str(a[0].ix[i+1,1])
        if a4!='-'and a4!='nan':
            #print(a1,a2,a3,a4)
            update_value_lendrate(a1,a2,a3,a4)
    for i in range(0,len(a[1])-2,1):
        a1='玉山銀行'
        a2=ccysnames[i]
        a3=time.strftime("%F")
        if i==0:
            a4=str(a[0].ix[i+1,1])
        else:
            a4=str(a[0].ix[i+1,1])
        if a4!='-'and a4!='NAN':
            #print(a1,a2,a3,a4)
            update_value_lendrate(a1,a2,a3,a4)


# In[246]:


#國泰世華銀行
def get_cathay_deposit_rate():   
    ccysname=["美金 (USD)","人民幣 (CNY)","港幣 (HKD)","英鎊 (GBP)","瑞士法郎 (CHF)","澳幣 (AUD)","新加坡幣 (SGD)",
              "加拿大幣 (CAD)","瑞典幣 (SEK)","南非幣 (ZAR)","日圓 (JPY)","丹麥幣 (DKK)","泰銖 (THB)","紐元 (NZD)",
              "歐元 (EUR)","土耳其幣(TRY)"]
    url='https://www.cathaybk.com.tw/cathaybk/personal/exchange/product/account/?page=current01#first-tab-04'
    res=get_requests(url)
    content=BeautifulSoup(res.text,"lxml")
    a=content.find('table',{'class':'table-rate'})
    a=get_pd_html(str(a))   
    for i in range(0,len(a[0]),1):
        a1='國泰世華銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(a[0].ix[i,1]).replace('--','-').replace('%','')
        a5=str(a[0].ix[i,2]).replace('--','-').replace('%','')
        a6=str(a[0].ix[i,3]).replace('--','-').replace('%','')
        a7=str(a[0].ix[i,4]).replace('--','-').replace('%','')
        a8=str(a[0].ix[i,5]).replace('--','-').replace('%','')
        a9=str(a[0].ix[i,6]).replace('--','-').replace('%','')
        a10=str(a[0].ix[i,7]).replace('--','-').replace('%','')
        a11=str(a[0].ix[i,8]).replace('--','-').replace('%','')
        a12=str(a[0].ix[i,9]).replace('--','-').replace('%','')
        a13="---"
        #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
        insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
    Cathaybank_lendrate()
    print(a1+a3+'更新成功')


# In[247]:


def Cathaybank_lendrate():    
    ccysname=["美金 (USD)","港幣 (HKD)","英鎊 (GBP)","瑞士法郎 (CHF)","澳幣 (AUD)","新加坡幣 (SGD)", "加拿大幣 (CAD)",
              "瑞典幣 (SEK)","南非幣 (ZAR)","日圓 (JPY)","丹麥幣 (DKK)","泰銖 (THB)","紐元 (NZD)",
              "人民幣 (CNY)","歐元 (EUR)"]    
    url='https://www.cathaybk.com.tw/cathaybk/personal/exchange/product/foreign-loan/foreign-loan/'
    res=get_requests(url)
    content=BeautifulSoup(res.text,"lxml")
    a=content.find('table',{'class':'table-rate'})
    a=get_pd_html(str(a))
    for i in range(0,len(a[0]),1):
        a1='國泰世華銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(a[0].ix[i,1]).replace('%','')
        #print(a1,a2,a3,a4)
        update_value_lendrate(a1,a2,a3,a4)


# In[248]:


#彰化銀行
def get_CHB_deposit_rate():   
    ccysname=["美金 (USD)","英鎊 (GBP)","澳幣 (AUD)","港幣 (HKD)","新加坡幣 (SGD)","加拿大幣 (CAD)","瑞士法郎 (CHF)",
              "南非幣 (ZAR)","瑞典幣 (SEK)","日圓 (JPY)","泰銖 (THB)","歐元 (EUR)","紐元 (NZD)","人民幣 (CNY)"]
    url='https://www.bankchb.com/frontend/G0260G0111.html#'
    a=get_pd_html(url)      
    for i in range(0,len(a[0]),1):
        a1='彰化銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(a[0].loc[i,'活期']).replace('－','-').replace('%','')
        a5=str(a[0].loc[i,'7天']).replace('－','-').replace('%','')
        a6=str(a[0].loc[i,'14天']).replace('－','-').replace('%','')
        a7=str(a[0].loc[i,'21天']).replace('－','-').replace('%','')
        a8=str(a[0].loc[i,'1個月']).replace('－','-').replace('%','')
        a9=str(a[0].loc[i,'3個月']).replace('－','-').replace('%','')
        a10=str(a[0].loc[i,'6個月']).replace('－','-').replace('%','')
        a11=str(a[0].loc[i,'9個月']).replace('－','-').replace('%','')
        a12=str(a[0].loc[i,'1年']).replace('－','-').replace('%','')
        a13=str(a[0].loc[i,'授信']).replace('－','-').replace('%','')
        #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
        insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
    print(a1+a3+'更新成功')


# In[249]:


#兆豐銀行
def get_Mega_deposit_rate():   
    ccysname=["美金 (USD)","港幣 (HKD)","英鎊 (GBP)","澳幣 (AUD)","新加坡幣 (SGD)","瑞士法郎 (CHF)","日圓 (JPY)",
               "加拿大幣 (CAD)","瑞典幣 (SEK)","泰銖 (THB)","紐元 (NZD)","南非幣 (ZAR)","歐元 (EUR)","人民幣 (CNY)"]    
    url='https://ebank.megabank.com.tw/global2/rs/rs04/PRS4020.faces?taskID=PRS400'
    a=get_pd_html(url)    
    for i in range(0,1,1):
        a1='兆豐銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(a[1].ix[i,1]).replace('---','-').replace('%','')
        a5=str(a[1].ix[i,3]).replace('---','-').replace('%','')
        a6=str(a[1].ix[i,4]).replace('---','-').replace('%','')
        a7=str(a[1].ix[i,5]).replace('---','-').replace('%','')
        a8=str(a[1].ix[i,6]).replace('---','-').replace('%','')
        a9=str(a[1].ix[i,7]).replace('---','-').replace('%','')
        a10=str(a[1].ix[i,8]).replace('---','-').replace('%','')
        a11=str(a[1].ix[i,9]).replace('---','-').replace('%','')
        a12=str(a[1].ix[i,10]).replace('---','-').replace('%','')
        a13=str(a[1].ix[15,1]).replace('---','-').replace('%','')
        #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
        insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
    for i in range(1,14,1):
        a1='兆豐銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(a[1].ix[i+1,1]).replace('---','-').replace('%','')
        a5=str(a[1].ix[i+1,3]).replace('---','-').replace('%','')
        a6=str(a[1].ix[i+1,4]).replace('---','-').replace('%','')
        a7=str(a[1].ix[i+1,5]).replace('---','-').replace('%','')
        a8=str(a[1].ix[i+1,6]).replace('---','-').replace('%','')
        a9=str(a[1].ix[i+1,7]).replace('---','-').replace('%','')
        a10=str(a[1].ix[i+1,8]).replace('---','-').replace('%','')
        a11=str(a[1].ix[i+1,9]).replace('---','-').replace('%','')
        a12=str(a[1].ix[i+1,10]).replace('---','-').replace('%','')
        if i==13:
            a13=str(a[1].ix[16,1]).replace('---','-').replace('%','')
        else:
            a13='---'
        #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
        insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
    print(a1+a3+'更新成功')


# In[250]:


#中國信託銀行
def get_CTBC_deposit_rate():   
    ccysname=["美金 (USD)","日圓 (JPY)","港幣 (HKD)","歐元 (EUR)","英鎊 (GBP)","加拿大幣 (CAD)","澳幣 (AUD)","紐元 (NZD)",
              "瑞士法郎 (CHF)","瑞典幣 (SEK)","新加坡幣 (SGD)","泰銖 (THB)","南非幣 (ZAR)","人民幣 (CNY)"]
    
    url='https://www.ctbcbank.com/CTCBPortalWeb/toPage?id=TW_RB_CM_ebank_019001'
    res=get_requests(url)
    content=BeautifulSoup(res.text,"lxml")
    a=content.find_all('table',{'class':'maintable'})
    a=get_pd_html(str(a[1]))   
    for i in range(0,len(a[0])-1,1):
        a1='中國信託'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(a[0].ix[i+1,1]).replace('nan','-').replace('%','')
        a5=str(a[0].ix[i+1,2]).replace('nan','-').replace('%','')
        a6=str(a[0].ix[i+1,3]).replace('nan','-').replace('%','')
        a7=str(a[0].ix[i+1,4]).replace('nan','-').replace('%','')
        a8=str(a[0].ix[i+1,5]).replace('nan','-').replace('%','')
        a9=str(a[0].ix[i+1,6]).replace('nan','-').replace('%','')
        a10=str(a[0].ix[i+1,7]).replace('nan','-').replace('%','')
        a11=str(a[0].ix[i+1,8]).replace('nan','-').replace('%','')
        a12=str(a[0].ix[i+1,9]).replace('nan','-').replace('%','')
        a13="---"
        #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
        insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
    CTBCbank_lendrate()
    print(a1+a3+'更新成功')


# In[251]:


def CTBCbank_lendrate():     
    ccysname=["英鎊 (GBP)","南非幣 (ZAR)","日圓 (JPY)","紐元 (NZD)","瑞典幣 (SEK)","新加坡幣 (SGD)","泰銖 (THB)",
              "美金 (USD)","歐元 (EUR)","瑞士法郎 (CHF)","加拿大幣 (CAD)","澳幣 (AUD)", "港幣 (HKD)"]    
    url='https://www.ctbcbank.com/CTCBPortalWeb/toPage?id=TW_RB_CM_ebank_019001'
    res=get_requests(url)
    content=BeautifulSoup(res.text,"lxml")
    a=content.find_all('table',{'class':'maintable'})
    a=get_pd_html(str(a[3]))
    for i in range(0,1,1):
        a1='中國信託'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(a[0].ix[i+5,3]).replace('%','')
        #print(a1,a2,a3,a4)
        update_value_lendrate(a1,a2,a3,a4)
    for i in range(1,3,1):
        a1='中國信託'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(a[0].ix[i+5,2]).replace('%','')
        #print(a1,a2,a3,a4)
        update_value_lendrate(a1,a2,a3,a4)        
    for i in range(3,7,1):
        a1='中國信託'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(a[0].ix[i+6,2]).replace('%','')
        #print(a1,a2,a3,a4)
        update_value_lendrate(a1,a2,a3,a4)         
    for i in range(7,13,1):
        a1='中國信託'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(a[0].ix[i+7,2]).replace('%','')
        #print(a1,a2,a3,a4)
        update_value_lendrate(a1,a2,a3,a4)         


# In[252]:


#永豐銀行
def get_sinopac_deposit_rate():   
    ccysname=["南非幣 (ZAR)","美金 (USD)","新加坡幣 (SGD)","瑞典幣 (SEK)","紐元 (NZD)","日圓 (JPY)","港幣 (HKD)",
              "英鎊 (GBP)","歐元 (EUR)","人民幣 (CNY)","瑞士法郎 (CHF)","加拿大幣 (CAD)","澳幣 (AUD)"]    
    url='https://mma.sinopac.com/ws/share/rate/ws_interest.ashx?InterestType=NTWD_CURR&Curr=&Cross=genSetCellResult&1504667863330&callback=genSetCellResult&_=1504667863234'   
    res=get_requests(url)
    a=res.text[18:-3]
    jsonobj=json.loads(a)
    data=jsonobj.get("SubInfo")
    a=[]
    b=[]
    namelast=[]
    for i in range(0,len(data),1):
        name=data[i]['DataValue3']
        value=data[i]['DataValue']
        if value=='':
            value='--'
        tenor=data[i]['DataText']
        if i==0:
            b.append(name)
        if namelast==name:
            b.append(value)
        elif namelast==[]:
            b.append(value)
            namelast=name
        else :
            namelast=[]
            a.append(b)
            b=[]        
            b.append(name)
            b.append(value)
    a.append(b)
    b=[]              
    for i in range(0,len(a),1):
        a1='永豐銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4='--'
        a5=str(a[i][1]).replace('--','-').replace('%','')
        a6=str(a[i][2]).replace('--','-').replace('%','')
        a7=str(a[i][3]).replace('--','-').replace('%','')
        a8=str(a[i][4]).replace('--','-').replace('%','')
        a9=str(a[i][5]).replace('--','-').replace('%','')
        a10=str(a[i][6]).replace('--','-').replace('%','')
        a11=str(a[i][7]).replace('--','-').replace('%','')
        a12=str(a[i][8]).replace('--','-').replace('%','')
        a13="---"
        #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
        insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
    get_sinopac_saving()
    sinopac_lendrate()
    print(a1+a3+'更新成功')


# In[253]:


def update_value_savingrate(a1,a2,a3,a4):
    conn=psycopg2.connect(database="postgres",user="quant",password="quant",host="localhost",port="5432")
    cur=conn.cursor()
    a5=time.strftime("%x %X" )
    update_str="UPDATE funding_rate SET "
    set_str="活期='"+a4+"',"+"更新時間='"+a5+"'"
    where_str="WHERE bank ='"+a1+"' AND ccys='"+a2+"'AND date='"+a3+"'"
    cur.execute(update_str+set_str+where_str)
    conn.commit()


# In[254]:


def get_sinopac_saving():
    ccysname=["澳幣 (AUD)","加拿大幣 (CAD)","瑞士法郎 (CHF)","人民幣 (CNY)","歐元 (EUR)","英鎊 (GBP)","港幣 (HKD)"
              ,"日圓 (JPY)","紐元 (NZD)","瑞典幣 (SEK)","新加坡幣 (SGD)","美金 (USD)","南非幣 (ZAR)"]
    url='https://mma.sinopac.com/ws/share/rate/ws_interest.ashx?InterestType=NTWD&Cross=genNTWDResult&1504667864333&callback=genNTWDResult&_=1504667863235'
    res=get_requests(url)
    a=res.text[15:-3]
    jsonobj=json.loads(a)
    depodit=jsonobj.get("SubInfo")
    for i in range(0,len(depodit),1):
        a1='永豐銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(depodit[i]['DataValue2']).replace('%','')
        update_value_savingrate(a1,a2,a3,a4)
        #print(a1,a2,a3,a4)  


# In[255]:


def sinopac_lendrate():    
    ccysname=["南非幣 (ZAR)","美金 (USD)","泰銖 (THB)","新加坡幣 (SGD)","瑞典幣 (SEK)","紐元 (NZD)",
              "日圓 (JPY)","港幣 (HKD)","英鎊 (GBP)","歐元 (EUR)","人民幣 (CNY)","瑞士法郎 (CHF)", "加拿大幣 (CAD)","澳幣 (AUD)"]
    url='https://mma.sinopac.com/ws/share/rate/ws_interest.ashx?InterestType=NTWD_LOAN&Cross=genNTWD_LOANResult&1504745907345&callback=genNTWD_LOANResult&_=1504745882830'
    res=get_requests(url)
    a=res.text[20:-3]
    jsonobj=json.loads(a)
    depodit=jsonobj.get("SubInfo")
    for i in range(0,6,1):
        a1='永豐銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(depodit[i]['DataValue']).replace('%','')
        #print(a1,a2,a3,a4)
        update_value_lendrate(a1,a2,a3,a4)
    for i in range(6,len(depodit)-1,1):
        a1='永豐銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(depodit[i+1]['DataValue']).replace('%','')
        #print(a1,a2,a3,a4)
        update_value_lendrate(a1,a2,a3,a4)


# In[256]:


#華南銀行
def get_hnbc_deposit_rate():
    ccysname=["美金 (USD)","港幣 (HKD)","英鎊 (GBP)","紐元 (NZD)","澳幣 (AUD)","新加坡幣 (SGD)","瑞士法郎 (CHF)",
              "加拿大幣 (CAD)","日圓 (JPY)","瑞典幣 (SEK)", "南非幣 (ZAR)",
              "泰銖 (THB)","歐元 (EUR)","人民幣 (CNY)"]   
    url='http://www.hncb.com.tw/hncb/rest/inRate/imm'
    res=get_requests(url)
    a=res.text[:]
    jsonobj=json.loads(a)
    a=[]
    b=[]
    for i in range(0,len(jsonobj),1):
        a1='華南銀行'
        a2=ccysname[i]
        a3=time.strftime("%F")
        a4=str(jsonobj[i].get("CURRENT_DEPOSIT")).replace('None','-').replace('%','')
        a5=str(jsonobj[i].get("DEPOSIT_1W")).replace('None','-')
        a6=str(jsonobj[i].get("DEPOSIT_2W")).replace('None','-')
        a7=str(jsonobj[i].get("DEPOSIT_3W")).replace('None','-')
        a8=str(jsonobj[i].get("DEPOSIT_1M")).replace('None','-')
        a9=str(jsonobj[i].get("DEPOSIT_3M")).replace('None','-')
        a10=str(jsonobj[i].get("DEPOSIT_6M")).replace('None','-')
        a11=str(jsonobj[i].get("DEPOSIT_9M")).replace('None','-')
        a12=str(jsonobj[i].get("DEPOSIT_1Y")).replace('None','-')
        a13=str(jsonobj[i].get("INTEREST_RATE")).replace('None','-')
        #print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
        insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
    print(a1+a3+'更新成功')


# In[258]:


def update_all_bank():
    try:
        warnings.filterwarnings('ignore')
        get_twbank_deposit_rate()
    except:
        print('台灣銀行更新失敗')
    try:
        warnings.filterwarnings('ignore')
        get_firstbank_deposit_rate()
    except:
        print('第一銀行更新失敗')
    try:
        warnings.filterwarnings('ignore')
        get_fubon_deposit_rate()
    except:
        print('富邦銀行更新失敗')
    try:
        warnings.filterwarnings('ignore')
        get_esun_deposit_rate()
    except:
        print('玉山銀行更新失敗')
    try:
        warnings.filterwarnings('ignore')
        get_cathay_deposit_rate()
    except:
        print('國泰銀行更新失敗')
    try:
        warnings.filterwarnings('ignore')
        get_CHB_deposit_rate()
    except:
        print('彰化銀行更新失敗')
    try:
        warnings.filterwarnings('ignore')
        get_Mega_deposit_rate()
    except:
        print('兆豐銀行更新失敗')
    try:
        warnings.filterwarnings('ignore')
        get_CTBC_deposit_rate()
    except:
        print('中國信託銀行更新失敗')
    try:
        warnings.filterwarnings('ignore')
        get_hnbc_deposit_rate()
    except:
        print('華南銀行更新失敗')
    try:
        warnings.filterwarnings('ignore')
        get_sinopac_deposit_rate()
    except:
        print('永豐銀行更新失敗')


# In[259]:


update_all_bank()


# In[ ]:




