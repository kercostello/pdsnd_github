import time
import pandas as pd
import numpy as np
from datetime import datetime


city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
input_options = {'city': ['chicago', 'new york city','washington'],
               'month': ['all','january', 'february', 'march', 'april', 'may', 'june'],
               'day': ['all','monday', 'tuesday','wednesday','thursday','friday','saturday','sunday']}

def validate_filters(input_type, question):
     """
    Checks for valid user input.

    Args:
        (str) input_type - name of input type (city, month, or day)
        (str) question - question to prompt user with to get input
    
    Returns:
         (str) curr_input - validated user input
     """
     curr_list = input_options[input_type]
     while True:
         curr_input = input(question + ': \n')        
         try:
             if curr_input.lower() not in curr_list:
                 raise ValueError("Input is not in the list.")
             else:
                 break
         except (ValueError, TypeError):
             print("Invalid input, please try again.")

     return curr_input.lower()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = validate_filters('city','Which city would you like to explore? Enter chicago, new york city, or washington')

    # get user input for month (all, january, february, ... , june)
    month = validate_filters('month','Which month would you like to explore? Enter all, january, february, march, april, may, or june')
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = validate_filters('day','Which day of the week would you like to explore? Enter all, monday, tuesday, wednesday, thursday, friday, saturday, or sunday')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        bikeshare_data - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    bikeshare_data = pd.read_csv(city_data[city])
    # convert the Start Time column to datetime
    bikeshare_data['Start Time'] = pd.to_datetime(bikeshare_data['Start Time'])
 
    # extract month and day of week from Start Time to create new columns
    bikeshare_data['month'] = bikeshare_data['Start Time'].dt.month
    bikeshare_data['day_of_week'] = bikeshare_data['Start Time'].dt.dayofweek+1
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = input_options['month'].index(month)
    
        # filter by month to create the new dataframe
        bikeshare_data = bikeshare_data[bikeshare_data['month']==month]
    
    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        day = input_options['day'].index(day)
        # filter by day of week to create the new dataframe
        bikeshare_data = bikeshare_data[bikeshare_data['day_of_week']==day]

    return bikeshare_data


def time_stats(bikeshare_data):
    """Displays statistics on the most frequent times of travel.
    
    Args:
        (Pandas DataFrame) bikeshare_data - bikeshare data file
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if (bikeshare_data['month'].unique().size == 1):
        selected_month = bikeshare_data.iloc[0]['month']
        print('Only one month selected: \n', input_options['month'][selected_month].title())
    else:
        common_month = bikeshare_data['month'].mode()[0]
        print('Most common month: \n', input_options['month'][common_month].title())
    
    # display the most common day of week
    if (bikeshare_data['day_of_week'].unique().size == 1):
        selected_day = bikeshare_data.iloc[0]['day_of_week']
        print('Only one day of the week selected: \n', input_options['day'][selected_day].title())
    else:
        common_day = bikeshare_data['day_of_week'].mode()[0]
        print('Most common day of week: \n', input_options['day'][common_day].title())
    
    # display the most common start hour
    bikeshare_data['hour'] = bikeshare_data['Start Time'].dt.hour
    common_start_hour = bikeshare_data['hour'].mode()[0]
    
    d = datetime.strptime(str(common_start_hour), "%H")
    print('Most common start hour: \n', d.strftime("%l %p"))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(bikeshare_data):
    """Displays statistics on the most popular stations and trip.
    
    Args:
        (Pandas DataFrame) bikeshare_data - bikeshare data file
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = bikeshare_data['Start Station'].mode()[0]
    print('Most common start station: \n', common_start_station)

    # display most commonly used end station
    common_end_station = bikeshare_data['End Station'].mode()[0]
    print('Most common end station: \n', common_end_station)

    # display most frequent combination of start station and end station trip
    bikeshare_data['trip'] = bikeshare_data['Start Station'] + " to " + bikeshare_data['End Station']
    common_trip = bikeshare_data['trip'].mode()[0]
    print('Most common trip: \n', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(bikeshare_data):
    """Displays statistics on the total and average trip duration.
    
    Args:
        (Pandas DataFrame) bikeshare_data - bikeshare data file
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = bikeshare_data['Trip Duration'].sum()
    print('Total travel time (seconds): \n', total_travel_time)

    # display mean travel time
    total_travel_time = bikeshare_data['Trip Duration'].mean()
    print('Mean travel time (seconds): \n', total_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(bikeshare_data):
    """Displays statistics on bikeshare users.
    
    Args:
        (Pandas DataFrame) bikeshare_data - bikeshare data file
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Types: \n', bikeshare_data['User Type'].value_counts().to_string(header=False))
    
    if 'Gender' in bikeshare_data.columns:
        # Display counts of gender
        print('Gender: \n', bikeshare_data['Gender'].value_counts().to_string(header=False))
    else:
        print("This city does not have data on gender.")
    
    if 'Birth Year' in bikeshare_data.columns:
        # Display earliest, most recent, and most common year of birth
        print('Earliest birth year: \n', int(bikeshare_data['Birth Year'].min()))
        print('Most recent birth year: \n',int(bikeshare_data['Birth Year'].max()))
        print('Most common birth year: \n',int(bikeshare_data['Birth Year'].mode()[0]))
    else:
        print("This city does not have data on birth year.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw(bikeshare_data):
    """Displays raw bikeshare data on user request.
    
    Args:
        (Pandas DataFrame) bikeshare_data - bikeshare data file
    """

    see_raw = input('\nWould you like to see five lines of raw data? Enter yes or no.\n')
    i=0
    while see_raw == 'yes' and i<bikeshare_data.shape[0]:
        print(bikeshare_data[i:min((i+5),bikeshare_data.shape[0])])
        i +=5
        if i > bikeshare_data.shape[0]:
            see_raw = 'no'
            print('You reached the end of the raw data.\n')
        else:
            see_raw = input('\nWould you like to see five more lines of raw data? Enter yes or no.\n')
        

def get_stats(bikeshare_data):
    time_stats(bikeshare_data)
    station_stats(bikeshare_data)
    trip_duration_stats(bikeshare_data)
    user_stats(bikeshare_data)     


def main():
    while True:
        city, month, day = get_filters()
        bikeshare_data = load_data(city, month, day)

        get_stats(bikeshare_data)

        show_raw(bikeshare_data)

        restart = input('\nWould you like to explore more? Enter yes or no.\n')
        if restart.lower() not in ['yes','y','yeah','yea','sure']:
            break


if __name__ == "__main__":
	main()
