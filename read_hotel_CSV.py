import csv, os
'''
_taiwan_cities = ['臺北市', '新北市', '基隆市', '桃園市', '新竹縣', \
                  '新竹市', '苗栗縣', '臺中市', '南投縣', '彰化縣', \
                  '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', \
                  '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', \
                  '金門縣', '連江縣'
                  ]  
'''

def get_city_hotel(city_for_hotel, price):
    FilePath = os.path.abspath(os.path.dirname(__file__)) + "/" + city_for_hotel + "_hotels_v2.csv" 
    file = open(FilePath)
    reader = csv.DictReader(file)
    hotel_list = []
    hotel_dict = {}
    for r in reader:
        hotel_list.append(r)
    hotel_dict[city_for_hotel] = hotel_list
    '''
    for i, hotel in enumerate(hotel_dict[city_for_hotel]):
        print(hotel["定價"])
        if hotel["定價"] == '-':
            hotel_dict[city_for_hotel][i]["定價i"] = 0
            continue
        hotel_dict[city_for_hotel][i]["定價i"] = int(hotel["定價"].split('$')[1].split('-')[0])
   
    hotel_dict[city_for_hotel] = sorted(hotel_dict[city_for_hotel], key=lambda _dict: _dict["定價i"], reverse=False)
    
    print(hotel_dict[city_for_hotel])
    '''
    info = ''
    max_index = search_hotel(hotel_dict[city_for_hotel], price)
    #print(f"找到數值於索引為：{max_index}")
    info = '以下為' + city_for_hotel + '最低價格為' + str(price) + '元以下的所有飯店:' + "\n\n" 
    for i in range(max_index + 1):
        info += hotel_dict[city_for_hotel][i]['旅宿名稱'] + "\n" 
    info += '\n請問需要哪間飯店的詳細資訊?'
    #print(info)
    file.close()
    
    return info, hotel_dict

def search_hotel(list, price):
    low = 0
    upper = len(list) - 1
    max_index = -1

    while low <= upper:
        mid = int((low + upper) / 2)
        current_num = int(list[mid]['定價i'])

        if current_num <= price:
            max_index = mid
            low = mid + 1
        else:
            upper = mid - 1

    return max_index

'''
if __name__ == "__main__":
    city_for_hotel = '新竹市'
    get_city_hotel(city_for_hotel, 1000)
'''