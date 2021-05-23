""" 
{"sessions": [
    {
      "center_id": 1234,
      "name": "District General Hostpital",
      "name_l": "",
      "address": "45 M G Road",
      "address_l": "",
      "state_name": "Maharashtra",
      "state_name_l": "",
      "district_name": "Satara",
      "district_name_l": "",
      "block_name": "Jaoli",
      "block_name_l": "",
      "pincode": "413608",
      "lat": 28.7,
      "long": 77.1,
      "from": "09:00:00",
      "to": "18:00:00",
      "fee_type": "Paid",
      "fee": "250",
      "session_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "date": "31-05-2021",
      "available_capacity": 50,
      "available_capacity_dose1": 25,
      "available_capacity_dose2": 25,
      "min_age_limit": 18,
      "vaccine": "COVISHIELD",
      "slots": [
        "FORENOON",
        "AFTERNOON"
      ]
    }
  ]
}
"""
# from bs4 import BeautifulSoup
import sys
import requests
import json
import pandas as pd
from tabulate import tabulate

def main(script, pin='393001', date='13-05-2021'):
    # url = 'https://www.oscars.org/oscars/ceremonies/2021'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pin}&date={date}'
    # print(url)
    result = requests.get(url, headers=headers)
    info = result.content.decode()
    # print(info)
    dld = json.loads(info)
    tabhdr = ['name', 'address', 'state_name', 'district_name', 'block_name', 'pincode', 'date', 'available_capacity', 'fee', 'min_age_limit', 'vaccine'] 
    # width = pd.util.terminal.get_terminal_size() # find the width of the user's terminal window
    pd.set_option('display.max_rows', None, 'display.max_columns', None, 'display.expand_frame_repr', False, 'display.max_colwidth', None, 'display.width', None)
    # print(tabhdr)
    for ld in dld.values():
        print(f'Number of Centres found for PIN {pin}: {len(ld)}')
        df = pd.DataFrame(ld, columns=tabhdr)
        # print(df)
        print(tabulate(df, headers=['name', 'address', 'state', 'district', 'block', 'pincode', 'date', 'available', 'fee', 'min_age', 'vaccine'], tablefmt='simple')) 
    # print(brokendown)

    # soup = BeautifulSoup(html, 'html5lib')
    # soup.p.text
    # print(soup.p.text.split())
    # # soup.p['title']
if __name__ == '__main__':
    main(*sys.argv)
