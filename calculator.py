import fetcher
import consts
import helper
import mongodb_handler
import time

def rate_converter(code,instance):
    base = instance[code]
    rate = {}
    for key in instance:
        rate[key] = round(instance[key]/base,5)
    return rate;

def all_rates():
    rate = {}
    data = fetcher.instance()
    instance = data['rates']
    for code in consts.all_codes:
        rate[code] = helper.ref().code(code)
        rate[code]['date'] = time.strftime("%Y-%m-%d", time.localtime())
        rate[code]['rates'] = rate_converter(code,instance)
    return rate

if __name__=='__main__':
    rates = all_rates()
    fetch_time = time.strftime("%Y-%m-%d", time.localtime())
    for code in rates:
        db = mongodb_handler.db('currency_database',code)
        if not db.getOne('date',fetch_time):
            db.addOne(rates[code])
