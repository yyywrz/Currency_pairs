import requests
from info import consts
import logging as logger
from info import helper

def fetcher(currency_code):
# 
# requst currency exchange rate data, it returns a JSON dict
# 
    if currency_code not in consts.all_codes:
        logger.warning('Invalid Input')
        return False
    url = 'https://api.exchangerate-api.com/v4/latest/'+ currency_code;
    try:
        logger.info('request exchange rate data of ' +currency_code)
        response = requests.get(url)
        data = response.json()
        logger.info('successfully recieve rate data')
    except:
        logger.warning('request failed')
        data = False    
    return data

def instance():
# 
# in case of some unexpecting request failure, it will try all codes.
# it ends once a instance available
# 
    for base in consts.all_codes:
        data = fetcher(base)
        if data:
            return data
    logger.error('All requests failed, Check Network!')
    return False

def historical_fetcher(date):  
# 
#get historical currency exchange rate data in a specific date, it returns a JSON dict
#This api limites 1000 attempts per month
# 
    web_link = 'http://data.fixer.io/api/'
    apikey = '0a1de30b7d7412fc06850856b3e9cf84'
    url = web_link + date + '?access_key=' + apikey
    try:
        logger.info('request historical exchange rate data')
        response = requests.get(url)
        data = response.json()
        if 'error' in data:
            logger.warning('request failed: '+ data['error']['info'])
            return False
        rates = {}
        for key in data['rates']:
            if key in consts.all_codes:
                rates[key] = data['rates'][key]
        data['rates'] = rates
        logger.info('successfully recieve rate data')

    except:
        logger.warning('request failed')
        data = False    
    return data

if '__main__'==__name__:
    print(fetcher('USD'))
    print(historical_fetcher('2019-12-2'))