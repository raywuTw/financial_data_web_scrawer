from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import sys

driver=webdriver.Firefox()
driver.get("https://statementdog.com/pick/tpe")

#=================================================================
#               這塊你在自行整理一下
#=================================================================
driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])").click()
Select(driver.find_element_by_css_selector(u"#已選負債比率近一年數據 > select[name=\"rational-operator\"]")).select_by_visible_text(u"大於")
Select(driver.find_element_by_css_selector(u"#已選負債比率近一年數據 > select[name=\"filter-value\"]")).select_by_visible_text("20")
#=================================================================
driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[2]").click()
Select(driver.find_element_by_css_selector(u"#已選負債比率近三年平均 > select[name=\"rational-operator\"]")).select_by_visible_text(u"大於")
Select(driver.find_element_by_css_selector(u"#已選負債比率近三年平均 > select[name=\"filter-value\"]")).select_by_visible_text("10")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[3]").click()
#Select(driver.find_element_by_css_selector(u"#已選負債比率近五年平均 > select[name=\"rational-operator\"]")).select_by_visible_text(u"大於")
#Select(driver.find_element_by_css_selector(u"#已選負債比率近五年平均 > select[name=\"filter-value\"]")).select_by_visible_text("10")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[4]").click()
#Select(driver.find_element_by_css_selector(u"#已選ROE近一年數據 > select[name=\"rational-operator\"]")).select_by_visible_text(u"小於")
#Select(driver.find_element_by_css_selector(u"#已選ROE近一年數據 > select[name=\"filter-value\"]")).select_by_visible_text("10")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[5]").click()
#Select(driver.find_element_by_css_selector(u"#已選ROE近三年平均 > select[name=\"rational-operator\"]")).select_by_visible_text(u"小於")
#Select(driver.find_element_by_css_selector(u"#已選ROE近三年平均 > select[name=\"filter-value\"]")).select_by_visible_text("5")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[6]").click()
#Select(driver.find_element_by_css_selector(u"#已選ROE近五年平均 > select[name=\"rational-operator\"]")).select_by_visible_text(u"小於")
#Select(driver.find_element_by_css_selector(u"#已選ROE近五年平均 > select[name=\"filter-value\"]")).select_by_visible_text("20")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[7]").click()
#Select(driver.find_element_by_css_selector(u"#已選每股自由現金流近一年數據 > select[name=\"rational-operator\"]")).select_by_visible_text(u"小於")
#Select(driver.find_element_by_css_selector(u"#已選每股自由現金流近一年數據 > select[name=\"filter-value\"]")).select_by_visible_text("1")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[8]").click()
#Select(driver.find_element_by_css_selector(u"#已選每股自由現金流近三年平均 > select[name=\"rational-operator\"]")).select_by_visible_text(u"小於")
#Select(driver.find_element_by_css_selector(u"#已選每股自由現金流近三年平均 > select[name=\"filter-value\"]")).select_by_visible_text("1")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[9]").click()
#Select(driver.find_element_by_css_selector(u"#已選每股自由現金流近五年平均 > select[name=\"rational-operator\"]")).select_by_visible_text(u"小於")
#Select(driver.find_element_by_css_selector(u"#已選每股自由現金流近五年平均 > select[name=\"filter-value\"]")).select_by_visible_text("1")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[10]").click()
#Select(driver.find_element_by_css_selector(u"#已選每股自由現金流近五年平均 > select[name=\"rational-operator\"]")).select_by_visible_text(u"小於")
#Select(driver.find_element_by_css_selector(u"#已選每股自由現金流近五年平均 > select[name=\"filter-value\"]")).select_by_visible_text("1")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[11]").click()
#Select(driver.find_element_by_css_selector(u"#已選流動比率近三年平均 > select[name=\"rational-operator\"]")).select_by_visible_text(u"小於")
#Select(driver.find_element_by_css_selector(u"#已選流動比率近三年平均 > select[name=\"filter-value\"]")).select_by_visible_text("50")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[12]").click()
#Select(driver.find_element_by_css_selector(u"#已選流動比率近五年平均 > select[name=\"rational-operator\"]")).select_by_visible_text(u"小於")
#Select(driver.find_element_by_css_selector(u"#已選流動比率近五年平均 > select[name=\"filter-value\"]")).select_by_visible_text("50")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[13]").click()
#Select(driver.find_element_by_css_selector(u"#已選EPS近一年數據 > select[name=\"rational-operator\"]")).select_by_visible_text(u"小於")
#Select(driver.find_element_by_css_selector(u"#已選EPS近一年數據 > select[name=\"filter-value\"]")).select_by_visible_text("1")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[14]").click()
#Select(driver.find_element_by_css_selector(u"#已選EPS近三年平均 > select[name=\"rational-operator\"]")).select_by_visible_text(u"小於")
#Select(driver.find_element_by_css_selector(u"#已選EPS近三年平均 > select[name=\"filter-value\"]")).select_by_visible_text("1")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[15]").click()
#Select(driver.find_element_by_css_selector(u"#已選EPS近五年平均 > select[name=\"rational-operator\"]")).select_by_visible_text(u"小於")
#Select(driver.find_element_by_css_selector(u"#已選EPS近五年平均 > select[name=\"filter-value\"]")).select_by_visible_text("2")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[17]").click()
#Select(driver.find_element_by_css_selector(u"#已選本益比目前 > select[name=\"rational-operator\"]")).select_by_visible_text(u"大於")
#Select(driver.find_element_by_css_selector(u"#已選本益比目前 > select[name=\"filter-value\"]")).select_by_visible_text("6")
#=================================================================
#driver.find_element_by_xpath("(//div[@onclick='addMstrIdx(this)'])[18]").click()
#Select(driver.find_element_by_css_selector(u"#已選股價淨值比目前 > select[name=\"rational-operator\"]")).select_by_visible_text(u"大於")
#Select(driver.find_element_by_css_selector(u"#已選股價淨值比目前 > select[name=\"filter-value\"]")).select_by_visible_text("1")


driver.find_element_by_link_text(u"開始選股").click()
time.sleep(10)
pure_html=driver.page_source
driver.close()

soup=BeautifulSoup(pure_html,'html5lib')
tbody=soup.find('div',{'id':'result-content'}).find('tbody')
div=soup.find('div',{'id':'result-content'})

for tr in tbody.findAll('tr'):
    output_str=''
    for td in tr.findAll('td'):
        output_str=output_str + td.text + ', '
    print(output_str)