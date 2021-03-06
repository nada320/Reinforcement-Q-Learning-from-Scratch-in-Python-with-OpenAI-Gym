# -*- coding: utf-8 -*-
"""RL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18qp_96eWojjfPndwqtlfIXAIPYmFIuou

#Install liberary
"""

!pip install cmake 'gym[atari]' scipy

"""#Import libraries"""

from IPython.display import clear_output
from time import sleep
import random
from IPython.display import clear_output
import numpy as np
import gym

"""#Brute Force approach





"""

def SetEnvironment(env):
  env.s = 328  # set environment to illustration's state

  epochs = 0
  penalties, rewards = 0, 0

  frames = [] # for animation

  done = False

  while not done:
      action = env.action_space.sample()
      state, reward, done, info = env.step(action)

      if reward == -10:
          penalties += 1
      
      if reward > 0:
        rewards += 1
     # Put each rendered frame into dict for animation
      frames.append({
          'frame': env.render(mode='ansi'),
          'state': state,
          'action': action,
          'reward': reward})

      epochs += 1
      
      
  print("Timesteps taken: {}".format(epochs))
  print("Penalties incurred: {}".format(penalties))
  return frames

def print_frames(frames):
    for i, frame in enumerate(frames):
        clear_output(wait=True)
        print(frame['frame'])
        print(f"Timestep: {i + 1}")
        print(f"State: {frame['state']}")
        print(f"Action: {frame['action']}")
        print(f"Reward: {frame['reward']}")
        sleep(1)

"""#Training function
take hyperparameters alpha, gamma, and epsilon and return quality table(q_table) 
"""

def training(alpha,gamma,epsilon,env):
  # Initialize the q table
  q_table = np.zeros([env.observation_space.n, env.action_space.n])
  # For plotting metrics
  all_epochs = []
  all_penalties = []

  for i in range(1, 100001):
      state = env.reset()

      epochs, penalties, reward, = 0, 0, 0
      done = False

      if epsilon>0.1:
          epsilon -= 0.1*epsilon  
      while not done:
          if random.uniform(0, 1) < epsilon:
              action = env.action_space.sample() # Explore action space
          else:
              action = np.argmax(q_table[state]) # Exploit learned values

          next_state, reward, done, info = env.step(action) 
          
          old_value = q_table[state, action]
          next_max = np.max(q_table[next_state])
      
          new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
          q_table[state, action] = new_value

          if reward == -10:
              penalties += 1

          state = next_state
          epochs += 1
          
      if i % 1000 == 0:  
        clear_output(wait=True)
        print(f"Episode: {i}")
        print("epsilon")

  print("Training finished.\n")
  return q_table

"""#Evaluate agent's performance after Q-learning"""

def Evaluate(q_table,env):
  total_epochs, total_penalties = 0, 0
  episodes = 1000

  for _ in range(episodes):
      state = env.reset()
      epochs, penalties, reward = 0, 0, 0
      
      done = False
      
      while not done:
          action = np.argmax(q_table[state])
          state, reward, done, info = env.step(action)

          if reward == -10:
              penalties += 1

          epochs += 1

      total_penalties += penalties
      total_epochs += epochs

  print(f"Results after {episodes} episodes:")
  print(f"Average timesteps per episode: {total_epochs / episodes}")
  print(f"Average penalties per episode: {total_penalties / episodes}")
  return total_epochs / episodes

env = gym.make("Taxi-v3").env
Evaluate(training(.1,0.6,.1,env),env)

ls



def GridSearch(EnviromentName):
    
  env = gym.make(EnviromentName).env
  alpha=[0.5,0.7,0.9]
  gamma=[0.5,0.7,0.9]
  epsilon=[0.5,0.7,0.9]
  Average_timesteps_per_episode=[]
  listOfHyperParameter=[]
  for i in alpha:
    for j in gamma:
      for k in epsilon:
        hyperparameters=[i,j,k]
        q_table=training(i,j,k,env)
        Average_timesteps_per_episode.append(Evaluate(q_table,env))
        listOfHyperParameter.append(hyperparameters)
  return Average_timesteps_per_episode,listOfHyperParameter

l,ll= GridSearch("Taxi-v3")

Best_hyperparameters=ll[l.index(min(l))]

"""Best Hyperparameters"""

alpha=Best_hyperparameters[0]
gamma=Best_hyperparameters[1]
epsilon=Best_hyperparameters[2]
print("I choice hyperparameters alpha = {} , gamma = {} , epsilon = {} with Average timesteps per episode  {}".format(alpha,gamma,epsilon,min(l)) )

