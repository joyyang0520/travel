import firebase_admin
from firebase_admin import credentials, firestore
import random
from google.cloud.firestore_v1.base_query import FieldFilter
import os

def get_recommend_hotels(city):

    # keyFilePath = os.path.abspath(os.path.dirname(__file__)) + "/hotel-1a77a-firebase-adminsdk-bnri1-fd5cb200db.json"
    # cred = credentials.Certificate(keyFilePath)
    # firebase_admin.initialize_app(cred)

    cred = credentials.Certificate("hotel-1a77a-firebase-adminsdk-bnri1-fd5cb200db.json")
    firebase_admin.initialize_app(cred)

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
    #num_choices = min(num_choices, len(hotel_info_list))
    random_hotels = random.sample(hotel_info_list, num_choices)
    #print(hotel_info_list)

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
    cities = ['台中','基隆','彰化','屏東','新竹市','苗栗','南投','雲林','嘉義縣','嘉義市','屏東','宜蘭','花蓮','台東','台北','新北','台南','高雄','新竹縣']
    for city in cities:   
        get_recommend_hotels(city)
'''
