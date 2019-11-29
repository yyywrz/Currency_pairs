
import time

from info import consts
from info import helper
from util import mongodb_handler
from util import file_handler

def rate_converter(code,instance):
    base = instance[code]
    rate = {}
    for key in instance:
        rate[key] = round(instance[key]/base,6)
    return rate;

def all_rates(data):
    rate = {}
    instance = data['rates']
    for code in consts.all_codes:
        rate[code] = helper.ref().code(code)
        rate[code]['date'] = time.strftime("%Y-%m-%d", time.localtime())
        rate[code]['rates'] = rate_converter(code,instance)
    return rate

def storeData(rates):
    fetch_time = time.strftime("%Y-%m-%d", time.localtime())
    for code in rates:
        db = mongodb_handler.db('currency_database',code)
        if not db.getOne('date',fetch_time):
            db.addOne(rates[code])
        file_handler.outputToFile(code,rates[code])        
