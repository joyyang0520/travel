from bs4 import BeautifulSoup
import requests

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
print(count)
print(train_ID_dict)

'''
page = 1
train_ID_dict = {}

for page in range(1,7):
    URL = 'https://sheethub.com/tra.gov.tw/%E8%87%BA%E9%90%B5%E8%BB%8A%E7%AB%99%E4%BB%A3%E8%99%9F?page=' + str(page)
    r = requests.get(URL)
    soup = BeautifulSoup(r.text,'html.parser') 

    stations = soup.find('table',class_='display sheet-table').tbody.find_all('tr')

    for tr in stations:
        element = tr.find_all('td')
        ID = element[0].text.replace(' ','').replace('\n','')
        station = element[1].text.replace(' ','').replace('\n','')
        train_ID_dict[station] = ID
        # print(ID)
        # print(station)
print(train_ID_dict)
'''