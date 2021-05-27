import sys
import requests
import json
import pandas as pd
from tabulate import tabulate
from datetime import timedelta, datetime
import streamlit as st

def max_width():
    max_width_str = f"max-width: 1280px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

def main():
    max_width()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    st.title('CoWIN Vaccine Availability Search')
    st.markdown("""
    ## 🔍 Search for Vaccine availability at your location
    *Source:* [CoWIN portal](https://www.cowin.gov.in/)
    - This page provides realtime slot information only. 
    - For vaccine slot booking please visit [Self Registration Page](https://selfregistration.cowin.gov.in)
    """)
    state_raw = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states', headers=headers).json()
    state_data = [dict1['state_name'] for dict1 in state_raw['states']]
        
    st.sidebar.markdown("## Select your input here")
    option = st.sidebar.selectbox('How do you want to search?', ['PIN', 'District'])
    
    if option == 'District':
        state_name = st.sidebar.selectbox('State: ', state_data)
        for dict1 in state_raw['states']:
                    if dict1['state_name'] == state_name:
                        state_id = dict1['state_id']

        district_raw = requests.get(f'https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}', headers=headers).json()
        district_data = [dict2['district_name'] for dict2 in district_raw['districts']]
        district_name = st.sidebar.selectbox('District:', district_data)
        for dict2 in district_raw['districts']:
            if dict2['district_name'] == district_name:
                locator = dict2['district_id']
        st.write(f'💉 Status of Vaccine Availability at **{state_name} /** {district_name}')
    
    else:
        locator = st.sidebar.text_input('PIN', max_chars=6)
        st.write(f'💉 Status of Vaccine Availability at {locator}')

    dt_obj = st.sidebar.date_input('Start Date', value=datetime.today(), min_value=datetime.today(), max_value=None, key=None, help=None)
    dt = datetime.strftime(dt_obj, '%d-%m-%Y')
    min_age = st.sidebar.selectbox('Minimum Age:', [18, 45])
    # st.write(dt)

    if option == 'District':
        # assert len(locator) <= 3
        # url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={locator}&date={dt}'
        url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={locator}&date={dt}'

    if option == 'PIN':
        # assert len(locator) == 6
        # url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={locator}&date={dt}'
        url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={locator}&date={dt}'
    
    # st.write(url)

    result = requests.get(url, headers=headers)

    st.write('- Status for Minimum Age:', min_age)
    table=[['Date', 'Name', 'Address', 'Block', 'District', 'State', 'Pincode', 'Availabity', 'Vaccine']]
    # table = [[]]
    if result.ok:
        cowin_info = result.json()
        if cowin_info["centers"]:
            # if(print_flag.lower() =='y'):
            for center in cowin_info["centers"]:
                for session in center["sessions"]:
                    if (session["min_age_limit"] ==  min_age and session["available_capacity_dose1"] >= 0 ):
                        # st.write('**Status for**', session["date"])
                        table.append([session["date"], center["name"], center["address"], center["block_name"], center["district_name"], center["state_name"], center["pincode"], session["available_capacity_dose1"], session["vaccine"]])
            # st.write(table)
            df = pd.DataFrame(table)
            df.columns = df.iloc[0]
            # df.index.name = 'Date'
            # st.dataframe(df)
            df2 = df.loc[1:].sort_values(by='Date')
            st.table(df2)
        else:
            st.write("No slots available for the given period.")
    else:
        st.write("No Response!")

if __name__ == '__main__':
    main()