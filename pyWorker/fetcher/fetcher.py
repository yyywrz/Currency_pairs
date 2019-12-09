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