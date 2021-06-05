import requests

def main():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    # pd.set_option('display.max_rows', None, 'display.max_columns', None, 'display.expand_frame_repr', False)
    
    state_url = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
    state_result = requests.get(state_url, headers=headers)
    state_info = state_result.json()
    for state in state_info['states']:
        print(state['state_id'], state['state_name'])

    state_code = input('Please input state code from the above list: ')

    dist_url = f'https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_code}'
    dist_result = requests.get(dist_url, headers=headers)
    dist_info = dist_result.json()
    for district in dist_info['districts']:
        print(district['district_id'], district['district_name'])

if __name__ == '__main__':
    main()