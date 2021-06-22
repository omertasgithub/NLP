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
#this could be trouble because covid caused unusual market move recent years

result = paper.news(company_tickers="AAPL",date_from='2021-05-22', date_to='2021-06-20', pagesize=200)
#pprint.pprint(result)
print(len(result))
"""
lenght of the data is not more than 100 regardles of date interval
one solution could be pulling data within 1 week interval then combine 
instead of pulling data between date_from='2021-05-22', date_to='2021-06-20'
it can be done between '2021-05-22', '2021-05-27','2021-06-5','2021-06-15','2021-06-20'
The combine them may be there could be 500 line of news instead of 100
"""
#print(result[4])

#Don snetiment analysis with title only
dic = {}
for i in range(len(result)):
    dic[result[i]['updated']] = result[i]['title']
    
    
"""
yahoo stock issues
1 Failed download:
- AAPL: 1m data not available for startTime=1592110800 and endTime=1592715600. The requested range must be within the last 30 days.
Empty DataFrame
Columns: [Open, High, Low, Close, Adj Close, Volume]
Index: []


#data = yf.download('AAPL', start="2021-05-22", end="2021-06-20", interval='2m')
#onyl last 25 days data   
"""  
stock_data = pd.read_csv("data.csv")   

#time and new headline stored into dic. Lets create a dataframe  
stock_news_headline = pd.DataFrame(dic.items(), columns = ["Time", "News_headline"])


#vader sentiment anlaysis 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader = SentimentIntensityAnalyzer()
scores = stock_news_headline['News_headline'].apply(vader.polarity_scores).tolist()
compound_scores = [scores[i]["compound"] for i in range(len(scores))]

#add compound score inot stoakc_news_headline data frame
stock_news_headline["compound score"] = compound_scores 
print(stock_data)
print(stock_news_headline)

#how can we compare dates between to different dataframe


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

#beatiful soup gets body of the page but there
#are constant paragrpahs like mission statement vs on every page
#this extra words could be a trouble because they appear on every page and has nothing to do with the news

#body start from key word #Share but there is no specieific key word to end it
#not like wikie pedia.  it is unorgnaized
#Also, some url is about benzinga adds only
#using regex inconvinient 

#print(soup)
#print(soup.prettify())

x = soup.split("Share:")[1].split("\n\n\n\n\n")[1]



print(x)
"""




