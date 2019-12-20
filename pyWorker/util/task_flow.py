import logging as logger
from taskflow.patterns import linear_flow
from taskflow import task, engines
from util import file_handler

class RemoveDataInFile(task.Task):
    def execute(self, filename, path):
        logger.info("Executing '%s'" % (self.name))
        file_handler.removeDataInFile(filename,path)

