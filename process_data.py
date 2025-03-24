# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 21:50:42 2022

Rewritten ta-lib script to calculate the indicators as well as normalize the data.

@author: ahhua
"""


import pandas as pd
import numpy as np
from talipp.indicators import ATR, BB, EMA, MACD, OBV, RSI, SMA, VWAP
from talipp.ohlcv import OHLCVFactory
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

#Our cryptocurrencies
# cryptos = ['AVAX', 'UNI', 'AAVE', 'ALGO', 
#            'LTC', 'LRC', 'BTC', 'ETH', 
#            'BCH', 'LINK', 'SOL', 'ATOM', 
#            'MANA', 'MATIC', 'DOT', 'ADA']
#cryptos = ['BTC']
cryptos = ['ETH', 'XRP', 'ADA']
datasets = ["training", "validation"]
for dataset in datasets:
    for c in cryptos:
        df = pd.read_csv('./data/' + c + f'_{dataset}_data.csv')
        print(f"{dataset} set for {c}")
        ohlcv = OHLCVFactory.from_matrix2([
            list(df['open']),
            list(df['high']),
            list(df['low']),
            list(df['close']),
            list(df['volume'])]
        )
        #Instead of calculating indicators for each of OHCL, 
        #I'm just doing Close price indicators to avoid cluttering the state space
        closes = list(df['close'])
        actual_closes = closes.copy()
        volumes = list(df['volume'])
        ema_12 = list(EMA(period = 12, input_values = closes))
        ema_26 = list(EMA(period = 26, input_values = closes))
        sma = list(SMA(period = 50, input_values = closes))
        rsi = list(RSI(period = 14, input_values = closes))
        macd = list(MACD(12, 26, 9, input_values = closes))
        macd = [None] * 25 + [x.macd for x in macd if x is not None]
        atr = list(ATR(period = 14, input_values = ohlcv)) 
        bb = list(BB(20, 2, closes))
        ub = [None] * 19 + [x.ub for x in bb if x is not None]
        cb = [None] * 19 + [x.cb for x in bb if x is not None]
        lb = [None] * 19 + [x.lb for x in bb if x is not None]
        obv = list(OBV(input_values = ohlcv))
        vwap = list(VWAP(input_values = ohlcv))
        
        #Now the data needs to be standardized
        timestamps = list(df['timestamp'])
        opens = scaler.fit_transform(np.array(df['open']).reshape(-1, 1)).reshape(-1).tolist()
        highs = scaler.fit_transform(np.array(df['high']).reshape(-1, 1)).reshape(-1).tolist()
        lows = scaler.fit_transform(np.array(df['low']).reshape(-1, 1)).reshape(-1).tolist()
        closes = scaler.fit_transform(np.array(df['close']).reshape(-1, 1)).reshape(-1).tolist()
        volumes = scaler.fit_transform(np.array(df['volume']).reshape(-1, 1)).reshape(-1).tolist()
        ema_12 = scaler.fit_transform(np.array(ema_12).reshape(-1, 1)).reshape(-1).tolist()
        ema_26 = scaler.fit_transform(np.array(ema_26).reshape(-1, 1)).reshape(-1).tolist()
        sma = scaler.fit_transform(np.array(sma).reshape(-1, 1)).reshape(-1).tolist()
        rsi = scaler.fit_transform(np.array(rsi).reshape(-1, 1)).reshape(-1).tolist()
        macd = scaler.fit_transform(np.array(macd).reshape(-1, 1)).reshape(-1).tolist()
        atr = scaler.fit_transform(np.array(atr).reshape(-1, 1)).reshape(-1).tolist()
        ub = scaler.fit_transform(np.array(ub).reshape(-1, 1)).reshape(-1).tolist()
        cb = scaler.fit_transform(np.array(cb).reshape(-1, 1)).reshape(-1).tolist()
        lb = scaler.fit_transform(np.array(lb).reshape(-1, 1)).reshape(-1).tolist()
        obv = scaler.fit_transform(np.array(obv).reshape(-1, 1)).reshape(-1).tolist()
        vwap = scaler.fit_transform(np.array(vwap).reshape(-1, 1)).reshape(-1).tolist()
        
        new_df = pd.DataFrame({'timestamp' : timestamps, 'open' : opens, 
                                      'high' : highs, 'low' : lows, 
                                      'close' : closes, 'volume' : volumes, 
                                      'ema_12' : ema_12, 'ema_26' : ema_26, 
                                      'sma' : sma, 'rsi' : rsi, 'macd' : macd, 
                                      'atr' : atr, 'ub' : ub, 'cb' : cb, 
                                      'lb' : lb, 'obv' : obv, 'vwap' : vwap,
                                      "actual_closes" : actual_closes})
                              
        
        #Just going to cut off the parts with nans
        new_df.dropna(inplace = True)
        new_df = new_df.reset_index(drop = True)
        new_df.to_csv('./data/' + c + f'_{dataset}_ta_data.csv', index = False)
    