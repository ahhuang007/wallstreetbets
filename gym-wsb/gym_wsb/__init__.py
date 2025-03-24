# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 00:16:01 2020

@author: MSI
"""

from gym.envs.registration import register

register(
    id='gym-wsb-v2',
    entry_point='gym_wsb.envs:WSBEnv',
)
register(
    id='gym-wsb-val-v2',
    entry_point='gym_wsb.envs:ValEnv')
