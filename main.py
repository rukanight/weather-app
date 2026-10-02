import requests

print("Weather App")

while True:
    city =input("都市名を入力してください:")

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "ja"
    }

    response = requests.get(url, params=params)

    # print(response.status_code)
    data = response.json()

    if "results" not in data:
        print("都市が見つかりませんでした。英語表記で入力してください。")
        continue

    result = data["results"][0]
    break

# print(result["name"])
# print(result["latitude"])
# print(result["longitude"])

latitude = result["latitude"]
longitude = result["longitude"]
cityname = result["name"]

# print(latitude)
# print(longitude)


weather_url = "https://api.open-meteo.com/v1/forecast"

weather_params = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
}

weather_response = requests.get(weather_url, params=weather_params)

# print(weather_response.status_code)
# print(weather_response.json())

weather_data = weather_response.json()
temperature = weather_data["current"]["temperature_2m"]
relative_humidity = weather_data["current"]["relative_humidity_2m"]
weather_code = weather_data["current"]["weather_code"]
if weather_code == 0:
    weather = "快晴"
elif weather_code == 1:
    weather = "晴れ"
elif weather_code == 2:
    weather = "一部曇り"
elif weather_code == 3:
    weather = "曇り"
elif weather_code in [45, 48]:
    weather = "霧"
elif weather_code in [51, 53, 55, 56, 57]:
    weather = "霧雨"
elif weather_code in [61, 63, 65, 66, 67]:
    weather = "雨"
elif weather_code in [71, 73, 75, 77]:
    weather = "雪"
elif weather_code in [80, 81, 82]:
    weather = "にわか雨"
elif weather_code in [85, 86]:
    weather = "にわか雪"
elif weather_code in [95, 96, 99]:
    weather = "雷雨"
else:
    weather = "不明"
wind_speed = weather_data["current"]["wind_speed_10m"]

print(f"{cityname}の現在の天気")
print(f"気温:{temperature}度")
print(f"湿度:{relative_humidity}%")
print(f"天気:{weather}")
print(f"風速:{wind_speed}km/s")

