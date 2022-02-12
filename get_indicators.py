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
cryptos = ["ALGO"]

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