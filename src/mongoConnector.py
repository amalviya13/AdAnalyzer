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
collectionNike = companiesDB['nike']

@app.route('/image/upload', methods=['POST'])
def uploadImage():
    data = json.loads(request.data)
    route = data['route']
    ctr = data['ctr']
    warm_cool = warm_or_cool(data['route'])
    top_color = weightedColors(data['route'])
    status = companiesDB.nike.insert_one({'image_route' : route, 'warm_or_cool' : warm_cool, 'top_colors' : top_color, 'ctr' : ctr})
    return "Uploaded Image"

@app.route('/image/set/upload', methods=['POST'])
def uploadImageSet():
    data = json.loads(request.data)
    fileDict = getCSVData(data['route'])
    counter = 0
    for key, value in fileDict.items():  
        warm_cool = warm_or_cool(key)
        top_color = weightedColors(key)
        companiesDB.nike.insert_one({'image_route' : key, 'warm_or_cool' : warm_cool, 'top_colors' : top_color, 'ctr' : value})
        counter = counter + 1

    color_set = get_color_set(data['route'])
    status = companiesDB.nike.insert_one({'set_route' : route, 'color_set' : color_set, 'num_images' : counter})
    return "Uploaded Set"

if __name__ == '__main__': 
    app.run(debug=True) 
