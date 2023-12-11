from flask import Flask, render_template, request, make_response, jsonify
from firebase_read import get_all_view
from weather import get_weather_data
import chatGPT
from get_help import get_help
from read_hotel_firebase import get_city_hotel
from read_recommend_hotel import get_recommend_hotels
import re
import random

app = Flask(__name__)

app.config['all_area_view'] = {}
app.config['request_area'] = ''
app.config['request_city'] = ''
app.config['city_hotels'] = {}
app.config['R_request_city'] = ''
app.config['R_city_hotels'] = {}
app.config['checkin'] = ''
app.config['checkout'] = ''
app.config['adults'] = ''
app.config['children'] = ''
app.config['children_age'] = ''
app.config['room_need'] = ''
app.config['age_list'] = []

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    # force=True

    # request_data = request.get_json()
    action = req.get("queryResult").get("action")
    user_message = req.get("queryResult").get("queryText")

    #print(action)

    if (user_message == "help"):
        info = get_help()

        return make_response(jsonify({"fulfillmentText": info}))
# --------------------------------------------------------------------------- #
    if (action == "countyChoice"):
        area = req.get("queryResult").get("parameters").get("county")

        if area in app.config['all_area_view'].keys():
            info = get_saved_area_view(area)
        else:
            info, all_area_views = get_all_view(area)
            app.config['all_area_view'].update(all_area_views)
        #print(app.config['all_area_view'])
        app.config['request_area'] = area

        return make_response(jsonify({"fulfillmentText": info}))
    
    elif (action == "viewintroduction"):
        view = req.get("queryResult").get("parameters").get("any")
        info = ''
        for area in app.config['all_area_view'][app.config['request_area']]:
            if 'view' in area.keys() and area['view'] == view:
                info += "景點：" + area['view'] + "\n\n"
                info += "景點介紹：" + area['introduction'] + "\n\n"
                info += "地址：" + area['address'] + "\n\n"
                info += "更多資訊：" + area['link']
                break
        #print(info)

        #info = get_view_introducion(view)

        return make_response(jsonify({"fulfillmentText": info}))

    # -------------------------Recommend Hotel--------------------------- #
    
    elif (action == "Rcitychoice"):
        city = req.get("queryResult").get("parameters").get("Rcities")
        city = city + '推薦飯店'
        #print(city)

        if city in app.config['R_city_hotels'].keys():
            info = get_saved_Rcity_hotel(city)
        else:
            info, all_Rcity_hotels = get_recommend_hotels(city)
            app.config['R_city_hotels'].update(all_Rcity_hotels)

            # delete the blank of hotel's name
            for i in range(len(app.config['R_city_hotels'][city])):
                n = len(app.config['R_city_hotels'][city][i]['飯店名稱'])
                if app.config['R_city_hotels'][city][i]['飯店名稱'][n-1] == " ":
                    app.config['R_city_hotels'][city][i]['飯店名稱'] = app.config['R_city_hotels'][city][i]['飯店名稱'][:n-1] 
            
        app.config['R_request_city'] = city

        return make_response(jsonify({"fulfillmentText": info}))
    
    elif (action == "Rhotelselect"): 
        name = req.get("queryResult").get("parameters").get("any")

        for hotel in app.config['R_city_hotels'][app.config['R_request_city']]:
            if '飯店名稱' in hotel.keys() and hotel['飯店名稱'] == name:
                app.config['single_hotel'] = hotel
                #print(app.config['single_hotel'])
                break

        return make_response()
    
    elif (action == "Rhotelservice"):
        info = ''
        info += '為您提供此飯店所提供的熱門設施服務:\n\n'
        services = app.config['single_hotel']['熱門設施']

        for service in services:
            info += '-' + service + '\n'
        #print(info)

        return make_response(jsonify({"fulfillmentText": info}))
    
    elif (action == "Rhotelroom"):
        info = ''
        info += '為您提供此飯店的所有房型和床型:\n\n'
        rooms = app.config['single_hotel']['房型']
        
        for room in rooms:
            info += '-' + room + '\n'
        #print(info)

        return make_response(jsonify({"fulfillmentText": info}))
    
    elif (action == "checkin_time"):
        info = ''
        info += app.config['single_hotel']['入住時間']

        return make_response(jsonify({"fulfillmentText": info}))
    
    elif (action == "checkout_time"):
        info = ''
        info += app.config['single_hotel']['退房時間']

        return make_response(jsonify({"fulfillmentText": info}))
    
    elif (action == "Rhotelweb"):
    
        return make_response()

    elif (action == "checkin_checkout"):
        app.config['checkin'] = req.get("queryResult").get("parameters").get("any")
        app.config['checkout'] = req.get("queryResult").get("parameters").get("any1")
        app.config['checkin'] = app.config['checkin'].replace(' ','')
        app.config['checkout'] = app.config['checkout'].replace(' ','')
        #print(app.config['checkin'])
        #print(app.config['checkout'])
        return make_response()
    
    elif (action == "peoplecount"):
        info = ''
        info += '請問需要幾間房間呢?'
        app.config['adults'] = req.get("queryResult").get("parameters").get("any")
        app.config['children'] = req.get("queryResult").get("parameters").get("any1")
        #print(app.config['adults'])
        #print( app.config['children'])

        if app.config['children'] != '0':
            return make_response()
        else:
            return make_response(jsonify({"fulfillmentText": info}))
        
    elif (action == "children_age"):
        app.config['children_age'] = req.get("queryResult").get("parameters").get("any")
        #print(app.config['children_age'])
        
        #將字串中的數字提取出來轉換成整數存入list
        app.config['age_list'] = re.findall(r'\d+', app.config['children_age'])
        app.config['age_list'] = [age for age in app.config['age_list']]
        #print(app.config['age_list'])

        return make_response()
       
    elif (action == "room_need"):
        app.config['room_need'] = req.get("queryResult").get("parameters").get("any")
        #print(app.config['room_need'])
        info = ''
        web = app.config['single_hotel']['訂房網站']

        if app.config['children'] == '0':
            info += web + '?checkin=' + app.config['checkin'] + '&checkout=' + app.config['checkout']\
                        + '&group_adults=' + app.config['adults'] + '&req_adults=' + app.config['adults'] + '&no_rooms=' + app.config['room_need']
            #print(info)
        else:
            info += web + '?checkin=' + app.config['checkin'] + '&checkout=' + app.config['checkout'] \
                        + '&group_adults=' + app.config['adults'] + '&req_adults=' + app.config['adults']\
                        + '&no_rooms=' + app.config['room_need'] + '&group_children=' + app.config['children'] + '&req_children=' + app.config['children']
            for i in app.config['age_list']:
                info += '&age=' + str(i) + '&req_age=' + str(i)
            #print(info)
            
        return make_response(jsonify({"fulfillmentText": info}))

    # ----------------------------Query Hotel--------------------------- #
   
    # elif (action == "hotelcitychoice"):
    #     app.config['request_city'] = req.get("queryResult").get("parameters").get("cities")
        
    #     return make_response()
    
    # elif (action == "hotelprice"):
    #     price = req.get("queryResult").get("parameters").get("any")
    #     print(f"price string : {price}")
    #     extracted_integer = int(''.join(filter(str.isdigit, price))) #??
    #     print(extracted_integer)
    
    #     if app.config['request_city'] in app.config['city_hotels'].keys():
    #         info = get_saved_city_hotel(app.config['request_city'], extracted_integer)
    #     else:
    #         info, all_city_hotels = get_city_hotel(app.config['request_city'], extracted_integer)
    #         app.config['city_hotels'].update(all_city_hotels)

    #     return make_response(jsonify({"fulfillmentText": info}))
    
    # elif (action == "hotelintroduction"):
    #     hotel = req.get("queryResult").get("parameters").get("any")

    #     info = hotel_details(hotel)

    #     return make_response(jsonify({"fulfillmentText": info}))
        
    elif (action == "search_weather"):
        area = req.get("queryResult").get("parameters").get("county")

        info = get_weather_data(area)

        return make_response(jsonify({"fulfillmentText": info}))

    elif (action == "input.unknown"):

        info = chatGPT.reply(user_message)

        return make_response(jsonify({"fulfillmentText": info}))
    
    elif (action == "input.welcome"):

        info = "您好~~\n我是旅遊推薦機器人^^\n"
        info += "以下為我能夠為您提供的服務:\n"
        info += "1.推薦景點--請輸入推薦景點\n2.推薦飯店--請輸入推薦飯店\n3.縣市天氣查詢--請輸入縣市+天氣"

        #print('action: ' + action + 'info :' + info)

        return make_response(jsonify({"fulfillmentText": info}))

'''
def get_saved_city_hotel(city_for_hotel, price):
    info = ''
    city_for_hotel = app.config['request_city']

    if city_for_hotel in app.config['city_hotels'].keys():
        max_index = search_hotel(app.config['city_hotels'][city_for_hotel], price)     
        if max_index == -1:
            print(f"找到數值於索引為：{max_index}")
            info = city_for_hotel + '無符合條件最低價格為' + str(price) + '元的飯店，請重新輸入更高的價格'
        else:
            print(f"找到數值於索引為：{max_index}")
            info = '以下為' + city_for_hotel + '最低價格為' + str(price) + '元以下的所有飯店:' + "\n\n" 
            for i in range(max_index + 1):
                info += app.config['city_hotels'][city_for_hotel][i]['旅宿名稱'] + "\n" 
            info += '\n請問需要哪間飯店的詳細資訊?'

    return info
'''

def get_saved_area_view(area):
    info = "以下是" + area + "推薦的著名景點:\n\n"
    num_choices = 5
    random_views = random.sample(app.config['all_area_view'][area], num_choices)

    for view in random_views:  
        info += view['view'] + '\n'
    info += "\n" + "想了解哪個景點?"
    return info

def get_saved_Rcity_hotel(city):
    info = ''
    info += '以下為您推薦三間訂房網站上評價非常好的飯店!' + '\n\n'

    num_choices = 3
    #num_choices = min(num_choices, len(hotel_info_list))
    random_hotels = random.sample(app.config['R_city_hotels'][city], num_choices)
    #print(hotel_info_list)

    for hotel in random_hotels:
        hotel_name = hotel['飯店名稱']
        hotel_score = hotel['評分']    
        info += hotel_name + '\n'
        info += '評分:' + hotel_score + '\n\n'
    #print(info)
    #print(random_hotels)
    info += '請問您對哪家有興趣呢，以便為您提供更詳細的資訊'
    return info
'''
def search_hotel(list, price):
    low = 0
    upper = len(list) - 1
    max_index = -1

    while low <= upper:
        mid = int((low + upper) / 2)
        current_num = int(list[mid]['定價i'])

        if current_num <= price:
            max_index = mid
            low = mid + 1
        else:
            upper = mid - 1

    return max_index

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

    return info
'''
if __name__ == "__main__":
    app.run()
