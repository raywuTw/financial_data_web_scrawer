

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import datetime
import psycopg2




def get_soup(YYY,MM,sii):
    url='http://mops.twse.com.tw/nas/t21/'+sii+'/t21sc03_'+YYY+'_'+MM+'_0.html'
    print(url)
    #res=requests.get(url)
    #if res.isOK==True
    try:
        df=pd.read_html(url)
        a=[]
        for i in range(2,57,2):
            a.append(df[i])
    except:
        time.sleep(10)
        a=get_soup(YYY,MM,sii)        
    #requests.exceptions.HTTPError:

    #df[2]水泥 df[4]食品 df[6]塑膠 df[8]紡織纖維 df[10]電機機械 df[12]電器電纜 #df[14]化學工業
    #df[16]生技醫療  df[18]波離陶瓷 df[20]造紙工業 df[22]鋼鐵工業 df[24]橡膠工業 df[26]汽車工業 
    #df[30]半導體業  df[32]電腦及週邊設備業 df[34]光電業 df[36]通信網路業 df[38]電子零組件
    #df[40]電子通路業  df[42]資訊服務業 df[34]光電業 df[36]其他電子葉 df[40]油電燃氣業 
    #df[42]建材營造 df[44]航運業 df[46]觀光事業 df[48]金融保險業 df[50]貿易百貨 df[52] 其他

        #print(df[i].ix[0:,0])
    return a




def get_pastmonth():
    today=datetime.date.today()
    a=[]
    for i in range(0,2000,28):
        #dayss=i
        pastmonth=today-datetime.timedelta(days=i)
        YYY=pastmonth.strftime("%Y")
        YYY=int(YYY)
        MM=pastmonth.strftime("%m")
        #MM=int(MM)
        YYYMM=str(YYY)+str(MM)
        a.append(YYYMM)
    return a




def insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13):
    conn=psycopg2.connect(database="equity",user="quant",password="quant",host="localhost",port="5432")
    cur=conn.cursor()
    a13=a13.replace("'","")
    insert_str1="insert into 每月營收(id,yyymm,股票,產業別,當月營收,上月營收,去年當月營收,yoy,mom,當月累積營收"
    insert_str2=",去年累積營收,累積營收前期增減百分比,備註)"
    values_str1="VALUES('"+a1+"','"+a2+"','"+a3+"','"+a4+"',"+a5+","+a6+",'"+a7+"','"+a8+"','"
    values_str2=a9+"',"+a10+","+a11+",'"+a12+"','"+a13+"')"
    str1=insert_str1+insert_str2+values_str1+values_str2
    try:
        cur.execute(str1)
        conn.commit()
        #print(str1)
    except psycopg2.IntegrityError:
        update_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)




def update_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13):
    conn=psycopg2.connect(database="equity",user="quant",password="quant",host="localhost",port="5432")
    cur=conn.cursor()
    a14=time.strftime("%x %X" )
    update_str="UPDATE 每月營收 SET "
    set_str1="股票='"+a3+"',"+"產業別='"+a4+"',"+"當月營收="+a5+","+"上月營收="+a6+","+"去年當月營收="+a7+","+"yoy='"+a8+"',"+"mom='"+a9+"',"
    set_str2="當月累積營收="+a10+","+"去年累積營收="+a11+","+"累積營收前期增減百分比='"+a12+"',"+"備註='"+a13+"'"
    where_str="WHERE id ='"+a1+"' AND yyymm='"+a2+"'"
    cur.execute(update_str+set_str1+set_str2+where_str)
    #print(update_str+set_str1+set_str2+where_str)
    conn.commit()




def run_insert(YYYYMM,sii):
    indust=['水泥工業','食品工業','塑膠工業','紡織纖維','電機機械','電器電纜','化學工業','生技醫療業','玻璃陶瓷','造紙工業','鋼鐵工業'
        ,'橡膠工業','汽車工業','半導體業','電腦及週邊設備業','光電業','通信網路業','電子零組件業','電子通路業','資訊服務業',
        '其他電子業','油電燃氣業','建材營造','航運業','觀光事業','金融保險業','貿易百貨','其他']
    YYY=str(int(YYYYMM[0:4])-1911)
    MM=str(int(YYYYMM[4:]))
    print(YYY,MM)
    a=get_soup(YYY,MM,sii)
    for j in range(0,len(a),1):
        for i in range(0,len(a[j])-3,1):
            a1=str(a[j].ix[2+i,0])
            a2=YYYYMM
            a3=str(a[j].ix[2+i,1])
            a4=indust[j]
            a5=str(a[j].ix[2+i,2])
            a6=str(a[j].ix[2+i,3])
            a7=str(a[j].ix[2+i,4])
            a8=str(a[j].ix[2+i,6])
            a9=str(a[j].ix[2+i,5])
            a10=str(a[j].ix[2+i,7])
            a11=str(a[j].ix[2+i,8])
            a12=str(a[j].ix[2+i,9])
            a13=str(a[j].ix[2+i,10])
            #print(i,j,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)
            insert_value(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13)

pastmonth=get_pastmonth()[1:3]
for i in range(0,len(pastmonth),1):
    run_insert(pastmonth[i],'sii')
    run_insert(pastmonth[i],'otc')





