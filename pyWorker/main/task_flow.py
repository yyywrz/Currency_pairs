import logging as logger

from taskflow import engines, task
from taskflow.patterns import linear_flow, unordered_flow

from main import operation


class calculateRates(task.Task):
    def execute(self, instance):
        logger.info("Executing '%s'" % (self.name))
        logger.warning(instance)
        rates = operation.all_rates(instance)
        logger.warning(rates)
        return rates

def calculate_rates_flow(date=''):
    flow = linear_flow.Flow('calculate_rates')
    store = {}
    flow.add(
        calculateRates(
            'calculate all exchange rates ' + date,
            rebind={'instance':'one_rate_instance' + date},
            provides = 'rates' + date 
        )
    )
    return(flow, store)


class storeData(task.Task):
    def execute(self, rates, datafile_path):
        logger.info("Executing '%s'" % (self.name))
        operation.storeData(rates,datafile_path)

def store_data_flow(date=''):
    flow =  unordered_flow.Flow('store_rates')
    store = {}
    flow.add(
        storeData(
            'store all rates in both database and files '+date,
            rebind = {
                'rates':'rates' + date,
                'datafile_path':'datafile_path'
            })
    )
    return(flow,store)
