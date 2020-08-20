from sklearn.cluster import KMeans
from argparse import ArgumentParser
import numpy as np
import matplotlib
from scipy.spatial import KDTree
import cv2
from colormap import rgb2hex
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
from matplotlib.colors import rgb2hex
from colorAnalyzer import *
import os
import webcolors

def closest_color(imagePath):
    colorList = printTopRGB(imagePath)
    for requested_colour in colorList:
        min_colours = {}
        for key, name in webcolors.css21_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        #return min_colours[min(min_colours.keys())]
        print(min_colours[min(min_colours.keys())])

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--imagePath', default='N/A')
    args = parser.parse_args()
    closest_color(args.imagePath)
