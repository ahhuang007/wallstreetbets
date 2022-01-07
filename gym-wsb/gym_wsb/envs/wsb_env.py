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

initial_balance = 100 #Initial amount of money
transaction_fee = 0.005 #May be 0.0035
num_cryptos = 8 #Cryptos we will trade

class WSBEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self,
               episode_timesteps, df, data):
    super(WSBEnv, self).__init__()
    #Setting up inital prices/data
    self.df = df
    self.data = data
    
    #initializing state
    self.balance = inital_balance
    self.shares = [0] * num_cryptos
    self.prices = 
    self.cur_data = 
    
    observations = [self.balance] + self.shares + self.prices + self.data
    self.timestep = 0
    self.action_space = spaces.Box(low = -1, high = 1, shape = (num_cryptos,)) 
    self.observation_space = spaces.Box(low=0, high=np.inf, shape = (len(observations),))
    self.done = False
    
  def step(self, action):
    #A way we can reconcile action space conundrum is to interpret the action 
    #space as range [-1,0) = sell a percentage of crypto ranging from 100 to 
    #0 percent, and range (0, 1] = buy crypto using a percentage of balance
    #ranging from 0 to 100 percent
    observations = []
    reward = 0
    
    info = {}
    self.timestep += 1
    return observations, reward, self.done, info

  def reset(self):
    self.balance = initial_balance
    self.shares = [0] * num_cryptos
    observations = [self.balance] + self.shares + self.prices + self.data
    self.done = False
    return observations
    
  def render(self, mode='human'):
    ...
    
  def close(self):
    pass