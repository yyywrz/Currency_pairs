import os
import sys
import time
from taskflow import engines
from taskflow.patterns import linear_flow
from taskflow import task
import logging as logger

from fetcher import fetcher
from main import operation
from util import path_helper
from util import file_handler

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

def runEngine(eng):
    try:
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
        wf = linear_flow.Flow("main-flow")
        wf.add(
            fetchData('fetch data'),
            calculateRates('calculate rates'),
            storeData('store data')
        )
        e = engines.load(wf)
    else:
        for term in sys.argv[1:]:
            try:
                [key,value] = term.split(':')
            except:
                logger.critical('Invalid arguments')
                sys.exit()
            if key == 'date':
                wf = linear_flow.Flow("main-flow")
                wf.add(
                    fetchHistoricalData('fetch data'),
                    calculateRates('calculate rates'),
                    storeData('store data')
                )
                e = engines.load(wf,store={key:value})
                runEngine(e)
                break
            elif key == 'remove':
                wf = linear_flow.Flow("main-flow")
                wf.add(
                    cleanData('remove data')
                )
                e = engines.load(wf,store={'date':value})
                runEngine(e)
                break
            elif key == 'rebase':
                if value not in ['file','db']:
                    logger.error('[rebase:Object] Object must be either "db" or "file"!')
                    sys.exit()
                wf = linear_flow.Flow("main-flow")
                wf.add(
                    rebaseData('rebase data')
                )
                e = engines.load(wf,store={'base':value})
                runEngine(e)
                break
            elif key == 'period':
                try:
                    print(value)
                    [start,end] = value.split(',')
                    
                except:
                    sys.exit()
                    logger.critical('Invalid arguments')
                wf = linear_flow.Flow("main-flow")
                wf.add(
                    getDateRange('get date range'),
                    processDaterangeData('process date-range data')
                )
                e = engines.load(wf,store={'start':start,'end':end})
                runEngine(e)
    logger.info("---PYWORKER EXIT---")
