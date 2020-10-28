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
from flask import jsonify
from flask_cors import CORS

config = {
  'ORIGINS': [
    'http://localhost:3000',  # React
    'http://127.0.0.1:8080',  # React
  ],

  'SECRET_KEY': '...'
}

app = Flask(__name__) 

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

#Get specific image from collection
#@app.route('/image/<company>/<collection>/<imageName>', methods=['GET'])
@app.route('/image', methods=['GET'])
def getImage():
    company = request.args.get('company')
    setName = request.args.get('set')
    imageName = request.args.get('imageName')
    obj = {'set' : setName, 'image_route' : imageName}
    img = dbGetImage(company, obj)
    #Sends back route to image - your computer will search for that image and pull it out
    #In the end it will return link to s3 image
    return img["image_route"]

#Get the names of all the sets of a company
@app.route('/collections', methods=['GET'])
def getCollections():
    company = request.args.get('company')
    companySetNames = dbGetAllCompanySetNames(company)
    return jsonify(list(companySetNames))

#Get all images of a collection
@app.route('/collection/images/', methods=['GET'])
def getSet():
    company = request.args.get('company')
    setName = request.args.get('set')
    obj = {'set' : setName}
    companySet = dbGetCompanySet(company, obj)
    imageList = []
    for image in companySet:
        print(image)
        if ("image_route" in image):
            imageList.append(image["image_route"])
    return jsonify(imageList)

#######
#Get array data of a collection
@app.route('/collection/array/', methods=['GET'])
def getCollectionArray():
    company = request.args.get('company')
    setName = request.args.get('set')
    obj = {'company': company, 'set' : setName}
    setArr = dbGetCompanySetArray(obj)
    return jsonify(setArr)

#Get array data of an image in collection
@app.route('/image/array/', methods=['GET'])
def getImageArray():
    company = request.args.get('company')
    setName = request.args.get('set')
    imageName = request.args.get('imageName')
    obj = {'set' : setName, 'image_route' : imageName}
    colorDict = {}
    imgArray = dbGetImageArray(company, obj)
    for img in imgArray:
        colorDict[img[0]] = img[1]
    return colorDict

#Upload new image   
#Needs to be changed so now it will get data array data of its set and recalculate it
@app.route('/image/upload', methods=['POST'])
def newImage():
    company = request.args.get('company')
    setName = request.args.get('set')
    route = request.args.get('route')
    ctr = request.args.get('ctr')
    warm_cool = warm_or_cool(data['route'])
    top_color = weightedColors(data['route'])
    obj = {'image_route' : route, 'set' : setName, 'warm_or_cool' : warm_cool, 'top_colors' : top_color, 'ctr' : ctr}
    status = dbCompanyInsertOne(company, obj)
    return "Uploaded Image"

#Upload new image set 
@app.route('/image/set/upload', methods=['POST'])
def newImageSet():
    company = request.args.get('company')
    setName = request.args.get('set')
    route = request.args.get('route')
    fileDict = getCSVData(route)
    counter = 0
    myObj = []
    for key, value in fileDict.items():  
        print(key)
        if(counter == 23):
            break
        counter = counter + 1
        warm_cool = warm_or_cool(key)
        top_color = weightedColors(key)
        myObj.append({'image_route' : key, 'set' : setName, 'warm_or_cool' : warm_cool, 'top_colors' : top_color, 'ctr' : value})

    dbCompanyInsertMany(company, myObj)

    color_set = get_color_set(route)
    obj = []
    obj.append({'company' : company, 'set_route' : route, 'set' : setName, 'color_set' : color_set, 'num_images' : counter})
    print(obj)
    status = dbCompanyInsertMany("company_set_data", obj)  #change such that it updates separate collection rather than same collection
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
    company = request.args.get('company')
    setName = request.args.get('set')
    obj = {'set' : setName}
    deleteImagesCount = dbCompanyDeleteMany(company, obj)
    return str(deleteImagesCount)

#Delete an image 
@app.route('/image/delete', methods=['DELETE'])
def deleteImage():
	company = request.args.get('company')
	setName = request.args.get('set')
	image_route = request.args.get('route')
	obj = {'set': setName, 'image_route': image_route}
	deleteCount = dbCompanyDeleteOne(company, obj)
	return str(deleteCount)

if __name__ == '__main__': 
    app.run(debug=True) 
