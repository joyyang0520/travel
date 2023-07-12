import requests
from bs4 import BeautifulSoup

def a_hotel_details(URL):
	hotel_info = {}

	r = requests.get(URL)
	soup = BeautifulSoup(r.text,'html.parser')
	tables = soup.find_all('table',class_='table table-striped')
	for table in tables:
		if '旅宿名稱' not in hotel_info.keys():
			hotel_info['旅宿名稱'] = table.find('caption').text.replace(' ','').replace('\n','')

		table_trs = table.find('tbody').find_all('tr')
		for tr in table_trs:
			x = tr.find('th').text.replace(' ','').replace('\n','')
			if x == '地址': 
				hotel_info[x] = tr.find('td').text.replace(' ','').replace('\n','')
			elif x == '電話':
				hotel_info[x] = tr.find('td').text.replace(' ','').replace('\n','')
			elif x == '官方網站':
				if tr.find('a') != None:
					hotel_info[x] = tr.find('a').get('href')
				else:
					hotel_info[x] = tr.find('span').text.replace(' ','').replace('\n','')
			elif x == '總房間數':
				hotel_info[x] = tr.find('td').text.replace(' ','').replace('\n','')
			elif x == '定價':
				hotel_info[x] = tr.find('td').text.replace(' ','').replace('\n','')
			#print(tr.find('th').text.replace(' ','').replace('\n',''))
			#print(tr.find('td').text.replace(' ','').replace('\n',''))

		#print(tables_result)
	#print(hotel_info)
	return(hotel_info)

#URL = 'https://www.taiwanstay.net.tw/room/1640'
#URL = 'https://www.taiwanstay.net.tw/room/2414'	
#print(a_hotel_details(URL))