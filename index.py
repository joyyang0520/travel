import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, request, make_response, jsonify
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    #action =  req.get("queryResult").get("action")
    msg =  req.get("queryResult").get("queryText")
    info = "查詢內容：" + msg

    db = firestore.client()

    collection_ref = db.collection("台中")
    view = "舊山線八號隧道"
    #view = input("景點 : ")  # 用於來讀取想要前往的景點名稱
    docs = collection_ref.get()

    msg = ""
    for doc in docs:
        result = doc.to_dict()
        if view in result.get("view"):
            msg += "景點：" + result.get("view") + "<br>"
            msg += "景點介紹：" + result.get("introduction") + "<br>"
            msg += "地址：" + result.get("address") + "<br>"
            msg += "開放時間：" + result.get("time") + "<br>"
            msg += "票價：" + result.get("ticket") + "<br><br>"
    msg = info + "<br>" + msg
    return make_response(jsonify({"fulfillmentText": msg}))

if __name__ == "__main__":
    app.run()
