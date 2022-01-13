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
from actions import buy_high, sell_low

initial_balance = 100 #Initial amount of money
transaction_fee = 0.005 #May be 0.0035
num_cryptos = 16 #Cryptos we will trade

class WSBEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self,
               dfs):
    super(WSBEnv, self).__init__()
    #Setting up inital prices/data
    self.dfs = dfs
    self.timestep = 0
    self.last_timestep = len(self.dfs[0]) - 1
    #initializing state
    self.balance = initial_balance
    self.shares = [0] * num_cryptos
    self.lows = [x.loc[self.timestep]['low'] for x in self.dfs]
    self.highs = [x.loc[self.timestep]['high'] for x in self.dfs]
    self.opens = [x.loc[self.timestep]['open'] for x in self.dfs]
    self.closes = [x.loc[self.timestep]['close'] for x in self.dfs]
    self.volumes = [x.loc[self.timestep]['volume'] for x in self.dfs]
    self.prices = self.lows + self.highs + self.opens + self.closes + self.volumes
    
    self.observations = [self.balance] + self.shares + self.prices
    self.action_space = spaces.Box(low = -1, high = 1, shape = (num_cryptos,)) 
    self.observation_space = spaces.Box(low=0, high=np.inf, shape = (len(self.observations),))

    
  def step(self, action):
    #A way we can reconcile action space conundrum is to interpret the action 
    #space as range [-1,0) = sell a percentage of crypto ranging from 100 to 
    #0 percent, and range (0, 1] = buy crypto using a percentage of balance
    #ranging from 0 to 100 percent
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
                                                 self.shares,
                                                 self.closes)
    
    
    reward = 0
    
    info = {}
    #Updating prices for next step
    if self.timestep != self.last_timestep:
        self.timestep += 1
        self.lows = [x.loc[self.timestep]['low'] for x in self.dfs]
        self.highs = [x.loc[self.timestep]['high'] for x in self.dfs]
        self.opens = [x.loc[self.timestep]['open'] for x in self.dfs]
        self.closes = [x.loc[self.timestep]['close'] for x in self.dfs]
        self.volumes = [x.loc[self.timestep]['volume'] for x in self.dfs]
        self.prices = self.lows + self.highs + self.opens + self.closes + self.volumes
        self.observations = [self.balance] + self.shares + self.prices
    else:
        done = True
    
    return self.observations, reward, done, info

  def reset(self):
    self.balance = initial_balance
    self.shares = [0] * num_cryptos
    self.timestep = 0
    self.lows = [x.loc[self.timestep]['low'] for x in self.dfs]
    self.highs = [x.loc[self.timestep]['high'] for x in self.dfs]
    self.opens = [x.loc[self.timestep]['open'] for x in self.dfs]
    self.closes = [x.loc[self.timestep]['close'] for x in self.dfs]
    self.volumes = [x.loc[self.timestep]['volume'] for x in self.dfs]
    self.prices = self.lows + self.highs + self.opens + self.closes + self.volumes
    observations = [self.balance] + self.shares + self.prices
    done = False
    return observations
    
  def render(self, mode='human'):
    ...
    
  def close(self):
    pass