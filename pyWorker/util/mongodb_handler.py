import pymongo


class db:

    def __init__(self,databaseName,collection):
        self.client =pymongo.MongoClient('localhost',27017)

        Database = self.client[databaseName]
        # name of database

        self.collection = Database[collection]
        # name of collection
        # launch database
        
        self.allCollections = Database.list_collection_names()
    
    def all(self):
        return self.collection.find()
    
    def removeAll(self):
        self.collection.drop()

    def getOne(self,key,value):
        return self.collection.find_one({key:value})

    def updateOne(self,query,key,value):
        new = {'$set':{key:value}}
        self.collection.update_one(query,new)

    def addOne(self,one):
        self.collection.insert_one(one)
    
    def deleteOne(self,key,value):
        self.collection.delete_one({key:value})
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
