# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 19:48:07 2022

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

#Importing data
dfs = []
cryptos = ['AAVE', 'ADA', 'ALGO', 'ATOM', 
           'AVAX', 'BCH', 'BTC', 'DOT', 
           'ETH', 'LINK', 'LRC', 'LTC', 
           'MANA', 'MATIC', 'SOL', 'UNI']
for c in cryptos:
    df = pd.read_csv('./data/' + c + '_data.csv')
    '''I think we'll do a similar plan to my source idea.
    5 months for training, 2 months for validation/tuning, 5 months for testing
    '''
    dfs.append(df[:175200])

env = gym.make('gym-wsb-v0', data = dfs)

from stable_baselines3.common.env_checker import check_env

check_env(env, warn=True)

model = PPO('MlpPolicy', env, verbose = 1)
env.seed(4)
env.action_space.seed(4)
env.observation_space.seed(4)
model.set_random_seed(4)

#performance with random model
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10, deterministic=True)

print(f"mean_reward={mean_reward:.2f} +/- {std_reward}")

model.save("models/random_models/random_model_ppo_v1")

#In case I want to load a previously trained model for more training
#ppo_model = PPO.load("models/trained_models/trained_model_ppo_v1", env = env)
#ppo_model.set_random_seed(4)
ppo_model = PPO('MlpPolicy', env, verbose = 1)
ppo_model.set_random_seed(4)


data = [] #Tracks reward at each timestep
cum_data = [] #Tracks cumulative rewards at end of each episode
crypto_data = [[]] * len(cryptos) #Tracks the amounts of crypto bought/sold
record = Recorder(data, cum_data, crypto_data)

env.reset()
#set total_timesteps equal to n_eval_episodes * max_timesteps
#model will go through 2048*x timsteps, where total_timesteps will be rounded up
#to nearest multiple of 2048
#action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

ppo_model = ppo_model.learn(total_timesteps = 100000, log_interval = 10000, callback = record)
ppo_model.save("models/trained_models/trained_model_ppo_v1")

mean_reward, std_reward = evaluate_policy(ppo_model, env, n_eval_episodes=10, deterministic=True)

print(f"mean_reward={mean_reward:.2f} +/- {std_reward}")