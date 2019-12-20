from taskflow import engines
from taskflow.patterns import linear_flow as lf
from taskflow.patterns import unordered_flow as uf
from taskflow import task
from time import time


class task1(task.Task):
    def execute(self):
        print('it is ',self.name)
        print('excuting task 1')

class task2(task.Task):
    def execute(self):
        print('it is ',self.name)
        print('excuting task 2')

class task3(task.Task):
    def execute(self):
        print('it is ',self.name)
        print('excuting task 3')

class task4(task.Task):
    def execute(self):
        print('it is ',self.name)
        print('excuting task 4')

flow123 = lf.Flow('123').add(
    task1('l1'),
    task2('linear2'),
    task3('linear3'),
)
flow1234 = uf.Flow('123').add(
    task1('u1'),
    task2('unordered2'),
    task3('unordered3'),
    task4('unordered4'),
)
flw=flow1234.add(flow123)

e = engines.load(flw, engine='parallel',
                 max_workers=4)
init_time = time()
e.run()
print('total',str(time()-init_time))