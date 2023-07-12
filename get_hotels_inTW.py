from hotel_info import a_hotel_details
import requests
from bs4 import BeautifulSoup


def get_hotels_bycity(city):
	_url = 'https://taiwanstay.net.tw'
	#saveHTMLFileName = 'test.html' 

	#print('請輸入縣市: ',end='')
	#user_input = input()
	#print(type(user_input))
	#user_input = '新竹市'
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
	add_hotel = 0
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
			#address = item.find('a',class_='blu').get('title')
			web = item.find('a').get('href')
			#print(web)
			hotel_list.append(a_hotel_details(web))
			#for k,v in hotel_list[add_hotel].items():
				#print("{}:{}".format(k,v))
			#print('\n')
			#hotel_dict[user_input].append({"旅宿名稱":title,"網址":web })
			add_hotel += 1
			#info += title + '\n' + web + '\n\n'
			#print(title + '\n' + address + '\n' + web + '\n\n')
		sum += 25
	print(city + "總共" + str(add_hotel) + "筆資料")
	return(hotel_list)

_taiwan_cities = ['臺北市', '新北市', '基隆市', '桃園市', '新竹縣', \
                  '新竹市', '苗栗縣', '臺中市', '南投縣', '彰化縣', \
                  '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', \
                  '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', \
                  '金門縣', '連江縣'
                  ]
get_all_hotels = {}
for city in _taiwan_cities:
	get_all_hotels[city] = get_hotels_bycity(city)
