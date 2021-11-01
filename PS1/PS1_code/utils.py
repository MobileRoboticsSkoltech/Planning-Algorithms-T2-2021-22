#!/usr/bin/python

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def normalize_image(img):
    dims = img.shape
    env = np.ones(dims)
    z = np.where(img < 0.1)
    env[z] = 0.0
    return env


def plot_enviroment(img,obj,x):
    """
    img: original image in 2d
    obj, is the 3d array of different configurations
    x is the curent pose of the object
    """
    dims = obj.shape
    dim_x = int((dims[0]-1)/2)
    dim_y = int((dims[1]-1)/2)
    merged_img = np.copy(img)
    merged_img[ x[0]-dim_x:x[0]+dim_x+1, x[1]-dim_y:x[1]+dim_y+1 ] += obj[:,:,x[2]]*0.5
    return merged_img



def plotting_results(environment,rod,plan):
    # plotting the result
    # ======================================
    fig = plt.figure()
    imgs = []
    for s in plan:
        im = plot_enviroment(environment,rod,s)
        plot = plt.imshow(im)
        imgs.append([plot])

    ani = animation.ArtistAnimation(fig, imgs, interval=50, blit=True)

    ani.save('rod_solve.mp4')

    plt.show()

        
    
