from util import calculator
from info import helper
import os

current_path = os.path.abspath(__file__)
pyworker = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
root = os.path.abspath(os.path.dirname(pyworker) + os.path.sep + ".")
root = root.replace('\\','//')
db_path = root + "//currency_exchange_data"
print(db_path)
print(calculator.rateInFile('CNY',db_path))
print()
#print(calculator.rateInDB('CNY'))