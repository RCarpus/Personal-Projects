
# coding: utf-8

# # Practice Assignment: Understanding Distributions Through Sampling
# 
# ** *This assignment is optional, and I encourage you to share your solutions with me and your peers in the discussion forums!* **
# 
# 
# To complete this assignment, create a code cell that:
# * Creates a number of subplots using the `pyplot subplots` or `matplotlib gridspec` functionality.
# * Creates an animation, pulling between 100 and 1000 samples from each of the random variables (`x1`, `x2`, `x3`, `x4`) for each plot and plotting this as we did in the lecture on animation.
# * **Bonus:** Go above and beyond and "wow" your classmates (and me!) by looking into matplotlib widgets and adding a widget which allows for parameterization of the distributions behind the sampling animations.
# 
# 
# Tips:
# * Before you start, think about the different ways you can create this visualization to be as interesting and effective as possible.
# * Take a look at the histograms below to get an idea of what the random variables look like, as well as their positioning with respect to one another. This is just a guide, so be creative in how you lay things out!
# * Try to keep the length of your animation reasonable (roughly between 10 and 30 seconds).

# In[1]:

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import matplotlib.widgets as widgets

#get_ipython().magic('matplotlib notebook')
# generate 4 random variables from the random, gamma, exponential, and uniform distributions
x1 = np.random.normal(0, 1, 10000)
x2 = np.random.gamma(1, 5, 10000)
x3 = np.random.exponential(3, 10000)
x4 = np.random.uniform(5,7, 10000)

# create the function that will do the plotting, where curr is the current frame
n=100 #iterations
m = 10000./n #multiplier for how many data points to add per frame
def update(curr):
    # check if animation is at the last frame, and if so, stop the animation a
    if curr == n: 
        a.event_source.stop()
    #plt.cla()
    #Normal Distribution
    plt.subplot(2,2,1)
    plt.cla()
    bins = np.arange(-4, 4, 0.5)
    plt.hist(x1[:curr*100], bins=bins)
    plt.axis([-4,4,0,2000])
    plt.gca().set_title('Sampling the Normal Distribution')
    plt.gca().set_ylabel('Frequency')
    plt.gca().set_xlabel('Value')
    plt.annotate('n = {}'.format(curr), [3,27])
    #Gamma Distribution
    plt.subplot(2,2,2)
    plt.cla()
    bins2 = np.arange(0,60,5)
    plt.hist(x2[:curr*100], bins=bins2)
    plt.axis([0,60,0,2000])
    plt.gca().set_title('Sampling the Gamma Distribution')
    plt.gca().set_ylabel('Frequency')
    plt.gca().set_xlabel('Value')
    #Exponential Distribution
    plt.subplot(2,2,3)
    plt.cla()
    bins3 = np.arange(0,10,2)
    plt.hist(x3[:curr*100], bins=bins3)
    plt.axis([0,10,0,5000])
    plt.gca().set_title('Sampling the Exponential Distribution')
    plt.gca().set_ylabel('Frequency')
    plt.gca().set_xlabel('Value')
    #Uniform Distribution
    plt.subplot(2,2,4)
    plt.cla()
    bins4 = np.arange(0,10,2)
    plt.hist(x4[:curr*100], bins=bins4)
    plt.axis([0,10,0,5000])
    plt.gca().set_title('Sampling the Uniform Distribution')
    plt.gca().set_ylabel('Frequency')
    plt.gca().set_xlabel('Value')
    
    plt.subplots_adjust(hspace=1, wspace=1)


# In[ ]:

plt.cla()
fig = plt.figure()
a = animation.FuncAnimation(fig, update, frames=100)
plt.show()


# In[2]:

#Creates normal distribution using adjustable parameters rather than hard coding
'''
def test_widget_click():
    new_mean = 20
    normal_sample = np.random.normal(new_mean, normal_std, normal_n)
    plt.subplot(1,2,1)
    plt.hist(normal_sample,20)
    plt.draw()
plt.cla()
normal_mean = 5
normal_std = 6
normal_n = 10000
normal_sample = np.random.normal(normal_mean, normal_std, normal_n)
plt.figure()
plt.subplot(1,2,1)
plt.hist(normal_sample, 20)
plt.subplot(1,2,2)
widget = widgets.Button(plt.gca(),'test widget')
widget.on_clicked(test_widget_click)

'''

