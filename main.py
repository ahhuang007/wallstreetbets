# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 19:48:07 2022

Rewriting this code to reflect my new approach

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
import pickle

#Importing data
dfs = []
closes = []
norm_dfs = []
cryptos = ['ETH', 'ADA', 'XRP']
for c in cryptos:
    df = pd.read_csv('./data/' + c + '_training_ta_data.csv')
    dfs.append(df)
#In previous approach data = closing prices for each currency
#cryptos was list of currencies
#norm_data was the normalized overall data along with ML predictions
env = gym.make('gym-wsb-v2', data = dfs, cryptos = cryptos)

env.seed(4)
env.action_space.seed(4)
env.observation_space.seed(4)

#%%

#In case I want to load a previously trained model for more training
#ppo_model = PPO.load("models/trained_models/trained_model_ppo_v40", env = env)
policy_kwargs = dict(net_arch=[64, 64, 64])
ppo_model = PPO('MlpPolicy', env, policy_kwargs = policy_kwargs, verbose = 1, learning_rate = 0.00001)
ppo_model.set_random_seed(4)


data = [] #Tracks reward at each timestep
cum_data = [] #Tracks cumulative rewards at end of each episode
crypto_data = [[] for x in cryptos] #Tracks the amounts of crypto bought/sold
total_data = [] #Tracks total money at each timestep
balance_data = [] #Tracks our balance at each timestep
record = Recorder(data, cum_data, crypto_data, total_data, balance_data, cryptos)

obs = env.reset()
#model will go through 2048*x timsteps, where total_timesteps will be rounded up
#to nearest multiple of 2048
#action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

#%%

ppo_model = ppo_model.learn(total_timesteps = 500000, callback = record, reset_num_timesteps=True)
ppo_model.save("models/trained_models/trained_model_ppo_v" + version)
env.close()
#%%

#Saving/plotting data
data_dict = {}
data_dict["reward"] = data
data_dict["total"] = total_data
data_dict["balance"] = balance_data
for i in range(len(cryptos)):
    data_dict[cryptos[i]] = crypto_data[i]
df = pd.DataFrame(data = data_dict)
df2 = pd.DataFrame(data = {"episode":range(1, len(cum_data) + 1), "cumulative reward": cum_data})

df.to_csv("./data/data_from_training/timestep_rewards/ppo_rewards_v" + version + ".csv")
df2.to_csv("./data/data_from_training/cumulative_rewards/ppo_cum_rewards_v" + version + ".csv")

import matplotlib.pyplot as plt
from scipy.ndimage.filters import uniform_filter1d

plt.plot(df.index, df['total'])
plt.xlabel('timestep')
plt.ylabel('moolah')
plt.title('total money over time (version ' + version + ')')
plt.show()

plt.rcParams["figure.figsize"]=(20,20)
plt.plot(df.index, df['balance'], label = "USD", linewidth = 0.2, alpha = 0.75)
for c in cryptos:
    plt.plot(df.index, df[c], label = c, linewidth = 0.2, alpha = 0.75)
plt.xlabel('timestep')
plt.ylabel('Amount (USD)')
plt.title('charting holdings over time (version ' + version + ')')
plt.legend()
plt.show()

N = 20000
plt.plot(df.index, df['reward'])
y = uniform_filter1d(df['reward'], size=N)
plt.plot(df.index, y)
plt.xlabel('timestep')
plt.ylabel('reward')
plt.title('reward at each timestep (version ' + version + ')')
plt.show()

plt.plot(df2['episode'], df2['cumulative reward'])
plt.xlabel('episode')
plt.ylabel('total reward')
plt.title('reward after each episode (version ' + version + ')')
plt.show()