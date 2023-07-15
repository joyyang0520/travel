from hotel_info import a_hotel_details
import requests
from bs4 import BeautifulSoup

def get_hotels_bycity(city):
	_url = 'https://taiwanstay.net.tw'
	#print('請輸入縣市: ',end='')
	#user_input = input()
	print('--------------------以下為' + city + '的所有住宿資訊--------------------')

	URL = _url + '/legal-hotel-list?hoci_city=' + city 
	r = requests.get(URL)
	soup = BeautifulSoup(r.text,'html.parser') 

	pages = ""
	page = soup.find_all('div',class_='text-center all_num')
	for p in page:
		all_page = p.find('span')
		pages += all_page.text
		print(pages)

	sum = 0
	hotel_count = 0
	hotel_list = []
	#info = ""
	for i in range(0,int(pages),1):	
		update_URL = _url + '/legal-hotel-list?hoci_city=' + city + '&start=' + str(sum)
		r = requests.get(update_URL)
		soup = BeautifulSoup(r.text,'html.parser') 

		#print(update_URL)
		result = soup.find_all('div',class_='row bg-color-white margin-bottom-20')
		for item in result:
			title = item.find('a').get('title')
			web = item.find('a').get('href')
			hotel_list.append(a_hotel_details(web))
			#for k,v in hotel_list[hotel_count].items():
				#print("{}:{}".format(k,v))
			#print('\n')
			#hotel_dict[user_input].append({"旅宿名稱":title,"網址":web })
			hotel_count += 1
		sum += 25
	print(city + "總共" + str(hotel_count) + "筆資料")
	return (hotel_list, hotel_count)
	#total_count += hotel_count

total_count = 0	

_taiwan_cities = ['臺北市', '新北市', '基隆市', '桃園市', '新竹縣', \
                  '新竹市', '苗栗縣', '臺中市', '南投縣', '彰化縣', \
                  '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', \
                  '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', \
                  '金門縣', '連江縣'
                  ]                 
get_all_hotels = {}
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
	cred = credentials.Certificate("hotel-1a77a-firebase-adminsdk-bnri1-fd5cb200db.json")
	firebase_admin.initialize_app(cred)
db = firestore.client()

for city in _taiwan_cities:
	info, count = get_hotels_bycity(city)
	get_all_hotels[city] = info
	total_count += count
	ref = db.collection("全台灣旅宿")
	db.collection("全台灣旅宿").document(city).set({"總旅宿":count})
	for i in range(count):
		ref.document(city + "-" + "旅宿編號" + str(i)).set(info[i])
	db.close()
print(total_count)
	