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
buys - list of purchases of the currency with the price they were bought at
Returns: balance - updated balance after transaction
shares - updated portfolio after transaction
buys (only for sell_low) - updated list of purchases at certain prices - 
this function removes as many purchases as needed to fulfill the sell order.
reward (sell_low only) - reward from selling currencies
'''

def sell_low(balance, action, fee, i, shares, closes, buys):
    reward = 0
    
    if shares[i] > 0:
        #update balance
        amt = abs(action) * shares[i]
        while amt > 0 and buys:
            
            share, price = buys[0][0], buys[0][1]
            
            if amt > share:
                prev = share * price
                amt -= share
                
                revenue = share * (1 - fee) * closes[i]
                balance += revenue
                reward += (revenue - prev)
                shares[i] -= share
                
                buys.pop(0)
            elif amt == share:
                prev = share * price
                amt = 0
                revenue = share * (1 - fee) * closes[i]
                balance += revenue
                reward += (revenue - prev)
                shares[i] -= share
                
                buys.pop(0)
            else:
                partial = share - amt
                prev = partial * price
                amt = 0
                revenue = partial * (1 - fee) * closes[i]
                balance += revenue
                reward += (revenue - prev)
                shares[i] -= partial
                buys[0][0] -= partial
        #balance += shares[i] * abs(action) * (1 - fee) * closes[i]
        
        #shares[i] -= abs(action) * shares[i]
        #cost += state[index+1]*min(abs(action), state[index+STOCK_DIM+1]) * fee
        #trades += 1
    else:
        pass #No shares to sell!
    return balance, shares, buys, reward

def buy_high(balance, action, fee, i, shares, closes):
    if balance > 0:
        #update balance
        if closes[i] > 0: #Price must exist to be able to be bought
            shares[i] += ((1 - fee) * balance * abs(action)) / closes[i]
            balance -= abs(action) * balance
        else:
            pass
        #cost+= state[index+1]*min(available_amount, action) * fee
        #trades += 1
    else:
        pass
    return balance, shares