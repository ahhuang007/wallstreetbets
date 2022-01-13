# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 03:24:07 2022

@author: ahhua
"""
'''Functions to take care of selling/buying
Inputs: balance - current amount of fiat currency
action - float in range [-1, 1]. Negative values indicate selling, positive
values indicate buying. Example - an action of value 0.5 means using 50% of
available balance to buy X crypto.
fee - transaction fee
i - index value for the crypto in question
shares - list of our current portfolio
closes - list of closing prices for our cryptocurrencies
Returns: balance - updated balance after transaction
shares - updated portfolio after transaction
'''

def sell_low(balance, action, fee, i, shares, closes):
    if shares[i] > 0:
        #update balance
        balance += shares[i] * abs(action) * (1 - fee) * closes[i]
        
        shares[i] -= abs(action) * shares[i]
        #cost += state[index+1]*min(abs(action), state[index+STOCK_DIM+1]) * fee
        #trades += 1
    else:
        pass #No shares to sell!
    return balance, shares

def buy_high(balance, action, fee, i, shares, closes):
    if balance > 0:
        #update balance
        
        shares[i] += ((1 - fee) * balance * abs(action)) / closes[i]
        balance -= abs(action) * balance
        #cost+= state[index+1]*min(available_amount, action) * fee
        #trades += 1
    else:
        pass
    return balance, shares