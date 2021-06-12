# import requests
from datetime import timedelta, datetime
import pandas as pd
import matplotlib.pyplot as plt
# import streamlit as st
 
def main():
    src_url = 'https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/vaccinations.csv'
    src_ind_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/India.csv'

    df = pd.read_csv(src_ind_url)
    df['daily_count_d1'] = df['people_vaccinated'].diff()
    
    print(df.tail(10))
    
    # define date parameters
    latest_date = df['date'].iloc[-1]
    latest_date_obj = datetime.strptime(latest_date, '%Y-%m-%d')
    deadline = '2021-12-31'
    deadline_obj = datetime.strptime(deadline, '%Y-%m-%d')
    duration = (deadline_obj - latest_date_obj).days
    
    # assign values to variables and calculate rates
    single_so_far = df['people_vaccinated'].iloc[-1]
    target_population = 1000000000
    balance_population = target_population - single_so_far
    rvr = round(balance_population / duration)  # required vaccination rate
    block = 10  # set of days to caluculate the current rate from
    cvr = round(df['daily_count_d1'].tail(block).mean()) # current vaccination rate

    # calculate forecast numbers 
    max_possible = cvr * duration
    trail = target_population - max_possible
    balance_days = round(balance_population / cvr)
    new_deadline_obj = latest_date_obj + timedelta(days=balance_days)
    new_deadline = datetime.strftime(new_deadline_obj, '%d %B %Y')
    last_date_disp = latest_date_obj.strftime('%d %B %Y')

    # display summary information on screen
    print(f'India COVID Vaccination Summary until {last_date_disp}')
    print(f'Vaccinated {single_so_far:,} out of {target_population:,} with only single dose.')
    print(f'Need {balance_population:,} in {duration} days @ {rvr:,} per day.')
    print(f'Current vaccination rate (last {block} days average): {cvr:,} per day.')
    print(f'May get only {max_possible:,} and will trail by {trail:,}.')
    print(f'May reach target population by {new_deadline} at this rate.')

    df_projected = pd.DataFrame({'date': [deadline], 'people_vaccinated': [target_population], 'projected_current': [max_possible]})
    # print(df_projected)

    """
    # fig = plt.figure(figsize=(16,9), dpi=300, facecolor=None, edgecolor=None, frameon=False)
    df2.plot('date', ['people_vaccinated', 'people_fully_vaccinated', 'projected_current'])
    # df['people_vaccinated'].plot(x=df['date'], secondary_y=True, color='green')
    plt.title('India Vaccination Trend', loc='left', fontname='Arial', fontsize=24, fontweight='bold')
    plt.xlabel('Days', fontname='Arial', fontsize=12, fontweight='bold')
    plt.ylabel('Population', fontname='Arial', fontsize=12, fontweight='bold')
    plt.xticks(fontname='Arial', fontsize=10, rotation='vertical')
    plt.yticks(fontname='Arial', fontsize=10)
    plt.ticklabel_format(axis='y', style='plain', scilimits=None, useOffset=None)
    # df.plot.bar('date', 'daily_count_d1', color='blue', linestyle='solid', ax=ax)
    plt.tight_layout()
    plt.show()
    # plt.savefig('file.png')
    plt.close()
    """
    
if __name__ == '__main__':
    main()
