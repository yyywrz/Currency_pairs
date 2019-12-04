import os
import time
import logging as logger

def newpath(path):
    if not os.path.exists(path):
        logger.info('make new directory')
        os.makedirs(path)

def outputToFile(name,data,path,date):
    newpath(path)
    datepath=(path+'\\'+date)
    newpath(datepath)
    filepath = datepath+'\\'+name+'.data'
    with open(filepath,'w') as f:
        for key in data:
            if key !='rates':
                f.write(str(key)+': '+str(data[key])+'\n')
            else:
                f.write(str(key)+':\n')
                for code in data[key]:
                    f.write('\t'+str(code)+': '+str(data[key][code])+'\n')

def getRate(name,path):
    instance = {}
    path = path+'\\'+name+'.data'
    with open(path,'r') as f:
        text = f.readlines()
        text = text[5:]
        for line in text:
            line = line.replace('\n','').replace('\t','').replace(' ','')
            (key,value) = line.split(':')
            instance[key]=value
    return instance
