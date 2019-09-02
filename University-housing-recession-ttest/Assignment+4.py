import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

#load housing data--Median home sale price data
homes = pd.read_csv('City_Zhvi_AllHomes.csv')#.set_index(['State', 'RegionName'])
homes['State'] = homes['State'].map(states)
homes = homes.set_index(['State', 'RegionName'])

#Load GDP data
GDP = pd.read_excel('gdplev.xls', header=5, skiprows=2, usecols=[4,6], names=['Quarter', 'GDP']).set_index('Quarter')
GDP = GDP[GDP.index>='2000']

#Load university town data
with open('university_towns.txt', 'r') as f:
    uni_towns = f.read().splitlines()
towns=[]

def clean_name(name):
    '''
    Removes text in parentheses from end of city names
    '''
    new_name = ''
    if ' (' in name:
        for letter in name:
            if letter != '(':
                new_name += letter
            else:
                break
        return new_name[:-1]
    else:
        return name
#Divide university town data into columns with state and city
#also removes '[edit]' from state name
for entry in uni_towns:
    if '[edit]' in entry:
        state = entry[:-6]
    else:
        towns.append([state, entry])

#cleans uni town names
for town in towns:
    town[1] = clean_name(town[1])
        
#converts uni towns to pandas DataFrame    
uni_towns = pd.DataFrame(towns, columns=['State', 'RegionName'])

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    return uni_towns
get_list_of_university_towns()

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    decline_count = 0
    for i in range(1,len(GDP['GDP'])):
        if GDP['GDP'][i] < GDP['GDP'][i-1]:
            decline_count += 1
            if decline_count == 2:
                return GDP['GDP'].index[i-1]
        else:
            decline_count = 0

    return "not found"
get_recession_start()

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    decline_count = 0
    increase_count = 0
    for i in range(1,len(GDP['GDP'])):
        if GDP['GDP'][i] < GDP['GDP'][i-1]:
            decline_count += 1
            if decline_count == 2:
                for j in range(i,len(GDP['GDP'])):
                    if GDP['GDP'][j] > GDP['GDP'][j-1]:
                        increase_count += 1
                        if increase_count == 2:
                            return GDP['GDP'].index[j]
                    else:
                        increase_count = 0
                
        else:
            decline_count = 0

    return "not found"       
get_recession_end()

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    values = []
    for i in range(GDP.index.get_loc(get_recession_start()), GDP.index.get_loc(get_recession_end())):
        values.append(GDP['GDP'].iloc[i])
    min_value = min(values)
    
    
    return GDP[GDP['GDP'] == min_value].index[0]
get_recession_bottom()

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    
    homes_quarters = homes[[]]
    for year in range(2000, 2017):
        homes_quarters[str(year) + 'q1'] = (homes[str(year) + '-01'] + homes[str(year) + '-02'] + homes[str(year) + '-03'])/3.
        homes_quarters[str(year) + 'q2'] = (homes[str(year) + '-04'] + homes[str(year) + '-05'] + homes[str(year) + '-06'])/3.
        if year < 2016:
            homes_quarters[str(year) + 'q3'] = (homes[str(year) + '-07'] + homes[str(year) + '-08'] + homes[str(year) + '-09'])/3.
            homes_quarters[str(year) + 'q4'] = (homes[str(year) + '-10'] + homes[str(year) + '-11'] + homes[str(year) + '-12'])/3.
        else:
            homes_quarters[str(year) + 'q3'] = (homes[str(year) + '-07'] + homes[str(year) + '-08']) / 2.
    return homes_quarters
homes_fixed = convert_housing_data_to_quarters()

def get_quarter_before_recession():
    '''Returns the year and quarter before the start of recession start time as a 
    string value in a format such as 2005q3'''
    decline_count = 0
    for i in range(1,len(GDP['GDP'])):
        if GDP['GDP'][i] < GDP['GDP'][i-1]:
            decline_count += 1
            if decline_count == 2:
                return GDP['GDP'].index[i-1]
        else:
            decline_count = 0

    return "not found"

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    #price_ratio=quarter_before_recession/recession_bottom
    recession_start = get_recession_start()
    recess_bottom = get_recession_bottom()
    #creates a new copy of homes_fixed to work with
    homes1 = homes_fixed#.head(20)
    #creates a new copy of uni_towns to work with
    uni_towns1 = uni_towns
    #flag for uni_towns
    homes1['is_uni_town'] = 0
    #sets index for uni_towns1 to be same as index for homes1
    uni_towns1 = uni_towns1.set_index(['State', 'RegionName'])
    #subset of homes1 that are uni_towns
    merged = homes1.merge(uni_towns1,how='inner', left_index=True, right_index=True)#.loc[('Michigan', 'Ann Arbor')]
    
    #
    homes2 = homes1.reset_index()
    homes_states = homes2['State'].tolist()
    homes_town = homes2['RegionName'].tolist()
    uni_towns2 = uni_towns1.reset_index()

    
    #creates a flag for university towns
    uni_states = uni_towns2['State'].tolist()
    uni_town = uni_towns2['RegionName'].tolist()
    flags = []
    count = 0
    match = 0
    for i in range(len(homes2)):
        match = 0
        for j in range(len(uni_towns2)):
            if homes_states[i] == uni_states[j] and homes_town[i] == uni_town[j]:
                count += 1
                match = 1
                #print('found')
        if match == 1:
            flags.append(1)
            #print('found')
        else:
            flags.append(0)
            
    homes2['is_uni_town'] = flags
    homes2['price_ratio'] = homes2[get_quarter_before_recession()] / homes2[get_recession_bottom()]
    final_uni_towns = homes2[homes2['is_uni_town'] == 1]
    final_uni_towns = final_uni_towns.dropna(subset = ['price_ratio'])
    final_non_uni_towns = homes2[homes2['is_uni_town'] == 0]
    final_non_uni_towns = final_non_uni_towns.dropna(subset = ['price_ratio'])    
    t_test = ttest_ind(final_uni_towns['price_ratio'], final_non_uni_towns['price_ratio'])
    
    different = (t_test[1] < .01)
    better = 'university town' if t_test[0]<=0 else 'non-university town'
    p = t_test[1]
    
    return (different, p, better)

print(run_ttest())


