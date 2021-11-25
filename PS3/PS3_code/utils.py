#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# this are the set of possible actions admitted in this problem
action_space = []
action_space.append((-1,0))
action_space.append((0,-1))
action_space.append((1,0))
action_space.append((0,1))


def plot_enviroment(env, x, goal):
    """
    env is the grid enviroment
    x is the state 
    """
    dims = env.shape    
    current_env = np.copy(env)
    # plot agent
    current_env[x] = 1.0 #yellow
    # plot goal
    current_env[goal] = 0.3
    return current_env



def transition_function(env,x,u):
    """Transition function for states in this problem
    x: current state, this is a tuple (i,j)
    u: current action, this is a tuple (i,j)
    env: enviroment
    
    Output:
    new state
    True if correctly propagated
    False if this action can't be executed
    """
    xnew = np.array(x) + np.array(u)
    xnew = tuple(xnew)
    #print('xnew',xnew)
    if state_consistency_check(env,xnew):
        return xnew, True
    return x, False

def state_consistency_check(env,x):
    """Checks wether or not the proposed state is a valid state, i.e. is in colision or our of bounds"""
    # check for collision
    if x[0] < 0 or x[1] < 0 or x[0] >= env.shape[0] or x[1] >= env.shape[1] :
        #print('out of bonds')
        return False
    if env[x] >= 1.0-1e-4:
        #print('Obstacle')
        return False
    return True


