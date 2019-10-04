'''
This code has some bugs that appeared due to differences between the online
client and real life somehow. Extra ticks on the graph, and the graph doesn't
save properly. This should be easily fixed.
'''
 # An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.

# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

import matplotlib.pyplot as plt

import pandas as pd

#load csv weather data
def load_weather_data(file_name):
    '''
    Load csv weather data
    '''
    df = pd.read_csv(file_name)
    return df
#Load data frame
df = load_weather_data('weather_data.csv')
#Create new column with year removed for easier sorting
df['mm-dd'] = df['Date'].str.slice(5)
#Remove leap days
df = df[df['mm-dd'] != '02-29']
#Convert data values from tenths of degrees C to degrees C
df['Data_Value'] /= 10.
#Collect Max temps 2006 to 2015
max_temps = df.groupby('mm-dd').max()
#Collect Min temps 2006 to 2015
min_temps = df.groupby('mm-dd').min()
#Extract data from 2015
temps_2015 = df[df['Date'].str.slice(0,4) == '2015']
temps_2015 = temps_2015.set_index('mm-dd')
#Remove 2015 data from min and max temps
max_temps_through_2014 = df[df['Date'].str.slice(0,4) != '2015'].groupby('mm-dd').max()
min_temps_through_2014 = df[df['Date'].str.slice(0,4) != '2015'].groupby('mm-dd').min()
#Extract record-breaking data from 2015
#Merges with max temps
record_high_2015 = temps_2015.merge(max_temps,how='inner',left_index=True, right_index=True)
#keeps only data where 2015 is the record
record_high_2015 = record_high_2015[record_high_2015['Data_Value_x'] == record_high_2015['Data_Value_y']]
#keeps only data where 2015 beat the record
record_high_2015 = record_high_2015.merge(max_temps_through_2014, how='inner', left_index=True, right_index=True)
record_high_2015 = record_high_2015[record_high_2015['Data_Value_x'] != record_high_2015['Data_Value']]
#Same process for lows
record_low_2015 = temps_2015.merge(min_temps,how='inner',left_index=True, right_index=True)
record_low_2015 = record_low_2015[record_low_2015['Data_Value_x'] == record_low_2015['Data_Value_y']]
record_low_2015 = record_low_2015.merge(max_temps_through_2014, how='inner', left_index=True, right_index=True)
record_low_2015 = record_low_2015[record_low_2015['Data_Value_x'] != record_low_2015['Data_Value']]

'''
converts record days in 2015 from mm-dd format to graphable index
'''

def mm_dd_to_num(mm_dd):
    '''
    Creates a library to map mm-dd format to an index
    '''
    mm_dd_map = {}
    for i in range(len(mm_dd)):
        mm_dd_map.update({mm_dd[i] : i})
    return mm_dd_map

mm_dd_to_index = mm_dd_to_num(min_temps.index.tolist())
record_high_index_2015 = [mm_dd_to_index[k] for k in record_high_2015.index.tolist()]
record_low_index_2015 = [mm_dd_to_index[k] for k in record_low_2015.index.tolist()]

#Plot
#Lists contain index and label names for x-axis
x_tick_index = [0,31,59,90,120,151,181,212,243,273,304,334] #Every month
#x_tick_index = [0,90,181,273] #Every quarter
x_tick_name = ['Jan 1', 'Feb 1', 'Mar 1', 'Apr 1', 'May 1', 'June 1', 'July 1',
               'Aug 1', 'Sept 1', 'Oct 1', 'Nov 1', 'Dec 1']
#x_tick_name = ['Jan 1', 'Apr 1', 'July 1', 'Oct 1']
#sets an index for each day in the year
date_index = [x for x in range(365)]
#initialize figure
plt.figure(figsize=(14,6))
#plot data
legend_label_hot = '10-year high record broken in 2015'
legend_label_cold = '10-year low record broken in 2015'
legend_label_just_right = '10-year high and low from 2006 to 2014'
plt.plot(date_index, min_temps_through_2014['Data_Value'], 'black', label='_nolegend_') 
plt.plot(date_index, max_temps_through_2014['Data_Value'], 'black', label=legend_label_just_right) 
plt.plot(record_high_index_2015, record_high_2015['Data_Value_x'], 'ro', label=legend_label_hot)
plt.plot(record_low_index_2015, record_low_2015['Data_Value_x'], 'o', label=legend_label_cold)
#Set x ticks
plt.xticks(x_tick_index,x_tick_name, rotation=45)
#Fills between min and max lines
plt.fill_between(date_index, min_temps_through_2014['Data_Value'], max_temps_through_2014['Data_Value'], color='gray', alpha=.5)
plt.title('Minimum and Maximum Temperatures By Day of Year\nSoutheast Michigan, 2006-2015', 
          fontdict={'fontsize':20})
plt.ylabel('Degrees Celsius', fontsize=15)
# remove the frame of the chart
for spine in plt.gca().spines.values():
    spine.set_visible(False)
# remove all the ticks (both axes)
plt.tick_params(top='off', bottom='off', left='off', right='off')
# Legend
plt.legend(loc=4, frameon=False)
#Horizontal line at 0
plt.hlines(0,0,364, colors='gray')

plt.show()
plt.savefig('myfig.png')


