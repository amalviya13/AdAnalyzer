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
import webcolors
import matplotlib

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
    answer = []
    colorDict = {}
    counter = 0
    for color in setArr['color_set']:
        if counter == 8:
            break
        if color[0] != 'black' and color[0] != 'white' and color[0] != 'grey':
            counter += 1
            colorDict["x"] = color[0]  
            colorDict["y"] = int(color[1])
            colorDict["color"] = matplotlib.colors.to_hex([ webcolors.name_to_rgb(color[0])[0]/256, webcolors.name_to_rgb(color[0])[1]/256, webcolors.name_to_rgb(color[0])[2]/256 ])
            answer.append(colorDict)
            colorDict = {}
    return jsonify(answer)

#Get array data of an image in collection
@app.route('/image/array/', methods=['GET'])
def getImageArray():
    company = request.args.get('company')
    setName = request.args.get('set')
    imageName = request.args.get('imageName')
    obj = {'set' : setName, 'image_route' : imageName}
    answer = []
    colorDict = {}
    imgArray = dbGetImageArray(company, obj)
    for color in imgArray:
        colorDict = {}
        colorDict["x"] = color[0]  
        colorDict["y"] = int(color[1])
        colorDict["color"] = matplotlib.colors.to_hex([ webcolors.name_to_rgb(color[0])[0]/256, webcolors.name_to_rgb(color[0])[1]/256, webcolors.name_to_rgb(color[0])[2]/256 ])
        answer.append(colorDict)
    return jsonify(answer)

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
    ctr_average = 0
    for key, value in fileDict.items():  
        ctr_average += value
        warm_cool = warm_or_cool(key)
        top_color = weightedColors(key)
        myObj.append({'image_route' : key, 'set' : setName, 'warm_or_cool' : warm_cool, 'top_colors' : top_color, 'ctr' : value})

    dbCompanyInsertMany(company, myObj)
    ctr_average = ctr_average/len(fileDict.items())
    color_set = get_color_set(route)
    obj = []
    obj.append({'company' : company, 'set_route' : route, 'set' : setName, 'color_set' : color_set, 'num_images' : counter, 'average_ctr': ctr_average})
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


@app.route('/image/set/CTR', methods=['GET'])
def getSetCTRs():
    company = request.args.get('company')
    setName = request.args.get('set')
    image_route = request.args.get('route')
    obj = {'set': setName, 'image_route': image_route}
    companySet = dbGetCompanySet(company, obj)
    ctrList = []
    for image in companySet:
        tempMap = {}
        tempMap['x'] = image['ctr']
        ctrList.append(tempMap)
    print(ctrList)
    return jsonify(ctrList)


# used to get the top 5 images from a set
@app.route('/set/image/best', methods=['GET'])
def getBestInSet():
    company = request.args.get('company')
    setName = request.args.get('set')
    image_route = request.args.get('route') 
    obj1 = {'set' : setName}
    companySet = dbGetCompanyImagesSorted(company, obj1) # get all images from set for sorting (to get top 5)
    obj2 = {'set' : setName, 'image_route' : image_route}
    currImage = dbGetImage(company, obj2)
    imageList = []
    for image in companySet:
        if(image['image_route'] != currImage['image_route']):
            imageList.append({'x': image['image_route'].split('/')[-1], 'y': float(image['ctr'])})
    imageList.append({'x': currImage['image_route'].split('/')[-1], 'y': float(currImage['ctr'])})
    return jsonify(imageList)

@app.route('/image/set/warmthDistribution', methods=['GET'])
def getSetWarmthDistribution():
    company = request.args.get('company')
    setName = request.args.get('set')
    obj1 = {'set' : setName}
    warmCoolDistribution = dbGetSetWarmCoolDistribution(company, obj1) # get all images from set for sorting (to get top 5)
    answer = []
    answer.append({'x': 'warm', 'y': warmCoolDistribution[0]})
    answer.append({'x': 'cool', 'y': warmCoolDistribution[1]})
    return jsonify(answer)

# used to get the top 5 sets
@app.route('/set/best', methods=['GET'])
def getBestSets():
    company = request.args.get('company')
    setName = request.args.get('set')
    obj = {'set' : setName}
    companySets = dbGetCompanySetsSorted(company) # get all images from set for sorting (to get top 5)
    currSet = dbGetCompanySetData(company, obj)
    setList = []
    for set in companySets:
        if(set['set'] != currSet['set']):
            setList.append({'x': set['set'], 'y': float(set['average_ctr'])})
    setList.append({'x': currSet['set'], 'y': float(currSet['average_ctr'])})
    return jsonify(setList)

if __name__ == '__main__': 
    app.run(debug=True) 
