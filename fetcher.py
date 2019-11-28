
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
        print(data)
        if data:
            return data
            
if __name__=='__main__':
    import consts
    rate ={}
    for base in consts.all_codes:
        print('get '+base)
        data = fetcher(base)
        rate['date'] = data['date']
        rate[base] = data['rates']
        print(data)
    for from_currency in consts.all_codes:
        for to_currency in consts.all_codes:
            print('The exchange rate from '+from_currency+' to '+to_currency+' is '+str(rate[from_currency][to_currency]))


