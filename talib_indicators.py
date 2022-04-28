# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 21:50:42 2022

@author: ahhua
"""

'''
Script to test TA-lib's indicators. Seems promising.
'''

import pandas as pd
import numpy as np
import talib

#Our cryptocurrencies
cryptos = ['AVAX', 'UNI', 'AAVE', 'ALGO', 
           'LTC', 'LRC', 'BTC', 'ETH', 
           'BCH', 'LINK', 'SOL', 'ATOM', 
           'MANA', 'MATIC', 'DOT', 'ADA']
#cryptos = ['BTC']

for c in cryptos:
    df = pd.read_csv('./data/' + c + '_data.csv')
    df = df.drop('Unnamed: 0', 1)
    print(c)
    #Don't need to calculate volume again in USD, since we already did that in
    #process_indicators
    
    #Getting MACD
    macd, macdsignal, macdhist = talib.MACD(df["close"], fastperiod=12, slowperiod=26, signalperiod=9)
    df["MACD"] = macd
    
    #Getting CCI
    periods = 20
    df["CCI"] = talib.CCI(df["high"], df["low"], df["close"], timeperiod=periods)
    
    #Getting RSI
    df["RSI"] = talib.RSI(df["close"], timeperiod=14)
    
    #Getting ADX
    interval = 14
    df["ADX"] = talib.ADX(df["high"], df["low"], df["close"], timeperiod=interval)
    
    #Just going to cut off the parts with nans
    df = df[33:].reset_index(drop = True)
    
    df.to_csv('./data/' + c + '_data.csv')