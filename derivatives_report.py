from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import psycopg2
import sys
import socket
import datetime

def second_page(sd):
    driver.find_element_by_xpath(u"(//input[@value='詳細資料'])[" + str(sd) + "]").click()

    time.sleep(6)
    now_handle=driver.current_window_handle
    all_handles=driver.window_handles
    driver.switch_to_window(all_handles[1])
    aa=driver.page_source
    driver.close()
    driver.switch_to_window(all_handles[0])
    soup=BeautifulSoup(aa,'html5lib')
    
    return soup

def parser(soup):
    compID=soup.find('input',{'name':'Q1V'})['value']
    compName=soup.find('input',{'name':'compName'})['value'].replace(' ','')
    yyymm=soup.find('input',{'name':'Q2V'})['value']
    mamaID=compID[0:4]
    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
    print("id=" + compID + "; compName=" + compName + "; yyymm=" + yyymm)

    name=[]
    name.append('非持有_符合避險_未沖銷_總金額')
    name.append('非持有_符合避險_未沖銷_公允價值')
    name.append('非持有_符合避險_未沖銷_未實現')
    name.append('非持有_符合避險_已沖銷_總金額')
    name.append('非持有_符合避險_已沖銷_已實現')
    name.append('非持有_不符合避險_未沖銷_總金額')
    name.append('非持有_不符合避險_未沖銷_公允價值')
    name.append('非持有_不符合避險_未沖銷_未實現')
    name.append('非持有_不符合避險_已沖銷_總金額')
    name.append('非持有_不符合避險_已沖銷_已實現')

    td=[]
    for i in range(0,10):
        td.append(0)

    for tb in soup.findAll('table',{'class':'hasBorder'}):
        a1=tb.findAll('tr',{'class':False})[0].findAll('td',{'class':'tblHead'})[0].text
        #print(first_head)
        if a1=='非持有供交易':
            a2=tb.findAll('tr',{'class':False})[0].findAll('td',{'class':'tblHead'})[1].text
            if a2=='不符避險會計':
                td[5]=tb.findAll('tr',{'class':False})[2].findAll('td',{'style':True})[-4].text.replace(',','').replace(' ','')
                td[6]=tb.findAll('tr',{'class':False})[3].findAll('td',{'style':True})[-4].text.replace(',','').replace(' ','')
                td[7]=tb.findAll('tr',{'class':False})[4].findAll('td',{'style':True})[-4].text.replace(',','').replace(' ','')
                td[8]=tb.findAll('tr',{'class':False})[5].findAll('td',{'style':True})[-4].text.replace(',','').replace(' ','')
                td[9]=tb.findAll('tr',{'class':False})[6].findAll('td',{'style':True})[-4].text.replace(',','').replace(' ','')
            elif a2=='符合避險會計':
                td[0]=tb.findAll('tr',{'class':False})[2].findAll('td',{'style':True})[-4].text.replace(',','').replace(' ','')
                td[1]=tb.findAll('tr',{'class':False})[3].findAll('td',{'style':True})[-4].text.replace(',','').replace(' ','')
                td[2]=tb.findAll('tr',{'class':False})[4].findAll('td',{'style':True})[-4].text.replace(',','').replace(' ','')
                td[3]=tb.findAll('tr',{'class':False})[5].findAll('td',{'style':True})[-4].text.replace(',','').replace(' ','')
                td[4]=tb.findAll('tr',{'class':False})[6].findAll('td',{'style':True})[-4].text.replace(',','').replace(' ','')
    isum=0
    for i in range(0,10):
        isum=isum+ int(td[i])
       
    if isum!=0:
        for i in range(0,10):
            cur.execute("insert into 遠期契約申報資料(id,mama_id,name,yyymm,item,value,insert_dt) values(" + compID + "," + mamaID + ",'" + compName + "'," + yyymm + ",'" + name[i] + "'," + str(td[i]) + ",'" + timestamp + "')")   
            conn.commit()

def isExist(soup):
    compID=soup.find('input',{'name':'Q1V'})['value']
    yyymm=soup.find('input',{'name':'Q2V'})['value']
    mamaID=compID[0:4]
    
    cur.execute("select count(id) from 遠期契約申報資料 where id='" + mamaID + "' and yyymm='" + yyymm + "';")   
    arr=cur.fetchall()
    conn.commit()
    return str(arr[0][0])

def start_level(sp):
    if isExist(sp)=='0': 
        all_lists=0
        for i in sp.findAll('input',{'type':'button','value':'詳細資料'}):
            all_lists=all_lists+1

        isSuccess=False
        iStart=1
        recursive=0
        while(isSuccess==False):
            try:
                for i in range(iStart,all_lists+1):
                    soup=second_page(i)
                    parser(soup)

                isSuccess=True
                print('Mission complete!!!')
            except:
                if recursive<3:
                    iStart=i
                    recursive=recursive+1
                    print('stop at ' + str(iStart) + ', and recursive times = ' + str(recursive))
                else:
                    iStart=i+1
                    recursive=0
                
        driver.close()
    else:
        print('Already exists!!!')
        driver.close()

def trigger(myID, myYYY, myMM):
    if socket.gethostbyname(socket.gethostname())=='172.27.110.104':	#Jack's pc
        ipath='D:\\Python36\\phantomjs.exe'
    elif socket.gethostbyname(socket.gethostname())=='172.27.111.34': 	#Jay's pc
        ipath='C:\\Program Files\\Python35\\Scripts\\phantomjs.exe'
    elif socket.gethostbyname(socket.gethostname())=='172.27.110.105': 	#Allen's pc
        ipath='D:\\Python\\Python35\\phantomjs.exe'
		
    global driver
    driver=webdriver.PhantomJS(ipath,service_args=['--ignore-ssl-errors=true','--ssl-protocol=TLSv1'])

    driver=webdriver.Firefox()
    driver.get("http://mops.twse.com.tw/mops/web/t15sf")

    driver.find_element_by_id('co_id').send_keys(myID)
    driver.find_element_by_id('year').send_keys(myYYY)
    driver.find_element_by_id('month').send_keys(int(myMM))
    #Select(driver.find_element_by_id('month')).select_by_visible_text(int(myMM))
    driver.find_element_by_css_selector('div.search > input[type=\"button\"]').click()
    time.sleep(6)
    soup=BeautifulSoup(driver.page_source,'html5lib')
    
    is_no_data=False
    for center in soup.findAll('center'):
        if center.text=='該公司並未申報本項資料':
            is_no_data=True
    
    if is_no_data:
        print('該公司並未申報本項資料')
    else:
        start_level(soup)		
		
def get_all_code(strName):
    host_str=connection_info()
    conn1=psycopg2.connect(host=host_str,port='5432',database='equity',user='quant',password='quant')
    cur1=conn1.cursor()
    cur1.execute("select id from " + strName + " order by id")   
    arr=cur1.fetchall()
    cur1.close()
    conn1.close()
    return arr
	
def iteration(arr, start_from=0, end_to=9999):
    lastmon=datetime.datetime.today()-datetime.timedelta(days=20)
    myYYY=str(int(lastmon.strftime("%Y"))-1911)
    myMM=lastmon.strftime("%m")
    myID=''
    
    for i in range(0,len(arr)):
        myID=arr[i][0]
        if int(myID)>=start_from and int(myID)<=end_to:
            trigger(myID, myYYY, myMM)

def connection_info():
    #ipstr=socket.gethostbyname(socket.gethostname())
    #if ipstr=='172.27.110.104':
    #    conn_info='localhost'
    #else:
    #    conn_info='172.27.110.104'  #this is Jack's pc
    conn_info='localhost'
    return conn_info
lastmon=datetime.datetime.today()-datetime.timedelta(days=20)
myYYY=str(int(lastmon.strftime("%Y"))-1911)
myMM=lastmon.strftime("%m")
myID=''

host_str=connection_info()
conn=psycopg2.connect(host=host_str,port='5432',database='postgres',user='quant',password='quant')
cur=conn.cursor()

ipstr=socket.gethostbyname(socket.gethostname())
#if ipstr=='172.27.110.104':
#    arr=get_all_code('上櫃股票代碼')
#    iteration(arr, 1001, 9999)		# for debug purpose
#elif ipstr=='172.27.110.105':
#    arr=get_all_code('上市股票代碼')
#    iteration(arr, 1101, 4500)  	# for debug purpose
#elif ipstr=='172.27.111.34':
    arr=get_all_code('上市股票代碼')
    iteration(arr, 4500, 9999)  	# for debug purpose

cur.close()
conn.close()