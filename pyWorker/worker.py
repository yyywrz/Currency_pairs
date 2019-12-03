import os
import sys
import time
from taskflow import engines
from taskflow.patterns import linear_flow
from taskflow import task
import logging as logger

from fetcher import fetcher
from util import calculator

def initlog():
    path = root_path()+'temp//log'
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    logger.basicConfig(level=logger.INFO,
                    filename=path+'//pyworker.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s: %(message)s - %(pathname)s[line:%(lineno)d] '
                    )

def root_path():
    current_path = os.path.abspath(__file__)
    pyworker = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    root = os.path.abspath(os.path.dirname(pyworker) + os.path.sep + ".")
    return root.replace('\\','//')

def dataFile_path():
    return root_path()+"//currency_exchange_data"

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
        calculator.processData(rates,dataFile_path())


if __name__=='__main__':
    initlog()
    logger.info("---START PYWORKER---")
    wf = linear_flow.Flow("pass-from-to")
    wf.add(
        fetchData('fetch data'),
        calculateRates('calculate rates'),
        storeData('store data')
    )
    e = engines.load(wf)
    try:
        e.run()
        logger.info("---PYWORKER SLEEP---")
    except KeyboardInterrupt:
        pass
    finally:
        exc_info = sys.exc_info()
        logger.critical(exc_info)
    logger.info("---PYWORKER EXIT---")
