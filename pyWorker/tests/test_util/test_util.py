import os

from util import file_handler as fh
from util import mongodb_handler as mh


def parent_path():
    current_path = os.path.abspath(__file__)
    parent = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    return parent

def test_filehandler():
    print(fh.getRate('CNY',parent_path()+'\\example_file'))

if __name__=='__main__':
    test_filehandler()
