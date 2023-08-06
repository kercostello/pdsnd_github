import time
import pandas as pd
import numpy as np
from datetime import datetime


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
userinputoptions = {'city': ['chicago', 'new york city','washington'],
               'month': ['all','january', 'february', 'march', 'april', 'may', 'june'],
               'day': ['all','monday', 'tuesday','wednesday','thursday','friday','saturday','sunday']}

def validate_filters(userinputoption, input_Q):
     """
    Checks for valid user input.

    Args:
        (str) userinputoption - name of input type (city, month, or day)
        (str) input_Q - question to prompt user with to get input
    
    Returns:
         (str) curr_input - validated user input
     """
     curr_list = userinputoptions[userinputoption]
     while True:
         curr_input = input(input_Q + ': \n')        
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
 
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek+1
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = userinputoptions['month'].index(month)
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]
    
    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        day = userinputoptions['day'].index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
    Args:
        (Pandas DataFrame) df - bikeshare data file
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if (df['month'].unique().size == 1):
        selected_month = df.iloc[0]['month']
        print('Only one month selected: \n', userinputoptions['month'][selected_month].title())
    else:
        common_month = df['month'].mode()[0]
        print('Most common month: \n', userinputoptions['month'][common_month].title())
    
    # display the most common day of week
    if (df['day_of_week'].unique().size == 1):
        selected_day = df.iloc[0]['day_of_week']
        print('Only one day of the week selected: \n', userinputoptions['day'][selected_day].title())
    else:
        common_day = df['day_of_week'].mode()[0]
        print('Most common day of week: \n', userinputoptions['day'][common_day].title())
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_starthour = df['hour'].mode()[0]
    
    d = datetime.strptime(str(common_starthour), "%H")
    print('Most common start hour: \n', d.strftime("%l %p"))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    
    Args:
        (Pandas DataFrame) df - bikeshare data file
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_startstn = df['Start Station'].mode()[0]
    print('Most common start station: \n', common_startstn)

    # display most commonly used end station
    common_endstn = df['End Station'].mode()[0]
    print('Most common end station: \n', common_endstn)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['trip'].mode()[0]
    print('Most common trip: \n', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    
    Args:
        (Pandas DataFrame) df - bikeshare data file
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time (seconds): \n', total_travel_time)

    # display mean travel time
    total_travel_time = df['Trip Duration'].mean()
    print('Mean travel time (seconds): \n', total_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users.
    
    Args:
        (Pandas DataFrame) df - bikeshare data file
        (str) city - name of the city to analyze
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Types: \n', df['User Type'].value_counts().to_string(header=False))
    
    if 'Gender' in df.columns:
        # Display counts of gender
        print('Gender: \n', df['Gender'].value_counts().to_string(header=False))
    else:
        print("This city does not have data on gender.")
    
    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        print('Earliest birth year: \n', int(df['Birth Year'].min()))
        print('Most recent birth year: \n',int(df['Birth Year'].max()))
        print('Most common birth year: \n',int(df['Birth Year'].mode()[0]))
    else:
        print("This city does not have data on birth year.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw(df):
    """Displays raw bikeshare data on user request.
    
    Args:
        (Pandas DataFrame) df - bikeshare data file
    """

    seeraw = input('\nWould you like to see five lines of raw data? Enter yes or no.\n')
    i=0
    while seeraw == 'yes' and i<df.shape[0]:
        print(df[i:min((i+5),df.shape[0])])
        i +=5
        if i > df.shape[0]:
            seeraw = 'no'
            print('You reached the end of the raw data.\n')
        else:
            seeraw = input('\nWould you like to see five more lines of raw data? Enter yes or no.\n')
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        show_raw(df)

        restart = input('\nWould you like to explore more? Enter yes or no.\n')
        if restart.lower() not in ['yes','y','yeah','yea','sure']:
            break


if __name__ == "__main__":
	main()
