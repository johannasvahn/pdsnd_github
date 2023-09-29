import time
import pandas as pd
import numpy as np
CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' } 

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
    while True:
      city = input("\nWhich city would you like to filter by? Chicago, Washington or New York City?\n").title()
      if city not in ('Chicago','Washington','New York City'):
        print("Sorry, I did not understand. Can you please try again!")
        continue
      else:
        break
    
    # get user input for month (all, january, february, ... , june)
    while True:
      month = input("\nWhich month would you like to see? January, February, March, April, May, June or 'all' if no preference?\n").title()
      if month not in ('January','February','March','April','May','June','all'):
        print("Sorry, that was not correct! Can you please try again!")
        continue
      else:
        break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
      day = input("\nWhich weekday would like to see? Please enter day like Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or if no preference put 'all'.\n").title()   
      if day not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'all'):   
        print("Please try again, remember to enter a specific weekday correctly or all")
        continue
      else:
        break          
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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city]) 
    
     # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
   
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'all':
   	 	
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
    	
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
       
        # filter by day of week if applicable
    if day != 'all':
       
        # filter by day of week to acreate the new dataframe
        df = df[df['day_of_week'] == day.title()] 
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)      

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common day:', popular_day)
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', Start_Station)
    
    # display most commonly used end station
    End_Station = df['End Station'].value_counts().idxmax()
    print('\nMost Commonly used end station:', End_Station)
    
    # display most frequent combination of start station and end station trip
    
    Combination_Station = df.groupby(['Start Station', 'End Station']).count()
    print('\nMost Frequently used combination of start station and end station trip:', Start_Station, " & ", End_Station)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total travel time:', Total_Travel_Time/86400, " Days")

    # display mean travel time
    Mean_Travel_Time = df['Trip Duration'].mean() 
    print('Mean travel time:', Mean_Travel_Time/60, " Minutes")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts() 
    print('User_Types:\n', user_types)

    # Display counts of gender
    try:
      Gender_Types = df['Gender'].value_counts()
      print('\nGender Types:\n', Gender_Types)
    except KeyError:
      print("\nGender Types:\nSorry, no gender data available.")         
    # Display earliest, most recent, and most common year of birth
    try:
      Earliest_Year = df['Birth Year'].min()
      print('\nEarliest Year:', Earliest_Year)
    except KeyError:
      print("\nEarliest Year:\nSorry, no birth year data available.")      
    try:
      Most_Recent_Year = df['Birth Year'].max()
      print('\nMost Recent Year:', Most_Recent_Year)
    except KeyError:
      print("\nMost Recent Year:\nSorry, no birth year data available.") 
    try:
      Most_Common_Birth_Year = df['Birth Year'].value_counts().idxmax() 
      print('\nMost Common Birth Year', Most_Common_Birth_Year)
    except KeyError:
      print("\nMost Common Year:\n Sorry,no data available.")
    
      print("\nThis took %s seconds." % (time.time() - start_time))
      print('-'*40) 

def display_raw_data(df):
    """Displays raw data when requested.

    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nWould you want to see the first five rows of raw data? Enter yes or no.\n')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            view_raw_data = input('\nDo you want to see the first five rows of raw data? Enter yes or no.\n')
            if view_raw_data.lower() != 'yes':
                break
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
                      
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
      

if __name__ == "__main__":
	main()
