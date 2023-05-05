import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def get_link():

    db = firestore.client()

    collection_ref = db.collection("台中")
    #view = "高美濕地"
    view = input("景點 : ")  # 用於來讀取想要前往的景點名稱
    docs = collection_ref.get()

    for doc in docs:
        result = doc.to_dict()
        if view in result.get("view"):
            #print("景點：" + result.get("view"))
            print("景點介紹：" + result.get("introduction"))
            print("地址：" + result.get("address"))
            print("開放時間：" + result.get("time"))
            print("票價：" + result.get("ticket"))

get_link()
