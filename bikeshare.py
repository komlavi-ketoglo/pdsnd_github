import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_month():
    """
    Asks user to specify a month.

    Returns:
        (str) month - name of the month to filter by
    """
    month = ""
    while month not in ('january', 'february', 'march', 'april', 'may', 'june'):
        try:
            month = input("Please specify the month you want to analyze (Choose between january, february, march, april, may or june.) : \n").lower()
            if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
                print("Wrong month input attempt, try again")
            else:
                print("Alright!!! You choosed {}".format(month))
        except ValueError:
            print("That's not a valid input")
    return month

def get_day():
    """
    Asks user to specify a day.

    Returns:
        (str) day - name of the day to filter by
    """
    
    day = ""
    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        try:
            day = input("Please specify the day you would like to analyze (Choose among monday, tuesday, wednesday, thursday, friday, saturday or sunday. Choose all if you don't want to filter by day) : \n").lower()
            if day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                print("Wrong day input attempt, try again")
            else:
                print("Wonderfull!!! You choosed {}".format(day))
        except ValueError:
            print("That's not a valid input")
    return day

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

    city=""

    while city not in ('chicago', 'new york city', 'washington'):
        try:
            city = input("Please specify the city you want to analyze (Choose among chicago, new york city or washington) : \n").lower()
            if city not in ('chicago', 'new york city', 'washington'):
                print("Wrong city input attempt, try again")
            else:
                print("Great!!! You choosed {}".format(city))
        except ValueError:
            print("That's not a valid input")
            
    filtering=""
    while filtering not in ('month', 'day', 'both', 'none'):
        try:
            filtering = input("Would you like to filter the data by month, day, both or not at all? Just type 'none' for no time filter. \n").lower()
            if filtering not in ('month', 'day', 'both', 'none'):
                print("Wrong filter attempt, please try again")
            elif filtering == 'month':
                month=get_month()
                day="all"
            elif filtering == 'day':
                day=get_day()
                month="all"
            elif filtering == 'both':
                month=get_month()
                day=get_day()
            elif filtering == 'none':
                month="all"
                day="all"
        except ValueError:
            print("That's not a valid input")
    
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
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def raw_data_preview(df):
    """Displays 5 rows ofraw data to the user until he answers 'no'
    
    Args
    df - Pandas DataFrame containing city data filtered by month and day
    
    Returns:
    Raw data from the dataframe
    """
    answer=""
    while answer not in ('yes', 'no'):
        try:
            answer = input("Would you like to preview some raw data? Type 'yes' or 'no' to make a choice: \n").lower()
            if answer not in ('yes', 'no'):
                print("Wrong answer \nPlease try again")
            elif answer == "yes":
                rows = 0
                while answer == "yes":
                    for i in range(5):
                        print(df.iloc[rows+i])
                    print('-'*40)
                    try:
                        answer = input("Would you like to preview more data?(yes or no): \n").lower()
                        if answer not in ('yes', 'no'):
                            print("Wrong answer \nPlease try again")
                        elif answer == "yes":
                            rows += 5
                    except ValueError:
                        print("That's not a valid input")
        except ValueError:
            print("That's not a valid input")
        print('-'*40)


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args
    df - Pandas DataFrame containing city data filtered by month and day
    
    Returns:
    
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    most_common_month = df['month'].mode()[0]

    print('The Most common month is : \n', calendar.month_name[most_common_month])

    # display the most common day of week
    
    most_common_weekday = df['day_of_week'].mode()[0]

    print('The Most common day of week is: \n', most_common_weekday)

    # display the most common start hour
    
    #Extract start hour from Start Time
    df['start_hour'] = df['Start Time'].dt.strftime('%H:%M')
    
    most_common_start_hour = df['start_hour'].mode()[0]
    
    print('The Most common start hour is : \n ', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    
    most_common_start_station = df['Start Station'].mode()[0]

    print('The Most commonly used Start Station is: \n', most_common_start_station)

    # display most commonly used end station
    
    most_common_end_station = df['End Station'].mode()[0]

    print('The Most commonly used End Station: \n', most_common_end_station)

    # display most frequent combination of start station and end station trip
    
    most_common_start_end_station_combination = (df['Start Station']+' - '+df['End Station']).mode()[0]

    print('The Most frequent combination of start station and end station trip: \n', most_common_start_end_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    
    total_travel_time = df['Trip Duration'].sum()
    
    #convert seconds to timestamp
    total_travel_time = time.strftime('%H:%M:%S', time.gmtime(total_travel_time))

    print('The total travel time is: \n', total_travel_time)

    # display mean travel time
    
    mean_travel_time = df['Trip Duration'].mean()
    
    #convert seconds to timestamp
    mean_travel_time = time.strftime('%H:%M:%S', time.gmtime(mean_travel_time))

    print('The mean travel time is: \n', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    
    user_type_count = df['User Type'].value_counts()

    print('The count of User Type is : \n', user_type_count)

    # Display counts of gender
    
    #Check if the column exists
    gender_count = df['Gender'].value_counts() if 'Gender' in df.columns else 0

    print('The count of User Type is : \n', gender_count)

    # Display earliest, most recent, and most common year of birth
    
    #Check if the column exists
	earliest_birth_year = df['Birth Year'].min() if 'Birth Year' in df.columns else 0

    print('The earliest year of birth is : \n', int(earliest_birth_year))
    
    
    #Check if the column exists
    if 'Birth Year' in df.columns:
        most_recent_birth_year = df['Birth Year'].max()
    else:
        most_recent_birth_year = 0
    

    print('The most recent year of birth is : \n', int(most_recent_birth_year))
    
    #Check if the column exists
    if 'Birth Year' in df.columns:
        most_common_birth_year = df['Birth Year'].mode()
    else:
        most_common_birth_year = 0
    

    print('The most common year of birth is : \n', int(most_common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        raw_data_preview(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
