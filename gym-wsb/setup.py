# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 00:13:50 2020

@author: MSI
"""

from setuptools import setup

setup(name='gym_wsb',
      version='0.0.2',
      description='gym for trading cryptocurrency',
      install_requires=['gym', 'ccxt', 'numpy', 'pandas', 'stable-baselines3']  # And any other dependencies foo needs
      
)