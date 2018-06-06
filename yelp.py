import requests
from bs4 import BeautifulSoup
import lxml, lxml.html
import pandas as pd
from time import sleep
from random import randint
from time import time
from IPython.core.display import clear_output
from warnings import warn
import credentials # credentials stored in credentials.py
import google_maps



url = 'https://www.yelp.com/login'
checkins = 'https://www.yelp.com/user_details_checkins?userid' + credentials.userid + 'start='
s = requests.Session()
login = s.get(url)
login_html = lxml.html.fromstring(login.content) # grab the html of the login page

hidden = login_html.xpath(r'//*[@id="ajax-login"]/input[1]') #navigate to the login input
form = {x.attrib["name"]: x.attrib["value"] for x in hidden} # create a form to pass your email and password
form['email'] = credentials.email
form['password'] = credentials.password

post = s.post(url, data=form) # send your email and password to the form

# Lists to hold scraped values
titles = []
cities = []
frequency = []


# list of URLs to scrape...each new checkin page is 12 higher than the last for start=*
pages = []
list = range(0, 12) # total of 396 checkins...change value to meet personal number of checkins

for x in list[0::12]:
    pages.append(checkins+"{}".format(x))
    
# monitor the loop  
start_time = time()
requests = 0

# for each page of checkins   
for page in pages:
    
    # get page
    response = s.get(page)
    
    # pause the loop for somehwere between 8-15 seconds
    sleep(randint(8,15))
    
    # monitor the requests
    requests += 1
    elasped_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elasped_time))
    clear_output(wait = True)
    
    # warning if you don't get successful page response
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))
    
    # parse the html and added the text to the corresponding lists
    page_html = BeautifulSoup(response.text, 'html.parser')
    names = page_html.find_all('a', {"class": "biz-name js-analytics-click"})
    city = page_html.find_all('span', {"class": "addr-city"})
    frequencies = page_html.find_all('li', {"class": "review-tags_item"})
    
    
    for x in names:
        titles.append(x.text)
        
    for y in city:
        cities.append(y.text)
        
    for z in frequencies:
        z = z.get_text().strip() # strip the extra newlines surrounding the text
        frequency.append(z)

# put the lists into a panda dataframe, then export it to csv        
df = pd.DataFrame({"Name": titles, "City": cities, "Frequency": frequency}, columns = ["Name","City","Frequency"])
for x in df:
    df.to_csv('yelp-checkins.csv', index=False)
    
"""for x in y:
    for name in titles:
        google_maps.google_maps(name)
    print(name)
"""

google_maps.google_maps(titles)




    
    
    
    

 
