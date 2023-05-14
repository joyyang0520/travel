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
