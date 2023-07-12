import requests
from bs4 import BeautifulSoup

#URL = 'https://www.taiwanstay.net.tw/room/19125'
URL = 'https://www.taiwanstay.net.tw/room/1934'
r = requests.get(URL)
soup = BeautifulSoup(r.text,'html.parser')
#star_count = 0
level = soup.find_all('i',class_='fa fa-star')
print(len(level))
	
#URL = 'https://www.taiwanstay.net.tw/room/1640'
#URL = 'https://www.taiwanstay.net.tw/room/2414'	
#print(a_hotel_details(URL))