# import requests
from datetime import timedelta, datetime
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def main():
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    # pd.set_option('display.max_columns', None, 'display.max_colwidth', None, 'display.max_rows', None)    
    src_url = 'https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/vaccinations.csv'
    src_ind_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/India.csv'

    df = pd.read_csv(src_ind_url)
    df['daily_count_d1'] = df['people_vaccinated'].diff()

    # print(df.tail(10))
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

    st.title('India COVID Vaccination Trend')
    st.markdown(f"""
    ## India COVID Vaccination Summary
    Until _{last_date_disp}_
    - Vaccinated **{single_so_far:,}** out of **{target_population:,}** with only single dose.
    - Need **{balance_population:,}** in **{duration}** days @ **{rvr:,}** per day.
    - Current vaccination rate (last **{block}** days average): **{cvr:,}** per day.
    - May get only **{max_possible:,}** and will trail by **{trail:,}**.
    - May reach target population by **{new_deadline}** at this rate.
    """)

    df_projected = pd.DataFrame({'date': [last_date, deadline], 'people_vaccinated': [single_so_far, target_population], 'projected_current': [single_so_far, max_possible]})
    
     
if __name__ == '__main__':
    main()
