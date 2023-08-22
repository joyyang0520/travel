import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager
import base64
import requests


options = Options() #取消網頁中的彈出視窗
options.add_argument("--disable-notifications")
 
chrome = webdriver.Chrome(options=options)
chrome.get("https://tw.piliapp.com/tw-railway/")

def get_timetale(station1, station2, date):
    request_text = chrome.find_element(By.ID, "q")
    request_text.send_keys(station1 + ' ' + station2 + ' ' + date)

    request_text.send_keys(Keys.RETURN)

    time.sleep(10)
    page_content = chrome.page_source #取得網頁內的內容

    soup = BeautifulSoup(page_content,'html.parser')

    time_list = []
    table_trs = soup.find_all('tr')

    for t in table_trs:
        if t.find('td'):
            td_text = [td.text.strip() for td in t.find_all('td')] #使用strip()，每個文字的前後空白字符都會被去除，進而過濾掉跳行和空格
            time_list.append(td_text)
        else:
            th_text = [th.text.strip() for th in t.find_all('th')]
            time_list.append(th_text)

    for i, train in enumerate(time_list):
        text = ' '.join(train)  # 將子列表中的文字連接起來
        print(f'({i}) {text}')

    #print(time_list)
    return time_list
    chrome.quit()

if __name__ == "__main__":
    station1 = '沙鹿'
    station2 = '台北'
    date = '8/18'
    get_timetale(station1, station2, date)