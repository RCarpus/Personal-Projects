import matplotlib.pyplot as plt
import numpy as np
import matplotlib.widgets as widgets
import matplotlib.gridspec as gridspec
from math import trunc

#Set initial values for distributions
normal_mean  = 0
normal_std   = 1
gamma_shape  = 1 #must be greater than 0
gamma_scale  = 1 #must be greater than 0
exp_scale    = 1
exp_offset   = 0
uniform_low  = -5
uniform_high = 5
n = 1000

#initial sampling
normal_sample  = np.random.normal(normal_mean, normal_std, n)
gamma_sample   = np.random.gamma(gamma_shape, gamma_scale, n)
exp_sample     = np.random.exponential(exp_scale, n) + exp_offset
uniform_sample = np.random.uniform(uniform_low,uniform_high, n)

animation_frames = 100
data_points_per_frame = int(n/animation_frames)

#Create GridSpec
gs = gridspec.GridSpec(6, 8)
n1, n2, n3, n4 = 0,3,0,3
g1, g2, g3, g4 = 0,3,4,7
e1, e2, e3, e4 = 3,6,0,3
u1, u2, u3, u4 = 3,6,4,7

#set axes
normal_axis  = [-10,10,0,1]
gamma_axis   = [0, 20, 0, 1]
exp_axis     = [-10,10,0,1]
uniform_axis = [-10,10,0,1]

#set bins
normal_bins  = np.arange(-10, 10, 1)
gamma_bins   = np.arange(0, 20, 0.5)
exp_bins     = np.arange(-10, 10, 1)
uniform_bins = np.arange(-10, 10, 1)

#set chart titles
normal_title  = 'Normal Distribution'
gamma_title   = 'Gamma Distribution'
exp_title     = 'Exponential Distribution'
uniform_title = 'Uniform Distribution'
xlabel        = 'Frequency'
ylabel        = 'Value'

def plot(loc_1, loc_2, loc_3, loc_4, bins, sample, axis, title, ylabel, xlabel):
    '''
    Creates plot for a distribution specified by input arguments
    '''   
    plt.subplot(gs[loc_1:loc_2,loc_3:loc_4])
    plt.cla()
    plt.hist(sample, bins=bins, density=True)
    plt.axis(axis)
    plt.gca().set_title(title)
    plt.gca().set_ylabel(ylabel)
    plt.gca().set_xlabel(xlabel)

def normal_mean_slide(scooby):
    global normal_mean
    normal_mean = normal_mean_slider.val
    normal_sample = np.random.normal(normal_mean, normal_std, n)
    plot(n1, n2, n3, n4, normal_bins, normal_sample, normal_axis, normal_title, ylabel, xlabel)
    plt.draw()

def normal_std_slide(doo):
    global normal_std
    normal_std = normal_std_slider.val
    normal_sample = np.random.normal(normal_mean, normal_std, n)
    plot(n1, n2, n3, n4, normal_bins, normal_sample, normal_axis, normal_title, ylabel, xlabel)
    plt.draw()

def gamma_shape_slide(zoom):
    global gamma_shape
    gamma_shape = gamma_shape_slider.val
    gamma_sample = np.random.gamma(gamma_shape, gamma_scale, n)
    plot(g1, g2, g3, g4, gamma_bins, gamma_sample, gamma_axis, gamma_title, ylabel, xlabel)
    plt.draw()

def gamma_scale_slide(bop):
    global gamma_scale
    gamma_scale = gamma_scale_slider.val
    gamma_sample = np.random.gamma(gamma_shape, gamma_scale, n)
    plot(g1, g2, g3, g4, gamma_bins, gamma_sample, gamma_axis, gamma_title, ylabel, xlabel)
    plt.draw()

def exp_scale_slide(bop):
    global exp_scale
    exp_scale = exp_scale_slider.val
    exp_sample = np.random.exponential(exp_scale, n) + exp_offset
    plot(e1, e2, e3, e4, exp_bins, exp_sample, exp_axis, exp_title, ylabel, xlabel)
    plt.draw()

def exp_offset_slide(bop):
    global exp_offset
    exp_offset = exp_offset_slider.val
    exp_sample = np.random.exponential(exp_scale, n) + exp_offset
    plot(e1, e2, e3, e4, exp_bins, exp_sample, exp_axis, exp_title, ylabel, xlabel)
    plt.draw()

def uniform_low_slide(scoop):
    global uniform_low
    uniform_low = uniform_low_slider.val
    uniform_sample = np.random.uniform(uniform_low,uniform_high, n)
    plot(u1, u2, u3, u4, uniform_bins, uniform_sample, uniform_axis, uniform_title, ylabel, xlabel)
    plt.draw()

def uniform_high_slide(scoop):
    global uniform_high
    uniform_high = uniform_high_slider.val
    uniform_sample = np.random.uniform(uniform_low,uniform_high, n)
    plot(u1, u2, u3, u4, uniform_bins, uniform_sample, uniform_axis, uniform_title, ylabel, xlabel)
    plt.draw()

def n_slide(Shabadoo):
    global n
    n = trunc(n_slider.val)

#Iniital plots    
fig = plt.gcf()
plt.cla()
plt.subplots_adjust(hspace=3, wspace=3)
plot(n1, n2, n3, n4, normal_bins, normal_sample, normal_axis, normal_title, ylabel, xlabel)
plot(g1, g2, g3, g4, gamma_bins, gamma_sample, gamma_axis, gamma_title, ylabel, xlabel)
plot(e1, e2, e3, e4, exp_bins, exp_sample, exp_axis, exp_title, ylabel, xlabel)
plot(u1, u2, u3, u4, uniform_bins, uniform_sample, uniform_axis, uniform_title, ylabel, xlabel)

#Build widgets
#normal mean widget
plt.subplot(gs[0,3])
normal_mean_slider = widgets.Slider(plt.gca(),'Normal mean',-5,5,0)
normal_mean_slider.on_changed(normal_mean_slide)
#normal std widget
plt.subplot(gs[1,3])
normal_std_slider = widgets.Slider(plt.gca(),'Normal std',0,5,1)
normal_std_slider.on_changed(normal_std_slide)

#gamma shape widget
plt.subplot(gs[0,7])
gamma_shape_slider = widgets.Slider(plt.gca(),'Gamma shape',0,5,1)
gamma_shape_slider.on_changed(gamma_shape_slide)

#gamma scale widget
plt.subplot(gs[1,7])
gamma_scale_slider = widgets.Slider(plt.gca(),'Gamma scale',0,5,1)
gamma_scale_slider.on_changed(gamma_scale_slide)

#exponential scale widget
plt.subplot(gs[3,3])
exp_scale_slider = widgets.Slider(plt.gca(),'Exponential scale',0,5,1)
exp_scale_slider.on_changed(exp_scale_slide)

#exponential offset widget
plt.subplot(gs[4,3])
exp_offset_slider = widgets.Slider(plt.gca(),'Exponential offset',-10,10,0)
exp_offset_slider.on_changed(exp_offset_slide)

#uniform low widget
plt.subplot(gs[3,7])
uniform_low_slider = widgets.Slider(plt.gca(),'Uniform low',-10,0,-5)
uniform_low_slider.on_changed(uniform_low_slide)

#uniform high widget
plt.subplot(gs[4,7])
uniform_high_slider = widgets.Slider(plt.gca(),'Uniform high',0,10,5)
uniform_high_slider.on_changed(uniform_high_slide)

#n slider
plt.subplot(gs[2,3])
n_slider = widgets.Slider(plt.gca(),'Sample size, n', 10,10000,1000)
n_slider.on_changed(n_slide)

plt.show()
