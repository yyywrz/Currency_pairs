import requests
import consts

def fetcher(currency_code):
    url = 'https://api.exchangerate-api.com/v4/latest/'+ currency_code;
    try:
        response = requests.get(url)
        data = response.json()
    except:
        data = False    
    return data

def instance():
    for base in consts.all_codes:
        print('get '+base)
        data = fetcher(base)
        if data:
            return data
    return False