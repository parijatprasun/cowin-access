import sys
import requests
from datetime import timedelta, datetime
import time
from plyer import notification

def main(script, option='pin', locator='734005', min_age='18', dt=datetime.strftime(datetime.today(), '%d-%m-%Y')):
    print('Query starts at', datetime.now())
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    dt_obj = datetime.strptime(dt, '%d-%m-%Y')
    
    while True:
        dt = datetime.strftime(dt_obj, '%d-%m-%Y')
        if option == 'pin':
            assert len(locator) == 6
            url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={locator}&date={dt}'
            # url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={locator}&date={dt}'
        if option == 'dist':
            assert len(locator) <= 3
            url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={locator}&date={dt}'
            # url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={locator}&date={dt}'

        result = requests.get(url, headers=headers)

        if result.ok:
            cowin_info = result.json()
            if cowin_info["sessions"]:
                for session in cowin_info["sessions"]:
                    if (session["min_age_limit"] ==  int(min_age) and session["available_capacity_dose1"] > 0 ):
                        if 'IIT BOMBAY' in session["name"]:
                            print('## Slot open!', session["date"])
                            print('Center Name:', session["name"], session["state_name"], session["pincode"])
                            print('Availability:', session["vaccine"], session["available_capacity_dose1"])
                            print('')
                            notification.notify(title = "Slots open!", message = f'▶ Slots open for age {min_age} on {dt} at {session["name"]}', app_name='CoWIN Slot', timeout=2)
                
            else:
                print("No slots available for the given period.")
        else:
            print("No Response from CoWin!")
    
        time.sleep(3.5)
        print('Next query at:', datetime.now())

if __name__ == '__main__':
    main(*sys.argv)
