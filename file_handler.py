import os

class file():
    def __init__(self,path = "currency_exchange_data"):
        self.path = path
        if not os.path.exists(path):
            os.makedirs(path)
            