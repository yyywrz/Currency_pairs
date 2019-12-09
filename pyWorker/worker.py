import os
import sys
import time
from taskflow import engines
from taskflow.patterns import linear_flow
from taskflow import task
import logging as logger

from fetcher import fetcher
from main import calculator
from util import path_helper

pyworker = path_helper.parent_path(path_helper.current_path(__file__))
root = path_helper.grandparent_path(path_helper.current_path(__file__))
dataFile_path = root + "//currency_exchange_data"

def initlog():
    path = root +'//temp//log'
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    logger.basicConfig(level=logger.INFO,
                    filename=path+'//pyworker.log',
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

class calculateRates(task.Task):
    default_provides = 'rates'
    def execute(self, instance):
        if instance == False:
            raise TypeError("instance needed!")
        else:
            logger.info("Executing '%s'" % (self.name))
            rates = calculator.all_rates(instance)
            return rates

class storeData(task.Task):
    def execute(self, rates):
        logger.info("Executing '%s'" % (self.name))
        calculator.processData(rates,dataFile_path)


if __name__=='__main__':
    initlog()
    add_lib_path()
    logger.info("---START PYWORKER---")
    wf = linear_flow.Flow("main-flow")
    wf.add(
        fetchData('fetch data'),
        calculateRates('calculate rates'),
        storeData('store data')
    )
    e = engines.load(wf)
    try:
        e.run()
    except KeyboardInterrupt:
        pass
    except err as e:
        logger.critical(e)
    logger.info("---PYWORKER EXIT---")
