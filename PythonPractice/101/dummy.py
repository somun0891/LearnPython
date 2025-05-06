
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
import datetime
import time

now = datetime.now()
today = date.today()

TwoDaysAgo = datetime(2024,3,27,19,25,00)
print(TwoDaysAgo)
print(now) #instance of datetime class
print(today) #instance of date class

now.month
now.year
now.second
now.microsecond

print(now - TwoDaysAgo) #1 day, 23:58:20.754478

# timedelta acts like an interval
#Syntax - datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minute=0, hours=0, weeks=0)

delta = timedelta(days=-2, hours = 1 ,seconds=0 )
print(delta) # -2 days, 1:00:00

print(now + delta) #2024-03-27 20:23:20.754478

today.isoformat() #'2024-03-29'  string rep of date
today.isoweekday() # Monday = 1 and Sunday = 7
today.weekday()  # Monday = 0 and Sunday = 6

Todays_time = time.time() #POSIX Timestamp 1711721307.7368417

# to get date from the current time 
date_From_CurrentTime = datetime.date.fromtimestamp(Todays_time)
  
# Printing the current date 
print("Date for the Timestamp is: %s"%date_From_CurrentTime)

date_From_CurrentTime.strftime("%Y-%m-%d %H:%M:%S")

#Calculate duration in seconds and then change back to  hours, minutes,seconds
days = 1
hours = 5
total_duration_in_secs = datetime.timedelta(days = 1,hours=5 , minutes = 30 , seconds = 10).total_seconds() #104400.0

minutes,seconds = divmod(total_duration_in_secs,60)
hours,minutes=divmod(minutes,60)

hours = int(hours)
minutes = int(minutes)
seconds = int(seconds)

print(f'{hours} hours {minutes} minutes {seconds} seconds')


total_duration_in_secs = relativedelta(years = 1 ,days = 1,hours=5 , minutes = 30 , seconds = 10)

dob=datetime.date(1991,8,7) #date
dob_ts=datetime.datetime(1991,8,7,10,15,00)

relativedelta(now,dob_ts) # difference between 2 dates
dob_ts + relativedelta(now,dob_ts)


from datetime import datetime,timezone
from dateutil import tz

# Define the UTC timezone
utc_zone = tz.tzutc()
# print(utc_zone)

# Define the desired local timezone
local_zone = tz.gettz('Asia/Kolkata')
# print(local_zone)

# Define the UTC time
utc_time = datetime.utcnow()
# print(utc_time)

# Convert UTC time to local time
local_time = utc_time.replace(tzinfo=utc_zone).astimezone(local_zone)

# Print the local time
print("Local time:", local_time)


students_scores = {"Jack":90 , "Jill":87 , "Sachi": 79,"Morris":95 , "Martha":39}
student_grades = {}

for student in students_scores:
    student_grades[student] = students_scores[student] #assign the grade in a new dict loop thu students
    if student_grades[student] > 90:
        student_grades[student] = "Outstanding"
    elif student_grades[student] > 80:
        student_grades[student] = "Excellent"    
    elif student_grades[student] > 70:
        student_grades[student] = "Good"    
    elif student_grades[student] > 60:
        student_grades[student] = "Average"         
    elif student_grades[student] > 40:
        student_grades[student] = "Below Average" 
    else:
        student_grades[student] = "Fail"  
              
print(student_grades)

fl = "yes"
bidders = {}
while fl == "yes":
    name = str(input("Please enter your name:\n"))
    print(name)
    bid = float(input("Please enter your bid:\n"))
    print(bid)   
    fl = str(input("Are there any other bidders(yes/no)?\n"))
    print(fl)
    bidders[name] = bid 

highestbidder = max({(int(v), str(k)) for k,v in bidders.items()})[1]
print('')

#Dict practice
#=============

#Add a list of values to a dict
celebs = {"Actor" : ["Shahrukh","Salman" ,"Aamir"] , "Cricketer":["Virat","Rohit","Hardhik"]  }
singer = ["Lata","Shreya","Atif","Sunidhi"]
celebs["singer"] = singer
if "singer" in celebs:
    celebs["singer"].append("Sonu") #adding another name to list of values for key = singer
print(celebs)


#Create a dictionary from a list of tuples
best_celeb = [("Actor","Shahrukh") , ("Singer","Sonu")  , ("Cricketer","Virat")]   
best_celeb = dict(best_celeb) #data has to be in a dict form to be converted to dict
print(best_celeb)

celebs = ["Shahrukh" , "Virat" , "Sonu"]
roles = ["Actor","Cricketer","Singer"]
best_celeb = {}
best_celeb.fromkeys(roles , "Unknown") #{'Actor': 'Unknown', 'Cricketer': 'Unknown', 'Singer': 'Unknown'}
for r,c in zip(roles,celebs):
    best_celeb[r] = c

print(best_celeb)

#Find length of nested dict
celeb = {
    "name": "Akshya",
    "Age": 50,
    "MoreInfo" : {
        "Job" : "Actor",
        "Movies" : ["Khakee","Welcome","Blue"],
        "Child" : {"Name":"Aarav", "Age" : 15 , "Hair":"Black" , "Gender":"Male" }
    }
}
templen = 0
totallen = len(celeb)
for c in celeb.values():
    print(c)
    if isinstance(c , dict):
        totallen += len(c)

totallen

#Find combined length of all string values in a dictionary
best_celeb = [("Actor","Shahrukh") , ("Singer","Sonu")  , ("Cricketer","Virat")]   
best_celeb = dict(best_celeb)
sum([len(v) for v in best_celeb.values()]) #17

#remove the last item
best_celeb.popitem() 
print(best_celeb)

if "Actor" in best_celeb:
    del best_celeb["Actor"]

print(best_celeb)

for kv in best_celeb.items():
    print(kv[0])

#Access dict inside list comphrehension
#Convert dict to tuple
print([(k,best_celeb[k]) for k in best_celeb]) #loop thru keys
print([(k,best_celeb[k]) for k in best_celeb.keys])

#Converts tuple to dict
print([{k:v} for k,v in best_celeb.items()])

#Merge 2 dict
male_celebs = {"Actor" : ["Shahrukh","Salman" ,"Aamir"] , "Cricketer":["Virat","Rohit","Hardhik"]  }
female_celebs = {"Actor" : ["Preeti","Kareena" ,"Zoha"] , "Tennis Stars":["Maria","Serena","Sania"]  }

#Union 2 tuples
all_celebs = dict(male_celebs.items() | female_celebs.items())

#Use update method
male_celebs.update(female_celebs)
print(male_celebs)

