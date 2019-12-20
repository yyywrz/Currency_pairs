import logging as logger
from taskflow.patterns import linear_flow
from taskflow import task, engines
from fetcher import fetcher

class fetchData(task.Task):
    def execute(self):
        logger.info("Executing '%s'" % (self.name))
        instance = fetcher.instance()
        return instance

class fetchHistoricalData(task.Task):
    def execute(self,date):
        logger.info("Executing '%s'" % (self.name))
        instance = fetcher.historical_fetcher(date)
        return instance

def fetcher_flow(opt, store={}, date=''):
# opt should be either 'historical_data' or 'current_data'
    if opt == 'historical_data':
        flow = linear_flow.Flow('sub_flow_add_historical_data_for_'+date)
        flow.add(
            fetchHistoricalData('fetch historical exchange rates',
            rebind={'date':'date'},
            provides = 'one_rate_instance'))
        store['date'] = date
    elif opt == 'current_data':
        flow = linear_flow.Flow('main_flow_keep_fetching_current_exchange_rates')
        flow.add(fetchData('fetch current exchange rates',
            provides = 'one_rate_instance'))
    else:
        return None
    return flow, store

if __name__=='__main__':
    (flow, store) = fetcher_flow('current_data')
    e = engines.load(flow, store=store)
    print(flow)
    e.run()
    (flow, store) = fetcher_flow('historical_data',date='2019-01-01')
    e = engines.load(flow, store=store)
    e.run()
    print(fetcher_flow('current') is None)