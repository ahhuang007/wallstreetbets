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

I think I used buys to be able to calculate rewards for selling at a higher price than I bought the currency at 
reward (sell_low only) - reward from selling currencies
'''

def sell_low(balance, action, fee, i, shares, closes, buys):
    
    balance += shares[i] * abs(action) * (1 - fee) * closes[i]
    transaction_cost = shares[i] * abs(action) * fee  * closes[i]
    shares[i] -= abs(action) * shares[i]
    #update balance
    amt = abs(action) * shares[i]
    while amt > 0 and buys: #This removes shares based on fifo
    #for example, if I buy 1 ETH at t = 1 and then 1 more ETH at t = 2,
    #if i sell 1 ETH at t = 3 I calculate the PNL based on the price at t = 1
        
        share, price = buys[0][0], buys[0][1]
        
        if amt > share:
            prev = share * price
            amt -= share
            
            revenue = share * (1 - fee) * closes[i]
            balance += revenue
            shares[i] -= share
            
            buys.pop(0)
        elif amt == share:
            prev = share * price
            amt = 0
            revenue = share * (1 - fee) * closes[i]
            balance += revenue
            shares[i] -= share
            
            buys.pop(0)
        else:
            partial = share - amt
            prev = partial * price
            amt = 0
            revenue = partial * (1 - fee) * closes[i]
            balance += revenue
            shares[i] -= partial
            buys[0][0] -= partial
        #balance += shares[i] * abs(action) * (1 - fee) * closes[i]
        
        #shares[i] -= abs(action) * shares[i]
        #cost += state[index+1]*min(abs(action), state[index+STOCK_DIM+1]) * fee
        #trades += 1

    return balance, shares, transaction_cost

def buy_high(balance, action, fee, i, shares, closes, buys):
    if balance > 0:
        #update balance
        amt = ((1 - fee) * balance * abs(action)) / closes[i] #amount of currency, e.g. 0.2 ETH
        shares[i] += amt
        balance -= abs(action) * balance
        transaction_cost = fee * balance * abs(action)
        buys.append([amt, closes[i]]) #Append the amount of currency bought at the price
        #cost+= state[index+1]*min(available_amount, action) * fee
        #trades += 1
    else:
        pass
    return balance, shares, transaction_cost, buys