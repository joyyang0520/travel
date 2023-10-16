import firebase_admin
from firebase_admin import credentials, firestore
import random

def get_recommend_hotels(city):
    city = city + '推薦飯店'
    # ===== while test on computer =====
    from google.cloud.firestore_v1.base_query import FieldFilter
    import os
    keyFilePath = os.path.abspath(os.path.dirname(__file__)) + "/hotel-1a77a-firebase-adminsdk-bnri1-fd5cb200db.json"
    cred = credentials.Certificate(keyFilePath)
    firebase_admin.initialize_app(cred)

    # cred = credentials.Certificate("hotel-1a77a-firebase-adminsdk-bnri1-fd5cb200db.json")
    # firebase_admin.initialize_app(cred)

    db = firestore.client()
    doc_ref = db.collection(city)
    Taichung_recommend_info = doc_ref.get()

    hotel_dict = {}
    hotel_info_list = []
    info = ''
    info += '以下為您推薦三間訂房網站上評價非常好的飯店!' + '\n\n'

    for hotel in Taichung_recommend_info:
        hotel_info = hotel.to_dict()
        hotel_info_list.append(hotel_info)
    hotel_dict[city] = hotel_info_list
    #print(hotel_dict)

    num_choices = 3
    random_hotels = random.sample(hotel_info_list, num_choices)
    
    for hotel in random_hotels:
        hotel_name = hotel['飯店名稱']
        hotel_score = hotel['評分']    
        info += hotel_name + '\n'
        info += '評分:' + hotel_score + '\n\n'
    #print(info)
    #print(random_hotels)
    info += '請問您對哪家有興趣呢，以便為您提供更詳細的資訊'
    firebase_admin.delete_app(firebase_admin.get_app())
    return info, hotel_dict
'''
if __name__ == "__main__":
    city = '台中'
    get_recommend_hotels(city)

hotel_indices = list(range(len(hotel_info_list)))
random.shuffle(hotel_indices)

for i in range(3):
    #當所有飯店都被選擇過之後，會全部reset
    if not hotel_indices:
        hotel_indices = list(range(len(hotel_info_list)))
        random.shuffle(hotel_indices)
    
    random_index = hotel_indices.pop()
    selected_hotel = hotel_info_list[random_index]
    print(selected_hotel)
'''
