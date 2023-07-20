import json
import requests


def get_weather_data(locationName):
    
    county = ["苗栗", "彰化", "南投", "雲林", "屏東", "台東", "花蓮", "宜蘭"]
    city = ["台中", "台北", "新北", "基隆", "桃園", "高雄", "台南", "新竹"]
    
    for c in county:
        if (c == locationName):
            locationName += "縣"
            
    for c in city:
        if (c == locationName):
            locationName += "市"
    
    if locationName.startswith("台"):
        locationName = "臺" + locationName[1:]
    
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": "CWB-E71F51E4-4EA8-4C5B-AE0A-348B3AB05749",
        "locationName": locationName
    }

    response = requests.get(url, params=params)
    # print(response.status_code)

    if response.status_code == 200:
        # print(response.text)
        data = json.loads(response.text)

        # 所查詢的地點名
        location = data["records"]["location"][0]["locationName"]

        weather_elements = data["records"]["location"][0]["weatherElement"]
        
        # 時間區段
        start_time = weather_elements[0]["time"][0]["startTime"]
        end_time = weather_elements[0]["time"][0]["endTime"]
        # 天氣狀況
        weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
        # 下雨概率
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        # 最低最高溫
        min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]
        # 體感
        comfort = weather_elements[3]["time"][0]["parameter"]["parameterName"]
        
        # print(location)
        # print(start_time)
        # print(end_time)
        # print(weather_state)
        # print(rain_prob)
        # print(min_tem)
        # print(comfort)
        # print(max_tem)
        
        info = ""
        info += "查詢天氣地點: " + location + "\n"
        info += "天氣內容時間段為:" + "\n" + start_time + "到" + end_time + "\n"
        info += "天氣狀況: " + weather_state + "\n"
        info += "降雨機率: " + rain_prob + "%" + "\n"
        info += "最高溫和最低溫:" + max_tem + "~" + min_tem + "\n"
        info += "體感較" + comfort
        
        return info
        
    else:
        return ("只能查詢臺灣地區的天氣")
        
# print(get_weather_data("台中"))