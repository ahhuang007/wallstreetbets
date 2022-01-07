# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 19:48:07 2022

@author: ahhua
"""

import gym
from gym import envs
import gym_wsb

env = gym.make('gym-wsb-v0', episode_timesteps=100)

from stable_baselines3.common.env_checker import check_env

check_env(env, warn=True)