# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 01:50:37 2022

@author: ahhua
"""

import requests
import pandas as pd
import datetime

'''
Script to gather data from Binance's API. Seeing if using a different API
will get me more complete data.
'''


def get_url(l1, c):
    #Puts datetime value into URL, returns URL string
    p1 = "https://api.binance.com/api/v3/klines?symbol=" + c + "USDT"
    p2 = "&interval=1m&startTime=" + l1
    p3 = "000&limit=999"
    url = p1 + p2 + p3
    return url

headers = {"Accept": "application/json"}


#List of cryptocurrencies:
#BTC, ETH, BCH, LINK, SOL, ATOM, MANA, MATIC, DOT, ADA
#AVAX, ALGO, AAVE, UNI, LTC, LRC


cryptos = ['AVAX', 'UNI', 'AAVE', 'ALGO',
           'LTC', 'LRC', 'BTC', 'ETH',
           'BCH', 'LINK', 'SOL', 'ATOM',
           'MANA', 'MATIC', 'DOT', 'ADA']
#cryptos = ['BTC']
for i in range(len(cryptos)):
    c = cryptos[i]
    print(c)
    #Creating DataFrame to save later with our data
    df = pd.DataFrame(columns = ['timestamp', 'open', 'high', 'low', 
                                 'close', 'volume', 'a', 'b',
                                 'c', 'd', 'e', 'f'])
    
    #Date/time range
    date_1 = datetime.datetime(2021, 1, 1)
    
    #Converting datetime stuff to strings for url
    strl_1 = str(int(date_1.timestamp()))
    #Making URL and request
    url = get_url(strl_1, c)
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    #Add to DataFrame
    subdf = pd.DataFrame(data = data, columns = df.columns)
    
    li = [df, subdf]
    df = pd.concat(li, ignore_index = True)
    
    date_1 = date_1 + datetime.timedelta(hours = 16, minutes = 40)
    while date_1.year < 2022:
    #while date_1.day < 6: #Test loop
        
        strl_1 = str(int(date_1.timestamp()))
        url = get_url(strl_1, c)
        
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        subdf = pd.DataFrame(data = data, columns = df.columns)
        li = [df, subdf]
        df = pd.concat(li, ignore_index = True)
        
        date_1 = date_1 + datetime.timedelta(hours = 16, minutes = 40)
        
    #Sort rows, save df
    df = df.drop(columns = ['a', 'b', 'c', 'd', 'e', 'f'], axis = 1)
    df['timestamp'] = df['timestamp'] / 1000
    df = df.sort_values('timestamp').reset_index(drop = True)
    df.to_csv("./data/" + c + "_data.csv")
    