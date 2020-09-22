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

import flask
from flask import request
from imageSetAnalyzer import *
from singleImageAnalyzer import get_dominant_color as image_dominant_color, getColorPercentage as get_image_percentage
from mongoConnector import *

app = flask.Flask(__name__)
app.config["DEBUG"] =    True

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