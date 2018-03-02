


import pandas as pd
import psycopg2



global conn,cur,today
conn = psycopg2.connect(database='equity', user='quant', password='quant', host='localhost', port='5432')
cur = conn.cursor()



#分公司
def branch_name():
    url='http://www.tse.com.tw/brokerService/branchList.html'
    a=pd.read_html(url)
    for i in range(0,len(a[0]),1):
        city=a[0].loc[i,'地址'][0:3]
        address=a[0].loc[i,'地址']
        name=a[0].loc[i,'證券商名稱']
        id=a[0].loc[i,'證券商代號']
        update_value(id,name,city,address)



def update_value(a1,a2,a3,a4):
    update_Str="UPDATE 劵商分支代碼 SET 劵商分支 ='"+a2+"',所在縣市='"+a3+"',地址='"+a4+"' WHERE 代碼 ='"+a1+"'"
    #print(update_Str)
    cur.execute(update_Str)
    conn.commit()



def HQ_name():
    url='http://www.tse.com.tw/brokerService/brokerList.html?lang=zh'
    a=pd.read_html(url)
    for i in range(0,len(a[0]),1):
        city=a[0].loc[i,'地址'][0:3]
        address=a[0].loc[i,'地址']
        name=a[0].loc[i,'證券商名稱']
        id=a[0].loc[i,'證券商代號']
        update_value(id,name,city,address)




branch_name()
HQ_name()




