# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 00:21:56 2020

@author: MSI
"""

import gym
from gym import error, spaces, utils
from gym.utils import seeding
import time
import pandas as pd
import numpy as np
from gym_wsb.envs.actions import buy_high, sell_low
import random

initial_balance = 100 #Initial amount of money
transaction_fee = 0.005 #May be 0.0035
alpha = 1 #hyperparameters for reward function
beta = 1
gamma = 1
delta = 1
epsilon = 1 #epsilon in this case is not for the exploration/exploitation

class WSBEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self, data, cryptos):
    super(WSBEnv, self).__init__()
    #Setting up inital prices/data
    self.dfs = data
    self.actual_closes = [x.loc[:, "actual_closes"] for x in data]
    self.num_cryptos = len(self.dfs) #Cryptos we will trade
    self.last_timestep = self.dfs[0].loc[len(self.dfs[0]) - 1, 'timestamp']
    #timestep is really row number
    self.timestep = 0 #self.dfs[0].loc[0, 'timestamp']
    self.cryptos = cryptos
    self.counter = 0
    #initializing state
    self.balance = initial_balance
    self.shares = [0] * self.num_cryptos
    self.lows = [x.loc[self.timestep, 'low'] for x in self.dfs]
    self.highs = [x.loc[self.timestep, 'high'] for x in self.dfs]
    self.opens = [x.loc[self.timestep, 'open'] for x in self.dfs]
    self.closes = [x.loc[self.timestep, 'close'] for x in self.dfs]
    self.volumes = [x.loc[self.timestep, 'volume'] for x in self.dfs]
    self.prices = self.lows + self.highs + self.opens + self.closes + self.volumes
    self.ema_12 = [x.loc[self.timestep, 'ema_12'] for x in self.dfs]
    self.ema_26 = [x.loc[self.timestep, 'ema_26'] for x in self.dfs]
    self.sma = [x.loc[self.timestep, 'sma'] for x in self.dfs]
    self.rsi = [x.loc[self.timestep, 'rsi'] for x in self.dfs]
    self.macd = [x.loc[self.timestep, 'macd'] for x in self.dfs]
    self.atr = [x.loc[self.timestep, 'atr'] for x in self.dfs]
    self.ub = [x.loc[self.timestep, 'ub'] for x in self.dfs]
    self.cb = [x.loc[self.timestep, 'cb'] for x in self.dfs]
    self.lb = [x.loc[self.timestep, 'lb'] for x in self.dfs]
    self.obv = [x.loc[self.timestep, 'obv'] for x in self.dfs]
    self.vwap = [x.loc[self.timestep, 'vwap'] for x in self.dfs]
    self.technicals = (self.ema_12 + self.ema_26 + self.sma + 
                    self.rsi + self.macd + self.atr + 
                    self.ub + self.cb + self.lb + 
                    self.obv + self.vwap)
    self.a_closes = [x.loc[self.timestep, 'actual_closes'] for x in self.dfs]
    self.observations = [self.balance] + self.shares + self.prices + self.technicals
    self.action_space = spaces.Box(low = -1, high = 1, shape = (self.num_cryptos,), dtype = 'float32') 
    self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape = (len(self.observations),), dtype = 'float32')
    self.done = False
    self.total = self.balance
    self.buys = [[] for x in self.cryptos] #For calculating pnl, each element is [amt, price]
    
  def step(self, action):
    #A way we can reconcile action space conundrum is to interpret the action 
    #space as range [-1,0) = sell a percentage of crypto ranging from 100 to 
    #0 percent, and range (0, 1] = buy crypto using a percentage of balance
    #ranging from 0 to 100 percent
    previous_total = self.total #apparently doesn't do anything
    argsort_actions = np.argsort(action) #sorting order of doing actions - selling actions first, then buying
          
    sell_index = argsort_actions[:np.where(action < 0)[0].shape[0]] #just the sells
    buy_index = argsort_actions[::-1][:np.where(action > 0)[0].shape[0]] #just the buys
    reward = 0
    #considering that the action is taken based on x state with y balance, the buy operations should
    #take place first, otherwise if they take place after sell operations they take place
    #with a different state of shares/balance
    transaction_costs = 0
    for index in buy_index: 
        # print('take buy action: {}'.format(actions[index]))
        #self._buy_stock(index, actions[index])
        prev_bal, prev_sha = self.balance, self.shares[index]
        self.balance, self.shares, transaction_cost, self.buys = buy_high(self.balance,
                 action[index],
                 transaction_fee,
                 index,
                 self.shares,
                 self.a_closes,
                 self.buys)
        transaction_costs += transaction_cost
        if self.balance < prev_bal:
            self.buys[index].append([self.shares[index] - prev_sha, self.a_closes[index]])
    
    for index in sell_index:
        # print('take sell action'.format(actions[index]))
        #self._sell_stock(index, actions[index])
        self.balance, self.shares, transaction_cost, self.buys[index] = sell_low(self.balance,
                 action[index],
                 transaction_fee,
                 index,
                 self.shares,
                 self.a_closes,
                 self.buys[index])
        transaction_costs += transaction_cost

    
    '''
    for i in range(len(action)):
        a = action[i]
        if a < 0:
            self.balance, self.shares = sell_low(self.balance, 
                                                 a, 
                                                 transaction_fee, 
                                                 i, 
                                                 self.shares, 
                                                 self.closes)
        elif a > 0: #If 0, do nothing
            self.balance, self.shares = buy_high(self.balance, 
                                                 a, 
                                                 transaction_fee,
                                                 i,
                                                 self.shares,
                                                 self.closes)
    '''
    #Calculating reward
    #reward = pnl - alpha*transaction_costs - beta*portfolio_volatility - gamma*maximum_drawdown - delta*shannon_entropy - epsilon*(position_size/portfolio_value)^2
    
    #reward = 0
    self.total = 0
    for j in range(self.num_cryptos):
        self.total += self.shares[j] * self.a_closes[j]
    self.total += self.balance
    #reward += self.balance
    #reward -= previous_total
    self.counter += 1
    #Broadcasting updates
    if self.timestep % 1000 == 0:
        print("Timestep " + str(self.timestep) + " holdings (USD):")
        for k in range(len(self.shares)):
            print("{}: {}".format(self.cryptos[k], self.shares[k] * self.a_closes[k]))
        print("Dollarydoos: {}".format(self.balance))
    info = {'shares': self.shares, 'balance': self.balance, 'total': self.total, 'closes': self.a_closes}
    #Updating prices for next step
    if self.counter < 10000:
        self.timestep = random.randint(0, self.last_timestep - 1)
        self.lows = [x.loc[self.timestep]['low'] for x in self.dfs]
        self.highs = [x.loc[self.timestep]['high'] for x in self.dfs]
        self.opens = [x.loc[self.timestep]['open'] for x in self.dfs]
        self.closes = [x.loc[self.timestep]['close'] for x in self.dfs]
        self.a_closes = [x.loc[self.timestep] for x in self.actual_closes]
        self.volumes = [x.loc[self.timestep]['volume'] for x in self.dfs]
        self.prices = self.lows + self.highs + self.opens + self.closes + self.volumes
        self.macd = [x.loc[self.timestep]['MACD'] for x in self.dfs]
        self.cci = [x.loc[self.timestep]['CCI'] for x in self.dfs]
        self.adx = [x.loc[self.timestep]['ADX'] for x in self.dfs]
        self.rsi = [x.loc[self.timestep]['RSI'] for x in self.dfs]
        self.pred = [x.loc[self.timestep]['pred'] for x in self.dfs]
        self.observations = [self.balance] + self.shares + self.prices + self.macd + self.cci + self.adx + self.pred
    else:
        self.done = True
        print("reached end of episode, resetting")
        if self.total <= 101:
            reward -= 50
        else:
            reward += 50
    if self.total < 20:
        print("balance too low")
        self.done = True
        reward -= 50
    return np.array(self.observations, dtype = 'float32'), reward, self.done, info

  def reset(self):
    self.balance = initial_balance
    self.shares = [0] * self.num_cryptos
    self.timestep = random.randint(0, self.last_timestep - 1)
    self.lows = [x.loc[self.timestep]['low'] for x in self.dfs]
    self.highs = [x.loc[self.timestep]['high'] for x in self.dfs]
    self.opens = [x.loc[self.timestep]['open'] for x in self.dfs]
    self.closes = [x.loc[self.timestep]['close'] for x in self.dfs]
    self.a_closes = [x.loc[self.timestep] for x in self.actual_closes]
    self.volumes = [x.loc[self.timestep]['volume'] for x in self.dfs]
    self.prices = self.lows + self.highs + self.opens + self.closes + self.volumes
    self.macd = [x.loc[self.timestep]['MACD'] for x in self.dfs]
    self.cci = [x.loc[self.timestep]['CCI'] for x in self.dfs]
    self.adx = [x.loc[self.timestep]['ADX'] for x in self.dfs]
    self.rsi = [x.loc[self.timestep]['RSI'] for x in self.dfs]
    self.pred = [x.loc[self.timestep]['pred'] for x in self.dfs]
    self.observations = [self.balance] + self.shares + self.prices + self.macd + self.cci + self.adx + self.pred
    self.done = False
    self.total = self.balance
    self.buys = [[] for x in self.cryptos]
    self.counter = 0
    print("resetting environment")
    return np.array(self.observations, dtype = 'float32')
    
  def render(self, mode='human'):
    ...
    
  def close(self):
    pass