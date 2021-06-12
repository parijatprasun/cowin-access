# import requests
from datetime import timedelta, datetime
import pandas as pd
import matplotlib.pyplot as plt
# import streamlit as st
 
def main():
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    # pd.set_option('display.max_columns', None, 'display.max_colwidth', None, 'display.max_rows', None)    
    src_url = 'https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/vaccinations.csv'
    src_ind_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/India.csv'

    # result = requests.get(src_ind_url, allow_redirects=True)
    # print(result.status_code)
    # print(result.content)
    df = pd.read_csv(src_ind_url)
    df['daily_count_d1'] = df['people_vaccinated'].diff()
    # for index, row in df.iterrows():
    #     df['daily_count_d1'][index] = df['people_vaccinated'][index] - df['people_vaccinated'][index-1]
    print(df.tail(10))
    # print(df.dtypes)
    # print(df.describe())
    last_date = df['date'].iloc[-1]
    last_date_obj = datetime.strptime(last_date, '%Y-%m-%d')
    # print(last_date_obj)
    deadline = datetime.strptime('31-12-2021', '%d-%m-%Y')
    duration = (deadline - last_date_obj).days
    # print(duration)
    single_so_far = df['people_vaccinated'].iloc[-1]
    target_population = 1000000000
    balance_population = target_population - single_so_far
    rvr = round(balance_population / duration)
    block = 10
    cvr = round(df['daily_count_d1'].tail(block).mean())
    max_possible = cvr * duration
    trail = target_population - max_possible
    balance_days = round(balance_population / cvr)
    new_deadline_obj = last_date_obj + timedelta(days=balance_days)
    new_deadline = datetime.strftime(new_deadline_obj, '%d %B %Y')
    last_date_disp = last_date_obj.strftime('%d %B %Y')

    print(f'India COVID Vaccination Summary until {last_date_disp}')
    print(f'Vaccinated {single_so_far:,} out of {target_population:,} with only single dose.')
    print(f'Need {balance_population:,} in {duration} days @ {rvr:,} per day.')
    print(f'Current vaccination rate (last {block} days average): {cvr:,} per day.')
    print(f'May get only {max_possible:,} and will trail by {trail:,}.')
    print(f'May reach target population by {new_deadline} at this rate.')

    df_projected = pd.DataFrame({'date': [last_date, deadline], 'people_vaccinated': [single_so_far, target_population], 'projected_current': [single_so_far, max_possible]})
    print(df_projected)

    """ # fig = plt.figure(figsize=(16,9), dpi=300, facecolor=None, edgecolor=None, frameon=False)
    df['daily_count_d1'].plot(x=df['date'], kind='bar', color='orange')
    df['people_vaccinated'].plot(x=df['date'], secondary_y=True, color='green')
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
    plt.close() """
    
if __name__ == '__main__':
    main()
