
import requests

def fetcher(currency_code):
    url = 'https://api.exchangerate-api.com/v4/latest/'+ currency_code;
    response = requests.get(url)
    return response.json()



if __name__=='__main__':
    import consts
    for base in consts.all_codes:
        print('get '+base)
        data = fetcher(base)
        rate['date'] = data['date']
        rate[base] = data['rates']
    for from_currency in consts.all_codes:
        for to_currency in consts.all_codes:
            print('The exchange rate from '+from_currency+' to '+to_currency+' is '+str(rate[from_currency, to_currency]))


