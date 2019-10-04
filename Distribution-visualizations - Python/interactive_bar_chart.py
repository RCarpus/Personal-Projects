# Use the following data for this assignment:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.gridspec as gridspec
import scipy.stats
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from math import trunc

description = ('This bar chart displays the mean and 95% confidence interval for 4 sets of arbitrary data\n taken from 4 different distributions.'
               +' Because this is a sample of data,\n we should not assume that the means plotted are necessarily accurate. '
               +'Use the slider\n to test a y-value. The color of each bar represents our level of certainty\n that the mean is'
               +' above (red) or below (blue) the tested value.')


np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
df = df.T

#Get mean for each column
means = df.mean()
stds = df.std()
line_value = 30000

def render_plot():
    '''
    plots bars and horizontal line
    '''
    fig = plt.gcf()
    plt.subplot(1,2,1)
    plt.cla()
    plt.axis([-.5,3.5,0,60000])
    plot_bar(0, df[1992], means.iloc[0], errors[0], '1992')
    plot_bar(1, df[1993], means.iloc[1], errors[1], '1993')
    plot_bar(2, df[1994], means.iloc[2], errors[2], '1994')
    plot_bar(3, df[1995], means.iloc[3], errors[3], '1995')
    line = plt.plot([-.5,3.5],[line_value,line_value], color='black')
    plt.errorbar(x=[0,1,2,3],y=means,yerr=errors, color='black',ls='none', capsize=10)
    plt.xticks([0,1,2,3],['1992','1993','1994','1995'])
    plt.title('A study of confidence levels on bar charts',pad=20, wrap=True)
    plt.gca().text(4,30000,description)
    # remove the frame of the chart
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.show()

def mean_slider_change(shabadoo):
    global line_value
    line_value = [mean_slider.val,mean_slider.val]
    render_plot()

def create_mean_slider():
    plt.subplot(3,3,3)
    mean_slider = Slider(plt.gca(),'value to check',1,60000,line_value)
    mean_slider.on_changed(mean_slider_change)
    return mean_slider

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)#Makes sure data is float
    n = len(a) 
    m, se = np.mean(a), scipy.stats.sem(a) #Calc mean and standard error
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1) #get intervals
    return h #just returns distance from mean

def calculate_confidence_intervals(df):
    error_1992 = mean_confidence_interval(df[1992])
    error_1993 = mean_confidence_interval(df[1993])
    error_1994 = mean_confidence_interval(df[1994])
    error_1995 = mean_confidence_interval(df[1995])
    return [error_1992, error_1993, error_1994, error_1995]

def plot_bar(i, year, sample_mean, error, label):
    plt.bar(i,sample_mean,tick_label=[label], width=.95,edgecolor='black', color=color_map(map_to_color(mean_slider.val,sample_mean,error)))
                    
def map_to_color(check_value, sample_mean, sample_error):
    error_ratio = (sample_mean - check_value) / sample_error
    return 4 + trunc(error_ratio)



#Calculate error bars
errors = calculate_confidence_intervals(df)
#color map
color_map = cm.get_cmap('seismic', 9)

mean_slider = create_mean_slider()
render_plot()

plt.show()

