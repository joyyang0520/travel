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
        info = "您所選擇的旅遊地區是：" + city + "，相關景點:\n"

        collection_ref = db.collection("台中")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if city in dict["city"]:
                result += "景點" + dict["title"]+"\n"
            info += result

    return make_response(jsonify({"fulfillmentText": info}))

if __name__ == "__main__":
    app.run()
