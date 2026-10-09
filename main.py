import requests
def weather_code_to_text(code):
    if code == 0:
        return "快晴"
    elif code == 1:
        return "晴れ"
    elif code == 2:
        return "一部曇り"
    elif code == 3:
        return "曇り"
    elif code in [45, 48]:
        return "霧"
    elif code in [51, 53, 55, 56, 57]:
        return "霧雨"
    elif code in [61, 63, 65, 66, 67]:
        return "雨"
    elif code in [71, 73, 75, 77]:
        return "雪"
    elif code in [80, 81, 82]:
        return "にわか雨"
    elif code in [85, 86]:
        return "にわか雪"
    elif code in [95, 96, 99]:
        return "雷雨"
    else:
        return "不明"

def get_city():
    while True:
        city = input("都市名を入力してください:")

        url = "https://geocoding-api.open-meteo.com/v1/search"

        params = {
            "name": city,
            "count": 1,
            "language": "ja"
        }

        response = requests.get(url, params=params)

        data = response.json()

        if "results" not in data:
            print("都市が見つかりませんでした。英語表記で入力してください。")
            continue

        return data["results"][0]

def get_weather(latitude, longitude):
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "hourly": "weather_code",
        "timezone": "auto"
    }

    weather_response = requests.get(weather_url, params=weather_params)
    return weather_response.json()

def get_today_forecast(weather_data):
    hourly_codes = weather_data["hourly"]["weather_code"]

    morning_code = hourly_codes[9]
    afternoon_code = hourly_codes[15]

    morning_weather = weather_code_to_text(morning_code)
    afternoon_weather = weather_code_to_text(afternoon_code)

    if morning_weather == afternoon_weather:
        return morning_weather
    else:
        return f"{morning_weather}のち{afternoon_weather}"

def display_weather(cityname, weather_data, today_forecast):
    temperature = weather_data["current"]["temperature_2m"]
    relative_humidity = weather_data["current"]["relative_humidity_2m"]

    weather_code = weather_data["current"]["weather_code"]
    weather = weather_code_to_text(weather_code)

    wind_speed = weather_data["current"]["wind_speed_10m"]


    print(f"{cityname}の現在の天気")
    print(f"気温:{temperature}℃")
    print(f"湿度:{relative_humidity}%")
    print(f"天気:{weather}")
    print(f"風速:{wind_speed}km/h")
    print(f"今日の予報:{today_forecast}")

print("Weather App")
result = get_city()

latitude = result["latitude"]
longitude = result["longitude"]
cityname = result["name"]

weather_data = get_weather(latitude, longitude)

today_forecast = get_today_forecast(weather_data)

display_weather(cityname, weather_data, today_forecast)


