import requests
from info import consts
import logging as logger

def fetcher(currency_code):
    url = 'https://api.exchangerate-api.com/v4/latest/'+ currency_code;
    try:
        logger.info('request exchange rate data of ' +currency_code)
        response = requests.get(url)
        data = response.json()
        logger.info('successfully recieve rate data')
    except:
        logger.warn('request failed')
        data = False    
    return data

def instance():
    for base in consts.all_codes:
        data = fetcher(base)
        if data:
            return data
    logger.error('All requests failed, Check Network!')
    return False
