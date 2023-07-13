import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
	cred = credentials.Certificate("hotel-1a77a-firebase-adminsdk-bnri1-fd5cb200db.json")
	firebase_admin.initialize_app(cred)
db = firestore.client()

_taiwan_cities = ['城市名稱']

for _city in _taiwan_cities:
	total_hotels = db.collection('全台灣旅宿').document(_city).get().to_dict()['總旅宿']
	print('{}, {}旅宿總數: {} '.format(type(total_hotels), _city, total_hotels))
	for i in range(total_hotels):
		_doc_id = _city + '-' + '旅宿編號' + str(i)
		_hotels_info = db.collection('全台灣旅宿').document(_doc_id).get().to_dict()
		print('({}) {}'.format(i, _hotels_info))
'''
data = [{
		"旅宿名稱":"台北美福大飯店",
		"地址":"台北市中山區樂群二路55號",
		"電話":"02-77223399",
		"官方網站":"https://www.grandmayfull.com/",
		"總房間數":"146間",
		"定價":"NT$14000-20000"
		},
		{
		"旅宿名稱":"瑞穗天合國際觀光酒店",
		"地址":"花蓮縣瑞穗鄉瑞祥村溫泉路2段368號",
		"電話":"03-8876000",
		"官方網站":"-",
		"總房間數":"198間",
		"定價":"NT$35200-35200"
		}
		]
ref = db.collection("全台灣旅宿")
db.collection("全台灣旅宿").document("城市名稱").set({"總旅宿":len(data)})
for i in range(len(data)):
	ref.document("城市名稱" + "-" + "旅宿編號" + str(i)).set(data[i])
db.close()

doc = db.collection("全台灣旅宿").document("城市名稱").get()
if doc.exists:
	for k, v in doc.to_dict().items():
		print("{}: {}".format(k, v))
else:
	print("No such document!")

'''