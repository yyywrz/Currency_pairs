import logging as logger
import os
import sys
import time

from taskflow import engines, task
from taskflow.patterns import linear_flow, unordered_flow

from fetcher import fetcher
from fetcher import task_flow as fetcher_tf
from main import operation
from main import task_flow as operation_tf
from util import datetime_helper, file_handler, path_helper

pyworker = path_helper.parent_path(path_helper.current_path(__file__))
root = path_helper.grandparent_path(path_helper.current_path(__file__))
dataFile_path = root + "\\currency_exchange_data"

def initlog():
    path = root +'\\temp\\log'
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    logger.basicConfig(level=logger.INFO,
                    filename=path+'\\pyworker.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s: %(message)s - %(pathname)s[line:%(lineno)d] '
                    )

def add_lib_path():
    for path in sys.path:
        if path_helper.file_name(path) == 'site-packages':
            pth_file = path+'\\currency_pair.pth'
            if not os.path.exists(pth_file):
                with open(pth_file,'w') as f:
                    f.write(pyworker)
                    logger.info("Add pyworker in system path")
            else:
                logger.info("Pyworker already in system path")

class fetchData(task.Task):
    default_provides = 'instance'
    def execute(self):
        logger.info("Executing '%s'" % (self.name))
        instance = fetcher.instance()
        return instance
    def revert(self, *args, **kwargs):
        logger.error("instance data invalid!")

class fetchHistoricalData(task.Task):
    default_provides = 'instance'
    def execute(self,date):
        logger.info("Executing '%s'" % (self.name))
        instance = fetcher.historical_fetcher(date)
        return instance
    def revert(self, *args, **kwargs):
        logger.error("instance data invalid!")

class calculateRates(task.Task):
    default_provides = 'rates'
    def execute(self, instance):
        if instance == False:
            raise TypeError("instance needed!")
        else:
            logger.info("Executing '%s'" % (self.name))
            rates = operation.all_rates(instance)
            return rates

class storeData(task.Task):
    def execute(self, rates):
        logger.info("Executing '%s'" % (self.name))
        operation.storeData(rates,dataFile_path)

class cleanData(task.Task):
    def execute(self, date):
        if date == 'all':
            logger.info("Executing  '%s'" % (self.name))
            operation.remove_all(dataFile_path)
        else:
            logger.info("Start to '%s' in Files" % (self.name))
            file_handler.removeDataInFile(date, dataFile_path)
            logger.info("Start to '%s' in DB" % (self.name))
            operation.removeDataInDB(date)

class rebaseData(task.Task):
    def execute(self, base):
        logger.info("Executing  '%s'" % (self.name))
        operation.rebaseData(dataFile_path, base)

class getDateRange(task.Task):
    default_provides = 'dateRange'
    def execute(self, start, end):
        logger.info("Executing '%s'" % (self.name))
        try:
            dr = datetime_helper.dateRange(start,end)
        except:
            raise TypeError("instance needed!")
        return dr

class processDaterangeData(task.Task):
    def execute(self, dateRange):
        for date in dateRange:
            wf = linear_flow.Flow("sub-flow"+date)
            wf.add(
                fetchHistoricalData('fetch data'),
                calculateRates('calculate rates'),
                storeData('store data')
            )
            e = engines.load(wf,store={'date':date})
            runEngine(e)
def update_flow(origin,toBeAdded):
    (flow,store) = origin
    (flow_toBeAdded,store_toBeAdded) = toBeAdded
    store.update(store_toBeAdded)
    return (flow.add(flow_toBeAdded), store)

def main_flow():
    (flow,store) = (linear_flow.Flow('main_flow'),{'datafile_path':dataFile_path})
    (flow,store) = update_flow((flow,store), fetcher_tf.fetcher_flow('current_data'))
    (flow,store) = update_flow((flow,store), operation_tf.calculate_rates_flow())
    (flow,store) = update_flow((flow,store), operation_tf.store_data_flow())
    e = engines.load(flow, store=store)
    runEngine(e,43200)


def historical_flow(key,date):
    store = {
        'datafile_path': dataFile_path,
        key: date
    }
    flow = linear_flow.Flow('sub_flow_historical')
    (flow,store) = update_flow(
        (flow,store), 
        fetcher_tf.fetcher_flow(
            'historical_data',
            date=date,
            rebind={'date':key}
        ))
    (flow,store) = update_flow(
        (flow,store),
        operation_tf.calculate_rates_flow(date=date))
    (flow,store) = update_flow(
        (flow,store),
        operation_tf.store_data_flow(date=date))
    return(flow,store)

def sub_flow():
    for term in sys.argv[1:]:
        try:
            [key,value] = term.split(':')
        except:
            logger.critical('Invalid arguments')
            sys.exit()
        if key == 'date':
            (flow,store) = historical_flow(key, value)
            e = engines.load(flow,store=store)
            runEngine(e)
        elif key == 'remove':
            if 'to' in value:
                try:
                    [start,end] = value.split('to')
                    date_range = datetime_helper.dateRange(start,end)
                    total_dates = len(date_range) 
                    logger.info(str(total_dates) + ' dates will be deleted')
                except:
                    logger.critical('Invalid arguments')
                    sys.exit()
                flow = unordered_flow.Flow("sub-flow-multiple-dates-remove")
                store = {}
                index = 0
                for date in date_range:
                    index += 1
                    flow.add(
                        cleanData('remove '+date+' data',
                        rebind={'date':'date'+str(index)}))
                    store['date'+str(index)]=date
                workers = 20 if total_dates>20 else total_dates
                e = engines.load(flow, store=store, engine='parallel', max_workers=workers)
            else:
                wf = linear_flow.Flow("sub-flow-remove")
                wf.add(
                    cleanData('remove data')
                )
                e = engines.load(wf,store={'date':value})
            runEngine(e)
        elif key == 'rebase':
            if value not in ['file','db']:
                logger.error('[rebase:Object] Object must be either "db" or "file"!')
                sys.exit()
            wf = linear_flow.Flow("sub-flow-rebase")
            wf.add(
                rebaseData('rebase data')
            )
            e = engines.load(wf,store={'base':value})
            runEngine(e)
        elif key == 'period':
            try:
                [start,end] = value.split('to')
                date_range = datetime_helper.dateRange(start,end)
                total_dates = len(date_range) 
                logger.info(str(total_dates) + ' dates will be processing')
            except:
                logger.critical('Invalid arguments')
                sys.exit()
            flow = unordered_flow.Flow("sub-flow-multiple-dates")
            store = {}
            index = 0
            for date in date_range:
                index += 1
                (sub_flow,sub_store) = historical_flow('date' + str(index), date)
                (flow,store) = update_flow((flow,store), (sub_flow,sub_store))
            workers = 20 if total_dates>20 else total_dates
            e = engines.load(flow, store=store, engine='parallel', max_workers=workers)
            runEngine(e)
        else:
            logger.error('Invalid arguments, worker is not generated!')
            print('Invalid arguments')

def runEngine(eng,frenquency=0):
    try:
        logger.info("---PYWORKER RUN---")
        if frenquency:
            while True:
                eng.run()
                logger.info("---PYWORKER SLEEP---")   
                time.sleep(frenquency)
                logger.info("---PYWORKER RESUME---")
        else:
            eng.run()
    except KeyboardInterrupt:
        pass
    except TypeError as t:
        logger.critical('Ileagal input')

if __name__=='__main__':
    initlog()
    add_lib_path()
    logger.info("---START PYWORKER---")
    if len(sys.argv) == 1:
        main_flow()
    else:
        sub_flow()
    logger.info("---PYWORKER EXIT---")
