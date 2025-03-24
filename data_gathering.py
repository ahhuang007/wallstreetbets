# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 01:50:37 2022

Rewrite of code since Binance is no longer available stateside, and
in general I want to update my code so I'm using Coinbase again and integrating CCXT

Adding technical indicators will be in separate file like before

@author: ahhua
"""

import ccxt
import numpy as np
import pandas as pd
from datetime import datetime


exchange = ccxt.coinbaseadvanced({
    'apiKey': "organizations/58c1ffde-f18d-424a-aa36-da4b43666f3d/apiKeys/54876ef5-034c-4ba9-b99f-c05efc6cc7fb",
    'secret': "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIBf1hhYe0o92VC3YNecW7ixZRghHmHvTybILulK2CmsRoAoGCCqGSM49\nAwEHoUQDQgAEft77NAAtT8hCgn/VKSIN4jAGWqLwvTqqX49+eYwEfrp6ipwopoTV\nxlsIh7/pmmg2pGPOTDV/hVQCPcTPz7twQA==\n-----END EC PRIVATE KEY-----\n",
})

#List of cryptocurrencies:
#BTC, ETH, BCH, LINK, SOL, ATOM, MANA, MATIC, DOT, ADA
#AVAX, ALGO, AAVE, UNI, LTC, LRC


cryptos = ['ETH', 'XRP', 'ADA']
#columns for dataframe
columns = ['timestamp', 'open', 'high', 'low', 
                             'close', 'volume']

datasets = ["training", "validation"]

for dataset in datasets:
    for c in cryptos:
        print(f"{dataset} set for {c}")
        
        #I will create a training and validation set
        #A month will separate the two to prevent any data leakage whatsoever
        if dataset == "training":
            start_timestamp = 1704085200000 #1/1/2024, 12 AM in UNIX (EST)
            end_timestamp = 1722484800000 #8/1/2024, 12 AM in UNIX (EST)
        else:
            start_timestamp = 1725163200000 #9/1/2024, 12 AM in UNIX (EST)
            end_timestamp = 1730433600000 #11/1/2024, 12 AM in UNIX (EST)
        
        dt = 1800000 #30 minutes in UNIX, the granularity of the data
        data = []
        
        while start_timestamp < end_timestamp:
            ohlcvs = exchange.fetch_ohlcv(f'{c}-USD', timeframe = '30m', since = start_timestamp, limit = 300)
            data = data + ohlcvs
            start_timestamp += dt * 300
        
        #Cleaning the data a bit - first, remove all data after endpoint
        data = [x for x in data if x[0] < end_timestamp]
    
        #Now, remove duplicates
        dupe_inds = []
        for i in range(len(data)):
            ts = data[i][0]
            if i + 1 < len(data):
                if data[i + 1][0] == ts:
                    dupe_inds = [i] + dupe_inds
        #Reversed the order in which I found the dupes so deleting works easier
        for ind in dupe_inds:
            del data[ind]
        
        #Finally, add rows for missing data
        missing_inds = []
        for i in range(len(data)):
            ts = data[i][0]
            if i + 1 < len(data):
                if data[i + 1][0] != ts + 1800000:
                    missing_inds = [i] + missing_inds
        
        for ind in missing_inds: #just interpolating will work I think
            pre_data = data[:ind + 1]
            post_data = data[ind + 1:]
            before_entry = pre_data[-1]
            after_entry = post_data[0]
            new_data = list(np.mean([before_entry, after_entry], axis = 0))
            new_data[0] = int(new_data[0])
            data = pre_data + [new_data] + post_data
        
        #Create dataframe from data
        df = pd.DataFrame(data = data, columns = columns)
        df['timestamp'] = df['timestamp'] / 1000
        
        df.to_csv("./data/" + c + f"_{dataset}_data.csv", index = False)
    