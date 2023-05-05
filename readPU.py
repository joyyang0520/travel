import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def get_link():

    db = firestore.client()

    collection_ref = db.collection("靜宜")
    #view = "高美濕地"
    cond = input("系級 : ")  # 用於來讀取想要前往的景點名稱
    docs = collection_ref.get()

    for doc in docs:
        result = doc.to_dict()
        if cond in result.get("name"):
        
        #print("景點：" + result.get("view"))
            print("系級：" + result.get("name"))
            print("班級：" + result.get("class"))
            

get_link()
