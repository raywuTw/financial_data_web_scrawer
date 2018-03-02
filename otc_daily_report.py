


import requests
from bs4 import BeautifulSoup
import os
import sys
import time
import shutil
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pandas as pd
import psycopg2
import datetime



def reflash():
    global rs,head,gtype,url
    url='http://www.tpex.org.tw/web/stock/aftertrading/broker_trading/brokerBS.php'
    head={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    rs = requests.session()
    res=rs.post(url , headers=head)
    soup=BeautifulSoup(res.text,"lxml")
    try:
        gtype=soup.find('input', {'name':"enname"})['value']
        urlpic='http://www.tpex.org.tw/web/inc/authnum_output.php?n='
        res2=rs.get(urlpic+gtype,headers=head,stream=True)
        f=open('D:\\daily_report\\otc\\ori_code\\CaptchaImage.jpg','wb')
        shutil.copyfileobj(res2.raw,f)
        f.close()
    except TypeError:
        time.sleep(10)
        print('407 or 502')
        reflash()




def pic_deal(image,j):
    kernel=np.ones((1,1),np.uint8)
    erosion=cv2.erode(image,kernel)
    blurred=cv2.GaussianBlur(erosion,(1,1),0)
    edged=cv2.Canny(blurred,30,150)
    kernel1=np.ones((1,1),np.uint8)
    dilation=cv2.dilate(edged,kernel1,iterations=1)
    res=cv2.resize(dilation,(50,50))
    cv2.imwrite("D:\\daily_report\\otc\\alphaset\\%d.png"%(j),res)
    #plt.imshow(dilation)
    #plt.show()




def mse(imageA,imageB):
    err=np.sum((imageA.astype("float")-imageB.astype("float"))**2)
    err/=float(imageA.shape[0]*imageA.shape[1])
    return err



def getNumber(pic):
    min_a=9999999999
    min_png=None
    #for (png,dirnames) in os.listdir('alphaset1'):
    for f in os.listdir("D:\\daily_report\\otc\\alphaset1"):
        i=0
        for png in os.listdir("D:\\daily_report\\otc\\alphaset1"+"\\"+f):
            i=i+1
            ref=cv2.imread("D:\\daily_report\\otc\\alphaset1"+"\\"+f+"\\"+png)
            if ref is None:
                continue
            else:
                var1=np.sum((ref.astype("float")-pic.astype("float"))**2)
                var1/=float(ref.shape[0]*pic.shape[1])
                if var1<min_a:
                    min_a=mse(ref,pic)
                    min_png=png
                    code=f
    return min_png, min_a,code




def readpic():
    pic0=cv2.imread("D:\\daily_report\\otc\\alphaset\\0.png")
    pic1=cv2.imread("D:\\daily_report\\otc\\alphaset\\1.png")
    pic2=cv2.imread("D:\\daily_report\\otc\\alphaset\\2.png")
    pic3=cv2.imread("D:\\daily_report\\otc\\alphaset\\3.png")
    pic4=cv2.imread("D:\\daily_report\\otc\\alphaset\\4.png")
    a1=getNumber(pic0)[2]
    a2=getNumber(pic1)[2]
    a3=getNumber(pic2)[2]
    a4=getNumber(pic3)[2]
    a5=getNumber(pic4)[2]
    #global code    
    code=a1+a2+a3+a4+a5
    print(code)
    return code


def login(code):
    payload={
    'enname':gtype,
    'stk_code':queryid,
    'auth_num':code
}
    res1=rs.post(url, headers=head, data=payload)
    if res1.status_code!=200:
        time.sleep(10)
        print(res1.status_code)
        return login(code)       
    
    res1.encoding = 'UTF8'
    soup=BeautifulSoup(res1.text,'lxml')
    try:
        staus=soup.find('div',{'class':'v-pnl pt10'}).text.replace('*','').replace('\n','').replace(' ','')
        print(staus)
        return False
    except AttributeError:
        download_page()
        return True


def download_page():
    payload={
    'enname':gtype,
    'stk_code':queryid,
    'topage':'1',
    'auth_num':code
}
    res1=rs.post(url, headers=head, data=payload)
    if res1.status_code!=200:
        time.sleep(10)
        print('407 or 502')
        return download_page()
    res1.encoding = 'UTF8'
    global soup
    soup=BeautifulSoup(res1.text,'lxml')
    pagenumber=soup.find_all('a',{'class':'table-text-over'})
   # try:
    global table
    table=soup.find_all('table',{'class':"table table-striped table-bordered"})
    #pagetable-text-over
    global today,name
    today=table[0].find_all('tr')[0].find_all('td')[1].text
    name=table[0].find_all('tr')[0].find_all('td')[3].text.split('\xa0')[1]
    table=str(table)
    for page in range(2,len(pagenumber)+2,1):
        print(page,len(pagenumber))
        time.sleep(5)
        table=table+catch_table(page)
        #print(table)
    f= open('D:\\daily_report\\otc\\'+ today + '_' + queryid +name+ '.txt' , 'wb')
    f.write(str(table).encode('utf8'))
    f.close
    return True



def catch_table(topage):
    payload={
    'enname':gtype,
    'stk_code':queryid,
    'topage':topage,
    'auth_num':code
}
    res1=rs.post(url, headers=head, data=payload)
    if res1.status_code!=200:
        time.sleep(10)
        print(res1.status_code)
        return catch_table(topage)
    res1.encoding = 'UTF8'
    soup=BeautifulSoup(res1.text,'lxml')    
    table=soup.find_all('table',{'class':"table table-striped table-bordered"})
    print(len(table[1]))
    return str(table)
    





def branchname(a1):
    #conn = psycopg2.connect(database='equity', user='quant', password='quant', host='localhost', port='5432')
    #cur = conn.cursor()
    select_str="select 劵商分支 from 劵商分支代碼 where 代碼='"+a1+"'"
    a=pd.read_sql(select_str,conn)
    return a.loc[0,'劵商分支']




def branchdeal(a1,a2,a3,a4,a5,a6,a7,a8):
    #conn = psycopg2.connect(database='equity', user='quant', password='quant', host='localhost', port='5432')
    #cur = conn.cursor()
    insert_str="INSERT INTO 劵商買賣日報表(日期,股票,id,劵商分支,劵商分支名稱,成交單價,買進股數,賣出股數)"
    value_str="VALUES('"+a1+"','"+a2+"','"+a3+"','"+a4+"','"+a5+"',"+a6+","+a7+","+a8+")"
    try:
        cur.execute(insert_str+value_str)
    except psycopg2.IntegrityError:
        pass
    #except psycopg2.ProgrammingError:
    #    pass    
    conn.commit()




def run_insert():
    file = open('D:\\daily_report\\otc\\'+ today + '_' + queryid +name+'.txt' , 'r',encoding='UTF-8')
    res=file.read()
    soup2=BeautifulSoup(res, "html5lib")
    a=pd.read_html(res)
    file.close
    YYYY=int(a[0].iloc[0,1].split('年')[0])+1911
    MM=int(a[0].iloc[0,1].split('月')[0].split('年')[1])
    DD=int(a[0].iloc[0,1].split('月')[1].replace('日',''))
    temp=datetime.date(YYYY,MM,DD)
    a1=temp.strftime("%y%m%d")
    a2=a[0].iloc[0,3].split('\xa0')[1]
    a3=a[0].iloc[0,3].split('\xa0')[0]
    for i in range(1,len(a)-1,1):
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
            print(a1,a2,a3,a4,a5,a6,a7,a8)
            branchdeal(a1,a2,a3,a4,a5,a6,a7,a8)





def firstdoor():
    firstlevel=False
    while(firstlevel==False):
        reflash()
        parse_captcha()
        spell=readpic()
        firstlevel=login(spell)





def parse_captcha():
    image=cv2.imread("D:\\daily_report\\otc\\ori_code\\CaptchaImage.jpg",0)
    j=0
    for i in range(10,120,24):
        a=image[2:23,i:i+16]
        pic_deal(a,j)
        j=j+1





global conn,cur
conn = psycopg2.connect(database='equity', user='quant', password='quant', host='localhost', port='5432')
cur = conn.cursor()





string='select A1.id,A1.name from 上櫃股票代碼 A1,stock_desk_id A2 where A1.id=A2.id'
stockid=pd.read_sql(string,conn)
stockid1=stockid['id'].values.tolist()
stockname=stockid['name'].values.tolist()
for i in range(0,len(stockid),1):
    global queryid,name
    queryid=stockid1[i]
    name=stockname[i].replace('-','')
    print(queryid,name)
    stats=firstdoor()
    

