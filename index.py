from flask import Flask, request, make_response, jsonify
app = Flask(__name__)
import openai
import os
openai.api_key = os.getenv("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")
@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    msg =  req["queryResult"]["queryText"]
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=msg,
        max_tokens=100,
        temperature=0.5,
    )
    info = "AI：" + response.choices[0].text
    return make_response(jsonify({"fulfillmentText": info}))
if __name__ == "__main__":
    app.run()
