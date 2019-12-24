import logging as logger
from taskflow.patterns import linear_flow
from taskflow import task, engines
from main import operation

class calculateRates(task.Task):
    def execute(self, instance):
        logger.info("Executing '%s'" % (self.name))
        rates = operation.all_rates(instance)
        return rates

def calculate_rates_flow():
    flow = linear_flow.Flow('calculate_rates')
    store = {}
    flow.add(
        calculateRates(
            'calculate all exchange rates',
            rebind = {'instance':'one_rate_instance'},
            provides = 'all_rates' 
        )
    )
    return(flow, store)


class storeData(task.Task):
    def execute(self, rates, datafile_path):
        logger.info("Executing '%s'" % (self.name))
        operation.storeData(rates,datafile_path)

def store_data_flow():
    flow = linear_flow.Flow('store_rates')
    store = {}
    flow.add(
        storeData(
            'store all rates in both database and files',
            rebind = {
                'rates':'all_rates',
                'datafile_path':'datafile_path'
            }
            )
    )
    return(flow,store)