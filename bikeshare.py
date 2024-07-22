import time
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input("Enter city name (Chicago, New York City, Washington): ").strip().casefold()
        if city in (key.casefold() for key in CITY_DATA):
            break
        print("Invalid city name.Please try again.")

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Enter month (all, January, February, ..., June): ").strip().lower()
        if month in months:
            break
        print("Invalid month. Please try again.")

    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Enter day (all, Monday, Tuesday, ..., Sunday): ").strip().lower()
        if day in days:
            break
        print("Invalid day. Please try again.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
    city (str): name of the city to analyze
    month (str): name of the month to filter by, or "all" to apply no month filter
    day (str): name of the day of week to filter by, or "all" to apply no day filter
    Returns:
    df (DataFrame): Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    if month != 'all':
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    popular_month = df['month'].mode()[0]
    popular_day = df['day_of_week'].mode()[0]
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f"Most Common Month: {popular_month}")
    print(f"Most Common Day of Week: {popular_day}")
    print(f"Most Common Start Hour: {popular_hour}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    common_start_station = df['Start Station'].mode()[0]
    common_end_station = df['End Station'].mode()[0]
    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Commonly Used Start Station:', common_start_station)
    print('Most Commonly Used End Station:', common_end_station)
    print('Most Common Trip from Start to End:', common_trip)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()
    print('Total Travel Time:', total_travel_time)
    print('Mean Travel Time:', mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_types_counts = df['User Type'].value_counts()
    print('User Types:', user_types_counts)
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Gender Counts:', gender_counts)
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print('Earliest Birth Year:', int(earliest_year))
        print('Most Recent Birth Year:', int(most_recent_year))
        print('Most Common Birth Year:', int(most_common_year))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    i = 0
    while True:
        raw = input("Would you like to see 5 rows of raw data? Enter yes or no: ").strip().lower()
        if raw == 'no':
            break
        if raw == 'yes':
            print(df.iloc[i:i+5])
            i += 5
        else:
            print("Please type 'yes' or 'no'.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()