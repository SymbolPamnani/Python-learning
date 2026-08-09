import requests

def heading():
    print("-------------------------------------")
    print("------WEATHER CHECK APPLICATION------")
    print("-------------------------------------")

def welcome():
    name= input("Enter your name: ").strip()
    print("Hey, Welcome ", name)
    print("Lets check weather toady!")

def get_city():
    while True:
        city = input("Enter city name: ").strip()
        if city == "":
            print("City name Required!")
        else:
            return city
heading()
welcome()
city = get_city()

api_key = "af5ff5fb6f8240b4b99110415260707"

url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
else:
    print("Unable to fetch weather.")
    
print("-------------------------------------")
print("\nCurrent Weather updates in ", city)
print("-------------------------------------")
wind = data["current"]["wind_kph"]
temp=data["current"]["temp_c"]
humid=data["current"]["humidity"]
upd = data["current"]["last_updated"]
cond=data["current"]["condition"]["text"]
coun=data["location"]["country"]
print("Temperature: ", temp)
print("Humididty: ",humid)
print("Wind speed: ", wind)
print("Last Updated: ",upd)
print("Condition: ",cond)
print("Country: ",coun)