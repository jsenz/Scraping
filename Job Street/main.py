from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time

def extract(page):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    url = f'https://www.jobstreet.co.id/id/job-search/python-developer-jobs-in-jakarta-raya/'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_ = 'sx2jih0 zcydq89e zcydq88e zcydq872 zcydq87e')
    for item in divs:
        title = item.find_all('span', class_ = 'sx2jih0')[0].text.strip()
        company = item.find_all('span', class_='sx2jih0')[1].text.strip()
        location = item.find_all('span', class_ = 'sx2jih0')[2].text.strip()
        try: 
            salary = item.find_all('span', class_ = 'sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc3 _18qlyvc7')[1].text.strip()
        except:
            salary = 'No Sallary Information'

        job = {
            'title' : title,
            'company' : company,
            'location' : location,
            'salary' : salary
        }
        joblist.append(job)

joblist = []
job_dict = {
    "data" : joblist,
    "datetime_fetch":f"{datetime.now()}"
}

print(f'Getting jobs!')
c = extract(0)
transform(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_excel('jobs.xlsx')

with open(f'joblist_{datetime.now().date()}.json', 'w+', encoding="utf-8") as outfile:
    outfile.write(json.dumps(job_dict))
    outfile.close()

schedule.every().hour.do(transform)