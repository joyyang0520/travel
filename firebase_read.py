import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey_Dorncy.json")
firebase_admin.initialize_app(cred)

def get_all_view(area):
    db = firestore.client()

    collection_ref = db.collection(area)
    docs = collection_ref.get()

    info = "以下是"+area+"的著名景點:\n\n"
    for doc in docs:
        result = doc.to_dict()
        info += result.get("view") + "\n"
    info += "\n" + "想了解哪個景點?"
    return info

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

def get_view_introducion(view):
    db = firestore.client()
    
    collection_names = [
       "台中", "苗栗", "彰化", "南投", "雲林", "台北", "新北", "基隆",
       "桃園", "新竹", "宜蘭", "高雄", "台南", "嘉義", "屏東", "花蓮", "台東"]
    info = ""
    for collection_name in collection_names:
        collection_ref = db.collection(collection_name)
        docs = collection_ref.where('view', '==', view)
        results = docs.get()
        for doc in results:
            result = doc.to_dict()
            info += "景點：" + result.get("view") + "\n\n"
            info += "景點介紹：" + result.get("introduction") + "\n\n"
            info += "地址：" + result.get("address")
            # info += "開放時間：" + result.get("time") + "\n\n"
            # info += "票價：" + result.get("ticket")
    # print(info)
    return info
    
# get_view_introducion("高美濕地")
