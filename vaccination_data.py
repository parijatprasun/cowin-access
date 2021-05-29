# import requests
# from datetime import timedelta, datetime
import pandas as pd
import streamlit as st
 
def main():
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        
    src_url = 'https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/vaccinations.csv'
    src_ind_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/India.csv'

    # result = requests.get(src_ind_url, allow_redirects=True)
    # print(result.status_code)
    # print(result.content)
    df = pd.read_csv(src_ind_url)
    df2 = pd.DataFrame(df, columns=['date', 'people_fully_vaccinated'])
    st.title('Vaccination Worm Plot')
    st.line_chart(df2)

if __name__ == '__main__':
    main()