import requests
from bs4 import BeautifulSoup
import json
import argparse
import sys
import time
from pathlib import Path
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

URL = 'https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime'
r = requests.get(URL)
soup = BeautifulSoup(r.text,'html.parser') 

stations = soup.find_all('div', class_='line-inner hr cityHr')
train_ID_dict = {}
count = 0

for station in stations:
    all_names = station.find_all('li')
    for station_name in all_names:
        #print(station_name.text)
        station_IDs = station_name.find_all('button')
        for ID in station_IDs:
            station_ID = ID.get('title')
            #print(station_ID)
            train_ID_dict[station_name.text] = station_ID
        count += 1
#print(count)
#print(train_ID_dict)

#print("參數範例：3160-苗栗 4080-嘉義 2023/08/30")
input_startStation = str(input('輸入起站：'))
if input_startStation in train_ID_dict:
    new_input_startStation = train_ID_dict[input_startStation]
    print(new_input_startStation)
input_endStation = str(input('輸入迄站：'))
if input_endStation in train_ID_dict:
    new_input_endStation = train_ID_dict[input_endStation]
    print(new_input_endStation)
input_rideDate = str(input('輸入日期yyyy/mm/dd：'))

print (sys.argv) #執行腳本為yq_train.py，後面參數為input_startStation,input_endStation,input_rideDate
argv_len = len(sys.argv) #計算命令行參數的數量儲存到argv_len,回傳總共4(腳本+3個參數)

print("請稍候...")
time.sleep(3)

is_run = False #預設不執行

input_s1 = ''
input_s2 = ''
input_ymd = ''
path = Path('.')

if argv_len == 4:
    input_s1 = sys.argv[1]
    input_s2 = sys.argv[2]
    input_ymd = sys.argv[3]
    is_run = True #程式執行
else :
    #print("確認參數如：3300-臺中 3160-苗栗 2023/09/09")
    input_s1 = new_input_startStation
    input_s2 = new_input_endStation
    input_ymd = input_rideDate
    is_run = True

#print(is_run)

#定義一個TrainProps的類別來儲存值(起始站、終點站和乘車日期)
class TrainProps:
    def __init__(self, s1, s2, ymd):
        self.input_s1 = s1
        self.input_s2 = s2
        self.input_ymd = ymd

props = TrainProps(input_s1, input_s2, input_ymd)

time_start = time.time()
def go_search(props):
    url = "https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime?transfer=ONE&trainTypeList=ALL&startOrEndTime=true&queryClassification=NORMAL&startStation={0}&endStation={1}&rideDate={2}&startTime=00:00&endTime=23:59&sort=departureTime,asc".format(props.input_s1, props.input_s2, props.input_ymd)
    res = requests.get(url)
    res.encoding = "utf-8"

    soup = BeautifulSoup(res.text, "html.parser")

    train_item = soup.select(".trip-column")
    train_item_len = len(train_item) #共有幾筆資料
    jsonString = '[';
    for index in range(len(train_item)):
        values = train_item[index].text.split('\n')
        values_len = len(values)
        #uid = '{ "uid": %s, ' % str(index)
        trainNumber = '{ "車種車次": "%s", ' % values[5]
        startStation = '"始發站": "%s", ' % values[7]
        endStation = '"終點站": "%s", ' % values[9]
        startTime = '"出發時間": "%s", ' % values[15]
        endTime = '"抵達時間": "%s", ' % values[16]
        trainTime = '"行駛時間": "%s", ' % values[17]
        trainLine = '"經由": "%s", ' % values[18]
        allPrice = '"全票": "%s", ' % values[25]
        childPrice = '"孩童票 ": "%s", ' % values[29]
        oldPrice = '"敬老票": "%s" }' % values[33]
        
        string_format =  trainNumber + startStation + endStation + startTime + endTime + trainTime + trainLine + allPrice + childPrice + oldPrice

        jsonString += string_format

        if index < train_item_len-1:
            jsonString+=','

    jsonString+=']' #end jsonString
    jsonData = json.loads(jsonString) #json.loads方法將JSON字串轉換為Python的字典或列表對象，存儲在jsonData變數中

    #write_firebase_firestore(jsonData)
    for index, train in enumerate(jsonData):
        print(f'({index}) {train}')

    #print(jsonData)
    print("共%s筆，查詢結束。" % len(jsonData))

    print(time.time() - time_start)
    
'''
def write_firebase_firestore(data):
    
    # Use a service account.
    path = Path('train-15397-firebase-adminsdk-c8665-4542ea4f64.json')
    isfile = path.is_file()
    firebase_json = 'train-15397-firebase-adminsdk-c8665-4542ea4f64.json'
    cred = credentials.Certificate(firebase_json)
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    #doc = db.collection("timeTable").document("tra_tip_data")
    
    for index in range(len(data)):
        item_data = data[index]
        #doc = db.collection("timeTable").document("tra_tip_data")
        doc_name = ''
        if index <= 9:
            doc_name = '0%s' % str(index)
        else:
            doc_name = str(index)
        #doc = db.collection("timeTable").document("tra_tip_data"+doc_name)
        doc = db.collection("timeTable").document()
        doc.set(item_data, merge=True)
'''    

if is_run :
    go_search(props)