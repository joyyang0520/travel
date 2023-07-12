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
	
	level = soup.find_all('i',class_='fa fa-star')
	if len(level) != 0:
		hotel_info['星級'] = len(level)
	else:
		hotel_info['星級'] = '-'
	
	return(hotel_info)
	
#print(a_hotel_details(URL))