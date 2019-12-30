import time
from copy import deepcopy

from info import consts


class validate:
#
# It verifys the currency code names, region names, and currency names.
# just return True/False
#
    def __init__(self):
        self.regions = set()
        self.currency_names = set()
        for region in consts.Europe:
            self.regions.add(region)
        for instance in consts.code_ref:
            self.currency_names.add(instance['Currency Name'])
            self.regions.add(instance['Region'])
    
    def code(self, code):
        return(code in consts.all_codes)
    
    def region(self, region):
        return(region in self.regions)

    def currency_name(self, name):
        return(name in self.currency_names)


class ref:
#
# Based on the input reference, it gives a data instance.
# Example : {'Currency Code': 'CNY', 'Currency Name': 'Chinese Renminbi', 'Region': 'China'} 
#
    def __init__(self):
        self.vali = validate()
        self.codes={}
        self.currency_names={}
        self.regions={}
        for instance in consts.code_ref:
            self.codes[instance['Currency Code']] = instance
            self.currency_names[instance['Currency Name']] = instance
            self.regions[instance['Region']] = instance
    
    def code(self,code):
        if self.vali.code(code):
            return self.codes[code]
        else:
            return 'invalid'
    
    def region(self,region):
        if self.vali.region(region):
            if region in consts.Europe:
                instance = deepcopy(self.regions['Europe'])
                instance['Region'] = region
                return instance
            return self.regions[region]
        else:
            return 'invalid'

    def currency_name(self,name):
        if self.vali.currency_name(name):
            return self.currency_names[name]
        else:
            return 'invalid'
