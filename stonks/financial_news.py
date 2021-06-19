import pandas as pd
import numpy as np

from benzinga import news_data
import pprint
api_key = "73711d8727b84da28609c76185c57afb"


"""
Arguments:
    Optional:
    pagesize (int) - default is 15
    page (int) - default is 0
    display_output (str) - select from (full, abstract, headline)
    base_date (str) - "YYYY-MM-DD" The date to query for calendar data. Shorthand for date_from and date_to if
    they are the same. Defaults for latest.
    date_from (str) - "YYYY-MM-DD"
    date_to (str) - "YYYY-MM-DD"
    last_id (str) - The last ID to start paging from and sorted by and sorted by the last updated date.
    updated_since (str) - he last updated unix timestamp (UTC) to pull and sort by.
    publish_since (str) - The last publish unix  timestamp (UTC) to pull and sort by.
    company_tickers (str)
    channel (str) - multiple channels separated by comma.
Returns:
    Author, created, updated, title, teaser, body, url, image, channels, stocks, tags
"""

paper = news_data.News(api_key)
#it seems no data avilable before Thu 21 May 2020
#this could be trouble because covid caused unusual market move

result = paper.news(company_tickers="AAPL",date_from='2020-06-14', date_to='2020-07-18', pagesize=200)
#pprint.pprint(result)
#print(len(result))
#print(result[4])

#Don snetiment analysis with title only
dic = {}
for i in range(len(result)):
    dic[result[i]['updated']] = result[i]['title']
    
stock_data = pd.read_csv("data.csv")    
#pprint.pprint(dic) 
"""
dic = {}
for i in range(len(result)):
    dic[result[i]['updated']] = result[i]['url']

import requests
link = result[4]['url']
page = requests.get(link)
page

from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser').get_text()



#print(soup)
#print(soup.prettify())

x = soup.split("Share:")[1].split("\n\n\n\n\n")[1]

#body start from key word #Share but there is no specieific key word to end it
#not like wikie pedia it is unorgnaized
#Also, some url is about benzinga adds only
#using regex inconvinient 

print(x)
"""