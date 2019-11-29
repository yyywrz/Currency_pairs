from info import consts
import time

class validate:
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
    def __init__(self):
        self.vali = validate()
        self.codes={}
        self.currency_names={}
        self.regions={}
        for instance in consts.code_ref:
            self.codes[instance['Currency Code']] = instance
            self.currency_names[instance['Currency Name']] = instance
            self.regions[instance['Region']] = instance
            if instance['Region'] == 'Europe':
                for country in consts.Europe:
                    instance['Region'] = country
                    self.regions[country] = instance
    
    def code(self,code):
        if self.vali.code(code):
            return self.codes[code]
        else:
            return 'invalid'
    
    def region(self,region):
        if self.vali.region(region):
            return self.regions[region]
        else:
            return 'invalid'

    def currency_name(self,name):
        if self.vali.currency_name(name):
            return self.currency_names[name]
        else:
            return 'invalid'


if __name__=='__main__':
    k = validate()
    print(k.code('CNY'))
    print(k.region('China'))
    print(k.region('Japan'))
    print(k.currency_name('US Dollar'))
    p = ref()
    print(p.code('CNY'))
    print(p.region('China'))
    print(p.region('Japan'))
    print(p.currency_name('US Dollar'))
    print(p.code('CNY1'))
    print(p.region('Chi2134na'))
    print(p.region('Japa234n'))
    print(p.currency_name('US Dol34lar'))
