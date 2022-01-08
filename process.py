# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 02:06:38 2022

@author: ahhua
"""

'''
Not all of my chosen coins date back to 1/1/2021 on Coinbase, and trades don't
always occur at every timestep, leading some timesteps to be skipped in the data.
I need to fill in the beginnings of some coins with null values, and fill in
the holes in some cryptos with the same value as the last previous cell where
trading occurred.
'''

import pandas as pd
import numpy as np

#Our cryptocurrencies
cryptos = ['AVAX', 'UNI', 'AAVE', 'ALGO', 
           'LTC', 'LRC', 'BTC', 'ETH', 
           'BCH', 'LINK', 'SOL', 'ATOM', 
           'MANA', 'MATIC', 'DOT', 'ADA']
cryptos = ['ADA']
#Starting and ending time range
starting_time = 1609459200
ending_time = 1640995140

for c in cryptos:
    df = pd.read_csv('./data/' + c + '_data.csv')
    print(len(df))
    first_time = df['timestamp'][0] #First recorded time in df
    
    #If first_time is after starting_time, then fill in values before first_time
    #with null values
    if first_time > starting_time:
        num_rows = int((first_time - starting_time) / 60) #number of null_rows
        #Creating null dataframe to add
        timestamps = list(np.linspace(starting_time, first_time, num_rows))
        timestamps = [int(x) for x in timestamps]
        null_col = [0] * num_rows
        null_df = pd.DataFrame(data={'timestamp':timestamps, 'low': null_col, 
                                     'high': null_col, 'open' : null_col,
                                     'close': null_col, 'volume': null_col})
        #Concatenating
        frames = [null_df, df]
        df = pd.concat(frames, ignore_index = True)
    
    #Now dealing with periods with no trading activity
    i = first_time + 60
    new_data = []
    while i != ending_time:
        print(i)
        if i not in df['timestamp']: #If row is missing, use data from previous row
            prev_row_index = df[df['timestamp'] == i - 60].index[0]    
            prev_row_close = df.loc[prev_row_index]['close']
            new_row = [i] + [prev_row_close] * 4 + [0]
            new_row = {'timestamp': i,
                       'low': prev_row_close,
                       'high': prev_row_close,
                       'open': prev_row_close,
                       'close': prev_row_close,
                       'volume': 0}
            df = df.append(new_row, ignore_index = True)
        i += 60
        
    #Add missing rows to df, sort values
    #new_df = pd.DataFrame(data = new_data, columns = df.columns)
    #frames = [df, new_df]
    df = df.sort_values('timestamp').reset_index(drop = True)
        

        
        