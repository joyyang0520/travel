from selenium import webdriver
from selenium.webdriver.common.by import By #用於指定不同的定位方式
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from tabulate import tabulate
import time

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)
driver.get("https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime")

time.sleep(5)

html = driver.page_source #獲取當前HTML的內容
doc = pq(html)

#--------------- CSS Selector 的寫法 ---------------
citiesSort_startSation = {}
cities_startStation = {}

print('縣市: ')
count = 2 #用來表示縣市的排序位置
for city in doc('#mainline > div:nth-child(1) > ul > li:nth-child(n+2)').items():
    print(city.text())
    temp_city_id = doc('#mainline > div:nth-child(1) > ul > li:nth-child(' + str(count) + ') > button').attr('data-type')
    citiesSort_startSation[city.text()] = count #縣市名稱為鍵:列表中的排序為值 ex:{'基隆市':2}
    cities_startStation[city.text()] = temp_city_id #縣市名稱為鍵:縣市代碼為值 ex:{'基隆市':'city10017'}
    count += 1

print(citiesSort_startSation)
print(cities_startStation)

input_startStationCity = input('請輸入出發縣市: ')
time.sleep(3)

driver.find_element(By.XPATH,"//*[@id='queryForm']/div/div[1]/div[2]/div[2]/button[1]").click()
time.sleep(1)

city_button_xpath = f"//*[@id='mainline']/div[1]/ul/li[{citiesSort_startSation[input_startStationCity]}]/button"
driver.find_element(By.XPATH,city_button_xpath).click()

stationsSort_startStation = {}

print('站名: ')
stationCount = 1
for station in doc('#{0} > ul > li:nth-child(n+1) > button'.format(cities_startStation[input_startStationCity])).items():
    stationsSort_startStation[station.text()] = stationCount
    print(station.text())
    stationCount += 1

print(stationsSort_startStation)

input_startStation = input('請輸入出發站: ')

print(cities_startStation[input_startStationCity])
print(stationsSort_startStation[input_startStation])

city_button_xpath = f"//*[@id='{cities_startStation[input_startStationCity]}'][{stationsSort_startStation}]/button"
driver.find_element(By.XPATH, city_button_xpath).click()

#print("XPATH:", city_button_xpath)

#driver.find_element_by_xpath("//*[@id='{0}'][{1}]/button".format(cities_startStation[input_startStationCity],stationsSort_startStation)).click()

'''
page_content = chrome.page_source #取得網頁內的內容
soup = BeautifulSoup(page_content,'html.parser')

city_buttons = soup.find_all('button',class_='btn tipCity')

city_names = []

for city in city_buttons:
    city_name = city.text
    city_names.append(city_name)

chrome.quit()

print(city_names)
'''

