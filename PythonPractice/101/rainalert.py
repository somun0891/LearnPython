import requests
from datetime import datetime,timedelta
from pprint import pprint
from twilio.rest import Client
import time

api_key= os.environ['open_weather_api_key']
twilio_account_sid = os.environ['twilio_account_sid']
twilio_auth_token = os.environ['twilio_auth_token']

# lat = 20.2602964
# lon= 85.8394521

lat = 34.083672
lon= 74.797279

params = {
    "lat" : lat 
    ,"lon" : lon
    ,"appid" :api_key
    ,"cnt" :8
    ,"mode" :"json"
}

#url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

url = "https://api.openweathermap.org/data/2.5/forecast"

resp = requests.get(url,params)

resp.status_code

data = resp.json()


print("\n")      
pprint("Weather data - limited to  1-day forecast...")
print("\n")      
pprint(data)


now = datetime.now()
Twelvehoursfromnow = now + timedelta(hours = 12)

# print(now)
# print(Twelvehoursfromnow)


Precipitation = 0
for wdata in data['list']:
    reported_ts = datetime.strptime(wdata['dt_txt'],"%Y-%m-%d %H:%M:%S")
    if now >= reported_ts <= Twelvehoursfromnow:
        for wcond in wdata['weather']:
            #print(w)
            if int(wcond['id']) < 700:
                Precipitation = 1
            else:
                Precipitation = 0            


print("\n")  

###Connect with twilio and send an SMS
account_sid = twilio_account_sid
auth_token = twilio_auth_token
client = Client(account_sid, auth_token)

if Precipitation == 1:     
               
    body = "Bring an Umbrella, Sabyasachi!. It's raining cats and dogs!" 
else:
    body =  "It's a great weather today! Have a great day outdoors!"   

message = client.messages.create(
  from_='+16812011775',
  body=body,
  to='+917358433329'
)

print(message.status)

print("\n")      












""" 
from datetime import datetime

# Unix time value
unix_time = 19800  # Example value

# Convert Unix time to datetime
datetime_obj = datetime.utcfromtimestamp(unix_time)

print("Unix time:", unix_time)
print("Datetime:", datetime_obj)
"""

import os
os.environ["api_key"]

