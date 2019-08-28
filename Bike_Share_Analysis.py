
# coding: utf-8

# # 2016 US Bike Share Activity Snapshot
# 
# ## Table of Contents
# - [Introduction](#intro)
# - [Posing Questions](#pose_questions)
# - [Data Collection and Wrangling](#wrangling)
#   - [Condensing the Trip Data](#condensing)
# - [Exploratory Data Analysis](#eda)
#   - [Statistics](#statistics)
#   - [Visualizations](#visualizations)
# - [Performing Your Own Analysis](#eda_continued)
# - [Conclusions](#conclusions)
# 
# <a id='intro'></a>
# ## Introduction
# 
# > **Tip**: Quoted sections like this will provide helpful instructions on how to navigate and use a Jupyter notebook.
# 
# Over the past decade, bicycle-sharing systems have been growing in number and popularity in cities across the world. Bicycle-sharing systems allow users to rent bicycles for short trips, typically 30 minutes or less. Thanks to the rise in information technologies, it is easy for a user of the system to access a dock within the system to unlock or return bicycles. These technologies also provide a wealth of data that can be used to explore how these bike-sharing systems are used.
# 
# In this project, you will perform an exploratory analysis on data provided by [Motivate](https://www.motivateco.com/), a bike-share system provider for many major cities in the United States. You will compare the system usage between three large cities: New York City, Chicago, and Washington, DC. You will also see if there are any differences within each system for those users that are registered, regular users and those users that are short-term, casual users.

# <a id='pose_questions'></a>
# ## Posing Questions
# 
# Before looking at the bike sharing data, you should start by asking questions you might want to understand about the bike share data. Consider, for example, if you were working for Motivate. What kinds of information would you want to know about in order to make smarter business decisions? If you were a user of the bike-share service, what factors might influence how you would want to use the service?
# 
# **Question 1**: Write at least two questions related to bike sharing that you think could be answered by data.
# 
# **Answer**: **Q-1**: How many bikes used by particular users in the city?
# <br>
# **Q-2**: Duration of bikes used by particular user_types?
# 
# > **Tip**: If you double click on this cell, you will see the text change so that all of the formatting is removed. This allows you to edit this block of text. This block of text is written using [Markdown](http://daringfireball.net/projects/markdown/syntax), which is a way to format text using headers, links, italics, and many other options using a plain-text syntax. You will also use Markdown later in the Nanodegree program. Use **Shift** + **Enter** or **Shift** + **Return** to run the cell and show its rendered form.

# <a id='wrangling'></a>
# ## Data Collection and Wrangling
# 
# Now it's time to collect and explore our data. In this project, we will focus on the record of individual trips taken in 2016 from our selected cities: New York City, Chicago, and Washington, DC. Each of these cities has a page where we can freely download the trip data.:
# 
# - New York City (Citi Bike): [Link](https://www.citibikenyc.com/system-data)
# - Chicago (Divvy): [Link](https://www.divvybikes.com/system-data)
# - Washington, DC (Capital Bikeshare): [Link](https://www.capitalbikeshare.com/system-data)
# 
# If you visit these pages, you will notice that each city has a different way of delivering its data. Chicago updates with new data twice a year, Washington DC is quarterly, and New York City is monthly. **However, you do not need to download the data yourself.** The data has already been collected for you in the `/data/` folder of the project files. While the original data for 2016 is spread among multiple files for each city, the files in the `/data/` folder collect all of the trip data for the year into one file per city. Some data wrangling of inconsistencies in timestamp format within each city has already been performed for you. In addition, a random 2% sample of the original data is taken to make the exploration more manageable. 
# 
# **Question 2**: However, there is still a lot of data for us to investigate, so it's a good idea to start off by looking at one entry from each of the cities we're going to analyze. Run the first code cell below to load some packages and functions that you'll be using in your analysis. Then, complete the second code cell to print out the first trip recorded from each of the cities (the second line of each data file).
# 
# > **Tip**: You can run a code cell like you formatted Markdown cells above by clicking on the cell and using the keyboard shortcut **Shift** + **Enter** or **Shift** + **Return**. Alternatively, a code cell can be executed using the **Play** button in the toolbar after selecting it. While the cell is running, you will see an asterisk in the message to the left of the cell, i.e. `In [*]:`. The asterisk will change into a number to show that execution has completed, e.g. `In [1]`. If there is output, it will show up as `Out [1]:`, with an appropriate number to match the "In" number.

# In[35]:


## import all necessary packages and functions.
import csv # read and write csv files
from datetime import datetime # operations to parse dates
from pprint import pprint # use to print data structures like dictionaries in
                          # a nicer way than the base print function.


# In[36]:


def print_first_point(filename):
    """
    This function prints and returns the first data point (second row) from
    a csv file that includes a header row.
    """
    # print city name for reference
    city = filename.split('-')[0].split('/')[-1]
    print('\nCity: {}'.format(city))
    
    with open(filename, 'r') as f_in:
        ## TODO: Use the csv library to set up a DictReader object. ##
        ## see https://docs.python.org/3/library/csv.html           ##
        trip_reader = csv.DictReader(f_in)
        
        ## TODO: Use a function on the DictReader object to read the     ##
        ## first trip from the data file and store it in a variable.     ##
        ## see https://docs.python.org/3/library/csv.html#reader-objects ##
        first_trip =next(trip_reader)
        
        ## TODO: Use the pprint library to print the first trip. ##
        ## see https://docs.python.org/3/library/pprint.html     ##
        pprint(first_trip)
    # output city name and first trip for later testing
    return (city, first_trip)

# list of files for each city
data_files = ['./data/NYC-CitiBike-2016.csv',
              './data/Chicago-Divvy-2016.csv',
              './data/Washington-CapitalBikeshare-2016.csv',]

# print the first trip from each file, store in dictionary
example_trips = {}
for data_file in data_files:
    city, first_trip = print_first_point(data_file)
    example_trips[city] = first_trip


# If everything has been filled out correctly, you should see below the printout of each city name (which has been parsed from the data file name) that the first trip has been parsed in the form of a dictionary. When you set up a `DictReader` object, the first row of the data file is normally interpreted as column names. Every other row in the data file will use those column names as keys, as a dictionary is generated for each row.
# 
# This will be useful since we can refer to quantities by an easily-understandable label instead of just a numeric index. For example, if we have a trip stored in the variable `row`, then we would rather get the trip duration from `row['duration']` instead of `row[0]`.
# 
# <a id='condensing'></a>
# ### Condensing the Trip Data
# 
# It should also be observable from the above printout that each city provides different information. Even where the information is the same, the column names and formats are sometimes different. To make things as simple as possible when we get to the actual exploration, we should trim and clean the data. Cleaning the data makes sure that the data formats across the cities are consistent, while trimming focuses only on the parts of the data we are most interested in to make the exploration easier to work with.
# 
# You will generate new data files with five values of interest for each trip: trip duration, starting month, starting hour, day of the week, and user type. Each of these may require additional wrangling depending on the city:
# 
# - **Duration**: This has been given to us in seconds (New York, Chicago) or milliseconds (Washington). A more natural unit of analysis will be if all the trip durations are given in terms of minutes.
# - **Month**, **Hour**, **Day of Week**: Ridership volume is likely to change based on the season, time of day, and whether it is a weekday or weekend. Use the start time of the trip to obtain these values. The New York City data includes the seconds in their timestamps, while Washington and Chicago do not. The [`datetime`](https://docs.python.org/3/library/datetime.html) package will be very useful here to make the needed conversions.
# - **User Type**: It is possible that users who are subscribed to a bike-share system will have different patterns of use compared to users who only have temporary passes. Washington divides its users into two types: 'Registered' for users with annual, monthly, and other longer-term subscriptions, and 'Casual', for users with 24-hour, 3-day, and other short-term passes. The New York and Chicago data uses 'Subscriber' and 'Customer' for these groups, respectively. For consistency, you will convert the Washington labels to match the other two.
# 
# 
# **Question 3a**: Complete the helper functions in the code cells below to address each of the cleaning tasks described above.

# In[37]:


def duration_in_mins(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the trip duration in units of minutes.
    
    Remember that Washington is in terms of milliseconds while Chicago and NYC
    are in terms of seconds. 
    
    HINT: The csv module reads in all of the data as strings, including numeric
    values. You will need a function to convert the strings into an appropriate
    numeric type when making your transformations.
    see https://docs.python.org/3/library/functions.html
    """
    # YOUR CODE HERE
    
    if (city == 'NYC') or (city == 'Chicago'):
        duration = int(datum['tripduration']) #We want time in terms of seconds for 'NYC' and 'Chicago'
    else: 
        duration = int(datum['Duration (ms)'])/1000 #We want time in terms of milliseconds for 'Washington' and 1 ms = 1/1000 
    
    return duration/60


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': 13.9833,
         'Chicago': 15.4333,
         'Washington': 7.1231}

for city in tests:
    assert abs(duration_in_mins(example_trips[city], city) - tests[city]) < .001


# In[38]:


def time_of_trip(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the month, hour, and day of the week in
    which the trip was made.
    
    Remember that NYC includes seconds, while Washington and Chicago do not.
    
    HINT: You should use the datetime module to parse the original date
    strings into a format that is useful for extracting the desired information.
    see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    """
    from datetime import datetime
    
    # YOUR CODE HERE
    if city == 'NYC':
        start_time = datum['starttime'] #Getting starttime from NewYork Data
        
        # we are calling one of the method 'strptime' for creating datetime object and creating formatted string 
        
        t1 = datetime.strptime(start_time, '%m/%d/%Y %H:%M:%S') #Newyork includes seconds, So we used %S.
        
        #We are converting a local time to the String format we need by using strftime module
        
        day_of_week = t1.strftime('%A') #For getting full weekday name in solution
        
        return (t1.month, t1.hour, day_of_week)
    elif city == 'Chicago':
        start_time = datum['starttime']
        
        # we are calling one of the method 'strptime' for creating datetime object and creating formatted string
        
        t2 = datetime.strptime(start_time, '%m/%d/%Y %H:%M') #Here we are not including seconds  
        
        #We are converting a local time to the String format we need by using strftime module
        day_of_week = t2.strftime('%A')
        
        return (t2.month, t2.hour, day_of_week)
    else:
        starttime = datum['Start date']
        
        # we are calling one of the method 'strptime' for creating datetime object and creating formatted string
        t3 = datetime.strptime(starttime, '%m/%d/%Y %H:%M')
        
        #We are converting a local time to the String format we need by using strftime module
        
        day_of_week = t3.strftime('%A')
        return (t3.month, t3.hour, day_of_week)


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': (1, 0, 'Friday'),
         'Chicago': (3, 23, 'Thursday'),
         'Washington': (3, 22, 'Thursday')}

for city in tests:
    assert time_of_trip(example_trips[city], city) == tests[city]


# In[39]:


def type_of_user(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the type of system user that made the
    trip.
    
    Remember that Washington has different category names compared to Chicago
    and NYC. 
    """
    
    # YOUR CODE HERE
    
    if city == 'NYC' :
        
        user_type = datum['usertype']
        
    elif city == 'Chicago':
        
        user_type = datum['usertype']
        
    elif city == 'Washington':
        
        if datum['Member Type'] == 'Registered':
            
            user_type = 'Subscriber'
            
        else:
            
            user_type = 'Customer'
    
    return user_type


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': 'Customer',
         'Chicago': 'Subscriber',
         'Washington': 'Subscriber'}

for city in tests:
    assert type_of_user(example_trips[city], city) == tests[city]


# **Question 3b**: Now, use the helper functions you wrote above to create a condensed data file for each city consisting only of the data fields indicated above. In the `/examples/` folder, you will see an example datafile from the [Bay Area Bike Share](http://www.bayareabikeshare.com/open-data) before and after conversion. Make sure that your output is formatted to be consistent with the example file.

# In[40]:


def condense_data(in_file, out_file, city):
    """
    This function takes full data from the specified input file
    and writes the condensed data to a specified output file. The city
    argument determines how the input file will be parsed.
    
    HINT: See the cell below to see how the arguments are structured!
    """
    
    with open(out_file, 'w') as f_out, open(in_file, 'r') as f_in:
        # set up csv DictWriter object - writer requires column names for the
        # first row as the "fieldnames" argument
        out_colnames = ['duration', 'month', 'hour', 'day_of_week', 'user_type']        
        trip_writer = csv.DictWriter(f_out, fieldnames = out_colnames)
        trip_writer.writeheader()
        
        ## TODO: set up csv DictReader object ##
        trip_reader = csv.DictReader(f_in)

        first_trip = next(trip_reader)
        # collect data from and process each row
        for row in trip_reader:
            # set up a dictionary to hold the values for the cleaned and trimmed
            # data point
            new_point = {}

            ## TODO: use the helper functions to get the cleaned data from  ##
            ## the original data dictionaries.                              ##
            ## Note that the keys for the new_point dictionary should match ##
            ## the column names set in the DictWriter object above.         ##
            month, hour, day_of_week = time_of_trip(row, city)
            new_point[out_colnames[0]] = duration_in_mins(row, city)
            new_point[out_colnames[1]] = month
            new_point[out_colnames[2]] = hour
            new_point[out_colnames[3]] = day_of_week
            new_point[out_colnames[4]] = type_of_user(row, city)
            

            ## TODO: write the processed information to the output file.     ##
            ## see https://docs.python.org/3/library/csv.html#writer-objects ##
            trip_writer.writerow(new_point)
            


# In[41]:


# Run this cell to check your work
city_info = {'Washington': {'in_file': './data/Washington-CapitalBikeshare-2016.csv',
                            'out_file': './data/Washington-2016-Summary.csv'},
             'Chicago': {'in_file': './data/Chicago-Divvy-2016.csv',
                         'out_file': './data/Chicago-2016-Summary.csv'},
             'NYC': {'in_file': './data/NYC-CitiBike-2016.csv',
                     'out_file': './data/NYC-2016-Summary.csv'}}

for city, filenames in city_info.items():
    condense_data(filenames['in_file'], filenames['out_file'], city)
    print_first_point(filenames['out_file'])


# > **Tip**: If you save a jupyter Notebook, the output from running code blocks will also be saved. However, the state of your workspace will be reset once a new session is started. Make sure that you run all of the necessary code blocks from your previous session to reestablish variables and functions before picking up where you last left off.
# 
# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# Now that you have the data collected and wrangled, you're ready to start exploring the data. In this section you will write some code to compute descriptive statistics from the data. You will also be introduced to the `matplotlib` library to create some basic histograms of the data.
# 
# <a id='statistics'></a>
# ### Statistics
# 
# First, let's compute some basic counts. The first cell below contains a function that uses the csv module to iterate through a provided data file, returning the number of trips made by subscribers and customers. The second cell runs this function on the example Bay Area data in the `/examples/` folder. Modify the cells to answer the question below.
# 
# **Question 4a**: Which city has the highest number of trips? Which city has the highest proportion of trips made by subscribers? Which city has the highest proportion of trips made by short-term customers?
# 
# **Answer**:  <strong>i) New York</strong>  has the highest number of trips.<br> <strong>ii) New York</strong> has the highest proportion of trips made by subscribers. <br> <strong>iii) Chicago</strong> has the proportion of trips made by short-term customers.

# In[42]:


def number_of_trips(filename):
    """
    This function reads in a file with trip data and reports the number of
    trips made by subscribers, customers, and total overall.
    """
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
        
        # initialize count variables
        n_subscribers = 0
        n_customers = 0
        
        # tally up ride types
        for row in reader:
            if row['user_type'] == 'Subscriber':
                n_subscribers += 1 #Counting the no of trips made by Subscribers and Customers.
            else:
                n_customers += 1
        
        # compute total number of rides
        n_total = n_subscribers + n_customers
        
        #Calculating proportion of the Subscribers and Customers using formula proportion = (count/total)*100
        
        sub_proportion = (n_subscribers/n_total)*100  #Here we used (count of ridership of subscribers/total)*100
        
        cus_proportion = (n_customers/n_total)*100 #Here we used (count of ridership of customers/total)*100
        # return tallies as a tuple
        return(n_subscribers, n_customers, n_total, sub_proportion, cus_proportion )


# In[43]:


## Modify this and the previous cell to answer Question 4a. Remember to run ##
## the function on the cleaned data files you created from Question 3.      ##


#Using my own new files of data created with middle name 'Summary1' 
data_file = ['./data/Washington-2016-Summary1.csv', './data/Chicago-2016-Summary1.csv', './data/NYC-2016-Summary1.csv'] 
for datafiles in data_file:
    print(datafiles,": \n")
    n_subscribers, n_customers, n_total, sub_proportion, cus_proportion = number_of_trips(datafiles)
    #print(number_of_trips(datafiles))
    print("n_subscribers: ", n_subscribers)
    print("n_customers: ", n_customers)
    print("n_total: ", n_total)
    print("proportion subscribers: ", sub_proportion)
    print("proportion customers: ", cus_proportion)
    print("\n")


# > **Tip**: In order to add additional cells to a notebook, you can use the "Insert Cell Above" and "Insert Cell Below" options from the menu bar above. There is also an icon in the toolbar for adding new cells, with additional icons for moving the cells up and down the document. By default, new cells are of the code type; you can also specify the cell type (e.g. Code or Markdown) of selected cells from the Cell menu or the dropdown in the toolbar.
# 
# Now, you will write your own code to continue investigating properties of the data.
# 
# **Question 4b**: Bike-share systems are designed for riders to take short trips. Most of the time, users are allowed to take trips of 30 minutes or less with no additional charges, with overage charges made for trips of longer than that duration. What is the average trip length for each city? What proportion of rides made in each city are longer than 30 minutes?
# 
# **Answer**: The Average trip length for <strong>Chicago: </strong>16.56 .<br>The Average trip length for<strong> Washington:  </strong> is 18.93.<br>The Average trip length for<strong> NewYork:  </strong> is 15.81.<br> The proportion of riders  that are more2 than 30 minutes is <strong>7.30% for NewYork</strong>, <strong> 10.83% for Washington</strong>,<strong> 8.33%  for Chicago</strong>.

# In[44]:


## Use this and additional cells to answer Question 4b.                 ##
##                                                                      ##
## HINT: The csv module reads in all of the data as strings, including  ##
## numeric values. You will need a function to convert the strings      ##
## into an appropriate numeric type before you aggregate data.          ##
## TIP: For the Bay Area example, the average trip length is 14 minutes ##
## and 3.5% of trips are longer than 30 minutes.                        ##
## I will need a function to convert the strings into an appropriate numeric type before you aggregate data. 
def len_of_trip(filename):
    
    with open(filename, 'r') as f_in:
        
        reader = csv.DictReader(f_in)
        
        s = 0 #Users taking time less than 30 min
        t = 0 #Users taking time more than 30 min
        total = 0 #Total duration
        for row in reader:
            s+=1
            duration=float(row['duration'])
            total=total + duration
            if duration > 30:
                t += 1
        avg_length = (total/s) # calculating average trip length
        
        #Calculating proportion of total users taking time more than 30 minutes to the users taking time less than 30 minutes
        prop = (t/s)*100 
        
        return (s, t, avg_length, prop, total)


# In[45]:


data_file = ['./data/Washington-2016-Summary1.csv', './data/Chicago-2016-Summary1.csv', './data/NYC-2016-Summary1.csv']
for datafiles in data_file:
    print(datafiles,": \n")
    
    s, t, avg_length, prop, total = len_of_trip(datafiles)
    print("Average trip : ", avg_length)
    print("Total duration length: ", total)
    print("Proportion : ", prop)
    print("User taking time less than 30: ", s)
    print("User taking time more than 30: ", t)
    print("\n")


# **Question 4c**: Dig deeper into the question of trip duration based on ridership. Choose one city. Within that city, which type of user takes longer rides on average: Subscribers or Customers?
# 
# **Answer**: We have chosen <strong>NewYork city.</strong>. <br>In <strong>NewYork</strong> Customers take longer rides on an Average: 33 minutes.<br> The Average time of subscribers taking rides is 13.68 minutes.

# In[46]:


## Use this and additional cells to answer Question 4c. If you have    ##
## not done so yet, consider revising some of your previous code to    ##
## make use of functions for reusability.                              ##
##                                                                     ##
## TIP: For the Bay Area example data, you should find the average     ##
## Subscriber trip duration to be 9.5 minutes and the average Customer ##
## trip duration to be 54.6 minutes. Do the other cities have this     ##
## level of difference?                                                ##
def Duration_RiderShip(filename):
    
    with open(filename, 'r') as f_in:
        
        reader = csv.DictReader(f_in)
        
        #Here we are counting the subscribers and customers and finding there total duration of each city
        sub = 0
        cus = 0
        sub_total = 0
        cus_total = 0
        for row in reader:
            user_type = row['user_type']
            duration=float(row['duration'])
            if user_type == 'Subscriber':
                
                sub += 1
                
                sub_total += duration
            elif user_type == 'Customer':
                
                cus += 1
                
                cus_total += duration
        average_sub = sub_total / sub
        average_cus = cus_total / cus
        
        return (sub, cus, average_sub, average_cus)


# In[47]:


data_file = ['./data/Washington-2016-Summary1.csv', './data/Chicago-2016-Summary1.csv', './data/NYC-2016-Summary1.csv']
for datafiles in data_file:
    
    print(datafiles,": \n")
    sub, cus, average_sub, average_cus = Duration_RiderShip(datafiles)
    print("Subscriber: ", sub)
    print("Customer: ", cus)
    print("Average Subscriber Ride duration: ", average_sub)
    print("Average Customer Ride duraion: ", average_cus)


# In[48]:


# load library
import matplotlib.pyplot as plt

# this is a 'magic word' that allows for plots to be displayed
# inline with the notebook. If you want to know more, see:
# http://ipython.readthedocs.io/en/stable/interactive/magics.html
get_ipython().run_line_magic('matplotlib', 'inline')

# example histogram, data taken from bay area sample
data = [ 7.65,  8.92,  7.42,  5.50, 16.17,  4.20,  8.98,  9.62, 11.48, 14.33,
        19.02, 21.53,  3.90,  7.97,  2.62,  2.67,  3.08, 14.40, 12.90,  7.83,
        25.12,  8.30,  4.93, 12.43, 10.60,  6.17, 10.88,  4.78, 15.15,  3.53,
         9.43, 13.32, 11.72,  9.85,  5.22, 15.10,  3.95,  3.17,  8.78,  1.88,
         4.55, 12.68, 12.38,  9.78,  7.63,  6.45, 17.38, 11.90, 11.52,  8.63,]
plt.hist(data)
plt.title('Distribution of Trip Durations')
plt.xlabel('Duration (m)')
plt.show()


# In the above cell, we collected fifty trip times in a list, and passed this list as the first argument to the `.hist()` function. This function performs the computations and creates plotting objects for generating a histogram, but the plot is actually not rendered until the `.show()` function is executed. The `.title()` and `.xlabel()` functions provide some labeling for plot context.
# 
# You will now use these functions to create a histogram of the trip times for the city you selected in question 4c. Don't separate the Subscribers and Customers for now: just collect all of the trip times and plot them.

# In[49]:


## Use this and additional cells to collect all of the trip times as a list ##
## and then use pyplot functions to generate a histogram of trip times.     ##
import pandas as pt
import matplotlib.pyplot as plt
import numpy as py
get_ipython().run_line_magic('matplotlib', 'inline')


# In[50]:


trip_times = pt.read_csv('./data/NYC-2016-Summary1.csv') 
duration = trip_times['duration']
bins = py.arange(0,75,4) # I am using arange function from numpy and we are giving it 3parameters namely- start, end, step
plt.hist(duration, bins)
plt.title('Trip Durations of NYC')
plt.xlabel('Duration(m)')
plt.show()


# If you followed the use of the `.hist()` and `.show()` functions exactly like in the example, you're probably looking at a plot that's completely unexpected. The plot consists of one extremely tall bar on the left, maybe a very short second bar, and a whole lot of empty space in the center and right. Take a look at the duration values on the x-axis. This suggests that there are some highly infrequent outliers in the data. Instead of reprocessing the data, you will use additional parameters with the `.hist()` function to limit the range of data that is plotted. Documentation for the function can be found [[here]](https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.hist.html#matplotlib.pyplot.hist).
# 
# **Question 5**: Use the parameters of the `.hist()` function to plot the distribution of trip times for the Subscribers in your selected city. Do the same thing for only the Customers. Add limits to the plots so that only trips of duration less than 75 minutes are plotted. As a bonus, set the plots up so that bars are in five-minute wide intervals. For each group, where is the peak of each distribution? How would you describe the shape of each distribution?
# 
# **Answer**:  For subscribers group, the peak of trip durations is 5-10 minutes. For customers group, the peak of trip durations is 20-25 minutes. The shape of the distribution of trip durations for subscribers is skewed to the right. The shape of the distribution of trip durations for customers is also skewed to the right.

# In[51]:


## Use this and additional cells to answer Question 5. ##
## For Subscribers
#query function from pandas library for checking user_type and duration
sub = trip_times.query('user_type == "Subscriber"') #query function from pandas library for checking user_type
sub1 = sub.query('duration < 75')
duration = sub1['duration']
bins = py.arange(0,75,5)

plt.hist(duration, bins)
bar = bins + 5 #We want bars at 5minutes wide interval
label = ['5','10','15','20','25','30','35','40','45','50','55,''60','65','70','75']
plt.xticks(bar, label)
plt.title('Trip Durations for subscribers')
plt.xlabel('Duration (m) ')
plt.show()


# In[52]:


##For Customers
cus = trip_times.query('user_type == "Customer"')
cus1 = cus.query('duration < 75')
duration = cus1['duration']
bins = py.arange(0,75,5)

plt.hist(duration, bins)
bar = bins + 5
labels = ['5','10','15','20','25','30','35','40','45','50','55,''60','65','70','75']
plt.xticks(bar, labels)
plt.title('Trip Durations for Customers')
plt.xlabel('Duration (m) ')
plt.show()


# <a id='eda_continued'></a>
# ## Performing My Own Analysis
# 
# So far, I've performed an initial exploration into the data available. I have compared the relative volume of trips made between three U.S. cities and the ratio of trips made by Subscribers and Customers. For one of these cities, I have investigated differences between Subscribers and Customers in terms of how long a typical trip lasts.
# 
# - How does ridership differ by month or season? Which month / season has the highest ridership? Does the ratio of Subscriber trips to Customer trips change depending on the month or season?
# - Is the pattern of ridership different on the weekends versus weekdays? On what days are Subscribers most likely to use the system? What about Customers? Does the average duration of rides change depending on the day of the week?
# - During what time of day is the system used the most? Is there a difference in usage patterns for Subscribers and Customers?
# 
# 
# **Question 6**: Continue the investigation by exploring another question that could be answered by the data available. Document the question you want to explore below. Your investigation should involve at least two variables and should compare at least two groups. You should also use at least one visualization as part of your explorations.
# 
# **Answer**: <strong>I would like to proceed with my investigation in the ridership pattern between weekends and weekdays for the Chicago City</strong>.<br> 
# 
# **Part A**: Is the pattern of ridership different on the weekends versus weekdays for Subscribers and Customers?<br>
# **Answer**: Yes, the ridership pattern different for subcribers on the weekends and weekdays But For customers it is same for both weekends and weekdays.
# <br>
# 
# **Part B**: On what days are Subscribers most likely to use the system? What about Customers?<br>
# **Answer**: The Subscribers on the weekends days are more likely to use the system with average subscriber weekend duration of 13.20 and For Customers it is almost same with approx 31.0 for both weekdays and weekends.
# <br>
# 
# **Part C**: Does the average duration of rides change depending on the day of the week?<br>
# **Answer**: For the Subscribers the average duration of rides changes according to the day of week with weekend average 13.20 and weekday average 11.78. But for the Customers it is almost same for both weekdays and weekends.
# 

# In[59]:


def rider_ship(filename,city): #making a function to calculate ridership
    #Subscriber count for weekdays and duration of subscribers for weekends and weekdays
    dur_wkend_Sub=0
    sub_wkend_count=0
    dur_wkday_Sub=0
    sub_wkday_count=0
    
    #Customer count for weekdays and duration of subscribers for weekends and weekdays
    dur_wkend_Cus=0
    Cus_wkend_count=0
    dur_wkday_Cus=0
    Cus_wkday_count=0
    
    
    with open(filename, 'r') as f_in:
        tripreader = csv.DictReader(f_in)
        
        for row in tripreader:
            day = time_of_trip(row,city)[2] # For Getting day
            user = type_of_user(row,city) # For Getting user_type
            dur = duration_in_mins(row, city) # For Getting Duration
            if user == 'Subscriber':
                if (day =='Saturday') or (day == 'Sunday'):
                    dur_wkend_Sub += dur
                    sub_wkend_count += 1
                else:
                    dur_wkday_Sub += dur
                    sub_wkday_count += 1
            else:
                if (day =='Saturday') or (day == 'Sunday'):
                    dur_wkend_Cus += dur
                    Cus_wkend_count += 1
                else:
                    dur_wkday_Cus += dur
                    Cus_wkday_count += 1
        
        avg_wkend_sub = dur_wkend_Sub/sub_wkend_count #Average weekend duration of Subscribers
        avg_wkday_sub = dur_wkday_Sub/sub_wkday_count #Average weekday duration of Subscribers
        avg_wkend_Cus = dur_wkend_Cus/Cus_wkend_count #Average weekend duration of Customers
        avg_wkday_Cus = dur_wkday_Cus/Cus_wkday_count #Average weekday duration of Customers
        
        return avg_wkend_Cus, avg_wkend_sub, avg_wkday_Cus, avg_wkday_sub
    


# In[54]:


data_file = './data/Chicago-Divvy-2016.csv'
city ='Chicago' 

print(data_file,": \n")
avg_wkend_Cus, avg_wkend_sub, avg_wkday_Cus, avg_wkday_sub = rider_ship(data_file, city)
print("Average Subscriber Weekday duration: ", avg_wkday_sub )
print("Average Customer Weekday duration: ", avg_wkday_Cus )
print("Average Subscriber Weekend duration: ", avg_wkend_sub )
print("Average Customer Weekend duraion: ", avg_wkend_Cus)


# In[55]:


# Here I used legend function from matlab library for labelling in our Histogram by passing list of label to legend()
Chicago_sbar = plt.bar([1], avg_wkend_sub, color = 'r', alpha = 0.9, label = 'Subscribers' )
Chicago_cbar = plt.bar([2], avg_wkend_Cus, color = 'b', alpha = 0.9, label = 'Customers' )
plt.legend([Chicago_sbar, Chicago_cbar], ['Subsciber', 'Customer'])
plt.title('Average Trip Duration for weekends for Chicago city')
plt.ylabel('Average trip Duration')
plt.xlabel('Subscribers and Customers')
plt.show()


# In[56]:


# Here I used legend function from matlab library for labelling in our Histogram by passing list of label to legend()
Chicago_sbar = plt.bar([1], avg_wkday_sub , color = 'y', alpha = 0.9, label = 'Subscribers' )
Chicago_cbar = plt.bar([2], avg_wkday_Cus, color = 'g', alpha = 0.9, label = 'Customers' )
plt.legend([Chicago_sbar, Chicago_cbar], ['Subsciber', 'Customer'])
plt.title('Average Trip Duration for weekdays for Chicago city')
plt.ylabel('Average trip Duration')
plt.xlabel('Subscribers and Customers')
plt.show()


# In[57]:


Chicago_sbar = plt.bar([1], avg_wkday_sub , color = 'r', alpha = 0.9, label = 'Weekdays' )
Chicago_cbar = plt.bar([2], avg_wkend_sub, color = 'y', alpha = 0.9, label = 'Weekends' )
plt.legend([Chicago_sbar, Chicago_cbar], ['Weekdays', 'Weekends'])
plt.title('Average Trip Duration for weekdays and Weekends of Subscribers')
plt.ylabel('Average trip Duration')
plt.xlabel('Subscribers')
plt.show()


# In[58]:


Chicago_sbar = plt.bar([1], avg_wkday_Cus , color = 'g', alpha = 0.9, label = 'Weekdays' )
Chicago_cbar = plt.bar([2], avg_wkend_Cus, color = 'b', alpha = 0.9, label = 'Weekends' )
plt.legend([Chicago_sbar, Chicago_cbar], ['Weekdays', 'Weekends'])
plt.title('Average Trip Duration for weekdays and Weekends of Customers')
plt.ylabel('Average trip Duration')
plt.xlabel('Customers')
plt.show()


# <h1>References Which Helped me in making this Project: </h1>
# 
# <h3>List of Links: </h3>
# <ol>
#     <li> https://docs.python.org/3/library/csv.html </li>
#     <li> https://matplotlib.org/users/legend_guide.html</li>
#     <li> https://stackoverflow.com/questions </li>
#     <li> https://docs.python.org/3/library/pprint.html  </li>
#     <li> http://ipython.readthedocs.io/en/stable/interactive/magics.html </li>
#     <li> https://pandas.pydata.org/pandas-docs/stable/visualization.html </li>
#     <li> https://docs.python.org/3.7/tutorial/index.html </li>
#     <li> https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior</li>
#     </ol>

# <a id='conclusions'></a>
# ## Conclusions
# 
# Congratulations on completing the project! This is only a sampling of the data analysis process: from generating questions, wrangling the data, and to exploring the data. Normally, at this point in the data analysis process, you might want to draw conclusions about the data by performing a statistical test or fitting the data to a model for making predictions. There are also a lot of potential analyses that could be performed on the data which are not possible with only the data provided. For example, detailed location data has not been investigated. Where are the most commonly used docks? What are the most common routes? As another example, weather has potential to have a large impact on daily ridership. How much is ridership impacted when there is rain or snow? Are subscribers or customers affected more by changes in weather?
# 
# **Question 7**: Putting the bike share data aside, think of a topic or field of interest where you would like to be able to apply the techniques of data science. What would you like to be able to learn from your chosen subject?
# 
# **Answer**: I would like to apply the techniques of data science for the **Treatment of Cancer Patients**. I would like to find the best treatment methods by collecting the data and verify the **Best Treatment methods for Cancer Patients** from the data collected all over the world.
# 
# > **Tip**: If we want to share the results of our analysis with others, we aren't limited to giving them a copy of the jupyter Notebook (.ipynb) file. We can also export the Notebook output in a form that can be opened even for those without Python installed. From the **File** menu in the upper left, go to the **Download as** submenu. You can then choose a different format that can be viewed more generally, such as HTML (.html) or
# PDF (.pdf). You may need additional packages or software to perform these exports.
# 
# > If you are working on this project via the Project Notebook page in the classroom, you can also submit this project directly from the workspace. **Before you do that**, you should save an HTML copy of the completed project to the workspace by running the code cell below. If it worked correctly, the output code should be a 0, and if you click on the jupyter icon in the upper left, you should see your .html document in the workspace directory. Alternatively, you can download the .html copy of your report following the steps in the previous paragraph, then _upload_ the report to the directory (by clicking the jupyter icon).
# 
# > Either way, once you've gotten the .html report in your workspace, you can complete your submission by clicking on the "Submit Project" button to the lower-right hand side of the workspace.

# In[ ]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Bike_Share_Analysis.ipynb'])

