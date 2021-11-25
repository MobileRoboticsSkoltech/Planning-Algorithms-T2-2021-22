#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils import plot_enviroment, action_space, transition_function
from vi import vi, policy_vi


data = np.load('data_ps3.npz')
environment = data['environment']
#plt.matshow(environment)


# (row index, colum index). In the image row corresponds to y, and colum to x.
x_ini = (11,6)
goal = (15,29)

# task 1 VI, Gopt
# ======================================
Gopt = vi(environment,goal)


# Visualization
# ======================================
if 1:
    im = plot_joint_enviroment(environment,x_e, x_p,goal)
    plt.matshow(im)
    plt.show()



# task 2: Plan
# ======================================
policy = policy_vi(Gopt)


# Visualization
# ======================================
if 0:
    fig = plt.figure()
    imgs = []
    x = x_ini
    for s in range(100):
        im = plot_enviroment(environment,x,goal)
        plot = plt.imshow(im)
        imgs.append([plot])
        
        # TODO, calculate a plan based on the policy calcualted in VI
        
        
        if x == goal:
            print('Goal achieved')
            break


    im = plot_enviroment(environment,x,goal)
    plot = plt.imshow(im)
    imgs.append([plot])
    ani = animation.ArtistAnimation(fig, imgs, interval=100, blit=True)
    ani.save('plan_vi.mp4')
    plt.show()
