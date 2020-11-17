from pymongo import MongoClient
import pymongo

connection_url = "mongodb+srv://admin:coloranalyzerboissquad123yeet@cluster0.vcfdv.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_url) 

# need to do error checking
# need to coordinate return values (make sures functions return expected data)

def dbCompanyUpdateOne(company, objToUpdate, newValues):
    companyCollection = dbGetCompanyCollection(company)
    companyCollection.update_one(objToUpdate, newValues)

def dbCompanyUpdateMany(company, objToUpdate, newValues):
    companyCollection = dbGetCompanyCollection(company)
    companyCollection.update_many(objToUpdate, newValues)

def dbCompanyDeleteOne(company, obj):
    companyCollection = dbGetCompanyCollection(company)
    return companyCollection.delete_one(obj).deleted_count

def dbCompanyDeleteMany(company, obj):
    companyCollection = dbGetCompanyCollection(company)
    return companyCollection.delete_many(obj).deleted_count # should add line to ensure set info is deleted from new dataset Collection

def dbCompanyInsertOne(company, obj):
    companyCollection = dbGetCompanyCollection(company)
    companyCollection.insert_one(obj)

def dbCompanyInsertMany(company, obj):
    companyCollection = dbGetCompanyCollection(company)
    companyCollection.insert_many(obj)

# Get a specific company collection
# Returns the entire collection (specifically the collection object) of a company
def dbGetCompanyCollection(companyName): #add obj
    print(type(companyName), "   " , companyName)
    db = client['companies']
    companyCollection = db[companyName]
    # return companyCollection.find({}) # return iterable list of all documents within collection
    return companyCollection

# returns list of all documents corresponding of the respective set
def dbGetCompanySet(companyName, obj):
	companyCollection = dbGetCompanyCollection(companyName)
	return companyCollection.find({'set': obj['set']})

# Get all the names of all sets within a company
# returns an array of all the set nams
def dbGetAllCompanySetNames(companyName):
    companyCollection = dbGetCompanyCollection('company_set_data')
    return companyCollection.find({'company': companyName}, {'_id': 0, 'set':1, 'num_images': 1})

# Gets the entire document of a specific image (returns all data of the given image)
def dbGetImage(companyName, obj):
    companyCollection = dbGetCompanyCollection(companyName)
    return companyCollection.find_one({'set': obj['set'], 'image_route': obj['image_route']})

# Get the data/stats of an image
# Finds the image with in the given path in the given set and returns the 'top_colors' attribute of found document
def dbGetImageArray(companyName, obj):
    companyCollection = dbGetCompanyCollection(companyName)
    image = companyCollection.find_one({'set': obj['set'], 'image_route': obj['image_route']})
    return image['top_colors']

# Get the data document for a specific image set
# Currently retrieves document from within company Collection, but will likely get from separate collection in future update
def dbGetCompanySetArray(obj):
    companyCollection = dbGetCompanyCollection('company_set_data')
    setData = companyCollection.find_one(obj, {'_id': 0})
    return setData

#get top 5 sorted images from a set
def dbGetCompanyImagesSorted(companyName, obj):
    companyCollection = dbGetCompanyCollection(companyName)
    return companyCollection.find({'set': obj['set']}, {'_id': 0}).sort('ctr').limit(5)

def dbGetSetWarmCoolDistribution(companyName, obj):
    companyCollection = dbGetCompanyCollection(companyName)
    numWarm = companyCollection.find({'set': obj['set'], 'warm_or_cool': 'warm'}).count()
    numCool = companyCollection.find({'set': obj['set'], 'warm_or_cool': 'cool'}).count()
    return (numWarm, numCool)

#get top 5 sets from a company
def dbGetCompanySetsSorted(companyName, obj):
    companyCollection = dbGetCompanyCollection('company_set_data')
    return companyCollection.find({'company': companyName}, {'_id': 0}).sort('ctr').limit(5)

def dbGetCompanySetData(companyName, obj):
	companyCollection = dbGetCompanyCollection('company_set_data')
	return companyCollection.findOne({'company': companyName, 'set': obj['set']})