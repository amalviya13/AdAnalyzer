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

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/image/upload', methods=['POST'])
def uploadImage():
    return "Testing API"

@app.route('/image/resize', methods=['POST'])
def resizeImage():
    return "Testing API"

@app.route('/image/calculate', methods=['POST'])
def calculateImage():
    return "Testing API"

@app.route('/image/dominant', methods=['GET'])
def dominantImage():
    print(request.args.get('imageID'))
    response = image_dominant_color('/Users/arnavmalviya/Desktop/bladerunner.jpg')
    return response

@app.route('/image/pallette/{numPallete}', methods=['GET'])
def palletteImage():
    return "Testing API"

@app.route('/image/weighted', methods=['GET'])
def weightedImage():
    return "Testing API"

@app.route('/image/percentage/{percentage}', methods=['GET'])
def percentageImage():
    return "Testing API"

@app.route('/image/warmcool', methods=['GET'])
def warmcoolImage():
    return "Testing API"

app.run()