import os
import time

def newpath(path):
    if not os.path.exists(path):
        os.makedirs(path)

def outputToFile(name,data, path = "currency_exchange_data"):
    newpath(path)
    date = time.strftime("%Y-%m-%d", time.localtime())
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
