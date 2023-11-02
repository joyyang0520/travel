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
import re

if __name__ == "__main__":

    cities = ['台中','基隆','彰化','屏東','新竹市','苗栗','南投','雲林','嘉義縣','嘉義市','屏東','宜蘭','花蓮','台東','台北','新北','台南','高雄','新竹縣']
    

    start_time = time.time()
    
    for city in cities:
        #url = 'https://www.booking.com/searchresults.zh-tw.html?ss=' + city + '&nflt=review_score%3D90%3Breview_score%3D80&order=bayesian_review_score'
        url = 'https://www.booking.com/searchresults.zh-tw.html?ss=' + city + '&nflt=review_score%3D80%3Breview_score%3D90%3Breview_score%3D70&order=bayesian_review_score'
        print(f'\nurl: {url}')

        user_agent = ua.UserAgent().get_latest('Chrome') # modified by Peter
        print(f"user_agent: {user_agent}")
        options = Options()
        options.add_argument("--headless")  # Remove this if you want to see the browser (Headless makes the chromedriver not have a GUI)
        options.add_argument("--window-size=1920,1080")
        options.add_argument("user-agent=%s"%user_agent)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        driver = webdriver.Chrome(options = options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { # 清空 window.navigator 
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """
        }) # added by Peter
        driver.implicitly_wait(20)   # added by Peter
        driver.get(url)
        #print(driver.page_source)
        page_content = driver.page_source #取得網頁內的內容
        soup = BeautifulSoup(page_content,'html.parser')

        hotel_info_list = []

        hotels = soup.find_all('div',class_='f6431b446c a15b38c233') 
        web_pages = soup.find_all('div',class_='e952b01718')
        scores = soup.find_all('div',class_='a3b8729ab1 d86cee9b25')

        driver.close() #關閉網頁 
        driver.quit()

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
            print(hotel_web)
            hotel_info_list.append(hotel_info_dict)

            url = hotel_web
            #print(f'\nurl: {url}')

            #user_agent = ua.UserAgent().get() # marked by Peter
            #print(f"user_agent: {user_agent}")
            options = Options()
            options.add_argument("--headless")  # Remove this if you want to see the browser (Headless makes the chromedriver not have a GUI)
            options.add_argument("--window-size=1920,1080")
            options.add_argument("user-agent=%s"%user_agent)
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-extensions")
            driver = webdriver.Chrome(options = options)
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { # 清空 window.navigator 
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """
            }) # added by Peter
            driver.implicitly_wait(20)  # added by Peter
            driver.get(url)
            # print(driver.page_source)
            WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"span.a5a5a75131"))) # added by Peter
            page_content = driver.page_source #取得網頁內的內容
            soup = BeautifulSoup(page_content,'html.parser')

            services = soup.find('div',class_='hp--popular_facilities js-k2-hp--block').find_all('span',class_='a5a5a75131')
            service_list = []
            for service in services:
                hotel_service = service.text
                service_list.append(hotel_service)
            hotel_info_dict['熱門設施'] = service_list  

            #print(f"{hotel_info_dict['飯店名稱']} {service_list}") 
            #print(services)   

            rooms = soup.find_all('div',class_='ed14448b9f b817090550 e7f103ee9e')
            room_list = []
            for room in rooms:
                hotel_room = room.text.strip()
                hotel_room = hotel_room.replace(' ','')
                #找到第一個出現1 2的位置
                first_one_index = hotel_room.find('1')
                first_two_index = hotel_room.find('2')

                #如果有找到1 2，確定添加(的位置
                if first_one_index != -1 or first_two_index != -1:
                    if first_one_index != -1 and (first_two_index == -1 or first_one_index < first_two_index):
                        insert_index = first_one_index
                    else:
                        insert_index = first_two_index

                    hotel_room = hotel_room[:insert_index] + '(' + hotel_room[insert_index:]
                hotel_room += ')'
                #print(hotel_room)
                room_list.append(hotel_room)

            hotel_info_dict['房型'] = room_list
            #print(room_list)

            checkin = soup.find('div', {'id': 'checkin_policy'})
            checkin_time = checkin.find_all('p')[1].text.strip().replace(' ','')
            hotel_info_dict['入住時間'] = checkin_time
            #print(checkin_time)

            checkout = soup.find('div', {'id': 'checkout_policy'})
            checkout_time = checkout.find_all('p')[1].text.strip().replace(' ','')
            hotel_info_dict['退房時間'] = checkout_time
            #print(checkout_time)
            
            driver.close() #關閉網頁
        driver.quit() #關閉瀏覽器
    #print(hotel_info_list)   

        print('將旅宿資料寫入 Firestore !')
        print('資料寫入中...')
        if not firebase_admin._apps:
            cred = credentials.Certificate("hotel-1a77a-firebase-adminsdk-bnri1-fd5cb200db.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()

        for i in range(len(hotel_info_list)):
            # document 由 firestore hash 產生
            db.collection(city + '推薦飯店').add(hotel_info_list[i])
        db.close()
        print('旅宿資料寫入完畢 !')

        hotel_info_list = []

end_time = time.time()
elapsed_time = end_time - start_time
#print(elapsed_time) 
#print(len(hotel_info_list))
