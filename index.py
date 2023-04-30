from flask import Flask, request, make_response, jsonify
app = Flask(__name__)
import openai
import os
openai.api_key = os.getenv("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")
@app.route("/webhook", methods=["POST"])
def webhook():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    parameters =  req.get("queryResult").get("parameters")
    if (parameters == "area"):
        area =  req.get("queryResult").get("parameters").get("area")
        info = "您選擇的旅遊區域是：" + area

    return make_response(jsonify({"fulfillmentText": info}))

if __name__ == "__main__":
    app.run()
