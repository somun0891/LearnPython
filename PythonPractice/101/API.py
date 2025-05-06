import requests
import pprint
from datetime import datetime,timezone
import pytz
import smtplib
import time

parameters = {
    "lat":20.296059
    ,"lng":85.824539
    ,"formatted":0
    ,"date":"2024-04-27"
}
response = requests.get("https://api.sunrise-sunset.org/json" ,params = parameters)

# response.raise_for_status()

#pprint.pprint(response.json())

data = response.json()
sunrise_utc_time = datetime.strptime(str(data["results"]["sunrise"])[0:19], "%Y-%m-%dT%H:%M:%S")
print(sunrise_utc_time)

sunrise = str(data["results"]["sunrise"].split("T")[1]

#convert to datetime first, only slice upto seconds
sunset_utc_time = datetime.strptime(str(data["results"]["sunset"])[0:19], "%Y-%m-%dT%H:%M:%S")


#convert UTC to local datetime
#Set timexone
IST = pytz.timezone('Asia/Calcutta')
sunrise_local_time = sunrise_utc_time.replace(tzinfo=pytz.utc).astimezone(IST)
sunset_local_time = sunset_utc_time.replace(tzinfo=pytz.utc).astimezone(IST)

pprint.pprint(str(sunrise_local_time)[:-6]) #local sunrise time 
pprint.pprint(str(sunset_local_time)[:-6]) #local sunset time 
# sunset_local_time.strftime("%Y-%m-%dT%H:%M:%S")


#convert to AM/PM format string and extract the hour part only
sunrise = datetime.strftime(sunrise_local_time , "%Y-%m-%dT%I:%M:%S %p" ).split("T")[1].split(":")[0]
print(sunrise)

sunset = datetime.strftime(sunset_local_time , "%Y-%m-%dT%I:%M:%S %p" ).split("T")[1].split(":")[0]
print(sunset)


pprint.pprint("The sunrises at " + sunrise + 
              " AM " + "and sets at " +sunset + " PM "+ "today in India." )

#track ISS overhead my location





current_hour = datetime.now().hour

def is_current_night():
    if current_hour < int(sunrise) or current_hour > int(sunset):
        return True


my_lat = 56.130367
my_long = -106.346771

def is_iss_overhead():
    iss_resp = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_resp.raise_for_status()
    iss_data = iss_resp.json()

    #pprint.pprint(iss_data)
    iss_latitude = iss_data['iss_posiiton']['latitude']
    iss_longitude= iss_data['iss_posiiton']['longitude']
       
    if  my_lat - 5 <= iss_latitude <= my_lat + 5 and my_long - 5 <= iss_longitude <= my_long + 5:
        return True

    MY_EMAIL = "connectsachi2016@gmail.com"
    MY_PASSWORD = "12343221112"
    
    #send email
    while(True):
        time.sleep(60)
        if is_current_night() and is_iss_overhead():
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr = "connectsachi2016@gmail.com",
                to_addrs = "connectsachi2016@gmail.com",
                msg = "Subject : Look up in the sky. \n\n ISS is overhead!"
            )


dir(smtplib)




"""

import time

local_time = time.localtime()

print("Time Zone: ", time.tzname)
print("Time Zone: ", time.strftime("%Z", local_time))
print("Date and Time Zone: ", time.strftime("%Y-%m-%d %H:%M:%S %Z", local_time) )
print("UTC Offset: ", time.strftime("%z", local_time))

from datetime import datetime, timezone

local_datetime = datetime.now()
utc_datetime = datetime.now(timezone.utc)

local_iso_str = datetime.strftime(local_datetime, "%Y-%m-%dT%H:%M:%S.%f")[:-3]
utc_iso_str = datetime.strftime(utc_datetime, "%Y-%m-%dT%H:%M:%S.%f")[:-3]

print(f"local dt: {local_iso_str}, tzname: {local_datetime.tzname()}")
print(f"  utc dt: {utc_iso_str}, tzname: {utc_datetime.tzname()}")

utc_2_local_iso_str = datetime.strftime(utc_datetime.astimezone(), "%Y-%m-%dT%H:%M:%S.%f")[:-3]

print(f"  local dt: {utc_2_local_iso_str}, tzname: {local_datetime.tzname()}")


import datetime

utc_time = datetime.datetime.utcnow()
local_time = utc_time.astimezone("Asia/Kolkata")

print(utc_time)
print(local_time)



import pytz
from datetime import datetime

# UTC time
utc_time = datetime.utcnow()

# Local timezone
local_timezone = pytz.timezone('Asia/Calcutta')  # Example: Eastern Time Zone

# Convert UTC time to local timezone
local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)

print("UTC time:", utc_time)
print("Local time:", local_time)

import datetime

# Get the current UTC datetime
utc_datetime = datetime.datetime.utcnow()

utc_datetime
# Specify the desired time zone
local_timezone = datetime.timezone(datetime.timedelta(hours=5.5))


# Convert UTC datetime to local datetime
local_datetime = utc_datetime.astimezone(local_timezone)

# Print the local datetime
print(local_datetime)


from datetime import datetime
import pytz

utc_str = str(datetime.utcnow()) # UTC datetime string
local_tz = pytz.timezone('Asia/Calcutta')
print(utc_str[:-7])
utc_dt = datetime.strptime(utc_str[:-7], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
local_dt = utc_dt.astimezone(local_tz)

print(local_dt)  # Output: 2023-03-07 14:30:00-05:00 (example)

def cls():
    import os 
    os.system('CLS')

"""  

