# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 23:28:16 2022

@author: ahhua
"""

#Simple class to record data during training

from stable_baselines3.common.callbacks import BaseCallback
import time

class Recorder(BaseCallback):
  '''
  callback for recording data
  '''
  def __init__(self, li, li2, li3, li4, li5, cryptos, verbose = 1):
    super(Recorder, self).__init__(verbose)
    self.data = li
    self.cum_data = li2
    self.cum_reward = 0
    self.crypto_data = li3
    self.total_data = li4
    self.balance_data = li5
    self.cryptos = cryptos
    
  def _on_step(self) -> bool:
      
    self.data.append(self.locals['rewards'][0])
    self.total_data.append(self.locals['infos'][0]['total'])
    self.balance_data.append(self.locals['infos'][0]['balance'])
    for i in range(len(self.cryptos)):
      self.crypto_data[i].append(self.locals['infos'][0]['shares'][i] *
                                 self.locals['infos'][0]['closes'][i])
    if self.locals['dones'][0] == False:
      self.cum_reward += self.locals['rewards'][0]
    else:
      self.cum_data.append(self.cum_reward)
      self.cum_reward = self.locals['rewards'][0]