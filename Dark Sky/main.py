import sys
import json
import requests
import csv
from datetime import datetime, time

LOCATION = "-6.135200,106.813301"

RAPIDAPI_KEY  = <Rapid_Api_key>

def trigger_api():

  url = "https://dark-sky.p.rapidapi.com/" + LOCATION

  querystring = {"lang":"en","units":"auto"}

  headers = {
    'X-RapidAPI-Key': <Rapid_Api_key>,
    'X-RapidAPI-Host': "dark-sky.p.rapidapi.com"
    }

  response = requests.request("GET", url, headers=headers, params=querystring)

  if(200 == response.status_code):
    return json.loads(response.text)
  else:
    return None

if __name__ == "__main__":

  try: 

    print("Getting Weather Data For Next Seven Days")

    api_response = trigger_api()

    current_date = datetime.fromtimestamp(api_response["currently"]["time"])

    with open('Weather_Data-' + current_date.strftime("%m-%d-%Y") +  '.csv', 'w',newline='') as csv_file:

      csv_writer = csv.writer(csv_file)

      csv_writer.writerow(["Parameter","Time", "Value"])  

      for record in api_response["daily"]["data"]:

        try: 

          time     = record["time"]
          tempH     = record["temperatureHigh"]
          tempL     = record["temperatureLow"]
          humidity = int(record["humidity"] * 100)
          cloud    = int(record["cloudCover"] * 100)
          

          time_of_day = datetime.fromtimestamp(time).strftime("%Y%m%d")

          print("Adding Record for " + time_of_day)
          csv_writer.writerow(["Temp High",time_of_day,tempH])
          csv_writer.writerow(["Temp Low",time_of_day,tempL])
          csv_writer.writerow(["Humidity",time_of_day,humidity])
          csv_writer.writerow(["Cloud Cover",time_of_day,cloud])  
          
        except TypeError as e:

          print(e)
          print("Type Error...Ignoring")
          
        except csv.Error as e:
          
          print(e)
          print("CSV Error...Ignoring")
          

      csv_file.close()

  except Exception as e:

    print("Major Exception ...Aborting")
    sys.exit(e)