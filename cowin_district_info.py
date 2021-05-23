import sys
import requests
import json
import pandas as pd
from tabulate import tabulate
from datetime import timedelta, datetime

def main():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    pd.set_option('display.max_rows', None, 'display.max_columns', None, 'display.expand_frame_repr', False)
    
    state_url = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
    state_result = requests.get(state_url, headers=headers)
    state_info = state_result.content.decode()
    state_dld = json.loads(state_info)
    # print(state_dld)
    state_df = pd.DataFrame(state_dld['states'])
    state_df.sort_values(by=['state_id'], inplace=True)
    split_row = len(state_df.index) // 2
    state_df_1 = state_df.iloc[:split_row,:].reset_index(drop=True)
    state_df_2 = state_df.iloc[split_row:,:].reset_index(drop=True)
    state_df_1_str = state_df_1.to_string(index=False)
    state_df_2_str = state_df_2.to_string(index=False)
    # table = [[state_df_1_str], [state_df_2_str]]
    state_df_split = pd.concat([state_df_1, state_df_2], axis=1)
    print(tabulate(state_df_split, headers=['State ID', 'State Name', 'State ID', 'State Name'], showindex="False", tablefmt='simple'))
    
    state_code = input('Please input state code from the above list: ')
    # print(state_code, dist_code)

    dist_url = f'https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_code}'
    dist_result = requests.get(dist_url, headers=headers)
    dist_info = dist_result.content.decode()
    dist_dld = json.loads(dist_info)
    # print(dist_dld)
    dist_df = pd.DataFrame(dist_dld['districts'])
    dist_df.sort_values(by=['district_id'], inplace=True)
    # state_dist_df = pd.concat([state_df, dist_df], axis=1).fillna('')
    # print(dist_df.to_string(index=False))
    print(tabulate(dist_df, headers=['District ID', 'District Name'], showindex="False", tablefmt='simple'))
    
if __name__ == '__main__':
    main()