import sys
import requests
import json
import pandas as pd
from tabulate import tabulate
from datetime import timedelta, datetime

def main(script, option='pin', locator='734005', dt=datetime.strftime(datetime.today(), '%d-%m-%Y')):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    pd.set_option('display.max_rows', None, 'display.max_columns', None, 'display.expand_frame_repr', False)
    
    # dt_obj = datetime.strptime(dt, '%d-%m-%Y')
    # dt = datetime.strftime(dt_obj+timedelta(days=next), '%d-%m-%Y')
    if option == 'pin':
        assert len(locator) == 6
        # url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={locator}&date={dt}'
        url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={locator}&date={dt}'
    if option == 'dist':
        assert len(locator) <= 3
        # url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={locator}&date={dt}'
        url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={locator}&date={dt}'
    
    slot_result = requests.get(url, headers=headers)
    slot_info = slot_result.content.decode()

    slot_dld = json.loads(slot_info)
    # print(slot_dld)
    tabhdr = ['name', 'address', 'state_name', 'district_name', 'block_name', 'pincode', 'available_capacity_dose1', 'available_capacity_dose2', 'min_age_limit', 'vaccine'] 

    # df = pd.DataFrame(slot_dld['sessions'], columns=tabhdr)
    data_norm = pd.json_normalize(slot_dld['centers'], record_path =['sessions'], meta=['name', 'address', 'state_name', 'district_name', 'block_name', 'pincode'])
    df = pd.DataFrame(data_norm, columns=tabhdr)

    print(f'Vaccination Centres at {option.upper()} {locator} on {dt}: {len(df.index)}')
    if len(df.index) > 0:
        print(tabulate(df, headers=['Name', 'Address', 'State', 'District', 'Block', 'Pincode', 'Dose1', 'Dose2', 'Age', 'Vaccine'] , tablefmt='simple'))
        print('')

if __name__ == '__main__':
    main(*sys.argv)