"""
not all of them in content-body only but 90% in that fomar
do try and expect and store only the one has 
<div class="article-content-body-only">…</div>

"""


import pandas as pd
import numpy as np

from benzinga import news_data
import pprint
api_key = "73711d8727b84da28609c76185c57afb"

##
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


stock_data1 = pd.read_csv("data1.csv")   #'AAPL', start="2021-06-01", end="2021-06-08", interval='1m'
stock_data2 = pd.read_csv("data2.csv")   #'AAPL', start="2021-06-08", end="2021-06-13", interval='1m'
stock_data3 = pd.read_csv("data3.csv")   #'AAPL', start="2021-06-13", end="2021-06-20", interval='1m'
stock_data4 = pd.read_csv("data4.csv")   #'AAPL', start="2021-06-20", end="2021-06-27", interval='1m'
stock_data5 = pd.read_csv("data5.csv")   #'AAPL', start="2021-06-27", end="2021-07-04", interval='1m'
frames_yahoo = [stock_data1, stock_data2, stock_data3, stock_data4, stock_data5]
stock_data = pd.concat(frames_yahoo, ignore_index=True)
#stock_data=stock_data1
result1 = paper.news(company_tickers="AAPL",date_from="2021-06-01", date_to="2021-06-08", pagesize=200)
result2 = paper.news(company_tickers="AAPL",date_from="2021-06-08", date_to="2021-06-13", pagesize=200)
result3 = paper.news(company_tickers="AAPL",date_from="2021-06-13", date_to="2021-06-20", pagesize=200)
result4 = paper.news(company_tickers="AAPL",date_from="2021-06-20", date_to="2021-06-27", pagesize=200)
result5 = paper.news(company_tickers="AAPL",date_from="2021-06-27", date_to="2021-07-04", pagesize=200)
result=result1+result2+result3+result4+result5
#pprint.pprint(result)
#print(len(result))
"""
lenght of the data is not more than 100 regardles of date interval
one solution could be pulling data within 1 week interval then combine 
instead of pulling data between date_from='2021-05-22', date_to='2021-06-20'
it can be done between '2021-05-22', '2021-05-27','2021-06-5','2021-06-15','2021-06-20'
The combine them may be there could be 500 line of news instead of 100
"""

dic = {}
for i in range(len(result)):
    dic[result[i]['updated']] = result[i]['url']

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()
import requests
from bs4 import BeautifulSoup


common = ['\nThis headline-only','\nThis unusual optio','\n\nThis headline-onl']
for i,j in dic.items():
    link = j
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        article_content = soup.find("div", {"class": "article-content-body-only"}).text
        if article_content[:19] not in common:
            dic[i]=article_content
        
        else:
           dic[i]=None
            
    except:
        dic[i]=None
    

#time and new headline stored into dic. Lets create a dataframe  
stock_news_headline = pd.DataFrame(dic.items(), columns = ["Time", "News_headline"])

stock_news_headline = stock_news_headline[stock_news_headline['News_headline'].notna()]
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader = SentimentIntensityAnalyzer()
scores = stock_news_headline['News_headline'].apply(vader.polarity_scores).tolist()
compound_scores = [scores[i]["compound"] for i in range(len(scores))]




#add compound score inot stoakc_news_headline data frame
stock_news_headline["compound score"] = compound_scores 
#print(stock_data)
#print(stock_news_headline)

#how can we compare dates between to different dataframe?
#the date from benzinga is formated as Tue, 01 Jun 2021 07:05:36 -0400
#the date from yahoo is formated as 2021-06-01 09:30:00-04:00
#first slice yahoo date from this format Tue, 01 Jun 2021 07:05:36 -0400 to 
#2021-06-01 09:30 get rid of -00-0400 and do similar for yahoo date
#we dont need seconds so remove that as well

yahoo_datetime = [i[:-9] for i in stock_data["Datetime"]]
#now Datetime is in 2021-06-03 12:35 format
#now replace this with existing Datetime column
stock_data["Datetime"] = yahoo_datetime

#now do similar for stock_news_headline data 
stock_news_time = [i[5:-9] for i in stock_news_headline["Time"]]
#i am not sure this could be done in better way, check for better way 
#may be regex?
stock_news_headline["Time"] = stock_news_time

#now we have 01 Jun 2021 07:05 for stock news
#and we have 2021-06-01 09:30 for yahoo stock
#lets convert stok date time format into yahoo's
list_news_time = [i.replace('Jun','06') for i in stock_news_headline["Time"]]
stock_news_headline["Time"] = list_news_time

#modif times so they are in the same format
stock_news_time = [i.split(" ") for i in stock_news_headline["Time"]]

def swap(lst):
    lst[2],lst[0] = lst[0],lst[2]
    return "-".join(lst[:-1]) + " " + lst[-1]

stock_news_time = [swap(i) for i in stock_news_time]

stock_news_headline["Time"] = stock_news_time


#now both are in the same ormat
#2021-06-01 09:30 yahooo
#2021-06-01-07:05 news

stock_data.rename(columns={'Datetime':"Time"}, inplace=True)

print(stock_data)
print(stock_news_headline)

merge_by = pd.merge(stock_news_headline, stock_data.reset_index(), how='inner')
#we know the intersection of the news came in
#2021-06-01 10:06 so we find the diference of one minute ahead and later
minute_in = [i for i in merge_by["index"]]
minute_later = [i+1 for i in merge_by["index"]]
price_change = [stock_data["Close"][j]-stock_data["Close"][i] 
                for i, j in zip(minute_in,minute_later)]
#we have news headline score and effects


dataFrame = pd.DataFrame()
dataFrame["price change"] = price_change
dataFrame["compound scores"] = merge_by["compound score"]


match = sum(sum([np.sign(dataFrame["price change"])==np.sign(dataFrame["compound scores"])]))

print(match/dataFrame.shape[0])
