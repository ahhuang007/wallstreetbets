# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 18:51:48 2022

Script to do validation testing on my models - uses a validation environment
Tests the model, then outputs some data on its results

@author: ahhua
"""

import gym
from gym import envs
import gym_wsb
import pandas as pd
from stable_baselines3.ddpg.policies import MlpPolicy
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import PPO
from recorder import Recorder
import numpy as np

#Importing data
dfs = []
cryptos = ['AAVE', 'ADA', 'ALGO', 'ATOM', 
           'AVAX', 'BCH', 'BTC', 'DOT', 
           'ETH', 'LINK', 'LRC', 'LTC', 
           'MANA', 'MATIC', 'SOL', 'UNI']
cryptos = ['BTC']
for c in cryptos:
    df = pd.read_csv('./data/' + c + '_data.csv')
    '''I think we'll do a similar plan to my source idea.
    5 months for training, 2 months for validation/tuning, 5 months for testing
    '''
    dfs.append(df[38:88000].reset_index(drop = True))

version = "12" #Latest version of model that we're training, for logging purposes
env = gym.make('gym-wsb-val-v0', data = dfs, cryptos = cryptos)

from stable_baselines3.common.env_checker import check_env

check_env(env, warn=True)

model = PPO('MlpPolicy', env, verbose = 1)
env.seed(4)
env.action_space.seed(4)
env.observation_space.seed(4)
model.set_random_seed(4)

#%%

#In case I want to load a previously trained model for more training
model = PPO.load("models/trained_models/trained_model_ppo_v" + version, env = env)
model.set_random_seed(4)
obs = env.reset()
data = [] #Tracks reward at each timestep
cum_data = [] #Tracks cumulative rewards at end of each episode
crypto_data = [[] for x in cryptos] #Tracks the amounts of crypto bought/sold
total_data = [] #Tracks total money at each timestep
balance_data = [] #Tracks our balance at each timestep

#model will go through 2048*x timsteps, where total_timesteps will be rounded up
#to nearest multiple of 2048
#action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

#%%
done = False
reward = 0
while not done:
    action, _states = model.predict(obs, deterministic = True)
    obs, rewards, done, info = env.step(action)
    #Appending data to lists
    data.append(rewards)    
    for i in range(len(cryptos)):
        crypto_data[i].append(info['shares'][i] * info['closes'][i])
    balance_data.append(info['balance'])
    total_data.append(info['total'])
    reward += rewards
    #print(obs)
    #i += 1

print("Final reward is {}".format(reward))
print("Average reward is {} with std of {}".format(np.mean(data), np.std(data)))

#%%

#Saving/plotting data
data_dict = {}
data_dict["reward"] = data
data_dict["total"] = total_data
data_dict["balance"] = balance_data
for i in range(len(cryptos)):
    data_dict[cryptos[i]] = crypto_data[i]
df = pd.DataFrame(data = data_dict)

df.to_csv("./data/data_from_validation/ppo_rewards_v" + version + ".csv")

import matplotlib.pyplot as plt
from scipy.ndimage.filters import uniform_filter1d

plt.plot(df.index, df['total'])
plt.xlabel('timestep')
plt.ylabel('moolah')
plt.title('total money over time (validation, version ' + version + ')')
plt.show()

plt.rcParams["figure.figsize"]=(20,20)
plt.plot(df.index, df['balance'], label = "USD", linewidth = 0.2, alpha = 0.75)
for c in cryptos:
    plt.plot(df.index, df[c], label = c, linewidth = 0.2, alpha = 0.75)
plt.xlabel('timestep')
plt.ylabel('Amount (USD)')
plt.title('charting holdings over time (validation, version ' + version + ')')
plt.legend()
plt.show()

#%%

N = 10000
plt.plot(df.index, df['reward'])
y = uniform_filter1d(df['reward'], size=N)
plt.plot(df.index, y)
plt.xlabel('timestep')
plt.ylabel('reward')
plt.title('reward at each timestep (validation, version ' + version + ')')
plt.show()

env.close()