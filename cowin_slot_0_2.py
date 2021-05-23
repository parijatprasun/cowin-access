import sys
import requests
import json
import pandas as pd
from tabulate import tabulate
from datetime import timedelta, datetime
from plyer import notification

def main(script, option='pin', locator='734005', dt=datetime.strftime(datetime.today(), '%d-%m-%Y'), dtrange='1'):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    pd.set_option('display.max_rows', None, 'display.max_columns', None, 'display.expand_frame_repr', False)
    
    dt_obj = datetime.strptime(dt, '%d-%m-%Y')
    next = 0
    while next < int(dtrange):
        dt = datetime.strftime(dt_obj+timedelta(days=next), '%d-%m-%Y')
        now = datetime.now()
        now_string = now.strftime("%d-%m-%Y %H:%M:%S")
        if option == 'pin':
            assert len(locator) == 6
            url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={locator}&date={dt}'
            # url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={locator}&date={dt}'
        if option == 'dist':
            assert len(locator) <= 3
            url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={locator}&date={dt}'
            # url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={locator}&date={dt}'
        
        slot_result = requests.get(url, headers=headers)
        slot_info = slot_result.content.decode()

        slot_dld = json.loads(slot_info)
        tabhdr = ['name', 'address', 'state_name', 'district_name', 'block_name', 'pincode', 'available_capacity_dose1', 'available_capacity_dose2', 'min_age_limit', 'vaccine'] 

        print(f'Vaccination Centres/Slots at {option.upper()} {locator} on {dt}: {len(slot_dld["sessions"])}{now_string:>80}')
        print('')
        df = pd.DataFrame(slot_dld['sessions'], columns=tabhdr)
        if len(slot_dld['sessions']) > 0:
            print(tabulate(df, headers=['Name', 'Address', 'State', 'District', 'Block', 'Pincode', 'Dose1', 'Dose2', 'Age', 'Vaccine'] , tablefmt='simple'))
            print('')
            for index, row in df.iterrows():
                if (row["min_age_limit"] == 18 and row["available_capacity_dose1"] > 0):
                    print(f'▶ Slots open at {row["name"]}, {row["address"]}, {row["pincode"]} for 18-44 age group!')
                    notification.notify(title = "Slots open!", message = f'▶ Slots open for {dt} at {row["pincode"]}', app_name='CoWIN Slot', app_icon = "PythonLogo.ico", timeout=5)
        next +=1

if __name__ == '__main__':
    main(*sys.argv)