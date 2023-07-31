from flask import Flask, render_template, request, make_response, jsonify
from firebase_read import get_all_view, get_view_introducion
from weather import get_weather_data
import chatGPT
from get_help import get_help
from read_hotel_CSV import get_city_hotel

app = Flask(__name__)
# 定義全局變數
app.config['request_city'] = ''
app.config['city_hotels'] = {} # {'基隆市':[...], '臺北市':[...], ...}

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    # force=True

    # request_data = request.get_json()
    action = req.get("queryResult").get("action")
    user_message = req.get("queryResult").get("queryText")

    print(action)

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
    
    elif (action == "hotelcitychoice"):
        # request_city = req.get("queryResult").get("parameters").get("cities")
        app.config['request_city'] = req.get("queryResult").get("parameters").get("cities")
        
        return make_response()
    
    elif (action == "hotelprice"):
        price = req.get("queryResult").get("parameters").get("any")
        # request_city = app.config['request_city']
        # print(request_city)
        # 原始字串
        #text = price
        # 使用內建方法提取整數
        extracted_integer = int(''.join(filter(str.isdigit, price)))

        info, all_city_hotel = get_city_hotel(app.config['request_city'], extracted_integer)
        app.config['city_hotels'].update(all_city_hotel)
        #print(app.config['city_hotels'][app.config['request_city']])

        return make_response(jsonify({"fulfillmentText": info}))
    
    elif (action == "hotelintroduction"):
        hotel = req.get("queryResult").get("parameters").get("any")

        info = hotel_details(hotel)

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

        print('action: ' + action + 'info :' + info)

        return make_response(jsonify({"fulfillmentText": info}))

    # return make_response(jsonify({"fulfillmentText": info}))

info = ''
def hotel_details(hotel):
    info = ''
    city = app.config['request_city']
    if city in app.config['city_hotels'].keys():
        for h in app.config['city_hotels'][city]:
            if hotel == h['旅宿名稱']:
                info += '以下為' + h['旅宿名稱'] + '的詳細資料\n\n' 
                info += '地址:' + h['地址'] + '\n\n'
                info += '電話:' + h['電話'] + '\n\n'
                info += '官方網站:' + h['官方網站'] + '\n\n'
                info += '總房間數:' + h['總房間數'] + '\n\n'
                info += '定價:' + h['定價'] + '\n\n'
                info += '星級:' + h['星級'] + '\n'
        print(info)
    return info

if __name__ == "__main__":
    app.run()
