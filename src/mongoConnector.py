from pymongo import MongoClient
import pymongo
import json
from flask import request
from flask import Flask 
from flask_cors import CORS 
from singleImageAnalyzer import *
from imageSetAnalyzer import *

connection_url = "mongodb+srv://admin:coloranalyzerboissquad123yeet@cluster0.vcfdv.mongodb.net/test?retryWrites=true&w=majority"
app = Flask(__name__) 
client = pymongo.MongoClient(connection_url) 
companiesDB = client["companies"]

#Upload new image   
@app.route('/image/upload', methods=['POST'])
def newImage():
    data = json.loads(request.data)
    route = data['route']
    ctr = data['ctr']
    setName = data['set']
    warm_cool = warm_or_cool(data['route'])
    top_color = weightedColors(data['route'])
    obj = []
    obj.append({'image_route' : route, 'set' : setName, 'warm_or_cool' : warm_cool, 'top_colors' : top_color, 'ctr' : ctr})
    status = companiesDB.nike.insert_one({'image_route' : route, 'set' : setName, 'warm_or_cool' : warm_cool, 'top_colors' : top_color, 'ctr' : ctr})
    return "Uploaded Image"

#Upload new image set 
@app.route('/image/set/upload', methods=['POST'])
def newImageSet():
    data = json.loads(request.data)
    fileDict = getCSVData(data['route'])
    setName = data['set']
    counter = 0
    myObj = []
    for key, value in fileDict.items():  
        warm_cool = warm_or_cool(key)
        top_color = weightedColors(key)
        myObj.append({'image_route' : key, 'set' : setName, 'warm_or_cool' : warm_cool, 'top_colors' : top_color, 'ctr' : value})

    companiesDB.nike.insert_many(myObj)

    color_set = get_color_set(data['route'])
    obj = []
    obj.append({'set_route' : route, 'set' : setName, 'color_set' : color_set, 'num_images' : counter})
    status = companiesDB.nike.insert_one({'set_route' : route, 'set' : setName, 'color_set' : color_set, 'num_images' : counter})
    return "Uploaded Set"

#Adding a new set to existing set
@app.route('/image/set/add', methods=['POST'])
def updateImageSet():
    data = json.loads(request.data)
    setName = data['set']
    route = data['route']
    #get array data for this set 
    #send array data and new csv to python function

#Add new image to a set
@app.route('/image/add', methods=['POST'])
def addImageToSet():
    data = json.loads(request.data)
    setName = data['set']
    route = data['route']
    #get array data for this set
    #send array data and route of image to python function

#Delete a set and all corresponding images
@app.route('/image/set/delete', methods=['DELETE'])
def deleteImageSet():
    data = json.loads(request.data)
    setName = data['set']
    obj = []
    obj.append({'set' : setName})
    status = companiesDB.nike.delete_many({'set' : setName})
    return "Deleted Set"

#Delete an image 
@app.route('/image/delete', methods=['DELETE'])
def deleteImage():
    data = json.loads(request.data)
    obj = []
    obj.append({'image_route' : data['route']})
    companiesDB.nike.delete_one({'image_route' : data['route']})
    return "Deleted Image"

if __name__ == '__main__': 
    app.run(debug=True) 
