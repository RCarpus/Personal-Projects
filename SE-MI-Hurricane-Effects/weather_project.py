import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#import data sets
weather = pd.read_excel('temperature_data_detroit_metro_airport_2018.xlsx', header=None,
                        names=['date','max_temp','avg_temp','min_temp',
                               'max_dew_point','avg_dew_point','min_dew_point',
                               'max_humidity','min_humidity',
                               'max_wind_speed','min_wind_speed',
                               'max_pressure','min_pressure',
                               'precipitation'],
                        usecols='A:H,J,K,M,N,P,R', skiprows=[0])

hurricanes = pd.read_excel('hurricane_data.xlsx', header=0, usecols='A:D,H')

month_key = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'June',
             7:'July', 8:'Aug', 9:'Sept', 10:'Oct', 11:'Nov', 12:'Dec'}

def fix_weather_dates(df):
    '''
    fixes format for dates to mm-dd. The .xlsx file has 1 row each month with the month name and restates the header names,
    and each row for the rest of the month is just an integer. This removes the row with the month name
    and adds the month number to the date. Last, it sets the index to the newly formatted date.
    '''
    old_dates = df['date'].to_list()
    new_dates = []
    current_month = 0
    for date in old_dates:
        if str(date).isalpha():
            current_month += 1
        elif len(str(date))==2:
            new_dates.append('{}-{}'.format(current_month,date))
        else:
            new_dates.append('{}-0{}'.format(current_month,date))

    df = df[df.max_temp.values != 'Max']
    df['date'] = new_dates
    df.reset_index(inplace=True)
    df.set_index('date', inplace=True)
    return df

#cleans weather df
weather = fix_weather_dates(weather)

def fix_hurricane_dates(df):
    '''
    Splits date range into separate start and end dates, and changes format
    from mm/dd to mm-dd
    '''
    joined_dates = df['Dates'].tolist()
    start_dates = []
    end_dates   = []
    for date in joined_dates:
        split = date.split('-')
        start_dates.append(split[0].replace('/','-'))
        end_dates.append(split[1].replace('/','-'))
    df['start_date'] = start_dates
    df['end_date']   = end_dates
    df.set_index('start_date', inplace=True)
    return df
#clean hurricanes df
hurricanes = fix_hurricane_dates(hurricanes)
#extract 2018 data from hurricanes
hurricanes_2018 = hurricanes[hurricanes['Year']==2018]

def create_index_day_dict(days):
    '''
    creates dictionary mapping mm-dd to an x axis value
    '''
    values = [x for x in range(365)]
    keys = days.tolist()
    return dict(zip(keys, values))
def index_list_from_dates(date_dict,dates):
    '''
    converts list of dates to list of date indexes
    '''
    date_list = []
    for date in dates:
        date_list.append(date_dict[date])
    return date_list

#Creates day to index dict
day_to_index = create_index_day_dict(weather.index)
#inner joins weather and hurricanes on mm-dd
inner_joined = weather.merge(hurricanes_2018, how='inner', left_index=True, right_index=True)
inner_joined.sort_values(by='index', inplace=True)
#creates a column in hurricanes_2018 for length of storm, to be used as width in bar chart
start_date_index = index_list_from_dates(day_to_index, hurricanes_2018.index.tolist())
end_date_index    = index_list_from_dates(day_to_index, hurricanes_2018['end_date'].tolist())
hurricanes_2018['duration'] = np.array(end_date_index) - np.array(start_date_index)

def plot_double_axis():
    y_range = 350
    plot_start_index = day_to_index['5-01']
    plot_end_index = day_to_index['12-01']
    #Top plot
    fig = plt.gcf()
    '''plot wind speed'''
    plt.subplot(2,1,2)
    #Lists contain index and label names for x-axis
    x_tick_index = [0,31,59,90,120,151,181,212,243,273,304,334] #Every month
    #x_tick_index = [0,90,181,273] #Every quarter
    x_tick_name = ['Jan 1', 'Feb 1', 'Mar 1', 'Apr 1', 'May 1', 'June 1', 'July 1',
                   'Aug 1', 'Sept 1', 'Oct 1', 'Nov 1', 'Dec 1']
    plt.xticks([],[])
    # remove the frame of the chart
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    #removes y axis
    plt.yticks([],[])
    plt.ylim(y_range,0)
    plt.bar([x for x in range(plot_start_index,plot_end_index)],weather['max_wind_speed'][plot_start_index:plot_end_index],
            color='black', width=1, align='edge', label='max wind speed, SE MI')
    plt.bar(index_list_from_dates(day_to_index,hurricanes_2018.index.tolist()),hurricanes_2018['Max Winds (mph)'],
            width=hurricanes_2018['duration'].tolist(), align='edge', alpha=.2, label='max wind speed, hurricanes')
    '''plot precipitation'''
    plt.subplot(2,1,1)
    plt.xticks(x_tick_index,x_tick_name, rotation=45, position=(0,-.1))
    #plt.xticks([],[])
    # remove the frame of the chart
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    #removes y axis
    plt.yticks([],[])
    plt.ylim(0,y_range)
    plt.bar([x for x in range(plot_start_index,plot_end_index)],weather['precipitation'][plot_start_index:plot_end_index]*100,color='black', width=1, align='edge')
    plt.bar(index_list_from_dates(day_to_index,hurricanes_2018.index.tolist()),hurricanes_2018['Max Winds (mph)'],
            width=hurricanes_2018['duration'].tolist(), align='edge', alpha=.2)
    plt.title('Precipitation (Top) and Maximum Wind Speed (Bottom) in Southeast Michigan\n and Maximum Wind Speed of North Atlantic Tropical Storms (Shaded Blue), 2018')    
    plt.subplots_adjust(wspace=0, hspace=0)
    
    plt.show()

plot_double_axis()
