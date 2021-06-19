#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 10:00:34 2021

@author: omertas
"""



import pprint
from benzinga import news_data
api_key = "73711d8727b84da28609c76185c57afb"
paper = news_data.News(api_key)
stories = paper.news(company_tickers='AAPL', date_from='2013-06-14', date_to='2018-06-15')
pprint.pprint(stories)

#result = paper.output(stories)
#print(result)
lst_title = []
for i in range(len(stories)):
    lst_title.append(stories[i]['title'])
    
print(lst_title)  
"""
from benzinga import financial_data
api_key = "testkey892834789s9s8abshtuy"
fin = financial_data.Benzinga(api_key)
"""

