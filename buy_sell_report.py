

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
    url='http://bsr.twse.com.tw/bshtm' 

    head={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }

    global rs, viewstate, eventvalidation
    rs = requests.session()
    res=rs.post(url + '/bsMenu.aspx', headers=head)
    #print(res.text)
    soup=BeautifulSoup(res.text,"lxml")
    #print(soup)
    try:
        viewstate=soup.find('input',{'id':'__VIEWSTATE'})['value']
        eventvalidation=soup.find('input',{'id':'__EVENTVALIDATION'})['value']
    
        #img=soup.findAll('img',src=True)[1]['src']
        #print(img)
        #res2=rs.get(url + '/' + img , stream = True)
        #f=open('test.png','wb')
        password=[]
        for img in soup.find_all('img'): 
            password.append(img['src'])
            #fname=img['src']
            #print(password)
        fname=password[1]
        res2=rs.get(url+'/'+fname,stream=True)
        f=open('D:\\daily_report\\ori_code\\CaptchaImage.jpg','wb')
        shutil.copyfileobj(res2.raw,f)
        f.close()
        del res2      
    except TypeError:
        print('407發生了',queryid)
        time.sleep(10)
        reflash()
        


global conn,cur,today
conn = psycopg2.connect(database='equity', user='quant', password='quant', host='localhost', port='5432')
cur = conn.cursor()
today=time.strftime("%Y%m%d")



def parse_captcha():
    image=cv2.imread("D:\\daily_report\\ori_code\\CaptchaImage.jpg",0)
    kernel=np.ones((4,4),np.uint8)
    erosion=cv2.erode(image,kernel)
    blurred=cv2.GaussianBlur(erosion,(5,5),0)
    edged=cv2.Canny(blurred,30,150)
    kernel1=np.ones((3,3),np.uint8)
    dilation=cv2.dilate(edged,kernel1,iterations=1)
    
    image, contours, hierarchy=cv2.findContours(dilation.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnts=sorted([(c,cv2.boundingRect(c)[0]) for c in contours], key=lambda x:x[1])

    ary=[]
    for (c, _) in cnts:
        (x,y,w,h)=cv2.boundingRect(c)
        if w>15 and h>15:
            ary.append((x,y,w,h))

    if len(ary)==5:
        fig=plt.figure()
        for id, (x,y,w,h) in enumerate(ary):
            roi=dilation[y:y+h,x:x+w]
            thresh=roi.copy()
            a=fig.add_subplot(1,len(ary),id+1)
            res=cv2.resize(thresh,(50,50))
            cv2.imwrite("D:\\daily_report\\alphaset\\%d.png"%(id),res)
        plt.close('all')
        return True
    else:
        return False


def mse(imageA,imageB):
    err=np.sum((imageA.astype("float")-imageB.astype("float"))**2)
    err/=float(imageA.shape[0]*imageA.shape[1])
    return err


def getNumber(pic):
    min_a=9999999999
    min_png=None
    #for (png,dirnames) in os.listdir('alphaset1'):
    for f in os.listdir("D:\\daily_report\\alphaset1"):
        i=0
        for png in os.listdir("D:\\daily_report\\alphaset1"+"\\"+f):
            i=i+1
            ref=cv2.imread("D:\\daily_report\\alphaset1"+"\\"+f+"\\"+png)
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
    pic0=cv2.imread("D:\\daily_report\\alphaset\\0.png")
    pic1=cv2.imread("D:\\daily_report\\alphaset\\1.png")
    pic2=cv2.imread("D:\\daily_report\\alphaset\\2.png")
    pic3=cv2.imread("D:\\daily_report\\alphaset\\3.png")
    pic4=cv2.imread("D:\\daily_report\\alphaset\\4.png")
    a1=getNumber(pic0)[2]
    a2=getNumber(pic1)[2]
    a3=getNumber(pic2)[2]
    a4=getNumber(pic3)[2]
    a5=getNumber(pic4)[2]
    code=a1+a2+a3+a4+a5
    return code



def login(spell):
    url1 = "http://bsr.twse.com.tw/bshtm/bsMenu.aspx"

    head={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }

    payload={
        '__EVENTTARGET':'',
        '__EVENTARGUMENT':'',
        '__LASTFOCUS':'',
        '__VIEWSTATE':viewstate,
        '__EVENTVALIDATION':eventvalidation,
        'RadioButton_Normal':'RadioButton_Normal',
        'TextBox_Stkno':queryid,
        'CaptchaControl1':spell,
        'btnOK':'%E6%9F%A5%E8%A9%A2'
    }

    res1=rs.post(url1, headers=head, data=payload)
    if res1.status_code!=200:
        res1=login(spell)
    return res1


def download_page():
    url_page2 = 'http://bsr.twse.com.tw/bshtm/bsContent.aspx?v=t'
    head={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    res2=rs.post(url_page2, headers=head)
    if res2.text=='':
        return False
    else:
        f= open('D:\\daily_report\\'+ today + '_' + queryid +name+ '.txt' , 'wb')
        f.write(res2.text.encode('utf8'))
        f.close
        return True


def firstdoor():
    firstlevel=False
    parse_status=False
    while(firstlevel==False):
        reflash()
        try:
            parse_status=parse_captcha()
        except:
            parse_status=False
        if parse_status==False:
            firstlevel=False  
        else:
            if len(readpic())!=5:
                firstlevel=False
            else:
                spell=readpic()
                res=login(spell)
                print(spell)
                soup=BeautifulSoup(res.text, "html5lib")
                status=soup.find('span',{'id':'Label_ErrorMsg'}).text
                #print(status)
                if status=='':
                    firstlevel=download_page()
                    return firstlevel
                elif status=='查無資料':
                    print(status)
                    firstlevel=True
                    return "NoData"
                #elif status=='驗證碼錯誤!'or status=='驗證碼已逾期.':
                    
                else:
                    print(status)
                    firstlevel=False


def stockbranch(a1,a2):
    #conn = psycopg2.connect(database='equity', user='quant', password='quant', host='localhost', port='5432')
    #cur = conn.cursor()
    insert_str="INSERT INTO 劵商分支代碼(代碼,劵商分支)"
    value_str="VALUES('"+a1+"','"+a2+"')"
    try:
        cur.execute(insert_str+value_str)
    except psycopg2.IntegrityError:
        pass
    conn.commit()


def branchname(a1):
    #conn = psycopg2.connect(database='equity', user='quant', password='quant', host='localhost', port='5432')
    #cur = conn.cursor()
    select_str="select 劵商分支 from 劵商分支代碼 where 代碼='"+a1+"'"
    a=pd.read_sql(select_str,conn)
    return a.loc[0,'劵商分支']


def branchdeal(a1,a2,a3,a4,a5,a6,a7,a8):
    conn = psycopg2.connect(database='equity', user='quant', password='quant', host='localhost', port='5432')
    cur = conn.cursor()
    insert_str="INSERT INTO daily_report(日期,股票,id,劵商分支,劵商分支名稱,成交單價,買進股數,賣出股數)"
    value_str="VALUES('"+a1+"','"+a2+"','"+a3+"','"+a4+"','"+a5+"',"+a6+","+a7+","+a8+")"
    try:
        cur.execute(insert_str+value_str)
    except psycopg2.IntegrityError:
        pass
    except psycopg2.ProgrammingError:
        pass    
    conn.commit()


def run_insert():
    file = open('D:\\daily_report\\'+ today + '_' + queryid +name+'.txt' , 'r',encoding='UTF-8')
    res=file.read()
    soup2=BeautifulSoup(res, "html5lib")
    a=pd.read_html(res)
    file.close
    for i in range(4,len(a),6):
        for j in range(1,len(a[i]),1):
            a1=a[2].iloc[0,1]
            a2=a[2].iloc[0,3].split('\xa0')[1]
            a3=a[2].iloc[0,3].split('\xa0')[0]
            a4=str(a[i].iloc[j,1]).replace(' ','')
            if len(a4)!=4:
                a5=a4[4:]
                a4=a4[0:4]
                stockbranch(a4,a5)
            else:
                a5=branchname(a4)
            a6=str(a[i].iloc[j,2]).replace(' ','')
            a7=str(a[i].iloc[j,3]).replace(' ','')
            a8=str(a[i].iloc[j,4]).replace(' ','')
        
            #print(a[i+1].iloc[j,1])
            a9=str(a[i+1].iloc[j,1]).replace(' ','')
            if len(a9)!=4:
                a10=a9[4:]
                a9=a9[0:4]
                stockbranch(a9,a10)
            else:
                a10=branchname(a9)
            a11=str(a[i+1].iloc[j,2]).replace(' ','')
            a12=str(a[i+1].iloc[j,3]).replace(' ','')
            a13=str(a[i+1].iloc[j,4]).replace(' ','')       
            print(a1,a2,a3,a4,a5,a6,a7,a8)
            print(a1,a2,a3,a9,a10,a11,a12,a13)
            branchdeal(a1,a2,a3,a4,a5,a6,a7,a8)
            branchdeal(a1,a2,a3,a9,a10,a11,a12,a13)    


string='select A1.id,A1.name from 上市股票代碼 A1,stock_desk_id A2 where A1.id=A2.id'
stockid=pd.read_sql(string,conn)
stockid1=stockid['id'].values.tolist()
stockname=stockid['name'].values.tolist()
for i in range(0,len(stockid),1):
    global queryid,name
    queryid=stockid1[i]
    name=stockname[i].replace('-','')
    stats=firstdoor()
    print(queryid,name)



for i in range(0,len(stockid),1):
    queryid=stockid1[i]
    name=stockname[i].replace('-','')
    run_insert()




