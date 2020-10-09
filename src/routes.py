# POST /image/upload - Uploads all images based on csv sent
# POST /image/resize - Resize image 200x200
# POST /image/calculate - Runs all calculations on image set
# GET /image/dominant - Dominant color in the image
# GET /image/pallette/{numPallete} - Top x colors in the image
# GET /image/weighted - Get all colors in image with # appearances
# GET /image/percentage/{percent} - Top x percentage of colors
# GET /image/warmcool - Is the image warm or cool

# POST /set/upload - Uploads all images based on csv sent
# POST /set/resize - Resize all images 200x200
# POST /set/calculate - Runs all calculations on image set
# GET /set/dominant - Dominant color overall
# GET /set/colorset - Gets all colors in image with # appearances
# GET /set/unique - Average number of unique colors
from mongoConnector import *
import json
from flask import request
from flask import Flask 
from flask_cors import CORS 
from singleImageAnalyzer import *
from imageSetAnalyzer import *

app = Flask(__name__) 

#Get specific image from collection
@app.route('/image/<company>/<collection>/<imageName>', methods=['GET'])
def getImage(company, collection, imageName):
    company = request.args.get('company')
    collection = request.args.get('collection')
    imageName = request.args.get('imageName')
    obj = {'company' : company, 'set' : collection, 'image_route' : imageName}
    return "Specific Image"

#Get all collections of a company
@app.route('/collections/<company>', methods=['GET'])
def getCollections(company):
    company = request.args.get('company')
    obj = {'company' : company}
    return "Collections"

#Get all images of a collection
@app.route('/collection/images/<company>/<collection>', methods=['GET'])
def getCollection():
    company = request.args.get('company')
    collection = request.args.get('collection')
    obj = {'company' : company, 'set' : collection}
    return "Images in Collection"

#Get array data of a collection
@app.route('/collections/array/<company>/<collection>', methods=['GET'])
def getCollectionArray():
    company = request.args.get('company')
    collection = request.args.get('collection')
    obj = {'company' : company, 'set' : collection}
    return "Collection Array"

#Get array data of an image in collection
@app.route('/image/array/<company>/<collection>/<imageName>', methods=['GET'])
def getImageArray():
    company = request.args.get('company')
    collection = request.args.get('collection')
    imageName = request.args.get('imageName')
    obj = {'company' : company, 'set' : collection, 'image_route' : imageName}
    return "Image Array"

#Upload new image   
#Needs to be changed so now it will get data array data of its set and recalculate it
@app.route('/image/upload', methods=['POST'])
def newImage():
    data = json.loads(request.data)
    company = data['company']
    route = data['route']
    ctr = data['ctr']
    setName = data['set']
    warm_cool = warm_or_cool(data['route'])
    top_color = weightedColors(data['route'])
    obj = {'image_route' : route, 'set' : setName, 'warm_or_cool' : warm_cool, 'top_colors' : top_color, 'ctr' : ctr}
    status = dbCompanyInsertOne(company, obj)
    return "Uploaded Image"

#Upload new image set 
@app.route('/image/set/upload', methods=['POST'])
def newImageSet():
    data = json.loads(request.data)
    fileDict = getCSVData(data['route'])
    setName = data['set']
    company = data['company']
    counter = 0
    myObj = []
    for key, value in fileDict.items():  
        print(key)
        if(counter == 25):
            break
        counter = counter + 1
        warm_cool = warm_or_cool(key)
        top_color = weightedColors(key)
        myObj.append({'image_route' : key, 'set' : setName, 'warm_or_cool' : warm_cool, 'top_colors' : top_color, 'ctr' : value})

    dbCompanyInsertMany(company, myObj)

    color_set = get_color_set(data['route'])
    obj = []
    obj.append({'set_route' : data['route'], 'set' : setName, 'color_set' : color_set, 'num_images' : counter})
    print(obj)
    status = dbCompanyInsertMany("nike", obj)
    return "Uploaded Set"

# #Adding a new set to existing set
# @app.route('/image/set/add', methods=['POST'])
# def updateImageSet():
#     data = json.loads(request.data)
#     setName = data['set']
#     route = data['route']
#     #get array data for this set 
#     #send array data and new csv to python function

#Delete a set and all corresponding images
@app.route('/image/set/delete', methods=['DELETE'])
def deleteImageSet():
    data = json.loads(request.data)
    setName = data['set']
    company = data['company']
    obj = {'set' : setName}
    dbCompanyDeleteMany(company, obj);
    dbCompanyDelete_
    return "Deleted Set"

#Delete an image 
@app.route('/image/delete', methods=['DELETE'])
def deleteImage():
    data = json.loads(request.data)
    company = data['company']
    obj = {'image_route' : data['route']}
    dbCompanyDeleteOne(company, obj)
    return "Deleted Image"

if __name__ == '__main__': 
    app.run(debug=True) 
