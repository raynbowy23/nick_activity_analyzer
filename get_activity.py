import os
from bs4 import BeautifulSoup as bs
import urllib
import urllib.request
import re
import csv
from datetime import datetime
import pytz
import pyowm
from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth, ServiceAccountCredentials

from nick_vis import visualize
import config as cfg

# Settings
# get the standard UTC time 
CST = pytz.timezone('America/Chicago')

# Get weather api
weather_api = os.environ['WEATHER_API'] # For github server
OpenMap = pyowm.OWM(weather_api)
mgr = OpenMap.weather_manager()
Weather = mgr.weather_at_place('Madison')
Data = Weather.weather
temp = Data.temperature('fahrenheit') # temp['temp'] for avg temp
climate = Data.detailed_status

# Set google drive authentication
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# nick's API
api = os.environ['NICK_API']
nick_api = bs(urllib.request.urlopen(api), "lxml")

now = datetime.now(CST)
current_time = now.strftime("%D:%H:%M:%S")

# Settings list
places = ['Nick Level 1 Fitness', 'Nick Level 2 Fitness', 'Nick Level 3 Fitness', 'Nick Power House', 'Nick Track', 'Nick Pool', 'Nick Courts 1 & 2', 'Nick Courts 3-6', 'Nick Courts 7 & 8', 'Shell Weight Machines', 'Shell Track', 'Shell Cardio Equipment']
active_people = []
capacity = []
# get lists from spi
nick_list = nick_api.get_text().replace("{", "").replace("[", "").replace("]", "").replace('"', "").split('}')
whole_list = []

# Make dictionary into list
for i in range(len(nick_list)-2): # len(nick_list) = 31
  nick_dict = {}
  if i > 0:
    nick_list[i] = nick_list[i][1:]
  for j in range(len(nick_list[i].split(','))):
    key = nick_list[i].split(',')[j].split(':')[0]
    value = nick_list[i].split(',')[j].split(':')[1]
    nick_dict[key] = str(value)
  whole_list.append(nick_dict)

# print(whole_list)

# Load csv file from google drive
f = drive.CreateFile({'id': os.environ['CSV_ID']})
content = f.GetContentString()

# Write into csv file
# with open('output.csv', mode='a') as csv_file:
#   nick_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

  # TODO: if csv file is empty, add field names
  # if csv_file == "":
  # fieldnames = ['date', 'Location', 'Total Capacity', 'Active People', 'Max Temperature', 'Min Temperature', 'Climate']
  # nick_writer.writerow(fieldnames)
new_row = ''
for i in range(len(whole_list)):
  location = whole_list[i]['LocationName']
  totalcapacity = whole_list[i]['TotalCapacity']
  active = whole_list[i]['LastCount']
  temp_max = temp['temp_max']
  temp_min = temp['temp_min']
    # if location in places:
    #   print('{} : {}/{}'.format(location, active, totalcapacity))

    # Save to csv
    # nick_writer.writerow([current_time, location, totalcapacity, active, temp_max, temp_min, climate])

    # csv_file.close()
  if i == 0:
    new_row += str(current_time) + ',' + str(location) + ',' + str(totalcapacity) + ',' + str(active) + ',' + str(temp_max) + ',' + str(temp_min) + ',' + str(climate)
  elif i != 0:
    new_row += '\n' + str(current_time) + ',' + str(location) + ',' + str(totalcapacity) + ',' + str(active) + ',' + str(temp_max) + ',' + str(temp_min) + ',' + str(climate)

f.SetContentString(content + new_row)
print(f.GetContentString())

# Update and upload csv file to google drive
# f = drive.CreateFile({'title': 'output.csv'})
# f.SetContentFile('output.csv')
f.Upload()

# visualize our data
# visualize()