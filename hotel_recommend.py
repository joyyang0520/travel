import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import UserAgent as ua
import time
import firebase_admin
from firebase_admin import credentials, firestore

if __name__ == "__main__":
    start_time = time.time()
   
    url = 'https://www.booking.com/searchresults.zh-tw.html?aid=304142&label=gen173nr-1FCAQoggJCDXNlYXJjaF_lj7DkuK1IMFgEaOcBiAEBmAEwuAEXyAEM2AEB6AEB-AEDiAIBqAIDuAKIzN-oBsACAdICJDdhNDAyYWQ4LWZmZTUtNGJmYi1iOGViLWI1Y2FkNDU4NzhjZNgCBeACAQ&ss=%E5%8F%B0%E4%B8%AD&nflt=review_score%3D90&order=bayesian_review_score'
    #print(f'\nurl: {url}')

    user_agent = ua.UserAgent().get()
    #print(f"user_agent: {user_agent}")
    options = Options()
    options.add_argument("--headless")  # Remove this if you want to see the browser (Headless makes the chromedriver not have a GUI)
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=%s"%user_agent)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options = options)
    driver.get(url)
    #print(driver.page_source)
    page_content = driver.page_source #取得網頁內的內容
    soup = BeautifulSoup(page_content,'html.parser')

    hotels = soup.find_all('div',class_='f6431b446c a15b38c233') 
    web_pages = soup.find_all('div',class_='e952b01718')
    scores = soup.find_all('div',class_='a3b8729ab1 d86cee9b25')

    #print((len(hotels)))
    
    hotel_info_list = []

    for i in range(len(hotels)):
        hotel_info_dict = {}
        hotel_name = hotels[i].text
        hotel_info_dict['飯店名稱'] = hotel_name
        #print(hotel_name)
    
        hotel_score = scores[i].text
        hotel_info_dict['評分'] = hotel_score
        #print(hotel_score)
    
        original_web = web_pages[i].find('a').get('href')
        hotel_web = original_web.split('?')[0]
        hotel_info_dict['訂房網站'] = hotel_web
        #print(hotel_web)
        hotel_info_list.append(hotel_info_dict)
   
        url = hotel_web
        #print(f'\nurl: {url}')

        user_agent = ua.UserAgent().get()
        #print(f"user_agent: {user_agent}")
        options = Options()
        options.add_argument("--headless")  # Remove this if you want to see the browser (Headless makes the chromedriver not have a GUI)
        options.add_argument("--window-size=1920,1080")
        options.add_argument("user-agent=%s"%user_agent)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        driver = webdriver.Chrome(options = options)
        driver.get(url)
        #print(driver.page_source)
        page_content = driver.page_source #取得網頁內的內容
        soup = BeautifulSoup(page_content,'html.parser')

        services = soup.find('div',class_='hp--popular_facilities js-k2-hp--block').find_all('div',class_='dc6c58be0b')
        
        service_list = []
        for service in services:
            hotel_service = service.text
            service_list.append(hotel_service)
            hotel_info_dict['熱門設施'] = service_list
        #print(service_list)
        #print(services)
       
    
        rooms = soup.find_all('a',class_='a83ed08757 f88a5204c2 d1c4779e7a js-legacy-room-name b98133fb50')
        beds = soup.find_all('span',class_='baf7cb1417')
        room_list = []
        for room in rooms:
            hotel_room = room.text
            for bed in beds:
                bed_type = bed.text 
                room_type = hotel_room + '(' + bed_type + ')'
            room_list.append(room_type)
            hotel_info_dict['房型'] = room_list
        #print(room_list)
    #print(hotel_info_list)   
      
'''

hotel_info_list = [{'飯店名稱': '風華嚼旅 ', 
                    '評分': '9.4', 
                    '訂房網站': 'https://www.booking.com/hotel/tw/zhong-laviefeng-hua-lu-zhan.zh-tw.html', 
                    '熱門設施': ['家庭房 ', '免費無線網路 ', '禁菸客房 ', '機場接駁車 ', '露台 ', '客房服務 ', '所有客房都有咖啡／沏茶設施 ', '早餐評價非常好 '], 
                    '房型': ['標準雙人房(1 張加大雙人床)', '標準雙床房(1 張加大雙人床)', '豪華四人房(1 張加大雙人床)', '高級雙人房(1 張加大雙人床)']},
                    {'飯店名稱': '夢想12旅店 ', 
                     '評分': '9.4', 
                     '訂房網站': 'https://www.booking.com/hotel/tw/hong-ding-guo-ji-shang-lu.zh-tw.html', 
                     '熱門設施': ['停車場 ', '家庭房 ', '免費無線網路 ', '禁菸客房 ', '機場接駁車 ', '餐廳 ', '客房服務 ', '所有客房都有咖啡／沏茶設施 ', '早餐評價優異 '], 
                     '房型': ['電影雙人房－附陽台(1 張雙人床)', '高級四人房－附陽台(1 張雙人床)', '高級雙人房－附陽台(1 張雙人床)', '豪華雙人房－附陽台(1 張雙人床)', '標準雙床房附陽台(1 張雙人床)', '標準雙人房－附陽台(1 張雙人床)']}
]
'''
print('將旅宿資料寫入 Firestore !')
print('資料寫入中...')
if not firebase_admin._apps:
    cred = credentials.Certificate("hotel-1a77a-firebase-adminsdk-bnri1-fd5cb200db.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

for i in range(len(hotel_info_list)):
    # document 由 firestore hash 產生
    db.collection('台中推薦飯店').add(hotel_info_list[i])
db.close()
print('旅宿資料寫入完畢 !')

end_time = time.time()
elapsed_time = end_time - start_time
print(elapsed_time) 
#print(len(hotel_info_list))
