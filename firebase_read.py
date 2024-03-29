import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import os
import random

def get_all_view(area):
    area_view_dict = {}
    area_view = []

    # keyFilePath = os.path.abspath(os.path.dirname(__file__)) + "/serviceAccountKey.json"
    # cred = credentials.Certificate(keyFilePath)
    # firebase_admin.initialize_app(cred)

    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    collection_ref = db.collection(area)
    views_info = collection_ref.get()

    info = "以下是"+area+"推薦的著名景點:\n\n"
    for view in views_info:
        view_info = view.to_dict()
        area_view.append(view_info)
    area_view_dict[area] = area_view
    # print(area_view_dict)
    # info += result.get("view") + "\n"
    
    # print(area_view)

    num_choices = 5
    random_views = random.sample(area_view, num_choices)

    for view in random_views:  
        info += view['view'] + '\n'
    info += "\n" + "想了解哪個景點?"

    #print(info)
    firebase_admin.delete_app(firebase_admin.get_app())
    
    return info, area_view_dict

# print(get_all_view("台中"))

# def get_view_introducion(area, view):
#     db = firestore.client()
    
#     collection_ref = db.collection(area)
#     docs = collection_ref.get()
    
#     introduction = ""
#     for doc in docs:
#         result = doc.to_dict()
#         if view in result.get("view"):
#             introduction += "景點：" + result.get("view")+ "\n"
#             introduction += "景點介紹：" + result.get("introduction")+ "\n"
#             introduction += "地址：" + result.get("address") + "\n"
#             introduction += "開放時間：" + result.get("time") + "\n"
#             introduction += "票價：" + result.get("ticket") + "\n"
    
#     # print(introduction)
#     return introduction

# # get_view_introducion("台中", "高美濕地")

# def get_view_introducion(view):
    
#     keyFilePath = os.path.abspath(os.path.dirname(__file__)) + "/serviceAccountKey.json"
#     cred = credentials.Certificate(keyFilePath)
#     firebase_admin.initialize_app(cred)

#     cred = credentials.Certificate("serviceAccountKey.json")
#     firebase_admin.initialize_app(cred)
    
#     db = firestore.client()
    
#     collection_names = [
#        "台中", "苗栗", "彰化", "南投", "雲林", "台北", "新北", "基隆",
#        "桃園", "新竹", "宜蘭", "高雄", "台南", "嘉義", "屏東", "花蓮", "台東"]
#     info = ""

#     for collection_name in collection_names:
#         collection_ref = db.collection(collection_name)
#         docs = collection_ref.where('view', '==', view)
#         results = docs.get()
#         for doc in results:
#             result = doc.to_dict()
#             info += "景點：" + result.get("view") + "\n\n"
#             info += "景點介紹：" + result.get("introduction") + "\n\n"
#             info += "地址：" + result.get("address")
#             # info += "開放時間：" + result.get("time") + "\n\n"
#             # info += "票價：" + result.get("ticket")
#     print(info)

#     firebase_admin.delete_app(firebase_admin.get_app())
    
#     return info

# # get_view_introducion("高美濕地")

# if __name__ == "__main__":
#     area = '台中'   
#     get_all_view(area)
#     # view = '高美濕地'
#     # get_view_introducion(view)
