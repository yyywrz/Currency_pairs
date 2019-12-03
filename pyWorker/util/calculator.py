
import time
import os
import logging as logger
import copy

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

def to_file(path,code, instance):
    try:
        file_handler.outputToFile(code,instance,path)  
    except:
        logger.warn('insert ' +collection+' data into files failed!')

def one_date_instance_in_file(code,path,base,date):
    target_path = path+'//'+date
    data={}
    data = base
    data['date'] = date
    data['rates'] = file_handler.getRate(code,target_path)
    return data

def rateInFile(code,path):
    dates = os.listdir(path)
    instance = []
    base=helper.ref().code(code)
    for date in dates:
        one =copy.deepcopy(one_date_instance_in_file(code,path,base,date))
        instance.append(one)
    return instance

def rateInDB(collection):
    db = mongodb_handler.db('currency_database',collection)
    instance=[]
    for one_date_instance in db.all():
        del one_date_instance['_id']
        instance.append(one_date_instance)
    return instance

def processData(rates,path):
    storeData(rates,path)
    rate_in_file = {}
    rate_in_db = {}
    for code in consts.all_codes:
        print(code)
        print(rateInFile(code,path) is rateInDB(code))
        print()

def storeData(rates,path):
    fetch_time = time.strftime("%Y-%m-%d", time.localtime())
    for code in rates:
        to_file(path,code,rates[code])
        to_mongodb(code,fetch_time,rates[code])  
