from pymongo import MongoClient
import pymongo

connection_url = "mongodb+srv://admin:coloranalyzerboissquad123yeet@cluster0.vcfdv.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_url) 

# do something with the return values

def dbCompanyUpdate(company, obj):
    companyCollection = getCompanyCollection("companies", company)
    companyCollection.update(obj)

def dbCompanyDeleteSingle(company, obj):
    companyCollection = getCompanyCollection("companies", company)
    companyCollection.delete_one(obj)

def dbCompanyDeleteMany(company, obj):
    companyCollection = getCompanyCollection("companies", company)
    companyCollection.delete_one(obj)

def dbCompanyInsertOne(company, obj):
    companyCollection = getCollection("companies", company)
    companyCollection.insert_one(obj)

def dbCompanyInsertMany(company, obj):
    companyCollection = getCollection("companies", company)
    companyCollection.insert_many(obj)

def dbCompanyGet(company, obj):
    companyCollection = getCollection("companies", obj)
    companyCollection.find(obj)


def getCompanyCollection(collectionName, company):
    companiesDB = client["companies"]
    return companiesDB[company]