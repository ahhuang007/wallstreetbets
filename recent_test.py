# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 03:24:40 2022

@author: ahhua
"""

'''
My SGDRegressor model is performing really well, to the point it's making
me paranoid - going to try testing it on data from 2022
'''

import requests
import pandas as pd
import datetime

#%%

def get_url(l1, c):
    #Puts datetime value into URL, returns URL string
    p1 = "https://api.binance.com/api/v3/klines?symbol=" + c + "USDT"
    p2 = "&interval=1m&startTime=" + l1
    p3 = "000&limit=999"
    url = p1 + p2 + p3
    return url

headers = {"Accept": "application/json"}



c = 'BTC'
#Creating DataFrame to save later with our data
df = pd.DataFrame(columns = ['timestamp', 'open', 'high', 'low', 
                             'close', 'volume', 'a', 'b',
                             'c', 'd', 'e', 'f'])

#Date/time range
date_1 = datetime.datetime(2022, 1, 1)

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
while date_1.month < 4:
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
df.to_csv("./data/2022_" + c + "_data.csv")

#%%
'''
Actual model testing portion here
'''
import pickle
import pandas as pd

df = pd.read_csv("./data/2022_BTC_data.csv")

with open('./ml_stuff/models/sgdreg_v2.pkl', 'rb') as f:
    model = pickle.load(f)

##Will continue eventually