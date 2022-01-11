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

def get_missing_rows(series):
    #Finds missing row numbers and returns a list of timestamps that are missing
    nums = []
    s1 = series[1:].reset_index(drop = True)
    s2 = series[:len(series) - 1]
    s3 = s1 - s2
    #Isolating indices where rows are skipped
    s4 = s3[s3 != 60]
    s4ind = list(s4.index)
    catchup = 0 #Keeps track of missing rows so we can update list appropriately
    start_time = series[0]
    for val, ind in zip(s4, s4ind):
        rows_missing = int((val - 60) / 60)
        for i in range(rows_missing):
            nums.append(int(start_time + (ind + 1 + catchup) * 60))
            catchup += 1
    
    return nums

#Our cryptocurrencies
cryptos = ['AVAX', 'UNI', 'AAVE', 'ALGO', 
           'LTC', 'LRC', 'BTC', 'ETH', 
           'BCH', 'LINK', 'SOL', 'ATOM', 
           'MANA', 'MATIC', 'DOT', 'ADA']

#Starting and ending time range
starting_time = 1609459200
ending_time = 1640995140

for c in cryptos:
    df = pd.read_csv('./data/' + c + '_data.csv')
    df = df.drop('Unnamed: 0', 1)
    print(c)
    print(len(df))
    first_time = df['timestamp'][0] #First/earliest recorded time in df
    
    #If first_time is after starting_time, then fill in values before first_time
    #with null values
    if first_time > starting_time:
        num_rows = int((first_time - starting_time) / 60) #number of null_rows
        #Creating null dataframe to add
        timestamps = list(np.linspace(starting_time, first_time - 60, num_rows))
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
    print(len(df))
    #Get missing timestamps
    missing_rows = get_missing_rows(df['timestamp'])
    
    #Now add timestamps to dataframe
    new_rows = []
    for tstamp in missing_rows:
        #Check if previous row exists in df
        prev_row = df[df['timestamp'] == tstamp - 60]
        if len(prev_row) > 0: #If so, then use that row as data
            pr_ind = prev_row.index[0]
            pr_close = df.loc[pr_ind]['close']
            new_row = [tstamp] + 4 * [pr_close] + [0]
            new_rows.append(new_row)
        else: #prev_row must be in new_rows
            prev_row = [x for x in new_rows if x[0] == tstamp - 60]
            pr_close = prev_row[0][4]
            new_row = [tstamp] + 4 * [pr_close] + [0]
            new_rows.append(new_row)
            
    #Concat df to original df, sort values, and save data
    missing_df = pd.DataFrame(data = new_rows, columns = df.columns)
    frames = [df, missing_df]
    df = pd.concat(frames, ignore_index = True)
    df = df.sort_values('timestamp').reset_index(drop = True)
    print(len(df))
    df.to_csv('./data/' + c + '_data.csv')

        
        