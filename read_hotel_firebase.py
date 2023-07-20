import firebase_admin
from firebase_admin import credentials, firestore
import time
'''
_taiwan_cities = ['臺北市', '新北市', '基隆市', '桃園市', '新竹縣', \
                  '新竹市', '苗栗縣', '臺中市', '南投縣', '彰化縣', \
                  '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', \
                  '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', \
                  '金門縣', '連江縣']  
'''
#time_start = time.time()
def get_hotels(_taiwan_cities):
	if not firebase_admin._apps:
		cred = credentials.Certificate("hotel-1a77a-firebase-adminsdk-bnri1-fd5cb200db.json")
		firebase_admin.initialize_app(cred)
	db = firestore.client()

	cities_dict = {}
	for _city in _taiwan_cities:
		total_hotels = db.collection('全台灣旅宿').document(_city).get().to_dict()['總旅宿']
		print('{}, {}旅宿總數: {} '.format(type(total_hotels), _city, total_hotels))

		cities_dict[_city] = []

		for i in range(total_hotels):
			_doc_id = _city + '-' + '旅宿編號' + str(i)
			_hotels_info = db.collection('全台灣旅宿').document(_doc_id).get().to_dict()
			#print('({}) {}'.format(i, _hotels_info))
			cities_dict[_city].append(_hotels_info)
		#print(cities_dict)

		for i, hotel in enumerate(cities_dict[_city]):
			   cities_dict[_city][i]["定價i"] = int(hotel["定價"].split('$')[1].split('-')[0])
		#print(hsin_chu_hotels)

		cities_dict[_city] = sorted(cities_dict[_city], key=lambda _dict: _dict["定價i"], reverse=False)
	return cities_dict

# ---- webhook ----
#if __name__ == '__main__':

hotels = {}
query_city = ['臺北市', '新北市', '基隆市', '桃園市', '新竹縣', \
              '新竹市', '苗栗縣', '臺中市', '南投縣', '彰化縣', \
              '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', \
              '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', \
              '金門縣', '連江縣'
              ]

#if query_city[0] not in hotels.keys():
	#city = []
	#city.append(query_city)
hotels.update(get_hotels(query_city))

#for i in range(21):
#for _hl in hotels[query_city[0]]:
	#print(_hl)
	#print('-----------------------------------------------------------')

#hotels[query_city][0] # 第一筆旅色資料
#for _hl in hotels[query_city[0]]:
#	print(_hl)
#print(hotels[query_city])

'''
		print(type(result))
		
		print("-----旅宿便宜到貴排序-----\n")
		for x in result:
			for k,v in cities_dict[_city].items():
				if k == "旅宿名稱":
					print(v)
				elif k == "定價i":
					print(v)
'''
#print(time.time() - time_start)
