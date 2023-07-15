from flask import Flask, render_template, request, make_response, jsonify
from firebase_read import get_all_view, get_view_introducion
from weather import get_weather_data
import chatGPT
from get_help import get_help


app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    req = request.get_json(force=True)
    # force=True

    # request_data = request.get_json()
    action = req.get("queryResult").get("action")
    user_message = req.get("queryResult").get("queryText")

    if (user_message == "help"):
        info = get_help()

        return make_response(jsonify({"fulfillmentText": info}))
# --------------------------------------------------------------------------- #
    if (action == "viewintroduction"):
        view = req.get("queryResult").get("parameters").get("any")

        info = get_view_introducion(view)
        return make_response(jsonify({"fulfillmentText": info}))

    elif (action == "countyChoice"):
        area = req.get("queryResult").get("parameters").get("county")

        info = get_all_view(area)

        return make_response(jsonify({"fulfillmentText": info}))

    elif (action == "search_weather"):
        area = req.get("queryResult").get("parameters").get("county")

        info = get_weather_data(area)

        return make_response(jsonify({"fulfillmentText": info}))

    elif (action == "input.unknown"):

        info = chatGPT.reply(user_message)

        return make_response(jsonify({"fulfillmentText": info}))
    
    elif (action == "input.welcome"):

        info = "你好~~，有需要什麼幫助嗎?"

        return make_response(jsonify({"fulfillmentText": info}))

    # return make_response(jsonify({"fulfillmentText": info}))


if __name__ == "__main__":
    app.run()
