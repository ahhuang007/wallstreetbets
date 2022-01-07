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

def get_date_nums(time_nums):
    #Function to update the datetime values to next range
    #Returns 4 ints (format = [month, day, hour_start, hour_end])
    
    
    #Revamp to use datetime library, this is ridiculous
    month = time_nums[0]
    day = time_nums[1]
    hour_start = time_nums[2]
    hour_end = time_nums[3]
    #Sorting out the new hours
    if hour_start > 19:
        new_hs = 24 - hour_start
    else:
        new_hs = hour_start + 5
    if hour_end > 19:
        new_he = 24 - hour_end
    else:
        new_he = hour_end + 5
    #Making sure days are updated
    if month == 2:
        if day == 28:
            day = 1
        else:
            day += 1
    return updated_nums

def stringify_nums(time_nums):
    #Function to convert datetime numbers into proper strings for URL
    #Returns 4 strings in a list
    str_li = []
    for el in time_nums:
        if el < 10:
            str_li.append("0" + str(el))
        else:
            str_li.append(str(el))
    return str_li

def get_url(str_li, c):
    #Puts datetime values into URL, returns URL string
    p1 = "https://api.pro.coinbase.com/products/" + c + "-USD/candles?"
    p2 = "start=2021-" + str_li[0] + "-" + str_li[1] + "T" + str_li[2] + ":00:00&"
    p3 = "end=2021-" + str_li[0] + "-" + str_li[1] + "T" + str_li[3] + ":59:00&granularity=60"
    url = p1 + p2 + p3
    return url

headers = {"Accept": "application/json"}

#Creating DataFrames to save later with our data
dfs = [pd.DataFrame(columns = ['timestamp', 'low', 'high', 'open', 'close', 'volume'])] * 10
#List cryptocurrencies by trade volume:
    #BTC, ETH, BCH, LINK, SOL, ATOM, MANA, MATIC, DOT, ADA


cryptos = ['ALGO']#['BTC', 'ETH', 'BCH', 'LINK', 'SOL', 'ATOM', 'MANA', 'MATIC', 'DOT', 'ADA']
for i in range(len(cryptos)):
    c = cryptos[i]
    #Starting date/time
    month = 1
    day = 1
    hour_start = 0
    hour_end = 4
    time_nums = [month, day, hour_start, hour_end]
    #Converting datetime stuff to strings for url
    string_list = stringify_nums(time_nums)
    #Making URL and request
    url = get_url(string_list, c)
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    #Add to DataFrame
    df = pd.DataFrame(data = data, columns = dfs[i].columns)
    li = [dfs[i], df]
    dfs[i] = pd.concat(li, ignore_index = True)
    #while month != 12 and day != 31 and hour != 19:
    while day != 5 and hour_start != 19: #Test loop
        #update at beginning
        time_nums = get_date_nums(time_nums)
        #Then proceed with rest of loop
        string_list = stringify_nums(time_nums)
        url = get_url(string_list, c)
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        df = pd.DataFrame(data = data, columns = dfs[i].columns)
        li = [dfs[i], df]
        dfs[i] = pd.concat(li, ignore_index = True)
    
    dfs[i].to_csv("./data/" + c + "_data.csv")

    
    
    
    
    
    
    
    