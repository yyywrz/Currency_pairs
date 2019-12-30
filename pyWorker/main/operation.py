
import copy
import logging as logger
import os
import time

from info import consts, helper
from util import file_handler, mongodb_handler

keys = [
    'Currency Code',
    'Currency Name',
    'Region',
    'date',
    'rates']

def rate_converter(code,instance):
    base = instance[code]
    rate = {}
    for key in instance:
        rate[key] = round(instance[key]/base,10)
    return rate;

def all_rates(data):
    rate = {}
    instance = data['rates']
    for code in consts.all_codes:
        rate[code] = helper.ref().code(code)
        rate[code]['date'] = data['date']
        rate[code]['rates'] = rate_converter(code,instance)
    return rate

def to_mongodb(collection,time,instance):
    #try:
    if True:
        with mongodb_handler.db('currency_database',collection) as db:
            if not db.getOne('date',time):
                one = {}
                for key,value in instance.items():
                    if key in keys:
                        one[key] = value           
                db.addOne(one)
    #except:
     #   logger.warning('insert ' +collection+time+' into database failed!')

def to_file(path,code,instance,date=time.strftime("%Y-%m-%d", time.localtime())):
    #try:
    if True:
        file_handler.outputToFile(code,instance,path,date)  
    #except:
        #logger.warning('insert '+code+date+' data into files failed!',)

def one_date_instance_in_file(code,path,base,date):
    target_path = path+'\\'+date
    data={}
    data = base
    data['date'] = date
    try:
        data['rates'] = file_handler.getRate(code,target_path)
    except:
        return False
    return data

def rateInFile(code,path):
    if not os.path.exists(path):
        return []
    dates = os.listdir(path)
    instance = []
    base=helper.ref().code(code)
    for date in dates:
        one =copy.deepcopy(one_date_instance_in_file(code,path,base,date))
        if one:
            instance.append(one)
    return instance

def rateInDB(collection):
    with mongodb_handler.db('currency_database',collection) as db:
        instance=[]
        for one_date_instance in db.all():
            one = copy.deepcopy(one_date_instance)
            del one['_id']
            instance.append(one)
        return instance

def rebaseData(path,base):
    rate_in_file = {}
    rate_in_db = {}
    if base == 'file':
        for code in consts.all_codes:
            fileData = rateInFile(code,path)
            dbData = rateInDB(code)
            if fileData is not dbData:
                for instance in fileData:
                    if instance not in dbData:
                        to_mongodb(code,instance['date'],instance)
    elif base == 'db':
        for code in consts.all_codes:
            fileData = rateInFile(code,path)
            dbData = rateInDB(code)
            for instance in dbData:
                if instance not in fileData:
                    to_file(path,code,instance,instance['date'])

def storeData(rates,path):
    for code in rates:
        fetch_time = rates[code]['date']
        to_file(path,code,rates[code],fetch_time)
        to_mongodb(code,fetch_time,rates[code])  


def removeDataInDB(date):
    for code in consts.all_codes:
        try:
            with mongodb_handler.db('currency_database',code) as db:
                db.deleteOne('date',date)
        except:
            logger.error('delete '+date+' in DB failed')

def remove_all(path):
    for date in os.listdir(path):
        file_handler.removeDataInFile(date,path)
    for code in consts.all_codes:
        try:
            with mongodb_handler.db('currency_database',code) as db:
                db.removeAll()
        except:
            logger.error('delete '+code+' in DB failed')
