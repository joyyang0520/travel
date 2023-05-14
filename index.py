import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import openai
openai.api_key = os.getenv("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")

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, request, make_response, jsonify
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    #action =  req.get("queryResult").get("action")
    #msg =  req.get("queryResult").get("queryText")
    view =  req.get("queryResult").get("parameters").get("any")
    info = "查詢內容：" + view

    db = firestore.client()

    collection_ref = db.collection("新北")
    docs = collection_ref.get()

    msg = ""
    for doc in docs:
        result = doc.to_dict()
        if view in result.get("view"):
            msg += "景點：" + result.get("view")+ "\n\n"
            msg += "景點介紹：" + result.get("introduction")+ "\n\n"
            msg += "地址：" + result.get("address") + "\n\n"
            msg += "開放時間：" + result.get("time") + "\n\n"
            msg += "票價：" + result.get("ticket") + "\n"

    msg = info + "\n\n" + msg
    return make_response(jsonify({"fulfillmentText": msg}))

    messages = ""
    while True:
    msg = input('me > ')
    messages.append({"role":"user","content":msg})   # 添加 user 回應
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=50,
        temperature=0.5,
        messages=messages
    )
    ai_msg = response.choices[0].message.content.replace('\n','')
    messages.append({"role":"assistant","content":ai_msg})   # 添加 ChatGPT 回應
    print(f'ai > {ai_msg}')

if __name__ == "__main__":
    app.run()
