# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 03:24:07 2022

@author: ahhua
"""
#functions to take care of selling/buying

def sell_low(index, action):
        if self.state[index+STOCK_DIM+1] > 0:
            #update balance
            self.state[0] += \
            self.state[index+1]*min(abs(action),self.state[index+STOCK_DIM+1]) * \
             (1- TRANSACTION_FEE_PERCENT)
            
            self.state[index+STOCK_DIM+1] -= min(abs(action), self.state[index+STOCK_DIM+1])
            self.cost +=self.state[index+1]*min(abs(action),self.state[index+STOCK_DIM+1]) * \
             TRANSACTION_FEE_PERCENT
            self.trades+=1
        else:
            pass

def _buy_stock(self, index, action):
    available_amount = self.state[0] // self.state[index+1]
    # print('available_amount:{}'.format(available_amount))
    
    #update balance
    self.state[0] -= self.state[index+1]*min(available_amount, action)* \
                      (1+ TRANSACTION_FEE_PERCENT)

    self.state[index+STOCK_DIM+1] += min(available_amount, action)
    
    self.cost+=self.state[index+1]*min(available_amount, action)* \
                      TRANSACTION_FEE_PERCENT
    self.trades+=1