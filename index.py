import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

from flask import Flask, request, make_response, jsonify
app = Flask(__name__)
import openai
import os
#openai.api_key = os.getenv("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")
@app.route("/webhook", methods=["POST"])
def webhook():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    if (action == "cityChoice"):
        city =  req.get("queryResult").get("parameters").get("city")
        info = "您所選擇的旅遊地區是：" + city 

    def get_link(https://console.firebase.google.com/u/2/project/travel-bc3b6/firestore/data/):

        db = firestore.client()

        collection_ref = db.collection("台中")
        #view = "高美濕地"
        view = input("景點 : ")  # 用於來讀取想要前往的景點名稱
        docs = collection_ref.where("view", "==", view).get()

        for doc in docs:
            result = doc.to_dict()
            print("景點：" + result.get("view"))
            print("景點介紹：" + result.get("introduction"))
            print("地址：" + result.get("address"))
            print("開放時間：" + result.get("time"))
            print("票價：" + result.get("ticket"))

    get_link()


    return make_response(jsonify({"fulfillmentText": info}))

if __name__ == "__main__":
    app.run()
