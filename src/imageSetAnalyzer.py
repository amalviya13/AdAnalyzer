from sklearn.cluster import KMeans
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
import os
from colorthief import ColorThief
from matplotlib.colors import rgb2hex
from colorAnalyzer import *
import webcolors
from scipy.spatial import KDTree
from PIL import Image
import operator
import csv

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def resize(path):
    dirs = os.listdir( path )
    for item in dirs:
        im = Image.open(path+item)
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        f, e = os.path.splitext(path+item)
        imResize = im.resize((200,200), Image.ANTIALIAS)
        print(imResize)
        imResize.save(f + '.jpg', 'JPEG', quality=90)

def get_dominant_colors(filePath):
    colorDict = {}
    counter = 0
    for filename in os.listdir(filePath):
        if filename.endswith(".jpg"): 
            color_thief = ColorThief(os.path.join(filePath, filename))
            dominant_color = closest_color(color_thief.get_color(quality=1))
            if dominant_color in colorDict:
                colorDict[dominant_color] = colorDict[dominant_color] + 1
            else:
                colorDict[dominant_color] = 1
        else:
            continue
        counter += 1
    return max(colorDict.items(), key=operator.itemgetter(1))[0]

def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.css21_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def get_color_set(csvPath):
    allColors = {}
    fileDict = getCSVData(csvPath)
    for key, value in fileDict.items():
        weightedColorsList(key, value, allColors)
    visualizeResults(allColors)
    return(sorted(allColors.items(), key=lambda x: x[1]))

def visualizeResults(colorDict):
    pieChartDict = colorDict
    del pieChartDict['black']
    del pieChartDict['white']
    del pieChartDict['silver']
    del pieChartDict['grey']
    plt.pie(colorDict.values(), labels = colorDict.keys(), colors = colorDict.keys())
    plt.show()


def getCSVData(csvPath):
    fileDict = {}
    with open(csvPath, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[0] != 'FileName':
                fileDict[row[0]] = float(row[1])
    return fileDict
            

def weightedColorsList(imagePath, ctr, colorDict):
    im = Image.open(imagePath)
    im = im.resize((200, 200))
    width, height = im.size
    for x in range(0,width,50):
        for y in range(0,height,50):
            close_color = closest_color(im.getpixel((x,y)))
            if close_color in colorDict:
                colorDict[close_color] = colorDict[close_color] + (1 * ctr)
            else:
                colorDict[close_color] = 1

def averageUniqueColors(filePath):
    counter = 1
    averageUnique = 0
    onGoingSum = 0
    for filename in os.listdir(filePath):
        if filename.endswith(".jpg"): 
            length = len(weightedColors(filePath + filename))
            onGoingSum += length
            averageUnique = onGoingSum / counter
            counter += 1
        else:
            continue
    return averageUnique

def weightedColors(imagePath):
    colorDict = {}
    im = Image.open(imagePath)
    width, height = im.size
    for x in range(0,width,2):
        for y in range(0,height,2):
            close_color = closest_color(im.getpixel((x,y)))
            if close_color in colorDict:
                colorDict[close_color] = colorDict[close_color] + 1
            else:
                colorDict[close_color] = 1
    return sorted(colorDict.items(), key=lambda x: x[1])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--filePath', default='N/A')
    args = parser.parse_args()
    #print(get_dominant_colors(args.filePath))
    print(get_color_set(args.filePath))
    #print(averageUniqueColors(args.filePath))
    #resize(args.filePath)

