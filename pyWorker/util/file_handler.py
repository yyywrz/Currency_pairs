import logging as logger
import os
import time

from info import consts

keys=['Currency Code', 'Currency Name', 'Region', 'date']

def newpath(path):
    if not os.path.exists(path):
        logger.info('make new directory:'+path)
        os.makedirs(path, exist_ok=True)

def outputToFile(name,data,path,date):
    newpath(path)
    datepath=(path+'\\'+date)
    newpath(datepath)
    filepath = datepath+'\\'+name+'.data'
    with open(filepath,'w') as f:
        for key in data:
            if key in keys:
                f.write(str(key)+': '+str(data[key])+'\n')
            elif key == 'rates':
                f.write(str(key)+':\n')
                for code in data[key]:
                    f.write('\t'+str(code)+': '+str(data[key][code])+'\n')

def getRate(name,path):
    instance = {}
    path = path+'\\'+name+'.data'
    with open(path,'r') as f:
        text = f.readlines()
        for line in text:
            if line.startswith('\t'):
                line = line.replace('\n','').replace('\t','').replace(' ','')
                (key,value) = line.split(':')
                if key in consts.all_codes:
                    instance[key]=value
    return instance

def removeDataInFile(date,path):
    # we use 'date' as file name
    if date in os.listdir(path):
        path = path +'\\'+date
        for x in os.listdir(path):
            try:
                os.remove(path+'\\'+x)
            except OSError as e:
                logger.error('delete '+path+'\\'+x+' failed')
        try:
            os.rmdir(path)
            logger.info('delete '+path+' successfully')
        except OSError as e:
            logger.error('delete '+path+' failed')
    else:
        logger.error('deletion failed, '+date+' does not exsit!')
