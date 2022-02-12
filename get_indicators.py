# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:30:47 2022

@author: ahhua
"""

'''
script to create indicators for data
MACD - Moving Average Convergence Divergence
RSI - Relative Strength Index
CCI - Commodity Channel Index
ADX - Average Directional Moving Index
'''

import pandas as pd
import numpy as np

cryptos = ['AAVE', 'ADA', 'ALGO', 'ATOM', 
           'AVAX', 'BCH', 'BTC', 'DOT', 
           'ETH', 'LINK', 'LRC', 'LTC', 
           'MANA', 'MATIC', 'SOL', 'UNI']
#cryptos = ["ALGO"]

for c in cryptos:
    df = pd.read_csv('./data/' + c + '_data.csv')
    df = df.drop('Unnamed: 0', 1)
    print(c)

    #Getting MACD
    ema26 = df["close"].ewm(span = 26).mean()
    ema12 = df["close"].ewm(span = 12).mean()
    df["MACD"] = ema12 - ema26
    
    #Getting CCI
    periods = 20
    tp = (df['high'] + df['low'] + df['close']) / 3 
    sma = tp.rolling(periods).mean()
    absdev = np.abs(sma - tp)
    md = absdev.rolling(periods).mean()
    #mad = tp.rolling(periods).apply(lambda x: pd.Series(x).mad())
    df['CCI'] = (tp - sma) / (0.015 * md) 
    #df['CCI3'] = (tp - sma) / (0.015 * md)
    
    #Getting RSI
    
    
    #Getting ADX
    interval = 14
    df['-DM'] = df['low'].shift(1) - df['low']
    df['+DM'] = df['high'] - df['high'].shift(1)
    df['+DM'] = np.where((df['+DM'] > df['-DM']) & (df['+DM']>0), df['+DM'], 0.0)
    df['-DM'] = np.where((df['-DM'] > df['+DM']) & (df['-DM']>0), df['-DM'], 0.0)  
    df['TR_TMP1'] = df['high'] - df['low']
    df['TR_TMP2'] = np.abs(df['high'] - df['close'].shift(1))
    df['TR_TMP3'] = np.abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['TR_TMP1', 'TR_TMP2', 'TR_TMP3']].max(axis=1)  
    df['TR'+str(interval)] = df['TR'].rolling(interval).sum()  
    df['+DMI'+str(interval)] = df['+DM'].rolling(interval).sum()
    df['-DMI'+str(interval)] = df['-DM'].rolling(interval).sum()  
    df['+DI'+str(interval)] = df['+DMI'+str(interval)] /   df['TR'+str(interval)]*100
    df['-DI'+str(interval)] = df['-DMI'+str(interval)] / df['TR'+str(interval)]*100
    df['DI'+str(interval)+'-'] = abs(df['+DI'+str(interval)] - df['-DI'+str(interval)])
    df['DI'+str(interval)] = df['+DI'+str(interval)] + df['-DI'+str(interval)]  
    df['DX'] = (df['DI'+str(interval)+'-'] / df['DI'+str(interval)])*100  
    df['ADX'] = df['DX'].rolling(interval).mean() 
    del df['TR_TMP1'], df['TR_TMP2'], df['TR_TMP3'], df['TR'], df['TR'+str(interval)]
    del df['+DMI'+str(interval)], df['DI'+str(interval)+'-']
    del df['DI'+str(interval)], df['-DMI'+str(interval)]
    del df['+DI'+str(interval)], df['-DI'+str(interval)]
    del df['DX']
    del df['-DM']
    del df['+DM']
    
    df.to_csv('./data/' + c + '_data.csv')