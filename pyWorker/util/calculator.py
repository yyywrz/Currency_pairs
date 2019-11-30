
import time
import logging as logger

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

def to_mongodb(collection,time,instance):
    try:
        db = mongodb_handler.db('currency_database',collection)
        if not db.getOne('date',time):
            db.addOne(instance)
    except:
        logger.warn('insert ' +collection+' into database failed!')

def to_file(code, instance):
    try:
        file_handler.outputToFile(code,instance)  
    except:
        logger.warn('insert ' +collection+' data into files failed!')

def storeData(rates):
    fetch_time = time.strftime("%Y-%m-%d", time.localtime())
    for code in rates:
        to_file(code,rates[code])
        to_mongodb(code,fetch_time,rates[code])  
