from pymongo import MongoClient
import json

def makeConnection():
    client = MongoClient()
    client = MongoClient('localhost', 27017)    

    dbname = "sample_training"
    mydb = client[dbname]

    for coll in mydb.list_collection_names():
        print(coll)

makeConnection()