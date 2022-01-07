# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 00:50:20 2022

@author: ahhua
"""

'''
Script to gather data from Coinbase Pro's API. API only allows 300 units of
data per request, so I had to make a loop to get all the data I wanted.
'''

import requests
import pandas as pd
import datetime


def stringify_nums(d1, d2):
    #Function to convert datetime numbers into proper strings for URL
    #Returns 6 strings in 2 lists (3 in each list)
    l1 = [d1.month, d1.day, d1.hour]
    l2 = [d2.month, d2.day, d2.hour]
    nl1 = []
    nl2 = []
    zipped = zip(l1, l2)
    for el1, el2 in zipped:
        if el1 < 10:
            nl1.append("0" + str(el1))
        else:
            nl1.append(str(el1))
        if el2 < 10:
            nl2.append("0" + str(el2))
        else:
            nl2.append(str(el2))
    return nl1, nl2

def get_url(l1, l2, c):
    #Puts datetime values into URL, returns URL string
    p1 = "https://api.pro.coinbase.com/products/" + c + "-USD/candles?"
    p2 = "start=2021-" + l1[0] + "-" + l1[1] + "T" + l1[2] + ":00:00&"
    p3 = "end=2021-" + l2[0] + "-" + l2[1] + "T" + l2[2] + ":59:00&granularity=60"
    url = p1 + p2 + p3
    return url

headers = {"Accept": "application/json"}


#List cryptocurrencies by trade volume:
#BTC, ETH, BCH, LINK, SOL, ATOM, MANA, MATIC, DOT, ADA


cryptos = ['BTC', 'ETH', 'BCH', 'LINK', 'SOL', 'ATOM', 'MANA', 'MATIC', 'DOT', 'ADA']
for i in range(len(cryptos)):
    c = cryptos[i]
    #Creating DataFrame to save later with our data
    df = pd.DataFrame(columns = ['timestamp', 'low', 'high', 'open', 'close', 'volume'])
    
    #Date/time range
    date_1 = datetime.datetime(2021, 1, 1)
    date_2 = date_1 + datetime.timedelta(hours = 4, minutes = 59)

    #Converting datetime stuff to strings for url
    strl_1, strl_2 = stringify_nums(date_1, date_2)
    
    #Making URL and request
    url = get_url(strl_1, strl_2, c)
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    
    #Add to DataFrame
    subdf = pd.DataFrame(data = data, columns = df.columns)
    li = [df, subdf]
    df = pd.concat(li, ignore_index = True)
    
    while date_1.month != 12 or date_1.day != 31 or date_1.hour != 19:
    #while date_1.day != 5 or date_1.hour != 19: #Test loop
        #update at beginning
        date_1 = date_2 + datetime.timedelta(minutes = 1)
        date_2 = date_1 + datetime.timedelta(hours = 4, minutes = 59)
        
        #Then proceed with rest of loop
        strl_1, strl_2 = stringify_nums(date_1, date_2)
        url = get_url(strl_1, strl_2, c)
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        subdf = pd.DataFrame(data = data, columns = df.columns)
        li = [df, subdf]
        df = pd.concat(li, ignore_index = True)
        
    #Reverse rows, save df
    df = df.iloc[::-1].reset_index(drop = True)
    df.to_csv("./data/" + c + "_data.csv")

    
    
    
    
    
    
    
    